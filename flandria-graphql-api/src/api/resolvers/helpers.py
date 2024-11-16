from functools import lru_cache
from typing import TYPE_CHECKING, Type, TypeVar, assert_never

import sqlalchemy as sa
from strawberry.types.nodes import (
    FragmentSpread,
    InlineFragment,
    SelectedField,
)

import src.api.types as objects
from src.database import models

if TYPE_CHECKING:
    from strawberry.types.nodes import Selection

    from src.database.types import Model, ModelCls

T = TypeVar("T")
NestedDict = dict[str, "NestedDict"]


def parse_nested_keys_from_selections(selections: list["Selection"]) -> NestedDict:
    """Parses the nested keys that are queried from the selection list.

    e.g.
        fragment messagesFragment on Monster {
        messages {
            code
                message
        }
        }

        query {
        all_monsters {
            items {
            ... on Monster {
                        drops {
                item_code
                monster {
                    name
                }
                }
            }
            name
            ...messagesFragment
            }
        }
    }

    to

    {'all_monsters': {'items': {'drops': {'monster': {}}, 'messages': {}}}}


    Args:
        selections (list[Selection]): List of selections.

    Returns:
        NestedDict: Parsed query keys
    """
    # FIXME (maybe?)
    # Technically, if we have a query that has multiple inline fragments, each with nested keys,
    # and our models share the nested key name, we query it, even if it's not required, because
    # we don't check the nested keys parsed from inline fragments for their type.
    # As we do not share any relationship names (aka keys), I don't care.
    #
    # Explanation by example:
    # query {
    # 	search(s: "fu") {
    #     ...on ActorMixin {
    #       grade
    #     }
    #     ...on Monster {
    #       drops {
    #         item_code
    #       }
    #     }
    #     ... on Quest {
    #       missions {
    #         description
    #       }
    #     }
    #   }
    # }
    # results in {'drops': {}, 'missions': {}}
    # if both Monster and Quest were to implement a relationship "missions", they would both be loaded / coereced.
    result: NestedDict = {}

    for selection in selections:
        if isinstance(selection, SelectedField):
            # only include the selected field if it contains sub-selections
            # -> this means it's a relationship that we need to load
            if selection.selections:
                result[selection.name] = parse_nested_keys_from_selections(
                    selection.selections
                )

        elif isinstance(selection, InlineFragment):
            # An inline fragment, e.g.
            #  all_monsters {
            #    items {
            #      ... on Monster {
            # 			drops {
            #          item_code
            #        }
            #      }
            #      name
            #    }
            #  }
            # can never be the topmost item (which means parent_name should be set) and
            # always consists of at least one child queried.
            # In our model, they belong to the quarried parent key.
            result.update(parse_nested_keys_from_selections(selection.selections))

        elif isinstance(selection, FragmentSpread):
            # A fragment spread is only a wrapper around multiple keys
            # fragment messagesFragment on Monster {
            #   messages {
            #     code
            # 		message
            #   }
            # }
            # query {
            #   all_monsters {
            #     items {
            #       ...messagesFragment
            #     }
            #   }
            # }
            result.update(parse_nested_keys_from_selections(selection.selections))

        else:
            assert_never(selection)

    return result


@lru_cache
def get_orm_to_strawberry_mapping() -> dict["ModelCls", type]:
    """Returns a lookup dictionary that maps the SQLAlchemy ORM Model to its strawberry type declaration.

    Assumes that both models are named the same.

    The return is cached, as the function is meant to be frequently called.

    Raises:
        ValueError: Raised if an ORM model cannot be mapped to it's strawberry type.

    Returns:
        dict["ModelCls", type]: Mapping.
    """
    orm_models: list["ModelCls"] = map(models.__dict__.get, models.__all__)  # type: ignore

    mapping = {}
    for model_cls in orm_models:
        strawberry_cls = objects.__dict__.get(model_cls.__name__)
        if strawberry_cls is None:
            raise ValueError(
                f"Missing strawberry type declaration for {model_cls.__name__}"
            )
        mapping[model_cls] = strawberry_cls

    return mapping


def coerce_orm_to_strawberry(
    item: "Model",
    strawberry_cls: Type[T],
    nk: "NestedDict",
) -> T:
    insp = sa.inspect(item.__class__)
    model_as_dict = {cname: getattr(item, cname) for cname in insp.columns.keys()}

    for rel_name, rel_property in insp.relationships.items():
        if rel_name not in nk:  # coercing ends here
            model_as_dict[rel_name] = [] if rel_property.uselist else None
            continue

        # Coerce the queried relationship
        orm_target_cls = rel_property.entity.class_
        strawberry_target_cls = get_orm_to_strawberry_mapping()[orm_target_cls]
        rel_value = getattr(item, rel_name)
        next_nested_keys = nk[rel_name]

        if rel_property.uselist:
            coerced_value = [
                coerce_orm_to_strawberry(o, strawberry_target_cls, next_nested_keys)
                for o in rel_value
            ]
        else:
            if rel_value is None:
                coerced_value = None
            else:
                coerced_value = coerce_orm_to_strawberry(
                    rel_value,
                    strawberry_target_cls,
                    next_nested_keys,
                )
        model_as_dict[rel_name] = coerced_value

    return strawberry_cls(**model_as_dict)
