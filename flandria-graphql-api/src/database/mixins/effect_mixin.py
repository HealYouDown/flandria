import sqlalchemy.orm as orm


class EffectMixin:
    @orm.declared_attr
    def effects(cls):
        cls_name = cls.__name__  # type: ignore
        return orm.relationship(
            "Effect",
            primaryjoin=(f"foreign(Effect.ref_code) == {cls_name}.code"),
            uselist=True,
            viewonly=True,
        )
