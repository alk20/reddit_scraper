SET UP THE SCRIPT

In `config.ini` you can set the max amount of posts to be scraped.
You can set it to 0 to scan without limit. This will be slow.
You can also set if you want to allow the scraping of NSFW posts or not.

In `banned_subs.txt` you can enter a list of the subreddits you can to 
blacklist from scraping.


RUN THE SCRIPT: To run the script, double click the file called `run.bat`.
A black window will pop up asking for the name of the subreddit.
3 things can happen:
    1. If it finds any posts, it will generate a csv file with the name of the subreddit.
    2. If it can't find any post it will inform it and finish.
    3. If the subreddit is in the list of banned subreddits it will inform it and finish.


