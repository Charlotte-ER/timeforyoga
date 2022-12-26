from yoga import get_user_input, validate, get_minimum_playtime, check_link, get_uploads_playlist_from_channel_name, get_videos_in_playlist, get_videos_of_correct_length, reformat_playtime_to_minutes

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os, pytest, sys


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


def youtube_api_builder_for_tests():
    return build('youtube', 'v3', developerKey=os.environ.get('YT_API_KEY'))


def test_get_uploads_playlist_from_channel_name():
    youtube = youtube_api_builder_for_tests()
    assert get_uploads_playlist_from_channel_name(youtube, 'yogawithadriene') == 'UUFKE7WVJfvaHW5q283SxchA'


def test_get_videos_in_playlist():
    youtube = youtube_api_builder_for_tests()
    assert type(get_videos_in_playlist(youtube, 'UUFKE7WVJfvaHW5q283SxchA')) == list
    assert len(get_videos_in_playlist(youtube, 'UUFKE7WVJfvaHW5q283SxchA')) > 0
    with pytest.raises(HttpError):
        get_videos_in_playlist(youtube, 'not a playlist id')


def test_get_videos_of_correct_length():
    youtube = youtube_api_builder_for_tests()
    sample_videos = ['bYQwM841ED4', 'LTdBUmHDA4s', 'p8oxM5j9eNE', 'raUEsDttCL4', 'ZbtVVYBLCug', 'GK28p-OdM4Y', 'j7rKKpwdXNE', 'CLDHeV9OI5U', 'klmBssEYkdU', '62rrpPfiAoI', 'vNyJuQuuMC8', 'zwoVcrdmLOE', 'AB3Y-4a3ZrU', '6uVSkvWO7As', 'x2j6rP0h7qg', 'QUPAFGv72PM', 'Ro_nYcdGVgM', 'uIfX-EqwWcM', '8CUzG_ny6sg', 'O7unqSzJhuM', 'JhU16ECcd5Y', 'lwmy2lGGy3A', 'IHow3Qt86jc', 'CEbfCdeLt9E', 'hPyBU52P_Xc', 'JnXP-60Og7E', 'YqyYCmem2oM', 'qWwN8DnEBBA', 'GfsnsS0Bq7I', 'vACdgwUuXII', 'K1RGa6sW4ME', 'KtJPbD8eUTU', 'Ev9cKmJZy8c', 'HUAvxMQWg1k', '6s5MEhUblzQ', '6xMcGzuORCM', 'EZ8H7AvIF3k', 'KxlAXZUmevo', 'I1VUTQCCgdw', 'dWpplJRh4xw', 'HnEqUkVNmPU', 'wDIr92u-2cY', 'qj9YLsjdAJg', 'GcclN_MKWsI', 'tLcHTdzykgk', 'Pmlh6AHFW0E', 'reZZP3f01Oc', '41_j1bkP0sc', 'QeELEBpVqhE']
    get_videos_of_correct_length(youtube, sample_videos, 10) == {'p8oxM5j9eNE': 7, 'Pmlh6AHFW0E': 6}
    get_videos_of_correct_length(youtube, sample_videos, 40) == {'AB3Y-4a3ZrU': 36, 'x2j6rP0h7qg': 38}
    get_videos_of_correct_length(youtube, [], 40) == {}


def test_reformat_playtime_to_minutes():
    reformat_playtime_to_minutes('PT9H29M59S') == 29
    reformat_playtime_to_minutes('PT3M59S') == 3
    reformat_playtime_to_minutes('PT59S') == 0
    reformat_playtime_to_minutes('not a playtime') == 0


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