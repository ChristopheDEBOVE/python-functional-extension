from src.functional import safe


def test_safe_success():
    @safe
    def lili():
        return 1

    result = lili()
    assert result.get_value_unsafe == 1


def test_safe_exception():
    @safe
    def i_raise_error():
        raise Exception("fatal error")

    result = i_raise_error()
    assert result.get_error_unsafe == "fatal error"
