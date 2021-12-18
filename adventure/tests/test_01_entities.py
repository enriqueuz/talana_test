from datetime import date

import pytest

from adventure import models


@pytest.fixture
def car():
    return models.VehicleType(max_capacity=4)


@pytest.fixture
def van():
    return models.VehicleType(max_capacity=6)


@pytest.fixture
def tesla(car):
    return models.Vehicle(
        name="Tesla", passengers=3, vehicle_type=car, number_plate="AA-12-34"
    )


class TestVehicle:
    def test_capacity_greater_than_passengers(self, car):
        vehicle = models.Vehicle(vehicle_type=car, passengers=2)
        assert vehicle.can_start()

    def test_vehicle_overload(self, car):
        vehicle = models.Vehicle(vehicle_type=car, passengers=10)
        assert not vehicle.can_start()

    # @pytest.mark.skip  # Remove
    def test_vehicle_distribution(self, car, van):
        # TODO: implement a method called "get_distribution" that returns a matrix filled of booleans
        # with the "standard distribution" in a vehicle, from top to bottom and left to right.
        # A Vehicle can have "n" rows with a maximum of 2 passengers per row.
        # The rows number depends on the vehicle max capacity.
        #
        # e.g: for 3 passengers
        # [
        #     [ True, True],
        #     [ True, False],
        # ]
        # for 5 passengers
        # [
        #     [ True, True],
        #     [ True, True],
        #     [ True, False],
        # ]
        vehicle = models.Vehicle(vehicle_type=car, passengers=3)
        distribution_expected = [[True, True], [True, False]]
        assert vehicle.get_distribution() == distribution_expected

        vehicle = models.Vehicle(vehicle_type=van, passengers=5)
        distribution_expected = [[True, True], [True, True], [True, False]]
        assert vehicle.get_distribution() == distribution_expected

    # @pytest.mark.skip  # Remove
    def test_valid_number_plate(self):
        # TODO: implement a function called "validate_number_plate"
        # a valid number plate consists of three pairs of alphanumeric chars separated by hyphen
        # the first pair must be letters and the rest must be numbers
        # e.g: AA-12-34
        assert models.validate_number_plate("AA-12-34")
        assert not models.validate_number_plate("AA-BB-34")
        assert not models.validate_number_plate("12-34-56")
        assert not models.validate_number_plate("AA1234")
        assert not models.validate_number_plate("AA 12 34")


# @pytest.mark.skip  # Remove
class TestJourney:
    # TODO: implement "is_finished" method
    # a finished journey depends on the end value
    def test_is_finished(self, tesla):
        journey = models.Journey(start=date.today(), end=date.today(), vehicle=tesla)
        assert journey.is_finished()

    def test_is_not_finished(self, tesla):
        journey = models.Journey(start=date.today(), vehicle=tesla)
        assert not journey.is_finished()
