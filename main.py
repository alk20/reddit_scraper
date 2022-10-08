import csv
import configparser
from pathlib import Path

from psaw import PushshiftAPI

master_path = Path(__file__).parent


class Bot:
    def __init__(self):
        pass

    def main(self):
        banned_subs = self.get_banned_subs()
        wanted_subreddit = input("Enter subreddit: ")

        if wanted_subreddit.lower() in banned_subs:
            print("That subreddit is banned from scraping.")
            return

        print(f"Scraping {wanted_subreddit}...")

        posts = self.get_posts(subreddit=wanted_subreddit)
        if not posts:
            print("No post found. Subreddit might not exists.")
            return

        self.write_to_csv(subreddit=wanted_subreddit, posts=posts)

        print("\nFinished!")

    def get_banned_subs(self):
        with open('banned_subs.txt', 'r', encoding='UTF-8') as file:
            return [line.lower() for line in file.read().splitlines() if line]

    @staticmethod
    def get_posts(subreddit):
        # Read config file.
        config = configparser.ConfigParser()
        config.read(master_path / "config.ini")
        config = config["DEFAULT"]

        # Set the limit for the amount of posts we'll ask pushshift.
        limit = config["LIMIT"]
        limit = None if limit == "0" else int(limit)

        # Set if we'll get NSFW posts or not.
        nsfw_allowed = None if config["NSFW"].upper() == "YES" else False

        # Search the submissions using Pushshift API.
        gen = PushshiftAPI(shards_down_behavior=None).search_submissions(limit=limit,
                                                                         subreddit=subreddit,
                                                                         filter=["author", "full_link", "title"],
                                                                         over_18=nsfw_allowed)

        # Since psaw returns a generator,
        #  we need to convert it into a list in order to actually retrieve all the results.
        return list(gen)

    @staticmethod
    def write_to_csv(subreddit, posts):
        with open(master_path / f"{subreddit}.csv", "w", newline="", encoding="UTF-8") as file:
            fieldnames = ["title", "author", "link"]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for post in posts:
                writer.writerow({
                    "title": post.title,
                    "author": post.author,
                    "link": post.full_link
                })


if __name__ == '__main__':
    print("Starting script...")

    bot = Bot()
    bot.main()
