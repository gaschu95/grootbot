#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

#run with python3

import praw
import logging
from time import sleep

def get_logger():
    log = logging.getLogger('_name_')
    logFormat = '[%(asctime)s] [%(levelname)s] - %(message)s'

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter(logFormat))
    log.addHandler(streamHandler)

    fileHandler = logging.FileHandler('grootbot.log')
    fileHandler.setFormatter(logging.Formatter(logFormat))
    log.addHandler(fileHandler)

    log.setLevel(level=logging.INFO)
    return log

def handle_comment(comment):
    global reddit
    #don't comment on own comments
    if comment.author == reddit.user.me():
        # log.info('own comment found: %s', comment.id)
        log_comment('own comment found', comment)
        return

    if ' groot' in comment.body.lower():
        log.info('" groot " found: %s', comment.id)
        comment.reply('I am Groot')
    elif ' bad bot' in comment.body.lower():
        log.info('sometimes we fail')
        comment.reply('^I^am^~~groot~~sorry')
    else:
        # print(comment.id)
        pass

log = get_logger()
reddit = praw.Reddit('grootbot')
attempts = 0
while True:
    try:
        for c in reddit.subreddit('all').stream.comments():
            handle_comment(c)
            attempts = 0
    except Exception as e:
        log.critical('well shit: ' + str(e))
        sleep(attempts)
        continue
