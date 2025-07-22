from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import xml.etree.ElementTree as ET
import time
import requests


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


def check_video_exists(video_id):
    """Check if video exists and is accessible"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except:
        return False


def fetch_transcript_with_retry(video_id, max_retries=3, delay=2):
    """Fetch transcript with retry logic for XML parsing errors"""

    for attempt in range(max_retries):
        try:
            # Get transcript list for the video
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try different transcript types in order of preference
            transcript_methods = [
                lambda tl: tl.find_transcript(['en']),
                lambda tl: tl.find_transcript(['en-US']),
                lambda tl: tl.find_manually_created_transcript(['en']),
                lambda tl: tl.find_generated_transcript(['en']),
                lambda tl: next(iter(tl))  # Get first available transcript
            ]

            for method in transcript_methods:
                try:
                    transcript_obj = method(transcript_list)
                    transcript_data = transcript_obj.fetch()

                    # Verify we got valid data
                    if transcript_data and len(transcript_data) > 0:
                        return transcript_data

                except (NoTranscriptFound, StopIteration):
                    continue
                except ET.ParseError as e:
                    print(f"XML Parse error on attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                        break  # Retry the entire process
                    else:
                        print("Max retries reached for XML parsing")
                        return None
                except Exception as e:
                    print(f"Unexpected error in transcript method: {e}")
                    continue

            # If we get here without XML error, no transcripts were found
            return None

        except TranscriptsDisabled:
            print(f"Transcripts are disabled for video {video_id}")
            return None
        except NoTranscriptFound:
            print(f"No transcript found for video {video_id}")
            return None
        except VideoUnavailable:
            print(f"Video {video_id} is unavailable")
            return None
        except ET.ParseError as e:
            print(f"XML Parse error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                continue
            else:
                print("Max retries reached for XML parsing")
                return None
        except Exception as e:
            print(f"Unexpected error fetching transcript for {video_id}: {e}")
            return None

    return None


def get_video_transcript(video_url_or_id, include_timestamps=False):
    """Main function to get transcript from YouTube video"""
    # Extract clean video ID
    clean_video_id = extract_video_id(video_url_or_id)
    print(f"Attempting to fetch transcript for video ID: {clean_video_id}")

    # Quick check if video exists (optional, can be commented out for speed)
    # if not check_video_exists(clean_video_id):
    #     print(f"Video {clean_video_id} does not exist or is not accessible")
    #     return None

    # Fetch transcript with retry logic
    transcript_data = fetch_transcript_with_retry(clean_video_id)

    if transcript_data:
        if include_timestamps:
            # Return full transcript data with timestamps
            return transcript_data
        else:
            # Convert transcript list to text only
            full_text = " ".join([entry['text'] for entry in transcript_data])
            print(f"Successfully fetched transcript: {len(full_text)} characters")
            return full_text
    else:
        print("Could not fetch transcript for this video")
        return None


def test_alternative_methods(video_id):
    """Test alternative methods to get transcript info"""
    try:
        # Try to get basic video info first
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        print("Available transcripts:")
        for transcript in transcript_list:
            print(f"- Language: {transcript.language}")
            print(f"- Language Code: {transcript.language_code}")
            print(f"- Is Generated: {transcript.is_generated}")
            print(f"- Is Translatable: {transcript.is_translatable}")
            print(f"- Is Fetch: {transcript.fetch(True)}")

    except Exception as e:
        print(f"Could not list transcripts: {e}")


# Usage examples:
if __name__ == "__main__":
    # Test with the problematic video
    test_video = "DrkqMDOD-jQ&t"

    print("=== Testing transcript fetch ===")
    result = get_video_transcript(test_video)

    if result:
        print("SUCCESS: Transcript preview:", result[:200] + "...")
    else:
        print("=== Testing alternative methods ===")
        test_alternative_methods(test_video)