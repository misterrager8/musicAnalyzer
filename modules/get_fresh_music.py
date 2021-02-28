import praw

reddit = praw.Reddit("bot1")


def get_fresh_music():
    for submission in reddit.subreddit("hiphopheads").new(limit=250):
        if "FRESH" in submission.title:
            print(submission.title)
