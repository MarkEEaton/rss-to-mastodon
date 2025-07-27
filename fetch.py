import argparse
import feedparser
import os
from mastodon import Mastodon

url = os.environ["KINGSURL"]
feed = feedparser.parse(url)
most_recent = feed.entries[0]
current_post = most_recent["title"]
link = most_recent["link"]

parser = argparse.ArgumentParser()
parser.add_argument("last_post")
last_post = parser.parse_args().last_post

if last_post == current_post:
    print("doing nothing")
    quit()
else:
    with open("current_title", "w") as f2:
        f2.write(current_post)

    base_url = "https://mastodon.ocert.at"
    mastodon = Mastodon(access_token=os.environ['KINGSBOTSECRET'], api_base_url=base_url)

    # Gather every new entry until we reach the one already posted
    new_entries = []
    for entry in feed.entries:        # entries are newest-first
        if entry["title"] == last_post:
            break
        new_entries.append(entry)

    # Post oldest → newest so the timeline looks natural
    for entry in reversed(new_entries):
        toot = (
            "New post on the Library Technology at Kingsborough blog:\n\n"
            f"{entry['title']}\n{entry['link']}"
        )
        print(toot)
        mastodon.toot(toot)

    # Save updated history (the newest item we just processed)
    with open("last_post.txt", "w") as f:
        f.write(current_post)
