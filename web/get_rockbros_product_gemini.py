import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import re # For regex and cleaning filenames
import json # To potentially parse JSON-like data if regex gets complex

def scrape_product_page(url, num_images_to_download=3):
    """
    Scrapes product info (item, price, description) and downloads images from a URL,
    prioritizing data within a specific JavaScript variable if standard HTML fails.

    Args:
        url (str): The URL of the product page.
        num_images_to_download (int): Max number of relevant images to download.

    Returns:
        dict: A dictionary containing 'title', 'price', 'description',
              and 'downloaded_images' (list of local file paths),
              or None if scraping fails.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    scraped_data = {
        'title': 'Title not found',
        'price': 'Price not found',
        'description': 'Description not found',
        'downloaded_images': []
    } # Initialize with defaults
    downloaded_image_paths = []

    try:
        print(f"Attempting to fetch URL: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        print("URL fetched successfully.")

        soup = BeautifulSoup(response.content, 'html.parser')

        #print(soup)

        # --- Attempt 1: Extract Name and Price from JavaScript ---
        found_in_script = False
        #script_tags = soup.find_all('script', type='text/javascript')
        script_tags = soup.find_all('script')
        print(f"Found {len(script_tags)} script tags. Searching for 'gsf_conversion_data'...")

        for script in script_tags:
            script_content = script.string # Get the text content of the script tag

            #print(script_content)

            if script_content and 'gsf_conversion_data' in script_content:
                print("Found script containing 'gsf_conversion_data'. Extracting data...")

                # Regex to find the name within the product_data structure
                # Looks for: name : "VALUE", handling potential whitespace
                name_match = re.search(r'name\s*:\s*"(.*?)"', script_content)
                if name_match:
                    scraped_data['title'] = name_match.group(1).strip()
                    print(f"  Extracted Title: {scraped_data['title']}")
                    found_in_script = True # Mark that we found at least part of the data

                # Regex to find the price within the product_data structure
                # Looks for: price : "VALUE", handling potential whitespace
                price_match = re.search(r'price\s*:\s*"(.*?)"', script_content)
                if price_match:
                    scraped_data['price'] = f"${price_match.group(1).strip()}" # Add currency symbol for clarity
                    print(f"  Extracted Price: {scraped_data['price']}")
                    found_in_script = True # Mark that we found at least part of the data

                # If we found both in this script, no need to check others
                if scraped_data['title'] != 'Title not found' and scraped_data['price'] != 'Price not found':
                     break # Exit the loop once data is found

        if not found_in_script:
            print("Could not find 'gsf_conversion_data' or extract data from scripts.")
            # --- Fallback Attempt: Extract Item Name (Title) from H1 (Original Method) ---
            title_tag = soup.find('h1', class_='product__title')
            if title_tag:
                scraped_data['title'] = title_tag.get_text(strip=True)
                print(f"  Fallback: Found Title in H1 tag: {scraped_data['title']}")

            # --- Fallback Attempt: Extract Price from Span (Original Method) ---
            price_container = soup.find('div', class_='price')
            if price_container:
                price_tag = price_container.find('span', class_='price-item') # More general class
                if price_tag:
                     scraped_data['price'] = price_tag.get_text(strip=True)
                     print(f"  Fallback: Found Price in span tag: {scraped_data['price']}")


        # --- 3. Extract Description (Keep original method) ---
        description_tag = soup.find('div', class_='product__description')
        if description_tag:
             scraped_data['description'] = description_tag.get_text(separator='\n', strip=True)
        else:
            desc_fallback = soup.find('div', class_='rte')
            scraped_data['description'] = desc_fallback.get_text(separator='\n', strip=True) if desc_fallback else scraped_data['description'] # Keep default if not found

        if scraped_data['description'] != 'Description not found':
            print("Found description.")
        else:
            print("Description tag not found.")


        # --- 4. Find Image URLs (Keep original method) ---
        image_urls = []
        media_gallery = soup.find('div', class_='product__media-list')
        img_tags = []
        if media_gallery:
            img_tags = media_gallery.find_all('img')
            print(f"Found {len(img_tags)} image tags in media gallery.")
        else:
             print("Warning: Specific media gallery container not found, searching all img tags.")
             img_tags = soup.find_all('img')


        for img in img_tags:
            src = img.get('src') or img.get('data-src')
            if src:
                if src.startswith('//'):
                    src = 'https:' + src
                absolute_url = urljoin(url, src)
                parsed_img_url = urlparse(absolute_url)
                if (parsed_img_url.scheme in ['http', 'https'] and
                    any(absolute_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']) and
                    absolute_url not in image_urls):
                     image_urls.append(absolute_url)

        print(f"Found {len(image_urls)} unique, valid image URLs.")

        # --- 5. Download Images (Keep original method) ---
        if not image_urls:
            print("No suitable image URLs found to download.")
            # scraped_data['downloaded_images'] already initialized as []
            return scraped_data

        image_dir = "rockbros_product_images"
        os.makedirs(image_dir, exist_ok=True)
        print(f"Saving images to directory: '{image_dir}'")

        count = 0
        for img_url in image_urls:
            if count >= num_images_to_download:
                break
            try:
                img_response = requests.get(img_url, headers=headers, stream=True, timeout=10)
                img_response.raise_for_status()

                parsed_url = urlparse(img_url)
                img_filename = os.path.basename(parsed_url.path)
                img_filename = re.sub(r'[\\/*?:"<>|]', "_", img_filename)
                if not img_filename or '.' not in img_filename:
                     img_filename = f"image_{count+1}.jpg"

                filepath = os.path.join(image_dir, img_filename)

                with open(filepath, 'wb') as f:
                    for chunk in img_response.iter_content(8192):
                        f.write(chunk)

                downloaded_image_paths.append(filepath)
                print(f"  Downloaded ({count+1}/{num_images_to_download}): {img_url} -> {filepath}")
                count += 1

            except requests.exceptions.RequestException as e:
                print(f"  Error downloading image {img_url}: {e}")
            except IOError as e:
                print(f"  Error saving image {img_url} to {filepath}: {e}")
            except Exception as e:
                print(f"  An unexpected error occurred for image {img_url}: {e}")

        scraped_data['downloaded_images'] = downloaded_image_paths
        return scraped_data

    except requests.exceptions.Timeout:
        print(f"Error: Request timed out for URL {url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP Error {e.response.status_code} for URL {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch URL {url}. Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_rock_product(target_url):

    o = {}

    # --- Main Execution ---
    target_url = "https://rockbrosbike.us/products/rockbros-cycling-glassesmtb-biking-sports-sunglasses-with-anti-blue-lenses-men?ref=glgipqco"
    product_info = scrape_product_page(target_url, num_images_to_download=3)

    print("\n" + "="*30)
    if product_info:
        print("--- Scraped Product Information ---")
        print(f"Title: {product_info.get('title', 'N/A')}")
        print(f"Price: {product_info.get('price', 'N/A')}")
        print(f"\nDescription:\n{product_info.get('description', 'N/A')[:500]}...") # Print first 500 chars
        print(f"\nDownloaded Images ({len(product_info.get('downloaded_images', []))} stored in '{os.path.abspath('../zTemp/rockbros_product_images')}'):")
        for img_path in product_info.get('downloaded_images', []):
            print(f"- {img_path}")
    else:
        print("Failed to scrape product information.")
    print("="*30)


    try:
        o["title"]=product_info.get('title', 'N/A')
    except:
        o["title"]=None


    try:
        o["price"]=product_info.get('price', 'N/A')
    except:
        o["price"]=None


    images = product_info.get('downloaded_images', [])
    o["images"] = images

    return o

if __name__ == "__main__":
    target_url = "https://rockbrosbike.us/products/rockbros-cycling-glassesmtb-biking-sports-sunglasses-with-anti-blue-lenses-men?ref=glgipqco"
    get_rock_product(target_url)
