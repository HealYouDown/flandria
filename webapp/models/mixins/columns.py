from webapp.models.custom_sql_classes import CustomColumn
from sqlalchemy import String, Integer

# Column definitions that are used multiple tables
CLASS_LAND_COLUMN = CustomColumn(String(8), nullable=False, mapper_key="사용직업")

LEVEL_LAND_COLUMN = CustomColumn(Integer, nullable=False, mapper_key="육상LV")

LEVEL_SEA_COLUMN = CustomColumn(Integer, nullable=False, mapper_key="해상LV")

UPGRADE_CODE_COLUMN = CustomColumn(
    String(32), mapper_key="업그레이드코드",
    transform=lambda v: v if v != "#" else None)

SET_CODE_COLUMN = CustomColumn(String(32), mapper_key="세트코드")
