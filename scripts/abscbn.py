#!/usr/bin/env python3

import requests
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Determine if the script is running on a Windows system
windows = "win" in sys.platform

# Create a requests session
session = requests.Session()

def fetch_url_content(url):
    """Fetch content from a URL with a timeout and return the response text."""
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to fetch URL {url}: {e}")
        return None

def curl_fallback(url):
    """Fallback to curl for fetching the URL content if requests fail."""
    try:
        os.system(f"curl '{url}' -o temp.txt")
        with open("temp.txt", 'r') as file:
            return "".join(file.readlines())
    except Exception as e:
        logging.error(f"Failed to fetch URL via curl {url}: {e}")
        return None

def find_m3u8_link(response):
    """Find and return the first occurrence of an .m3u8 link in the response."""
    if not response or ".m3u8" not in response:
        return None

    end = response.find(".m3u8") + 5
    tuner = 100

    while True:
        candidate_link = response[end - tuner:end]
        if "https://" in candidate_link:
            start = candidate_link.find("https://")
            full_link = candidate_link[start:end]
            return full_link if ".m3u8" in full_link else None
        tuner += 5

def grab(url):
    """Process the given URL to fetch and print the relevant .m3u8 stream URL."""
    response = fetch_url_content(url) or curl_fallback(url)
    m3u8_link = find_m3u8_link(response)

    if m3u8_link:
        logging.info(f"Found .m3u8 link: {m3u8_link}")
        try:
            streams = session.get(m3u8_link).text.split("#EXT")
            hd_stream = streams[-1].strip()
            stream_start = hd_stream.find("http")
            print(hd_stream[stream_start:].strip())
        except requests.RequestException as e:
            logging.error(f"Failed to fetch stream from {m3u8_link}: {e}")

def main(file_path):
    """Main function to process the channels list and fetch streams."""
    print("#EXTM3U")
    print("#EXT-X-STREAM-INF:BANDWIDTH=10000000")

    try:
        with open(file_path) as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("~~"):
                    continue
                if not line.startswith("https:"):
                    channel_info = line.split("|")
                    ch_name = channel_info[0].strip()
                    grp_title = channel_info[1].strip().title()
                    tvg_logo = channel_info[2].strip()
                    tvg_id = channel_info[3].strip()
                else:
                    grab(line)
    except FileNotFoundError as e:
        logging.error(f"Channel list file not found: {e}")
    except Exception as e:
        logging.error(f"Error reading channel list: {e}")

    # Cleanup temporary files if they exist
    for temp_file in ["temp.txt", "watch*"]:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            logging.info(f"Removed temporary file: {temp_file}")

if __name__ == "__main__":
    main("../information/abscbn.txt")
