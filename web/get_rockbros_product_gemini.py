import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import re # For cleaning filenames

def scrape_product_page(url, num_images_to_download=3):
    """
    Scrapes product info (item, price, description) and downloads images from a URL.

    Args:
        url (str): The URL of the product page.
        num_images_to_download (int): Max number of relevant images to download.

    Returns:
        dict: A dictionary containing 'title', 'price', 'description',
              and 'downloaded_images' (list of local file paths),
              or None if scraping fails.
    """
    headers = {
        # Mimic a browser to avoid potential blocking
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    scraped_data = {}
    downloaded_image_paths = []

    try:
        print(f"Attempting to fetch URL: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print("URL fetched successfully.")

        soup = BeautifulSoup(response.content, 'html.parser')

        print(soup)

        # --- 1. Extract Item Name (Title) ---
        # Inspecting the page, the title is in an <h1> with class 'product__title'
        title_tag = soup.find('h1', class_='product__title')
        scraped_data['title'] = title_tag.get_text(strip=True) if title_tag else "Title not found"

        # --- 2. Extract Price ---
        # Price seems to be in a <span> with class 'price-item--regular' inside a div with class 'price'
        # It might also be 'price-item--sale' if on sale
        price_container = soup.find('div', class_='price')
        if price_container:
            price_tag = price_container.find('span', class_='price-item--regular')
            if not price_tag: # Check for sale price if regular wasn't found
                price_tag = price_container.find('span', class_='price-item--sale')
            scraped_data['price'] = price_tag.get_text(strip=True) if price_tag else "Price not found"
        else:
             scraped_data['price'] = "Price container not found"

        # --- 3. Extract Description ---
        # The main description is often in a div with class 'product__description' or 'rte'
        description_tag = soup.find('div', class_='product__description')
        if description_tag:
             # Using separator='\n' preserves line breaks better than just get_text()
             scraped_data['description'] = description_tag.get_text(separator='\n', strip=True)
        else:
            # Fallback if the primary class isn't found
            desc_fallback = soup.find('div', class_='rte') # 'rte' is common for rich text editor content
            scraped_data['description'] = desc_fallback.get_text(separator='\n', strip=True) if desc_fallback else "Description not found"


        # --- 4. Find Image URLs ---
        image_urls = []
        # Target images within the main product media area for relevance
        # Often in a list or gallery container like 'product__media-list'
        media_gallery = soup.find('div', class_='product__media-list')
        if media_gallery:
            img_tags = media_gallery.find_all('img')
        else:
             # Broader search if specific container not found (might get unrelated images)
             print("Warning: Specific media gallery container not found, searching all img tags.")
             img_tags = soup.find_all('img')

        print(f"Found {len(img_tags)} potential image tags.")

        for img in img_tags:
            # Prioritize 'src', fallback to 'data-src' (used for lazy loading)
            src = img.get('src') or img.get('data-src')
            if src:
                # Clean '//' prefix sometimes found in src attributes
                if src.startswith('//'):
                    src = 'https:' + src

                # Convert relative URLs (like /path/image.jpg) to absolute URLs
                absolute_url = urljoin(url, src)

                # Basic filtering: ensure it's HTTP/HTTPS and likely an image format
                parsed_img_url = urlparse(absolute_url)
                if (parsed_img_url.scheme in ['http', 'https'] and
                    any(absolute_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']) and
                    absolute_url not in image_urls): # Avoid duplicates
                     image_urls.append(absolute_url)
                     # print(f"  Found potential image: {absolute_url}")


        print(f"Found {len(image_urls)} unique, valid image URLs.")

        # --- 5. Download Images ---
        if not image_urls:
            print("No suitable image URLs found to download.")
            scraped_data['downloaded_images'] = []
            return scraped_data

        # Create directory to save images
        image_dir = "../zTemp/rockbros_product_images"
        os.makedirs(image_dir, exist_ok=True)
        print(f"Saving images to directory: '{image_dir}'")

        count = 0
        for img_url in image_urls:
            if count >= num_images_to_download:
                break
            try:
                img_response = requests.get(img_url, headers=headers, stream=True, timeout=10)
                img_response.raise_for_status()

                # Extract filename from URL path
                parsed_url = urlparse(img_url)
                img_filename = os.path.basename(parsed_url.path)

                # Basic filename cleaning (remove invalid chars)
                img_filename = re.sub(r'[\\/*?:"<>|]', "_", img_filename)
                # Add default name if cleaning results in empty string or no extension
                if not img_filename or '.' not in img_filename:
                     img_filename = f"image_{count+1}.jpg" # Default name with jpg extension

                filepath = os.path.join(image_dir, img_filename)

                # Save the image
                with open(filepath, 'wb') as f:
                    for chunk in img_response.iter_content(8192): # Download in chunks
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
        # Catch other potential errors during parsing or file handling
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc() # Print detailed traceback for debugging
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
        o["price"]=17
    except:
        o["price"]=None



if __name__ == "__main__":
    target_url = "https://rockbrosbike.us/products/rockbros-cycling-glassesmtb-biking-sports-sunglasses-with-anti-blue-lenses-men?ref=glgipqco"
    get_rock_product(target_url)