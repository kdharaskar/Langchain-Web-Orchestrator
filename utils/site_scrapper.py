import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.parse
import config

# --- Configuration ---
BASE_URL = config.BASE_URL
OUTPUT_FILE = config.OUTPUT_FILE
HEADERS = config.HEADERS
REQUEST_DELAY_SECONDS = config.REQUEST_DELAY_SECONDS
PAGE_REQUEST_DELAY_SECONDS = config.PAGE_REQUEST_DELAY_SECONDS

# --- Main Scraping Logic ---
def scrape_isb_faculty():
    """
    Scrapes the ISB faculty directory, handling pagination.
    NOTE: HTML selectors (class names, tags) for faculty blocks, data points,
    and pagination links MUST be updated by inspecting the website's current HTML.
    """

    faculty_list = []
    serial_number = 1
    generic_page_url = "https://www.isb.edu/api/facultys?pageID=758712b3-23f9-4485-a875-025f0cd026c2&pageNumber={page_count}&itemsPerPage=12&filter={{}}&keywords="

    for page_num in range(1, 7):

        current_page_url = generic_page_url.format(page_count=page_num)
        print(f"\n--- Processing Page {page_num}: {current_page_url} ---")

        try:
            # Add a delay before fetching the directory page list
            time.sleep(PAGE_REQUEST_DELAY_SECONDS)
            response = requests.get(current_page_url, headers=HEADERS, timeout=45)  # Increased timeout
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        except requests.exceptions.RequestException as e:
            print(f"  Error fetching page {current_page_url}: {e}")
            print("  Stopping scraping.")
            break  # Stop if a page fails to load

        try:

            items = json.loads(response.content)['items']

            for item in items:

                properties = item['properties']
                name = properties['fullName']
                academic_area = properties['facultyType'] + ', ' + properties['area']
                profile_relative_url = properties['cTA']['items'][0]['content']['properties']['link'][0]['url']
                profile_url = urllib.parse.urljoin(BASE_URL, profile_relative_url)

                if profile_url:
                    print(f"Fetching profile details for: {name}") # Uncomment for debugging
                    # Add delay before fetching individual profile
                    time.sleep(REQUEST_DELAY_SECONDS)
                    try:
                        profile_response = requests.get(profile_url, headers=HEADERS, timeout=30)
                        profile_response.raise_for_status()
                        profile_soup = BeautifulSoup(profile_response.content, 'html.parser')

                        # !!! IMPORTANT: Update selector for Email !!!
                        # Example: email_tag = profile_soup.select_one('a.email-address[href^="mailto:"]')
                        email_tag = profile_soup.find('a',
                                                      href=lambda href: href and href.startswith('mailto:'))  # MODIFY THIS
                        email = email_tag['href'].replace('mailto:', '').strip() if email_tag else "N/A"

                        # !!! IMPORTANT: Update selector for Biography !!!
                        bio_section = profile_soup.find(id='biography')
                        outer_div_sibling_bio = bio_section.find_next_sibling('div')
                        biography_div = outer_div_sibling_bio.find('div', class_='APIRichtextContentBlock_description__X0x3G')
                        biography = biography_div.get_text(separator='\n', strip=True) if bio_section else "N/A"

                        # !!! IMPORTANT: Update selector for Research Speciality !!!
                        research_section = profile_soup.find(id='research-specialty')
                        outer_div_sibling_research = research_section.find_next_sibling('div')
                        research_div = outer_div_sibling_research.find('div', class_='APIRichtextContentBlock_description__X0x3G')
                        research_speciality = research_div.get_text(separator='\n', strip=True) if bio_section else "N/A"

                    except requests.exceptions.RequestException as e_profile:
                        print(f"      Error fetching profile page {profile_url}: {e_profile}")
                        email, research_speciality, biography = "Error fetching", "Error fetching", "Error fetching"
                    except Exception as e_parse:
                        print(f"      Error parsing profile page {profile_url}: {e_parse}")
                        email, research_speciality, biography = "Error parsing", "Error parsing", "Error parsing"

                    # --- Append data to list ---
                    faculty_list.append({
                        "Sr.No.": serial_number,
                        "Name": name,
                        "Email": email,
                        "Academic-Area": academic_area,
                        "Research-Speciality": research_speciality,
                        "Biography": biography,
                        "Profile-URL": profile_url  # Optional: Keep for debugging
                    })
                    print(f"Processed Sr.No. {serial_number}: {name}")
                    serial_number += 1

        except Exception as e_block:
            print(f"Error getting page {page_num}: {e_block}")
            continue  # Skip to next page

    # --- Create DataFrame and save to CSV (outside the while loop) ---
    if faculty_list:
        print(f"\n--- Scraping finished. Total entries processed: {len(faculty_list)} ---")
        df = pd.DataFrame(faculty_list)
        # Ensure columns are in the desired order
        df = df[["Sr.No.", "Name", "Email", "Academic-Area", "Research-Speciality", "Biography", "Profile-URL"]]
        try:
            # Use utf-8-sig for better compatibility with Excel
            df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
            print(f"\nData saved to {OUTPUT_FILE}")
            print("Please review the CSV file for completeness and accuracy, especially for entries marked with 'Error'.")
        except IOError as e_io:
            print(f"\nError saving data to CSV file: {e_io}")
        return df
    else:
        print("\nNo faculty data was successfully scraped from any page.")
        return None

# --- Run the scraper ---
if __name__ == "__main__":
    scraped_data = scrape_isb_faculty()
    if scraped_data is not None and not scraped_data.empty:
        print("\n--- First 5 Rows of Scraped Data ---")
        print(scraped_data.head())
        print("\n--- Last 5 Rows of Scraped Data ---")
        print(scraped_data.tail())
    elif scraped_data is not None and scraped_data.empty:
        print("\nScraping function completed, but no data was collected. Check selectors and website structure/access.")