import pytest
import re
from seating_chart import SeatingChart

class TestSeatingChart():

### Helper ###
  # def populate(self,chart,res):
  #   res = res.split()
  #   for x in res:
  #     r,c = re.match(r"\s*[Rr]([0-9]+)[Cc]([0-9]+)\s*",x).group(1,2)
  #     seat = (int(r),int(c))
  #     chart.reserve(seat)

### class SeatingChart ###
  def test_create_new_seating_chart(self):
    chart = SeatingChart(10,11)
    assert isinstance(chart,SeatingChart)
    assert chart._rows == 10
    assert chart._cols == 11
    assert chart._reserved_seats == {}
    assert chart._sold_out == False

### def _get_key(self,r,c) ###
  def test_cant_change_hash_formula_by_accident(self):
    chart = SeatingChart(10,11)
    assert chart._get_key(12,23) == 23012

### def _parse_key(self,key) ###
  # def test_get_seat(self):
  #   chart = SeatingChart(10,11)
  #   assert chart._parse_key(23012) == (12,23)

### def _get_taxi(self,a,b) ###
  def test_get_taxi_odd_cols(self):
    chart = SeatingChart(5,9)
    left = chart._get_taxi((4,8))
    right = chart._get_taxi((4,2))
    assert left == right

  def test_get_taxi_even_cols(self):
    chart = SeatingChart(5,10)
    left = chart._get_taxi((4,9))
    right = chart._get_taxi((4,2))
    assert left == right

### def _individual(self,seat) ###
  def test_reserving_a_seat_once(self):
    chart = SeatingChart(5,5)
    expected = [(2,8)]
    actual = chart.reserve((2,8))
    assert actual == expected

  def test_reserving_a_seat_twice(self):
    chart = SeatingChart(5,5)
    chart.reserve((2,8))
    expected = None
    actual = chart.reserve((2,8))
    assert actual == expected

### def _find_seats(self,sought) ###
  def test_group_bigger_than_a_row(self):
    chart = SeatingChart(10,6)
    expected = None
    actual = chart._find_seats(7)
    assert actual == expected

  def test_find_best_four_seats_in_empty_row_of_odd_columns(self):
    chart = SeatingChart(1,9)
    chart._find_seats(4)
    expected = {3001: 1, 4001: 1, 5001: 1, 6001: 1}
    actual = chart._reserved_seats
    assert expected == actual
    
  def test_find_best_four_seats_in_empty_row_of_even_columns(self):
    chart = SeatingChart(1,10)
    chart._find_seats(4)
    expected = {4001: 1, 5001: 1, 6001: 1, 7001: 1}
    actual = chart._reserved_seats
    assert expected == actual

  def test_find_best_five_seats_in_empty_row_of_odd_columns(self):
    chart = SeatingChart(1,9)
    chart._find_seats(5)
    expected = {3001: 1, 4001: 1, 5001: 1, 6001: 1, 7001: 1}
    actual = chart._reserved_seats
    assert expected == actual

  def test_find_best_five_seats_in_empty_row_of_even_columns(self):
    chart = SeatingChart(1,10)
    chart._find_seats(5)
    expected = {3001: 1, 4001: 1, 5001: 1, 6001: 1, 7001: 1}
    actual = chart._reserved_seats
    assert expected == actual

  def test_find_best_five_seats_in_second_row(self):
    chart = SeatingChart(5,10)
    chart.initialize([(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8),
                     (1,9), (1,10)])
    chart._find_seats(5)
    expected = {4001: 1, 2001: 1, 1001: 1, 9001: 1, 7001: 1, 6001: 1, 5001: 1,
                3001: 1, 10001: 1, 8001: 1, 3002: 1, 4002: 1, 5002: 1, 6002: 1,
                7002: 1}
    actual = chart._reserved_seats
    assert expected == actual

  def test_no_space_left_for_group(self):
    chart = SeatingChart(2,6)
    chart.initialize([(1,1), (1,3), (1,5), (2,2), (2,4), (2,6)])
    expected = None
    actual = chart._find_seats(2)
    assert actual == expected

  def test_example_input(self):
    chart = SeatingChart(3,11)
    chart.initialize([(1,4), (1,6), (2,3), (2,7), (3,9), (3,10)])
    chart._find_seats(3)
    chart._find_seats(3)
    chart._find_seats(3)
    chart._find_seats(1)
    chart._find_seats(10)
    expected = {3002: 1, 4001: 1, 4002: 1, 5001: 1, 5002: 1, 5003: 1, 6001: 1,
                6002: 1, 6003: 1, 7001: 1, 7002: 1, 7003: 1, 8001: 1, 9001: 1,
                9003: 1, 10003: 1}
    actual = chart._reserved_seats
    assert expected == actual

### def reserve(self,seats) ###
  def test_reserve_takes_only_strs_or_ints(self):
    chart = SeatingChart(5,5)
    with pytest.raises(ValueError):
      chart.reserve(4.5)

### def reserved(self,seat) ###
  def test_reserved_seat_is_marked_reserved(self):
    chart = SeatingChart(5,5)
    chart.reserve((1,3))
    expected = True
    actual = chart.reserved((1,3))
    assert actual == expected

  def test_unreserved_seat_is_marked_unreserved(self):
    chart = SeatingChart(5,5)
    expected = False
    actual = chart.reserved((1,3))
    assert actual == expected