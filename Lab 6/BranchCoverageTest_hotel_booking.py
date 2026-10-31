import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ---------------- booking_cost: validation branches ----------------
def test_standard_two_nights():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_unknown_room_raises():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 1, 1, False)


def test_invalid_nights_zero_raises():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 1, False)


def test_invalid_nights_negative_raises():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("suite", -3, 2, True)


def test_minimum_valid_nights_boundary():
    # nights == 1 is the smallest valid value (nights < 1 is False)
    assert booking_cost("standard", 1, 1, False) == 2000


# ---------------- booking_cost: peak season branch ----------------
def test_peak_season_true_branch():
    # deluxe 3500 + 875 = 4375
    assert booking_cost("deluxe", 1, 2, True) == 4375


def test_peak_season_false_branch():
    assert booking_cost("deluxe", 1, 2, False) == 3500


def test_peak_season_suite():
    # 6000 + 1500 = 7500
    assert booking_cost("suite", 1, 2, True) == 7500


# ---------------- booking_cost: extra guest branch ----------------
def test_guests_exactly_two_no_extra_charge():
    assert booking_cost("standard", 1, 2, False) == 2000


def test_guests_three_extra_charge_true_branch():
    # 2000 + 1 extra guest * 500 = 2500
    assert booking_cost("standard", 1, 3, False) == 2500


def test_multiple_extra_guests_multiple_nights():
    # 6000 + 2*500*3 = 9000
    assert booking_cost("standard", 3, 4, False) == 9000


def test_single_guest_no_extra_charge():
    assert booking_cost("standard", 2, 1, False) == 4000


# ---------------- booking_cost: long-stay discount branch ----------------
def test_six_nights_no_discount_boundary():
    # nights == 6 is below the threshold: 12000, no discount
    assert booking_cost("standard", 6, 2, False) == 12000


def test_seven_nights_discount_boundary():
    # nights == 7: 14000 - 10% = 12600
    assert booking_cost("standard", 7, 2, False) == 12600


def test_all_surcharges_and_discount_combined():
    # deluxe peak: 4375*7 = 30625; extra guest: 1*500*7 = 3500 -> 34125
    # 10% discount: 34125 - 3412 = 30713
    assert booking_cost("deluxe", 7, 3, True) == 30713


# ---------------- cancellation_refund ----------------
def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_full_refund_boundary_seven_days():
    assert cancellation_refund(1000, 7, False) == 1000


def test_half_refund_boundary_six_days():
    assert cancellation_refund(1000, 6, False) == 500


def test_half_refund_boundary_two_days():
    assert cancellation_refund(1000, 2, False) == 500


def test_no_refund_boundary_one_day():
    assert cancellation_refund(1000, 1, False) == 0


def test_no_refund_same_day():
    assert cancellation_refund(1000, 0, False) == 0


def test_member_gets_bonus_on_half_refund():
    assert cancellation_refund(1000, 5, True) == 750


def test_member_gets_bonus_on_no_refund_tier():
    assert cancellation_refund(1000, 0, True) == 250


def test_member_full_refund_returns_early_without_bonus():
    assert cancellation_refund(1000, 10, True) == 1000


# ---------------- room_upgrade ----------------
def test_no_upgrade_when_no_rooms_free_member():
    assert room_upgrade("standard", True, 0) == "standard"


def test_no_upgrade_when_no_rooms_free_non_member():
    assert room_upgrade("deluxe", False, 0) == "deluxe"


def test_standard_member_upgrades_to_deluxe():
    assert room_upgrade("standard", True, 5) == "deluxe"


def test_standard_non_member_not_upgraded():
    assert room_upgrade("standard", False, 5) == "standard"


def test_deluxe_member_upgrades_to_suite():
    assert room_upgrade("deluxe", True, 5) == "suite"


def test_deluxe_non_member_not_upgraded():
    assert room_upgrade("deluxe", False, 5) == "deluxe"


def test_suite_member_stays_suite():
    assert room_upgrade("suite", True, 5) == "suite"


def test_suite_non_member_stays_suite():
    assert room_upgrade("suite", False, 5) == "suite"
