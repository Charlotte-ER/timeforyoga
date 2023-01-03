import os, pytest, sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.append('..')
from yoga import parse_command_line_arguments, check_url_is_valid, get_uploads_playlist_from_channel_name, get_videos_in_playlist, get_videos_within_5_mins_of_max_duration, reformat_playtime_to_minutes


def test_parse_command_line_arguments():
    # Valid number of minutes supplied
    sys.argv = ['yoga.py', '-t', '35']
    assert parse_command_line_arguments() == (35, 'yogawithadriene')

    # Channel name provided is a string
    sys.argv = ['yoga.py', '-c', 'avalidchannelname']
    assert parse_command_line_arguments() == (30, 'avalidchannelname')

    # No command line arguments
    sys.argv = ['yoga.py']
    assert parse_command_line_arguments() == (30, 'yogawithadriene')

    # No flag provided
    sys.argv = ['yoga.py', '35']
    with pytest.raises(SystemExit):
        assert parse_command_line_arguments()

    # Invalid flag provided
    sys.argv = ['yoga.py', '-n', '35']
    with pytest.raises(SystemExit):
        assert parse_command_line_arguments()

    # Minutes not provided
    sys.argv = ['yoga.py', '-t']
    with pytest.raises(SystemExit):
        assert parse_command_line_arguments()

    # Float provided
    sys.argv = ['yoga.py', '-t', "4.5"]
    with pytest.raises(SystemExit):
        assert parse_command_line_arguments()

    # String provided
    sys.argv = ['yoga.py', '-t', "cat"]
    with pytest.raises(SystemExit):
        assert parse_command_line_arguments()

    # Zero minutes provided
    sys.argv = ['yoga.py', '-t', "0"]
    with pytest.raises(SystemExit):
        assert parse_command_line_arguments()

    # Negative minutes provided
    sys.argv = ['yoga.py', '-t', "-10"]
    with pytest.raises(SystemExit):
        assert parse_command_line_arguments()


def youtube_api_builder_for_tests():
    return build('youtube', 'v3', developerKey=os.environ.get('YT_API_KEY'))


def test_get_uploads_playlist_from_channel_name():
    youtube = youtube_api_builder_for_tests()

    # Valid channel name provided
    assert get_uploads_playlist_from_channel_name(youtube, 'yogawithadriene') == 'UUFKE7WVJfvaHW5q283SxchA'

    # Invalid channel name provided
    with pytest.raises(KeyError):
        assert get_uploads_playlist_from_channel_name(youtube, 'not a channel name')


def test_get_videos_in_playlist():
    youtube = youtube_api_builder_for_tests()

    # Valid playlist provided
    assert type(get_videos_in_playlist(youtube, 'UUFKE7WVJfvaHW5q283SxchA')) == list

    # Playlist provided contains videos
    assert len(get_videos_in_playlist(youtube, 'UUFKE7WVJfvaHW5q283SxchA')) > 0

    # Invalid playlist provided
    with pytest.raises(HttpError):
        get_videos_in_playlist(youtube, 'not a playlist id')


def test_get_videos_within_5_mins_of_max_duration():
    youtube = youtube_api_builder_for_tests()
    sample_videos = ['bYQwM841ED4', 'LTdBUmHDA4s', 'p8oxM5j9eNE', 'raUEsDttCL4', 'ZbtVVYBLCug', 'GK28p-OdM4Y', 'j7rKKpwdXNE', 'CLDHeV9OI5U', 'klmBssEYkdU', '62rrpPfiAoI', 'vNyJuQuuMC8', 'zwoVcrdmLOE', 'AB3Y-4a3ZrU', '6uVSkvWO7As', 'x2j6rP0h7qg', 'QUPAFGv72PM', 'Ro_nYcdGVgM', 'uIfX-EqwWcM', '8CUzG_ny6sg', 'O7unqSzJhuM', 'JhU16ECcd5Y', 'lwmy2lGGy3A', 'IHow3Qt86jc', 'CEbfCdeLt9E', 'hPyBU52P_Xc', 'JnXP-60Og7E', 'YqyYCmem2oM', 'qWwN8DnEBBA', 'GfsnsS0Bq7I', 'vACdgwUuXII', 'K1RGa6sW4ME', 'KtJPbD8eUTU', 'Ev9cKmJZy8c', 'HUAvxMQWg1k', '6s5MEhUblzQ', '6xMcGzuORCM', 'EZ8H7AvIF3k', 'KxlAXZUmevo', 'I1VUTQCCgdw', 'dWpplJRh4xw', 'HnEqUkVNmPU', 'wDIr92u-2cY', 'qj9YLsjdAJg', 'GcclN_MKWsI', 'tLcHTdzykgk', 'Pmlh6AHFW0E', 'reZZP3f01Oc', '41_j1bkP0sc', 'QeELEBpVqhE']
    
    assert get_videos_within_5_mins_of_max_duration(youtube, sample_videos, 10) == {'p8oxM5j9eNE': 7, 'Pmlh6AHFW0E': 6}
    assert get_videos_within_5_mins_of_max_duration(youtube, sample_videos, 40) == {'AB3Y-4a3ZrU': 36, 'x2j6rP0h7qg': 38}
    assert get_videos_within_5_mins_of_max_duration(youtube, [], 40) == {}


def test_reformat_playtime_to_minutes():
    assert reformat_playtime_to_minutes('PT9H29M59S') == 569
    assert reformat_playtime_to_minutes('PT3M59S') == 3
    assert reformat_playtime_to_minutes('PT59S') == 0
    assert reformat_playtime_to_minutes('not a playtime') == 0


def test_check_url_is_valid():
    # Valid link
    assert check_url_is_valid('https://www.google.co.uk/') == True

    # Invalid Link
    assert check_url_is_valid('totallyinvalid') == False

    # 404 Error
    assert check_url_is_valid('https://www.google.com/error') == False