# Python Functional Extensions

This library helps write code in more functional way.
## Core Concepts

## API Examples

### Result


#### Map

Use case: Transforming the inner value of a successful Result, without needing to check on
the success/failure state of the Result

**Note**: the function (ex `create_message`) passed to `Result.Map()` is only executed if the Result was successful

```python
    def create_message(inventory: FruitInventory):
        return f"There are {inventory.count} {inventory.name}(s)"

    apple_inventory = Result.success(FruitInventory("apple", 4))
    banana_inventory = Result.error(Exception("Could not find any bananas"))

    assert apple_inventory.map(create_message) == Result.success("There are 4 apple(s)")
    assert banana_inventory.map(create_message) == Result.error(Exception("Could not find any bananas"))
```



#### Example

```python

```

## Read or Watch more about these ideas


## Related Projects

- [CSharpFunctionalExtensions](https://github.com/vkhorikov/CSharpFunctionalExtensions)

## Contributors

A big thanks to the project contributors!