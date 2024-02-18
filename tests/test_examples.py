from src.functional import ensure, bind
from tests.test_result import with_id,map, account_to_user, get_account


def test_with_id():
    result = with_id(-1) \
             | ensure | (lambda x: x > -1, Exception("id must be positive")) \
             | bind | get_account \
             | map | account_to_user

    assert result._error == "id must be positive"

    result = with_id("&") \
        | bind | get_account \
        | map | account_to_user

    assert result._error == "id must be an integer"
