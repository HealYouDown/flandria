from sqlalchemy import Column, String, Integer
from ...extensions import db


class UpgradeRule(db.Model):
    __tablename__ = "upgrade_rule"
    __bind_key__ = "static_data"

    index = Column(Integer, primary_key=True, autoincrement=True)
    upgrade_code = Column(String)
    upgrade_level = Column(Integer)
    gelt = Column(Integer)

    code_0 = Column(Integer)
    operator_0 = Column(String)
    value_0 = Column(Integer)

    code_1 = Column(Integer)
    operator_1 = Column(String)
    value_1 = Column(Integer)

    code_2 = Column(Integer)
    operator_2 = Column(String)
    value_2 = Column(Integer)

    code_3 = Column(Integer)
    operator_3 = Column(String)
    value_3 = Column(Integer)

    def to_dict(self) -> dict:
        return {
            "upgrade_level": self.upgrade_level,
            "gelt": self.gelt,
            "code_0": self.code_0,
            "operator_0": self.operator_0,
            "value_0": self.value_0,
            "code_1": self.code_1,
            "operator_1": self.operator_1,
            "value_1": self.value_1,
            "code_2": self.code_2,
            "operator_2": self.operator_2,
            "value_2": self.value_2,
            "code_3": self.code_3,
            "operator_3": self.operator_3,
            "value_3": self.value_3
        }
