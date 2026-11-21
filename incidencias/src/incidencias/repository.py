from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol
from incidencias.domain import Incident, Status

class IncidentRepository(Protocol):
    def add(self, incident: Incident) -> None: ...
    def get(self, incident_id: int) -> Incident | None: ...
    def list_all(self) -> list[Incident]: ...


class InMemoryIncidentRepository: # cumple el Protocol sin declararlo
    def __init__(self) -> None:
        self._items: dict[int, Incident] = {}
    def add(self, incident: Incident) -> None:
        self._items[incident.id] = incident
    def get(self, incident_id: int) -> Incident | None:
        return self._items.get(incident_id)
    def list_all(self) -> list[Incident]:
        return list(self._items.values())


def open_incidents(repo: IncidentRepository) -> list[Incident]:
    return [i for i in repo.list_all() if i.status is not Status.CLOSED]
print(Status("closed"), Status.OPEN == "open") # closed True
# Status("borrado") -> ValueError: 'borrado' is not a valid Status