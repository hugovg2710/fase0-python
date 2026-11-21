import re
from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


PLATE_RE = re.compile(r"^[0-9]{4}[BCDFGHJKLMNPRSTVWXYZ]{3}$")  # matrícula española actual



class Urgency(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentCreate(BaseModel):
    """Datos que llegan de fuera para dar de alta una incidencia."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True,)

    plate: str
    description: str = Field(min_length=5, max_length=500)
    mileage_km: int | None = Field(default=None, ge=0, le=2_000_000)

    @field_validator("plate")
    @classmethod
    def normalize_plate(cls, value: str) -> str:
        plate = value.upper().replace(" ", "").replace("-", "")

        if not PLATE_RE.fullmatch(plate):
            raise ValueError(
                "matrícula con formato no válido (ej.: 1234BCD)"
            )

        return plate


class Incident(IncidentCreate):
    id: int
    urgency: Urgency = Urgency.NORMAL
    requires_review: bool = False
    created_at: datetime

    @model_validator(mode="after")
    def critical_needs_review(self) -> "Incident":
        if self.urgency is Urgency.CRITICAL and not self.requires_review:
            raise ValueError(
                "una incidencia crítica debe requerir revisión"
            )

        return self


class IncidentClassification(BaseModel):
    """La forma que tendrá en la fase 1 la respuesta del LLM."""

    intent: Literal[
        "breakdown",
        "appointment",
        "part",
        "repair_status",
        "general",
    ]

    provisional_urgency: Urgency
    summary: str = Field(min_length=1, max_length=500)
    missing_data: list[str]
    requires_review: bool


# Ejemplo de validación

ok = IncidentCreate(
    plate=" 1234-bcd ",
    description="Vibra al frenar",
    mileage_km="128000",
)

print(ok.model_dump())
# {
#   'plate': '1234BCD',
#   'description': 'Vibra al frenar',
#   'mileage_km': 128000
# }


try:
    IncidentCreate(
        plate="1234ABC",
        description="Ruido",
        mileage_km=-5,
        color="rojo",
    )

except ValidationError as e:
    for err in e.errors():
        print(
            err["loc"],
            err["type"],
            "-",
            err["msg"],
        )

# ('plate',) value_error - Value error, matrícula con formato no válido (ej.: 1234BCD)
# ('mileage_km',) greater_than_equal - Input should be greater than or equal to 0
# ('color',) extra_forbidden - Extra inputs are not permitted


raw = (
    '{"intent": "breakdown", '
    '"provisional_urgency": "high", '
    '"summary": "Vibra al frenar", '
    '"missing_data": ["matrícula"], '
    '"requires_review": false}'
)

print(
    IncidentClassification.model_validate_json(raw).intent
)
# breakdown