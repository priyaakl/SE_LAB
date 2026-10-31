import pytest
from recycling_rewards import (
    reward_points,
    collection_accepted,
    slot_status
)


# ==========================================
# BRANCH TESTS FOR reward_points()
# ==========================================

def test_unknown_material():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)


def test_valid_material():
    assert reward_points("paper", 10, False) == 30


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)


def test_zero_weight():
    assert reward_points("paper", 0, False) == 0


def test_bonus_for_paper():
    assert reward_points("paper", 10, True) == 36


def test_no_bonus_for_paper():
    assert reward_points("paper", 10, False) == 30


def test_bonus_for_plastic():
    assert reward_points("plastic", 10, True) == 48


def test_bonus_for_metal():
    assert reward_points("metal", 10, True) == 96


def test_metal_rate():
    assert reward_points("metal", 10, False) == 96


def test_non_metal_rate():
    assert reward_points("plastic", 10, False) == 42


def test_extra_weight_not_above_20():
    assert reward_points("paper", 25, False) == 120


def test_extra_weight_above_20():
    assert reward_points("paper", 30, False) == 250


def test_metal_extra_weight_above_20():
    assert reward_points("metal", 30, False) == 504


# ==========================================
# BRANCH TESTS FOR collection_accepted()
# ==========================================

def test_hazardous_weight_accepted():
    assert collection_accepted(5, 2, True) is True


def test_hazardous_weight_rejected():
    assert collection_accepted(6, 2, True) is False


def test_non_hazardous_weight_accepted():
    assert collection_accepted(20, 2, False) is True


def test_non_hazardous_weight_above_limit():
    assert collection_accepted(51, 2, False) is False


def test_bag_limit_accepted():
    assert collection_accepted(20, 3, False) is True


def test_bag_limit_exceeded():
    assert collection_accepted(20, 4, False) is False


# ==========================================
# BRANCH TESTS FOR slot_status()
# ==========================================

def test_morning_condition():
    assert slot_status(25, True, False) == "open"


def test_non_morning_condition():
    assert slot_status(15, False, False) == "open"


def test_holiday_condition():
    assert slot_status(35, True, True) == "open"


def test_non_holiday_condition():
    assert slot_status(25, True, False) == "open"


def test_slot_open():
    assert slot_status(20, True, False) == "open"


def test_slot_late():
    assert slot_status(10, True, False) == "late"


def test_slot_missed():
    assert slot_status(4, True, False) == "missed"


def test_holiday_slot_late():
    assert slot_status(20, True, True) == "late"


def test_holiday_slot_missed():
    assert slot_status(4, True, True) == "missed"


def test_non_morning_slot_missed():
    assert slot_status(-6, False, False) == "missed"