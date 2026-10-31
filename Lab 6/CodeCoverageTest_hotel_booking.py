import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ---------------- booking_cost ----------------
def test_standard_two_nights():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_unknown_room_raises():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 1, 1, False)


def test_invalid_nights_raises():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 1, False)


def test_peak_season_surcharge():
    # deluxe 3500 + 25% (875) = 4375 for one night
    assert booking_cost("deluxe", 1, 2, True) == 4375


def test_extra_guest_charge():
    # 2000*3 = 6000, plus 2 extra guests * 500 * 3 nights = 3000
    assert booking_cost("standard", 3, 4, False) == 9000


def test_long_stay_discount():
    # 2000*7 = 14000, 10% off -> 12600
    assert booking_cost("standard", 7, 2, False) == 12600


# ---------------- cancellation_refund ----------------
def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_half_refund():
    assert cancellation_refund(1000, 5, False) == 500


def test_no_refund_late_cancellation():
    assert cancellation_refund(1000, 1, False) == 0


def test_member_bonus_refund():
    # half (500) + member bonus quarter (250)
    assert cancellation_refund(1000, 5, True) == 750


# ---------------- room_upgrade ----------------
def test_no_upgrade_when_no_rooms_free():
    assert room_upgrade("standard", True, 0) == "standard"


def test_standard_member_upgrades_to_deluxe():
    assert room_upgrade("standard", True, 3) == "deluxe"


def test_deluxe_member_upgrades_to_suite():
    assert room_upgrade("deluxe", True, 3) == "suite"


def test_suite_stays_suite():
    assert room_upgrade("suite", True, 3) == "suite"
