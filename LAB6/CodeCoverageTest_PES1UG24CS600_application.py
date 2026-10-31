import pytest
from recycling_rewards import (
    reward_points,
    collection_accepted,
    slot_status
)


# ==========================================
# TEST CASES FOR reward_points()
# ==========================================

def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0


def test_unknown_material():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -2, False)


def test_paper_without_bonus():
    assert reward_points("paper", 10, False) == 30


def test_plastic_without_bonus():
    assert reward_points("plastic", 10, False) == 42


def test_metal_without_bonus():
    assert reward_points("metal", 10, False) == 96


def test_paper_with_bonus():
    assert reward_points("paper", 10, True) == 36


def test_plastic_with_bonus():
    assert reward_points("plastic", 10, True) == 48


def test_metal_with_bonus():
    assert reward_points("metal", 10, True) == 96


def test_extra_weight_above_20():
    assert reward_points("paper", 30, False) == 250


def test_metal_extra_weight_above_20():
    assert reward_points("metal", 30, False) == 504


# ==========================================
# TEST CASES FOR collection_accepted()
# ==========================================

def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True


def test_hazardous_collection_accepted():
    assert collection_accepted(5, 5, True) is True


def test_hazardous_collection_rejected():
    assert collection_accepted(6, 2, True) is False


def test_weight_above_50_rejected():
    assert collection_accepted(51, 2, False) is False


def test_more_than_3_bags_rejected():
    assert collection_accepted(20, 4, False) is False


def test_weight_exactly_50_accepted():
    assert collection_accepted(50, 3, False) is True


# ==========================================
# TEST CASES FOR slot_status()
# ==========================================

def test_morning_slot_open():
    assert slot_status(25, True, False) == "open"


def test_non_morning_slot_open():
    assert slot_status(15, False, False) == "open"


def test_morning_slot_late():
    assert slot_status(10, True, False) == "late"


def test_non_morning_slot_late():
    assert slot_status(5, False, False) == "late"


def test_morning_slot_missed():
    assert slot_status(4, True, False) == "missed"


def test_non_morning_slot_missed():
    assert slot_status(-6, False, False) == "missed"


def test_holiday_slot_open():
    assert slot_status(35, True, True) == "open"


def test_holiday_slot_late():
    assert slot_status(20, True, True) == "late"


def test_holiday_slot_missed():
    assert slot_status(4, True, True) == "missed"