from src import main

def test_sum_two_numbers():
    assert main.sum_two_numbers(1, 2) == 3

def test_multiply_two_numbers():
    assert main.multiply_two_numbers(2, 2) == 4

def test_divide_two_numbers():
    assert main.divide_two_numbers(4, 2) == 2

def test_subtract_two_numbers():
    assert main.subtract_two_numbers(4, 2) == 2