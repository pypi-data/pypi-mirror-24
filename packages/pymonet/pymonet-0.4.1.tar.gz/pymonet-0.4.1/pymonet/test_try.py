from pymonet.monad_try import Try


def divide(dividend, divisor):
    return dividend / divisor


def test_try_should_call_success_callback_with_result_of_function_when_exception_was_not_thrown():

    def success_callback(value):
        assert value == 21

    def fail_callback(_):
        assert True is False

    (Try.of(divide, 42, 2)
        .on_success(success_callback)
        .on_fail(fail_callback))


def test_try_should_call_fail_callback_with_result_of_function_when_exception_was_thrown():

    def success_callback(_):
        assert True is False

    def fail_callback(error):
        assert isinstance(error, ZeroDivisionError)
        assert str(error) == 'division by zero'

    (Try.of(divide, 42, 0)
        .on_success(success_callback)
        .on_fail(fail_callback))


def test_try_eq_should_compare_value_and_result_of_try():
    assert Try.of(divide, 42, 2) == Try.of(divide, 42, 2)
    assert Try.of(divide, 43, 2) != Try.of(divide, 42, 2)
    assert Try.of(divide, 43, 1) != Try.of(divide, 42, 0)


def test_try_should_appied_map_when_exception_was_thrown():

    def success_callback(value):
        assert value == 22

    def fail_callback(_):
        assert True is False

    (Try.of(divide, 42, 2)
        .map(lambda value: value + 1)
        .on_success(success_callback)
        .on_fail(fail_callback))


def test_try_should_not_applied_map_when_exception_thrown():
    def success_callback(_):
        assert True is False

    def fail_callback(error):
        assert isinstance(error, ZeroDivisionError)
        assert str(error) == 'division by zero'

    def mapper(_):
        assert True is False

    (Try.of(divide, 42, 0)
        .map(mapper)
        .on_success(success_callback)
        .on_fail(fail_callback))


def test_get_or_default_method_should_return_value_when_exception_was_not_thrown():
    assert Try.of(divide, 42, 2).get_or_else('Holy Grail') == 21


def test_get_or_default_method_should_return_default_value_when_exception_was_thrown():
    assert Try.of(divide, 42, 0).get_or_else('Holy Grail') == 'Holy Grail'


def test_get_method_should_return_value_with_or_without_exception_thrown():
    assert Try.of(divide, 42, 2).get() == 21

    failed_value = Try.of(divide, 42, 0).get()
    assert isinstance(failed_value, ZeroDivisionError)
    assert str(failed_value) == 'division by zero'
