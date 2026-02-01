import requests
import json
import time

# --- CONFIGURATION ---
start_offset = 0  # Starting where your last file left off
limit = 100          # Keep this at 100 (Server Limit)
# ---------------------

base_url = "https://www.moltbook.com/api/v1/posts"
headers = {"User-Agent": "MoltbookScraper/1.0"}
all_posts = []
current_offset = start_offset

print(f"Starting scrape from offset {current_offset}...")

while True:
    # Build the URL for the current page
    url = f"{base_url}?limit={limit}&sort=new&offset={current_offset}"
    
    try:
        print(f"Fetching offset {current_offset}...", end=" ")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
            
        data = response.json()
        posts = data.get('posts', [])
        
        if not posts:
            print("No posts found. Stopping.")
            break
            
        # Add posts to our list
        all_posts.extend(posts)
        print(f"Got {len(posts)} posts. (Total collected: {len(all_posts)})")
        
        # Check if there are more pages
        if not data.get('has_more', False):
            print("End of feed reached.")
            break
            
        # Get the next offset provided by the API
        current_offset = data.get('next_offset')
        
        # Sleep to be polite to the server
        time.sleep(0.5)

    except Exception as e:
        print(f"\nCrash: {e}")
        break

# Save everything to a file
filename = "moltbook_full_dataset.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_posts, f, indent=2, ensure_ascii=False)

print(f"\nSUCCESS: Saved {len(all_posts)} posts to {filename}")
