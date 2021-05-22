from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.enums import SealOptionType
from webapp.models.transforms import florensia_probability_transform


class SealOption(db.Model):
    __tablename__ = "seal_option"

    _mapper_utils = {
        "files": {
            "server": [
                "s_SealOptionData.bin"
            ]
        },
    }

    code = CustomColumn(db.String(32), primary_key=True,
                        mapper_key="코드")

    # Link seal option to table. Used to reference the table later.
    # This is done in the update_database.py loop.
    seal_option_type = CustomColumn(db.Enum(SealOptionType), nullable=False,
                                    mapper_key="_seal_option_type")


# Add columns with data dynamically
for i in range(0, 63):
    # Option code
    setattr(
        SealOption, f"option_{i}_code",
        CustomColumn(db.String(32), db.ForeignKey("seal_option_data.code"),
                     mapper_key=f"옵션코드{i}")
    )

    # Option probability
    setattr(
        SealOption, f"option_{i}_chance",
        CustomColumn(db.Float, mapper_key=f"확률{i}",
                     transform=(lambda v: florensia_probability_transform(v)
                                if v != 0 else None))
    )

    # Option relationship
    setattr(
        SealOption, f"option_{i}",
        db.relationship(
            "SealOptionData",
            foreign_keys=[getattr(SealOption, f"option_{i}_code")],
            viewonly=True,)
    )
