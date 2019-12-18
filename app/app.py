#!/usr/bin/python3
import sys
import requests
import smtplib
import configparser
import argparse
from tests import Test

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, dest='config_file')
args = parser.parse_args()
if not args.config_file:
    print("No config file specified")
    sys.exit(1)
config = configparser.ConfigParser()
config.read(args.config_file)

# run tests
results = []
for _, test in Test.Tests.items():
    results.append(test(config))
should_notify = False
test_messages = ''
for result in results:
    if result.notify:
        test_messages += result.testdesc + ": " + result.message
        should_notify = True
    
if should_notify:
    from_email = config["Mail"]["email"]
    from_password = config["Mail"]["password"]
    to_email = config["Mail"]["to_email"]
    subject = config["Mail"]["subject"]

    message = 'Subject: {}\n\n{}'.format(subject, test_messages)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, message)
    server.quit()

