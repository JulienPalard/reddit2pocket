#!/usr/bin/env python

import feedparser
import re
import sys
import smtplib
from email.mime.text import MIMEText


def send_to_pocket(email_from, link):
    msg = MIMEText(link)
    msg['Subject'] = ''
    msg['From'] = email_from
    msg['To'] = 'add@getpocket.com'

    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.quit()


for subreddit in sys.argv[2:]:
    feed = feedparser.parse('http://www.reddit.com/r/%s/top/.rss?sort=top&t=week' % subreddit)
    for i in range(5):
        entry = feed['entries'][i]
        source = re.findall(r'href=(["\'])(.*?)\1', entry['summary'])[1][1]
        send_to_pocket(sys.argv[1], source)
