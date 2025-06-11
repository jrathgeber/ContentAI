from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable


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


def fetch_transcript_safely(video_id):
    try:
        # Get transcript list for the video
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try to find English transcript first
        try:
            transcript = transcript_list.find_transcript(['en']).fetch()
            return transcript
        except NoTranscriptFound:
            # If no English transcript, try any manually created transcript
            try:
                transcript = transcript_list.find_manually_created_transcript(['en']).fetch()
                return transcript
            except NoTranscriptFound:
                # If no manual transcript, try auto-generated
                try:
                    transcript = transcript_list.find_generated_transcript(['en']).fetch()
                    return transcript
                except NoTranscriptFound:
                    # Last resort: get any available transcript
                    for transcript_info in transcript_list:
                        try:
                            transcript = transcript_info.fetch()
                            print(f"Using transcript in language: {transcript_info.language}")
                            return transcript
                        except:
                            continue
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
    except Exception as e:
        print(f"Unexpected error fetching transcript for {video_id}: {e}")
        return None


def get_video_transcript(video_url_or_id):
    """Main function to get transcript from YouTube video"""
    # Extract clean video ID
    clean_video_id = extract_video_id(video_url_or_id)
    print(f"Attempting to fetch transcript for video ID: {clean_video_id}")

    # Fetch transcript
    video_text = fetch_transcript_safely(clean_video_id)

    if video_text:
        # Convert transcript list to text
        full_text = " ".join([entry['text'] for entry in video_text])
        print(f"Successfully fetched transcript: {len(full_text)} characters")
        return full_text
    else:
        print("Could not fetch transcript for this video")
        return None


# Usage example:
# Replace your current line with:
# video_text = get_video_transcript(value)

# Or if you want just the transcript data (list of dicts):
# transcript_data = fetch_transcript_safely(extract_video_id(value))

# For debugging, you can also do:
if __name__ == "__main__":
    # Test with a video URL or ID
    test_video = "73_PDzqByIY"
    result = get_video_transcript(test_video)
    if result:
        print("Transcript preview:", result[:200] + "...")
    else:
        print("No transcript available")

