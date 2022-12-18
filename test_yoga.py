from yoga import get_user_input, validate, get_minimum_playtime, check_link

import sys, pytest


def test_get_user_input():
    # Valid command line arguments
    sys.argv = ['yoga.py', '-n', '35']
    assert get_user_input() == '35'

    # No command line arguments
    sys.argv = ['yoga.py']
    assert get_user_input() == None

    # No flag provided
    sys.argv = ['yoga.py', '35']
    with pytest.raises(SystemExit):
        assert get_user_input()

    # Invalid flag provided
    sys.argv = ['yoga.py', '-t', '35']
    with pytest.raises(SystemExit):
        assert get_user_input()

    # Minutes not provided
    sys.argv = ['yoga.py', '-n']
    with pytest.raises(SystemExit):
        assert get_user_input()


def test_validate():
    # Valid minutes
    assert validate("5") == 5

    # Float provided
    with pytest.raises(SystemExit):
        assert validate("4.5")

    # String provided
    with pytest.raises(SystemExit):
        assert validate("cat")

    # Time is not positive integer
    with pytest.raises(SystemExit):
        assert validate("0")
    with pytest.raises(SystemExit):
        assert validate("-10")


def test_get_minimum_playtime():
    assert get_minimum_playtime(50) == 45
    assert get_minimum_playtime(5) == 0
    assert get_minimum_playtime(3) == 0


def test_check_link():
    # Valid link
    assert check_link('https://www.google.co.uk/') == True

    # Invalid Link
    assert check_link('totallyinvalid') == False

    # 404 Error
    assert check_link('https://www.google.com/error') == False