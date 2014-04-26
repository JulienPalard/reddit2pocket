#!/usr/bin/env python

import feedparser
import re
import sys
import smtplib
from email.mime.text import MIMEText
import cPickle
import os.path
from contextlib import contextmanager
from datetime import datetime


@contextmanager
def pickeled(pickle_file):
    if os.path.isfile(pickle_file):
        with open(pickle_file, 'rb') as f:
            env = cPickle.load(f)
    else:
        env = {}
    try:
        yield env
    finally:
        pickle_file = os.path.expanduser("~/.reddit2pocket.pickle")
        with open(pickle_file, 'wb') as f:
            cPickle.dump(env, f, -1)


def send_to_pocket(email_from, link):
    msg = MIMEText(link)
    msg['Subject'] = ''
    msg['From'] = email_from
    msg['To'] = 'add@getpocket.com'

    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.quit()


with pickeled(os.path.expanduser("~/.reddit2pocket.pickle")) as env:
    if 'seen' not in env:
        env['seen'] = {}
    for subreddit in sys.argv[2:]:
        feed = feedparser.parse('http://www.reddit.com/r/%s/top/.rss?sort=top&t=day' % subreddit)
        for i in range(min(3, len(feed['entries']))):
            entry = feed['entries'][i]
            source = re.findall(r'submitted by <a href.*?href=(["\'])(.*?)\1', entry['summary'])[0][1]
            if source not in env['seen']:
                send_to_pocket(sys.argv[1], source)
                env['seen'][source] = datetime.now()
