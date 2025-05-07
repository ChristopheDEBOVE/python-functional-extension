# Python Functional Extensions

This library helps write code in more functional way.
## Core Concepts

### Get rid of primitive obsession (pydantic compatible)

```python
    first_name = CustomerName.create("")
    second_name = CustomerName.create("John")

    assert first_name.is_failure
    assert first_name.get_error_unsafe == "Invalid name"

    assert second_name.is_success
    assert str(second_name.get_value_unsafe) == "John"
```

### Get rid of the Errors raised and regain control of your flow

```python
    @safe
    def raise_error():
        raise Exception("fatal error")

    result = raise_error()
    assert result.is_failure
    assert result.get_error_unsafe == "fatal error"
```

### Adopt a new development style - Railway programming flavor

```python
    response = (get_account(3) 
               | map | account_to_user 
               | map | user_to_account 
               | bind | delete_account 
               | map | increment 
               | bind | get_account 
               | success_unsafe)
```

    
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
