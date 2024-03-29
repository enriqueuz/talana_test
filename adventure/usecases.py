from __future__ import annotations

from .notifiers import Notifier
from .repositories import JourneyRepository
from adventure import models

# Django
from django.utils import timezone

class StartJourney:
    def __init__(self, repository: JourneyRepository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

    def set_params(self, data: dict) -> StartJourney:
        self.data = data
        return self

    def execute(self) -> None:
        car = self.repository.get_or_create_car()
        vehicle = self.repository.create_vehicle(vehicle_type=car, **self.data)
        if not vehicle.can_start():
            raise StartJourney.CantStart("vehicle can't start")

        journey = self.repository.create_journey(vehicle)
        self.notifier.send_notifications(journey)
        return journey

    class CantStart(Exception):
        pass

class StopJourney:

    def set_params(self, serializer):
        self.serializer = serializer
        return self

    def execute(self) -> None:
        if self.serializer.is_valid(raise_exception=True):
            self.serializer.save()
            return self.serializer
    
    class CantStop(Exception):
        pass
