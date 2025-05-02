import sys
import os
from urllib.parse import urlparse
import re
from newspaper import Article, ArticleException
import requests # newspaper uses requests, but good to handle potential request errors explicitly


def sanitize_filename(filename):
    """Removes or replaces characters invalid for filenames."""
    # Remove invalid characters
    sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(" ", "_")
    # Truncate if too long (optional, depends on filesystem limits)
    max_len = 100
    if len(sanitized) > max_len:
        sanitized = sanitized[:max_len]
    # Ensure it's not empty
    if not sanitized:
        sanitized = "untitled_article"
    return sanitized


def generate_filename_from_url(url):
    """Generates a plausible filename from the URL path."""
    try:
        parsed_url = urlparse(url)
        # Get the last part of the path
        path_parts = [part for part in parsed_url.path.split('/') if part]
        if path_parts:
            # Use the last part as the base name
            base_name = path_parts[-1]
        elif parsed_url.netloc:
             # Use domain if path is empty
             base_name = parsed_url.netloc.replace('www.','')
        else:
            # Fallback
            base_name = "article"

        # Sanitize and add extension
        filename = sanitize_filename(base_name) + ".txt"
        return filename
    except Exception:
        # Fallback in case of parsing error
        return "article.txt"


def download_article_text(url, output_filename=None):
    """
    Downloads the main text content of an article from a URL
    and saves it to a text file.
    """
    print(f"Attempting to download article from: {url}")

    # Create an Article object
    article = Article(url)

    try:
        # Download the HTML content
        # Setting a user-agent can sometimes help avoid blocks
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        article.download(input_html=requests.get(url, headers=headers, timeout=15).text) # Download manually with headers
        print("Download complete.")

        # Parse the article to extract main content
        article.parse()
        print("Parsing complete.")

        # Get the extracted text
        article_text = article.text

        if not article_text:
            print("Warning: Could not extract article text.")
            return False

        # Determine the output filename
        if output_filename is None:
            output_filename = "c:\\dep\\ContentAI\\zTemp\\articles\\" + generate_filename_from_url(url)

        # Save the text to the file
        print(f"Saving article text to: {output_filename}")
        try:
            # Use utf-8 encoding for broad character support
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(f"Source URL: {url}\n\n") # Optional: Add URL to file
                f.write(f"Title: {article.title}\n\n") # Optional: Add title
                f.write("--- Article Text ---\n\n")
                f.write(article_text)
            print(f"Successfully saved article to {output_filename}")
            return True
        except IOError as e:
            print(f"Error: Could not write to file {output_filename}. Reason: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during file writing: {e}")
            return False

    except requests.exceptions.RequestException as e:
         print(f"Error: Network error downloading URL. Reason: {e}")
         return False
    except ArticleException as e:
        print(f"Error: Failed to process the article. Reason: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1) # Exit if something unexpected happened


# --- Main execution part ---
if __name__ == "__main__":

    # Example URL from your question
    default_url = "https://www.ironman.com/news/2026-world-championship-announcement?utm_campaign=7180588-GLOBAL%202025%20-%20IM%20%7C%20Global%20-%20Emails&utm_medium=email&_hsenc=p2ANqtz-8ZGdXZOzTV-aUf_CnSGKj2QpLyjMg-AmfXgTAcmTLs25rZN4FPcW5SVjWiqWggZA1VMo-xqJ1-nOutNsSrHeDW-jqosg&_hsmi=359200270&utm_content=359200270&utm_source=hs_email"

    # Download and save the article
    download_article_text(default_url)