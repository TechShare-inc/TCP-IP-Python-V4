"""Unit tests for dobot_api_v4.commands._serialization module."""

import pytest

from dobot_api_v4.commands._serialization import _SerializationMixin


class _Stub(_SerializationMixin):
    """Concrete stub so we can instantiate the mixin for testing."""

    pass


@pytest.mark.unit
class TestFmt:
    """Tests for _fmt method."""

    def setup_method(self):
        self.s = _Stub()

    def test_int_formatting(self):
        assert self.s._fmt(42) == "42"
        assert self.s._fmt(0) == "0"
        assert self.s._fmt(-1) == "-1"

    def test_float_formatting(self):
        result = self.s._fmt(3.14)
        assert result.startswith("3.14")
        # Should use {:f} format -- 6 decimal places by default
        assert "." in result

    def test_string_passthrough(self):
        assert self.s._fmt("hello") == "hello"
        assert self.s._fmt("192.168.1.1") == "192.168.1.1"

    def test_list_formatting(self):
        result = self.s._fmt([1, 2, 3])
        assert result == "{1,2,3}"

    def test_tuple_formatting(self):
        result = self.s._fmt((10, 20))
        assert result == "{10,20}"

    def test_nested_list(self):
        result = self.s._fmt([[1, 2], [3, 4]])
        assert result == "{{1,2},{3,4}}"

    def test_mixed_list(self):
        result = self.s._fmt([1, 2.5, "x"])
        assert result == "{1,2.500000,x}"


@pytest.mark.unit
class TestBuildCmd:
    """Tests for _build_cmd method."""

    def setup_method(self):
        self.s = _Stub()

    def test_no_args(self):
        assert self.s._build_cmd("Foo") == "Foo()"

    def test_positional_args(self):
        result = self.s._build_cmd("Bar", 1, 2, 3)
        assert result == "Bar(1,2,3)"

    def test_keyword_args(self):
        result = self.s._build_cmd("Baz", user=1, tool=2)
        assert result == "Baz(user=1,tool=2)"

    def test_mixed_args(self):
        result = self.s._build_cmd("Cmd", 1, 2.0, key="val")
        assert result == "Cmd(1,2.000000,key=val)"

    def test_list_arg(self):
        result = self.s._build_cmd("Cmd", [1, 2, 3])
        assert result == "Cmd({1,2,3})"
