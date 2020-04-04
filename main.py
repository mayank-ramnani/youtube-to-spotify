import os
import argparse
import googleapiclient.discovery
import youtube_dl

class DownloadLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

def ydl_progress_hook(d):
    if d['status'] == 'finished':
        print(f'Downloading { d["filename"] } finished, now converting ...')

class SaveYoutube:
    # class variables
    api_key = os.environ.get("YOUTUBE_API_KEY") 

    # class methods, also accesible by objects
    def __init__(self):
        self.youtube = self.get_youtube_client()
        self.videos = []

    # returns the youtube client
    def get_youtube_client(self):
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=self.api_key)

    # populates videos list with title and id of videos in the playlist
    def get_playlist_videos(self, playlist_id):
        request = self.youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId=playlist_id
        )
        # add support for fetching next page contents as well, only 50 results supported for now, check 'pageInfo' in response
        response = request.execute()
        for item in response["items"]:
            video = {}
            video["title"] = item["snippet"]["title"]
            video["id"] = item["snippet"]["resourceId"]["videoId"]
            self.videos.append(video)

    # transform the {title, id} array to {title, url}
    def make_youtube_urls(self):
        for video in self.videos:
            video["url"] = "https://www.youtube.com/watch?v=" + video["id"]

    def download_videos(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        'outtmpl': '%(title)s.%(ext)s',
        'logger': DownloadLogger(),
        'progress_hooks': [ydl_progress_hook],
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)

        for video in self.videos:
            ydl.download([video["url"]])

if __name__ == "__main__":
    # parse arguments
    arg_parser = argparse.ArgumentParser(description="Download music from any playlist on youtube")
    arg_parser.add_argument("-p", "--playlist-id", type=str, help="id of playlist to download")
    arg_parser.add_argument("-u", "--playlist-url", type=str, help="url of playlist to download")
    arg_parser.add_argument("-o", "--output-dir", type=str, help="output directory to download songs in")
    args = arg_parser.parse_args()

    playlist_id = args.playlist_id
    playlist_url = args.playlist_url
    output_dir = args.output_dir
    # playlist_id = "PLzMsvNpDYBM7ZdOvJdNVZkDhh9RHPkatv"
    # id for my 'new music' playlist
    playlist_id = "PLzMsvNpDYBM4DzLBWSuksozXUpDZxCyFD"

    save_youtube = SaveYoutube()
    save_youtube.get_playlist_videos(playlist_id)
    save_youtube.make_youtube_urls()
    print(save_youtube.videos)
    save_youtube.download_videos()


"""
enhancements:
    get the full playlist link and then extract the playlist id yourself.

    support for liked playlist, private playlists, watch later: would have to use google user authentication for  that.

    ***change download path to use the argument given instead of downloading in current dir.
    if unable to find option in youtube-dl, just change the current directory before calling download.
"""