import dataclasses

from src.functional import ensure, bind, Result
from tests.test_result import with_id, map, account_to_user, get_account


@dataclasses.dataclass
class FruitInventory:
    name: str
    count: int


def test_map():
    def create_message(inventory: FruitInventory):
        return f"There are {inventory.count} {inventory.name}(s)"

    apple_inventory = Result.success(FruitInventory("apple", 4))
    banana_inventory = Result.error(Exception("Could not find any bananas"))

    assert apple_inventory.map(create_message) == Result.success("There are 4 apple(s)")
    assert banana_inventory.map(create_message) == Result.error(Exception("Could not find any bananas"))
