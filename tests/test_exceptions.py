from sdk_payment_python.exceptions import KvellAPIError, KvellError, KvellValidationError


class TestExceptionHierarchy:
    def test_api_error_is_kvell_error(self):
        assert issubclass(KvellAPIError, KvellError)

    def test_validation_error_is_api_error(self):
        assert issubclass(KvellValidationError, KvellAPIError)

    def test_validation_error_is_kvell_error(self):
        assert issubclass(KvellValidationError, KvellError)


class TestKvellAPIError:
    def test_attributes(self):
        err = KvellAPIError(status_code=500, body="Internal Server Error")
        assert err.status_code == 500
        assert err.body == "Internal Server Error"

    def test_repr(self):
        err = KvellAPIError(status_code=404, body="Not found")
        assert "404" in repr(err)


class TestKvellValidationError:
    def test_attributes(self):
        errors = [{"message": "Invalid amount", "code": 1001}]
        err = KvellValidationError(errors=errors)
        assert err.errors == errors
        assert err.status_code == 422

    def test_repr(self):
        err = KvellValidationError(errors=[{"message": "Bad", "code": 1}])
        assert "Bad" in repr(err)
