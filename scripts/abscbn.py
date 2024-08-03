import requests
import os
import sys
import subprocess

def is_windows():
    return "win" in sys.platform

def grab_url_content(url, windows):
    s = requests.Session()
    response = s.get(url, timeout=15).text
    
    if ".m3u8" not in response:
        response = requests.get(url).text
        if ".m3u8" not in response:
            if windows:
                return None
            os.system(f"curl '{url}' > temp.txt")
            with open("temp.txt") as f:
                response = f.read()
            if ".m3u8" not in response:
                return None
    
    end = response.find(".m3u8") + 5
    tuner = 100
    while True:
        if "https://" in response[end - tuner: end]:
            link = response[end - tuner: end]
            start = link.find("https://")
            end = link.find(".m3u8") + 5
            break
        tuner += 5
    
    streams = s.get(link[start:end]).text.split("#EXT")
    hd = streams[-1].strip()
    st = hd.find("http")
    return hd[st:].strip()

def main():
    windows = is_windows()

    print("#EXTM3U")
    print("#EXT-X-STREAM-INF:BANDWIDTH=10000000")
    
    with open("../information/abscbn.txt") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("~~"):
                continue
            
            if not line.startswith("https:"):
                fields = line.split("|")
                ch_name = fields[0].strip()
                grp_title = fields[1].strip().title()
                tvg_logo = fields[2].strip()
                tvg_id = fields[3].strip()
            else:
                content = grab_url_content(line, windows)
                if content:
                    print(content)

def get_live_stream_info(youtube_url):
    try:
        # Use yt-dlp to fetch the stream URL
        result = subprocess.run(
            ['yt-dlp', '-g', youtube_url],
            capture_output=True, text=True, check=True
        )
        stream_url = result.stdout.strip()
        return stream_url
    except subprocess.CalledProcessError as e:
        print(f"Error fetching stream URL: {e.stderr}")
        return None

def generate_m3u8(stream_url, output_path):
    m3u8_content = f"#EXTM3U\n#EXTINF:-1,{'Live'}\n{stream_url}"

    try:
        with open(output_path, 'w') as m3u8_file:
            m3u8_file.write(m3u8_content)
        print(f"M3U8 file created at {output_path}")
    except IOError as e:
        print(f"Error writing M3U8 file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py https://www.youtube.com/@abscbnentertainment/live abscbn.m3u8")
        sys.exit(1)

    youtube_url = sys.argv[1]
    output_m3u8 = sys.argv[2]

    stream_url = get_live_stream_info(youtube_url)
    if stream_url:
        generate_m3u8(stream_url, output_m3u8)
    else:
        main()
