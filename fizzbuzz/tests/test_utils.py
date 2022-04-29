from utils import get_fizzbuzz


def test_fizzbuzz_nominal():
    fizzbuzz = get_fizzbuzz(3, 15, 30, "test1", "test2")

    expected = ['1', '2', 'test1', '4', '5', 'test1', '7', '8', 'test1', '10', '11',
                'test1', '13', '14', 'test1test2', '16', '17', 'test1', '19', '20',
                'test1', '22', '23', 'test1', '25', '26', 'test1', '28', '29', 'test1test2']

    assert fizzbuzz == expected


def test_fizzbuzz_no_multiple():
    fizzbuzz = get_fizzbuzz(23, 45, 20, "test1", "test2")

    expected = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '20']

    assert fizzbuzz == expected
