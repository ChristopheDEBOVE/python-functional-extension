from src.functional import safe


def test_safe_success():
    @safe
    def lili():
        return 1

    result = lili()
    assert result.get_value_unsafe == 1


def test_safe_exception():
    @safe
    def lili():
        raise Exception("qsd")

    result = lili()
    assert result.get_error_unsafe == "qsd"
