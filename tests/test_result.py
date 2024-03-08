import pytest

from src.functional import safe, map, error_unsafe, bind, success_unsafe, tap, if_failure, ensure, as_success


class Account:
    def __init__(self, account_id: int):
        self.id = account_id
        self.is_protected = account_id == 1

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(f"Account(id={self.id})")


@safe
def get_account(account_id: int) -> Account:
    if account_id == 0:
        raise ValueError("Account Not found")

    return Account(account_id=account_id)


@safe
def delete_account(account: Account):
    if account.is_protected:
        raise ValueError("Account protected cannot be deleted")

    return 1


class User:

    def __init__(self, user_id: int):
        self.id = user_id


def account_to_user(account: Account):
    return User(user_id=account.id)


def user_to_account(user: User):
    return Account(account_id=user.id)


def increment(n: int) -> int:
    return n + 1


def test_error_unsafe():
    response = get_account(0) \
               | map | account_to_user \
               | map | user_to_account \
               | bind | delete_account \
               | map | increment \
               | bind | get_account \
               | error_unsafe

    assert response() == 'Account Not found'


def test_right():
    response = get_account(3) \
               | map | account_to_user \
               | map | user_to_account \
               | bind | delete_account \
               | map | increment \
               | bind | get_account \
               | success_unsafe

    assert response().id == 2


def test_as_success():
    response = as_success(3) \
               | bind | get_account \
               | success_unsafe

    assert response().id == 3


@safe
def with_id(an_id):
    if isinstance(an_id, str):
        raise TypeError("id must be an integer")

    return an_id


def test_success8bind():
    response = with_id(3) \
               | bind | get_account \
               | success_unsafe

    assert response().id == 3


def test_success_unsafe():
    response = with_id(2) \
               | bind | get_account \
               | bind | delete_account \
               | success_unsafe

    assert response() == 1


def test_error_unsafe_success():
    response = with_id(1) \
               | bind | get_account \
               | bind | delete_account \
               | error_unsafe

    assert response() == "Account protected cannot be deleted"


def test_tap():
    steps = ""

    def log_steps(result):
        print(result)
        nonlocal steps
        steps += str(result) + "\n"

    with_id(2) \
     | tap | log_steps \
     | bind | get_account \
     | tap | log_steps \
     | bind | delete_account \
     | tap | log_steps \
     | bind | get_account \
     | tap | log_steps \
     | success_unsafe

    assert steps == """Result(_error=None, _value=2)
Result(_error=None, _value=Account(id=2))
Result(_error=None, _value=1)
Result(_error=None, _value=Account(id=1))
"""


def test_if_failure():
    def should_call(e):
        raise Exception(e)

    with pytest.raises(Exception) as e_info:
        with_id(0) \
         | bind | get_account \
         | if_failure | should_call

    assert "Account Not found" in str(e_info)

    result = with_id(1) \
        | bind | get_account \
        | if_failure | should_call

    assert result._value.id == 1


def test_ensure():
    result = with_id(1) \
             | bind | get_account \
             | ensure | (lambda account: account.id > 2, Exception("Should be superior to 2")) \
             | map | account_to_user

    assert result._error == "Should be superior to 2"

    result = with_id(3) \
        | bind | get_account \
        | ensure | (lambda account: account.id > 2, Exception("Should be superior to 2")) \
        | map | account_to_user

    assert isinstance(result._value, User)
