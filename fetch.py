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
    mastodon = Mastodon(access_token=os.environ([KINGSBOTSECRET]), api_base_url=base_url)

    # Save updated history
    with open("last_post.txt", "w") as f:
        f.write(current_post)

    toot = f"New post on the Library Technology at Kingsborough blog:\n\n{current_post}\n{link}"
    print(toot)
    mastodon.toot(toot)
