import feedparser
import settings
from mastodon import Mastodon

url = settings.url 
feed = feedparser.parse(url)
most_recent = feed.entries[0]
current_post = most_recent["title"]
link = most_recent["link"]

with open("current_title", "r") as f1:
    last_post = f1.read()

if last_post == current_post:
    print("doing nothing")
    quit()
else:
    with open("current_title", "w") as f2:
        f2.write(current_post)

    mastodon = Mastodon(
        access_token = settings.access_token,
        api_base_url = settings.api_base_url
    )

    toot = f"New post on the Library Technology at Kingsborough blog: {current_post}\n\n{link}"
    print(toot)
    mastodon.toot(toot)

