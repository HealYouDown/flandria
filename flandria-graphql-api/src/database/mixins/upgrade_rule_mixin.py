import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.updater.schema import ColumnInfo


class UpgradeRuleMixin:
    upgrade_rule_base_code = orm.mapped_column(
        sa.String(32),
        nullable=True,
        doc="Code to link to upgrade rule",
        info=ColumnInfo(key="업그레이드코드"),
    )

    @orm.declared_attr
    def upgrade_rule(cls):
        cls_name = cls.__name__  # type: ignore
        return orm.relationship(
            "UpgradeRule",
            primaryjoin=f"foreign(UpgradeRule.base_code) == {cls_name}.upgrade_rule_base_code",
            uselist=True,
            viewonly=True,
        )
