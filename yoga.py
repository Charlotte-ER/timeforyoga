import argparse, math, os, random, re, requests, sys, webbrowser
from googleapiclient.discovery import build


def main():
    max_playtime, channel_name = parse_command_line_arguments()

    with build('youtube', 'v3', developerKey=os.environ.get('YT_API_KEY')) as youtube:
        uploads_playlist_id = get_uploads_playlist_from_channel_name(youtube, channel_name)
        all_channel_videos = get_videos_in_playlist(youtube, uploads_playlist_id)
        videos = get_videos_of_correct_length(youtube, all_channel_videos, max_playtime)

    url = f'https://www.youtube.com/watch?v={random.choice(list(videos))}'

    if check_link(url):
        webbrowser.open_new(url)


def parse_command_line_arguments():
    """
    Parse command line arguments to get maximum video duration and channel name
    
    :return: Number of minutes available and channel name to select video from
    :rtype: tuple
    """
    parser = argparse.ArgumentParser(description='How long do you have available for yoga?')
    parser.add_argument('-t', '--time', default=30, help='number of minutes available', type=int)
    parser.add_argument('-c', '--channel', default='yogawithadriene', help='name of youtube channel', type=str)
    
    args = parser.parse_args()

    if args.time <= 0:
        sys.exit("No time!")

    return args.time, args.channel


def get_uploads_playlist_from_channel_name(youtube, channel_name):
    """
    Given channel name, return id of 'Uploads' playlist.
    
    :param youtube: Authenticated YouTube Data API service
    :type youtube: googleapiclient.discovery.Resource
    :param channel_name: Name of a YouTube channel
    :type channel_name: str
    :return: ID of the playlist containing all videos uploaded by specified channel
    :rtype: str
    """
    request = youtube.channels().list(part='contentDetails', forUsername=channel_name)
    response = request.execute()
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def get_videos_in_playlist(youtube, playlist_id):
    """
    Given a playlist id, return list of videos in playlist.
    
    :param youtube: Authenticated YouTube Data API service
    :type youtube: googleapiclient.discovery.Resource
    :param playlist_id: ID of a playlist on YouTube
    :type playlist_id: str
    :return: list of IDs of all videos in the specified playlist
    :rtype: list
    """
    nextPageToken = None
    videos = []
    while True:
        request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            )
        response = request.execute()

        for item in response['items']:
            videos.append(item['contentDetails']['videoId'])
        nextPageToken = response.get('nextPageToken')
        
        if not nextPageToken:
            break

    return videos


def get_videos_of_correct_length(youtube, videos, max_playtime):
    """
    Create a dictionary of videos that make best use of the available time.

    Given a list of video ids and maximum available time, retrieve the playtime
    in minutes for each video specified in the list. Add videos that have an 
    acceptable duration to a dictionary containing their video ID and duration
    in minutes. Videos are too long if their duration exceeds the specified 
    maximum playtime. The minimum allowed duration of videos is determined by 
    the get_minimum_playtime function.  Videos that are too long or too short
    are ignored.
    
    :param youtube: Authenticated YouTube Data API service
    :type youtube: googleapiclient.discovery.Resource
    :param videos: List of YouTube video IDs
    :type videos: list
    :param max_playtime: Maximum duration of video allowed, in whole minutes
    :type max_playtime: int
    :return: dictionary of video IDs alongside each video's duration in minutes
    :rtype: dict
    """
    yt_max_batch_size = 50
    video_lengths = {}
    batches_needed = int(math.ceil(len(videos)/yt_max_batch_size))
    batch_index = 0
    
    for _ in range(batches_needed):
        try:
            batch = videos[batch_index : batch_index + yt_max_batch_size]
        except IndexError:
            batch = videos[batch_index : ]

        batch_index += yt_max_batch_size
        request = youtube.videos().list(part='contentDetails', id=','.join(batch))
        response = request.execute()
        
        for item in response['items']:
            playtime = item['contentDetails']['duration']
            duration = reformat_playtime_to_minutes(playtime)
            if max_playtime >= duration and get_minimum_playtime(max_playtime) <= duration:
                video_lengths.update({item['id'] : duration})
    
    return video_lengths


def reformat_playtime_to_minutes(t):
    """
    Given a playtime in YouTube's format, return duration rounded down to nearest whole minute.
    
    :param t: Duration of video in YouTube's playtime format
    :type t: str
    :return: Number of minutes
    :rtype: int
    """
    matches = re.search(r'^PT(?:(\d+)H)?(\d+)M(\d+)S$', t)
    if matches:
        hours = int(matches.group(1)) if matches.group(1) else 0
        minutes = int(matches.group(2)) if matches.group(2) else 0
        duration = (hours*60) + minutes
    else:
        duration = 0
    return duration


def get_minimum_playtime(max):
    """
    Get shortest allowed video duration, defined as 5 minutes less than maximum playtime.

    :param max: Number of minutes available
    :type max: int
    :return: Number of minutes
    :rtype: int
    """
    if max <= 5:
        min = 0
    else:
        min = max - 5
    return min


def check_link(url):
    """
    Check if url is a valid link.

    :param url: URL to be checked
    :type max: str
    :return: True if link is valid, otherwise False
    :rtype: bool
    """
    success_state = False
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        pass
    else:
        if response.status_code == 200:
            success_state = True
    return success_state


if __name__ == '__main__':
    main()