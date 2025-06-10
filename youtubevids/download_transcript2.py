from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import configparser

config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')
code_path = config['blog']['blog_temp']


def fetch_transcript_safely(video_id):

    try:

        ytt_api = YouTubeTranscriptApi()

        transcript = ytt_api.fetch(video_id)

        # First try to get transcript in English
        # transcript = YouTubeTranscriptApi.fetch(video_id)

        return transcript
    except (TranscriptsDisabled, NoTranscriptFound):
        # If English not available, try to get any available transcript
        try:
            transcript_list = YouTubeTranscriptApi.list(video_id)

            # Get the first available transcript
            transcript = transcript_list.find_transcript(['en']).fetch(video_id)
            return transcript
        except:
            # If that fails, try auto-generated transcripts
            try:
                transcript_list = YouTubeTranscriptApi.list(video_id)
                # Try to get any transcript (including auto-generated)
                for transcript_info in transcript_list:
                    try:
                        transcript = transcript_info.fetch()
                        return transcript
                    except:
                        continue
                return None
            except Exception as e:
                print(f"No transcripts available for video {video_id}: {e}")
                return None
    except VideoUnavailable:
        print(f"Video {video_id} is unavailable")
        return None
    except Exception as e:
        print(f"Unexpected error fetching transcript for {video_id}: {e}")
        return None


def extract_video_id(url_or_id):
    """Extract clean video ID from various YouTube URL formats"""
    if "=" in url_or_id:
        video_id = url_or_id.partition("=")[2]
    else:
        video_id = url_or_id

    # Remove any additional parameters that might be attached
    if "&" in video_id:
        video_id = video_id.split("&")[0]

    # Clean any remaining special characters
    video_id = video_id.strip()

    return video_id

def fetch_it(video_id):

    # Usage in your code:
    clean_video_id = extract_video_id(video_id)
    print(f"Attempting to fetch transcript for video ID: {clean_video_id}")

    video_text = fetch_transcript_safely(clean_video_id)

    print(video_text)

    transcript_text = ""

    if video_text:
        # Process the transcript
        print("Transcript fetched successfully")
        # Convert transcript list to text if needed

        transcript_path = code_path + "transcript\\"

        file_to_download = transcript_path + "youtube_transcript_" + clean_video_id + ".txt"

        print("File" + file_to_download)

        with open(file_to_download, 'w') as file:
            for snippet in video_text:
                file.write(f"{snippet.text}\n")
                transcript_text += snippet.text
                print(snippet.text)
    else:
        print("Could not fetch transcript for this video")

    return transcript_text

if __name__ == '__main__':
    fetch_it('lLc0ArZj4zQ&t')
    #fetch_it('n1vxc0Q1NQk')