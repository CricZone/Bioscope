import os
import requests

def get_bioscope_m3u8(channel_id):
    # ২০২৬ সালের লেটেস্ট সিকিউরিটি এবং অ্যাপ টোকেন বাইপাস করার হেডার
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Referer": "https://www.bioscopelive.com/",
        "Origin": "https://www.bioscopelive.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        # আপডেটেড অফিশিয়াল প্লেয়ার এপিআই রুট
        api_url = f"https://api.bioscopelive.com/api/v1/channel/get-stream-url/{channel_id}"
        
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # নতুন রেসপন্স স্ট্রাকচার থেকে .m3u8 লিংকটি টেনে বের করা
            if 'data' in data:
                if isinstance(data['data'], dict) and 'url' in data['data']:
                    return data['data']['url']
                elif isinstance(data['data'], str) and '.m3u8' in data['data']:
                    return data['data']
    except Exception as e:
        print(f"Error fetching Bioscope link for {channel_id}: {e}")
    return None

try:
    with open("bioscope_channels.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = []

m3u_content = "#EXTM3U\n"
current_info = ""

for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith("#EXTINF"):
        current_info = line
    else:
        channel_name = current_info.split(',')[-1] if current_info else line
        print(f"Fetching Live Stream Link for: {channel_name}")
        m3u8_url = get_bioscope_m3u8(line)
        if m3u8_url and current_info:
            m3u_content += f"{current_info}\n{m3u8_url}\n"
            current_info = ""

with open("live_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)
print("Bioscope M3U Playlist Updated Successfully with New API!")
