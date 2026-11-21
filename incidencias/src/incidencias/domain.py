from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol

class Status(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class Urgency(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

ALLOWED_TRANSITIONS: dict[Status, set[Status]] = {
    Status.OPEN: {Status.IN_PROGRESS, Status.CLOSED},
    Status.IN_PROGRESS: {Status.CLOSED},
    Status.CLOSED: set(),
}


class InvalidTransitionError(Exception):
    pass


@dataclass
class Incident:
    id: int
    plate: str
    description: str
    mileage_km: int | None = None
    status: Status = Status.OPEN ##Valor por defecto
    urgency: Urgency = Urgency.NORMAL ##Valor por defecto
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def change_status(self, new: Status):
        if new not in ALLOWED_TRANSITIONS[self.status]:
            raise InvalidTransitionError(f"No se puede pasar de {self.status} a {new}")
        self.status = new


        

