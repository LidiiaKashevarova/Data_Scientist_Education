
# Define the function
def add_or_multiply_pytest(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    else:
        return 'Choose either "add" or "multiply"'
    
# Import pytest for testing    
import pytest

# Define test cases

def test_add_positive_numbers():
    assert add_or_multiply_pytest(2, 3, "add") == 5

def test_add_negative_and_positive():
    assert add_or_multiply_pytest(-1, 5, "add") == 4

def test_add_with_zero():
    assert add_or_multiply_pytest(0, 10, "add") == 10

def test_multiply_positive_numbers():
    assert add_or_multiply_pytest(6, 3, "multiply") == 18

def test_multiply_negative_numbers():
    assert add_or_multiply_pytest(-1000, 3, "multiply") == -3000

def test_multiply_two_negative_numbers():
    assert add_or_multiply_pytest(-500, -4, "multiply") == 2000

def test_invalid_operation():
    assert add_or_multiply_pytest(5, 3, "none") == 'Choose either "add" or "multiply"'
    

def test_multiply_with_zero():
    assert add_or_multiply_pytest(0, 10, "multiply") == 0   
    
# Run the tests if this script is executed directly
if __name__ == "__main__":
    pytest.main()
    