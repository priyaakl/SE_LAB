from hypothesis import given, strategies as st
from recycling_rewards import (
    parse_collection,
    weight_average,
    net_points
)


# TEST 1: parse_collection()

@given(st.one_of(st.text(), st.none()))
def test_parse_collection_handles_arbitrary_input(s):
    try:
        parse_collection(s)
    except ValueError:
        pass


@given(st.floats(allow_nan=False, allow_infinity=False))
def test_parse_collection_valid_input(weight):
    result = parse_collection(f"paper:{weight}")
    assert result == ("Paper", weight)


# TEST 2: weight_average()

@given(st.one_of(st.text(), st.none()))
def test_weight_average_handles_arbitrary_input(s):
    try:
        weight_average(s)
    except ValueError:
        pass


@given(st.lists(st.integers(), min_size=1))
def test_weight_average_valid_input(weights):
    text = ",".join(str(w) for w in weights)
    expected = sum(weights) // len(weights)
    assert weight_average(text) == expected


# TEST 3: net_points()

@given(st.one_of(st.text(), st.none()))
def test_net_points_handles_arbitrary_input(s):
    try:
        net_points(s)
    except ValueError:
        pass


@given(
    st.floats(allow_nan=False, allow_infinity=False),
    st.floats(allow_nan=False, allow_infinity=False)
)
def test_net_points_valid_input(points, penalty):
    result = net_points(f"{points}|{penalty}")
    expected = max(points * 2 - penalty, 0)
    assert result == expected
