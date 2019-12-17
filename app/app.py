#!/usr/bin/python3
import sys
import requests
import smtplib
import configparser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, dest='config_file')
args = parser.parse_args()
if not args.config_file:
    print("No config file specified")
    sys.exit(1)


config = configparser.ConfigParser()
config.read(args.config_file)

r = requests.get("http://ifconfig.me")
current_ip = r.text

cache_file = config["DEFAULT"]["cache_file"]
to_email = config["DEFAULT"]["to_email"]

with open(cache_file, 'r') as f:
    previous_ip = f.read().strip()
if not previous_ip == current_ip:
    
    from_email = config["AppCredentials"]["email"]
    from_password = config["AppCredentials"]["password"]
    to_email = config["DEFAULT"]["to_email"]
    subject = config["DEFAULT"]["subject"]

    msg = "New IP {} detected.\nOld IP was {}".format(current_ip, previous_ip)
    message = 'Subject: {}\n\n{}'.format(subject, msg)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, message)
    server.quit()

    with open(cache_file, 'w') as f:
        f.write(current_ip)
