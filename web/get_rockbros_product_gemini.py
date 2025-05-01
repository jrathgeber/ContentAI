import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import re # For regex and cleaning filenames
import json

def scrape_product_page(url, num_images_to_download=3):
    """
    Scrapes product info (item, price, description) and downloads images from a URL,
    checking standard HTML, JavaScript variables, and Open Graph meta tags.

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
    }
    downloaded_image_paths = []
    image_urls = [] # Initialize list to store all potential image URLs

    try:
        print(f"Attempting to fetch URL: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        print("URL fetched successfully.")

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- 1. Extract Name and Price (Prioritize JavaScript, then Fallback) ---
        found_in_script = False
        # Use the corrected find_all('script')
        script_tags = soup.find_all('script')
        print(f"Found {len(script_tags)} script tags. Searching for 'gsf_conversion_data'...")

        for script in script_tags:
            script_content = script.string
            if script_content and 'gsf_conversion_data' in script_content:
                print("Found script containing 'gsf_conversion_data'. Extracting data...")
                name_match = re.search(r'name\s*:\s*"(.*?)"', script_content)
                if name_match:
                    scraped_data['title'] = name_match.group(1).strip()
                    print(f"  Extracted Title: {scraped_data['title']}")
                    found_in_script = True

                price_match = re.search(r'price\s*:\s*"(.*?)"', script_content)
                if price_match:
                    # Try to find currency as well, default to $
                    currency_symbol = "$"
                    currency_match = re.search(r'currency\s*:\s*"([A-Z]{3})"', script_content)
                    if currency_match:
                         # You could add logic here to map USD -> $, EUR -> €, etc. if needed
                         pass # Keep default $ for now
                    scraped_data['price'] = f"{currency_symbol}{price_match.group(1).strip()}"
                    print(f"  Extracted Price: {scraped_data['price']}")
                    found_in_script = True

                if scraped_data['title'] != 'Title not found' and scraped_data['price'] != 'Price not found':
                     break

        if not found_in_script:
            print("Could not find 'gsf_conversion_data' or extract data from scripts. Using fallbacks.")
            title_tag = soup.find('h1', class_='product__title')
            if title_tag:
                scraped_data['title'] = title_tag.get_text(strip=True)
                print(f"  Fallback: Found Title in H1 tag: {scraped_data['title']}")

            price_container = soup.find('div', class_='price')
            if price_container:
                # Look for any span with 'price-item' class within the container
                price_tag = price_container.find('span', class_=lambda x: x and 'price-item' in x.split())
                if price_tag:
                     scraped_data['price'] = price_tag.get_text(strip=True)
                     print(f"  Fallback: Found Price in span tag: {scraped_data['price']}")

        # --- 2. Extract Description (Keep original method) ---
        description_tag = soup.find('div', class_='product__description')
        if description_tag:
             scraped_data['description'] = description_tag.get_text(separator='\n', strip=True)
        else:
            # Fallback check using og:description meta tag
            og_desc_tag = soup.find('meta', property='og:description')
            if og_desc_tag and og_desc_tag.get('content'):
                 scraped_data['description'] = og_desc_tag['content'].strip()
                 print("Found description in 'og:description' meta tag.")
            else:
                # Original fallback if product__description and og:description fail
                desc_fallback = soup.find('div', class_='rte')
                scraped_data['description'] = desc_fallback.get_text(separator='\n', strip=True) if desc_fallback else scraped_data['description']

        if scraped_data['description'] != 'Description not found':
            if not description_tag and not (og_desc_tag and og_desc_tag.get('content')):
                 print("Found description in 'div.rte' fallback.")
            elif not description_tag:
                 pass # Already printed the og:description message
            else:
                 print("Found description in 'div.product__description'.")
        else:
            print("Description tag not found.")


        # --- 3. Find Image URLs (Combine Meta Tags and Img Tags) ---

        # Method A: Check Open Graph Meta Tags
        print("Searching for 'og:image' meta tags...")
        og_image_tags = soup.find_all('meta', property='og:image')
        print(f"Found {len(og_image_tags)} 'og:image' meta tags.")
        for tag in og_image_tags:
            og_url = tag.get('content')
            if og_url:
                # OG URLs are typically absolute, but urljoin is safe
                absolute_url = urljoin(url, og_url)
                # Basic validation
                parsed_img_url = urlparse(absolute_url)
                if (parsed_img_url.scheme in ['http', 'https'] and
                    any(absolute_url.lower().split('?')[0].endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']) and # Check before query params
                    absolute_url not in image_urls):
                     print(f"  Found unique image URL in meta tag: {absolute_url}")
                     image_urls.append(absolute_url)

        # Method B: Check Specific Media Gallery or Fallback to All Img Tags
        print("Searching for images in primary media gallery or all img tags...")
        media_gallery = soup.find('div', class_='product__media-list')
        img_tags = []
        if media_gallery:
            img_tags = media_gallery.find_all('img')
            print(f"Found {len(img_tags)} image tags in media gallery.")
        else:
             print("Warning: Specific media gallery container not found, searching all img tags.")
             img_tags = soup.find_all('img')
             print(f"Found {len(img_tags)} img tags overall.")

        for img in img_tags:
            src = img.get('src') or img.get('data-src')
            if src:
                # Clean '//' prefix
                if src.startswith('//'):
                    src = 'https:' + src

                absolute_url = urljoin(url, src)
                parsed_img_url = urlparse(absolute_url)
                if (parsed_img_url.scheme in ['http', 'https'] and
                    any(absolute_url.lower().split('?')[0].endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']) and # Check before query params
                    absolute_url not in image_urls): # Avoid duplicates from meta tags or other imgs
                     print(f"  Found unique image URL in img tag: {absolute_url}")
                     image_urls.append(absolute_url)


        print(f"Found a total of {len(image_urls)} unique, valid image URLs.")

        # --- 4. Download Images (Uses the combined image_urls list) ---
        if not image_urls:
            print("No suitable image URLs found to download.")
            return scraped_data # scraped_data['downloaded_images'] is already []

        image_dir = "rockbros_product_images"
        os.makedirs(image_dir, exist_ok=True)
        print(f"Saving images to directory: '{image_dir}'")

        count = 0
        for img_url in image_urls:
            if count >= num_images_to_download:
                print(f"Reached download limit ({num_images_to_download}).")
                break
            try:
                # Add timeout to image request as well
                img_response = requests.get(img_url, headers=headers, stream=True, timeout=20)
                img_response.raise_for_status()

                parsed_url = urlparse(img_url)
                # Use the path part before any query string for the filename base
                img_filename_base = os.path.basename(parsed_url.path)
                img_filename = re.sub(r'[\\/*?:"<>|]', "_", img_filename_base)

                # Handle cases where filename is empty or has no extension after cleaning/parsing
                if not img_filename or '.' not in os.path.splitext(img_filename)[1]:
                     # Try to get extension from Content-Type header if possible
                     content_type = img_response.headers.get('Content-Type')
                     ext = '.jpg' # Default extension
                     if content_type:
                         if 'jpeg' in content_type: ext = '.jpg'
                         elif 'png' in content_type: ext = '.png'
                         elif 'gif' in content_type: ext = '.gif'
                         elif 'webp' in content_type: ext = '.webp'
                     img_filename = f"image_{count+1}{ext}"
                     print(f"  Generated filename: {img_filename} (from URL: {img_url})")


                filepath = os.path.join(image_dir, img_filename)

                with open(filepath, 'wb') as f:
                    for chunk in img_response.iter_content(8192):
                        f.write(chunk)

                downloaded_image_paths.append(filepath)
                print(f"  Downloaded ({count+1}/{len(image_urls)}): {img_url} -> {filepath}")
                count += 1

            except requests.exceptions.Timeout:
                print(f"  Timeout downloading image {img_url}")
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

    try:
        o["description"]=product_info.get('description', 'N/A')
    except:
        o["description"]=None

    images = product_info.get('downloaded_images', [])
    o["images"] = images

    return o


if __name__ == "__main__":
    target_url = "https://rockbrosbike.us/products/rockbros-cycling-glassesmtb-biking-sports-sunglasses-with-anti-blue-lenses-men?ref=glgipqco"
    tu2 = "https://rockbrosbike.us/products/rockbros-m1-wireless-bike-computer-waterproof-2-9inch-lcd-screen-gps-bds-galileo-position-system?ref=glgipqco"
    tu3 = "https://rockbrosbike.us/collections/up-to-50-off-clearence/products/rockbros-unisex-road-bike-helmet-for-adults-integrated-design-for-mtb-and-road"
    get_rock_product(tu2)
