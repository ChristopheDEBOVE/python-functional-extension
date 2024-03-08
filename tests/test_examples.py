import dataclasses

from src.functional import ensure, bind, Result
from tests.test_result import with_id, map, account_to_user, get_account


@dataclasses.dataclass
class FruitInventory:
    name: str
    count: int


@dataclasses.dataclass
class CustomerName:
    name: str

    def __repr__(self):
        return f"{self.name}"

    @classmethod
    def create(cls, value: str):
        if not value or len(value) < 4:
            return Result.error(Exception("Invalid name"))

        return Result.success(cls(value))


def test_create():
    first_name = CustomerName.create("")
    second_name = CustomerName.create("John")

    assert first_name.is_failure
    assert first_name.get_error_unsafe == "Invalid name"

    assert second_name.is_success
    assert str(second_name.get_value_unsafe) == "John"


def test_map():
    def create_message(inventory: FruitInventory):
        return f"There are {inventory.count} {inventory.name}(s)"

    apple_inventory = Result.success(FruitInventory("apple", 4))
    banana_inventory = Result.error(Exception("Could not find any bananas"))

    assert apple_inventory.map(create_message) == Result.success("There are 4 apple(s)")
    assert banana_inventory.map(create_message) == Result.error(Exception("Could not find any bananas"))
