import requests
import os, sys, time
import os.path
import time as t
import threading
import urllib.request
import urllib.parse
import pickle
import re
import json
import random
from uuid import uuid4
from subprocess import call

CRED = '\033[91m'
CEND = '\033[0m'
CGREEN = '\33[92m'
BLACK   = '\033[30m'
RED     = '\033[31m'
GREEN   = '\033[32m'
YELLOW  = '\033[33m'
BLUE    = '\033[34m'
MAGENTA = '\033[35m'
CYAN    = '\033[36m'
WHITE   = '\033[37m'
RESET   = '\033[39m'

username_list = "twitter_usernames.txt" #List of usernames to claim for turbo/autoclaimer
account_headers = "headers.txt" #Your account headers

os.system("cls") #clear panel
# Checking if program is up-to-date
version = "1.0"
check = requests.get(url = "https://raw.githubusercontent.com/itsunderscores/Twitter-Autoclaimer-Swapper/main/version.txt")
if(version in check.text):
    pass
else:
    print("This version is currently out of date and is recommended you download the updated one.")
    print("https://github.com/itsunderscores/Twitter-Autoclaimer-Swapper")
    print(check)
    exit()

def header():
    print(CRED+''' _              _           
| |_ _   _ _ __| |__   ___  
| __| | | | '__| '_ \ / _ \ 
| |_| |_| | |  | |_) | (_) |
 \__|\__,_|_|  |_.__/ \___/ 
    ''')
    print(CRED+"[+] Twitter Turbo v" + version)
    print(CRED+"[!] Autoclaimer will cause you to be rate limited if you use a lot of threads.")
    print(CRED+"[-] Developed by underscores#0001")
    print(WHITE+"-------------------------------------------------------"+YELLOW)


def unescape(in_str):
    """Unicode-unescape string with only some characters escaped."""
    in_str = in_str.encode('unicode-escape')   # bytes with all chars escaped (the original escapes have the backslash escaped)
    in_str = in_str.replace(b'\\\\u', b'\\u')  # unescape the \
    in_str = in_str.decode('unicode-escape')   # unescape unicode
    return in_str

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Check if string is blank
def is_not_blank(s):
    return bool(s and not s.isspace())

# Log to textfile
def logtofile(file, text):
	f = open(file, "w")
	f.write(str(text)+"\n") 
	f.close()
	return text

# Grab random proxy from file
def getproxy(file):
    proxy = random.choice(list(open(file)))
    proxy = proxy.strip()
    proxy = proxy.replace("\n", "")
    return proxy

# Grab random usernamer from file
def getusernamefromlist():
    username = random.choice(list(open(username_list)))
    username = username.strip()
    username = username.replace("\n", "")
    return username
    

# Grab headers and compile to format
def headers(file):
    with open(file, 'r') as f:
        for line in f:
            if not find_between(line, "x-csrf-token: ", "\n"):
                pass
            else:
                csrf = find_between(line, "x-csrf-token: ", "\n")

            if not find_between(line, "Cookie: ", "\n"):
                pass
            else:
                cookie = find_between(line, "Cookie: ", "\n")

            if not find_between(line, "authorization: Bearer ", "\n"):
                pass
            else:
                auth = find_between(line, "authorization: Bearer ", "\n")

    getheaders={ 
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0", 
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-csrf-token": ""+csrf+"",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
        "x-twitter-active-user": "yes",
        "authorization": "Bearer " + auth + "",
        "Origin": "https://twitter.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Referer": "https://twitter.com/settings/screen_name",
        "Connection": "keep-alive",
        "Cookie": "" + cookie + "",
        "TE": "trailers"
    }

    return getheaders

claimed = []

# Claim username
def claim(username, file):

    url = "https://twitter.com/i/api/1.1/account/settings.json"
    getheaders = headers(file)
    data1 = "screen_name=" + username
    attempts = 0

    while True:
        if attempts >= 5:
            return
        try:
            response = requests.post(url=url, data=data1, headers=getheaders, timeout=5)
            if not response.text:
                #randomnumber = random.randint(10,120)
                #print(MAGENTA + "[!] Could not grab information from website, rate limited, waiting %s seconds: %s" % (str(randomnumber), username))
                #time.sleep(randomnumber)
                time.sleep(1)
                attempts += 1
            else:
                try:
                    data = json.loads(str(response.text))
                    if data["screen_name"] == username:
                        claimed.append("1")
                        return "Y"
                    else:
                        return "N"
                except:
                    return "S"

        except requests.ConnectionError:
            print(RED + "[>] Connection timed out. Most likley rate limited, sleeping for 2 minutes.")
            time.sleep(120)

# Check if username is valid
def check(username, file):

    url = "https://twitter.com/i/api/i/users/username_available.json?full_name=" + username + "&suggest=true&username=" + username
    getheaders = headers(file)
    attempts = 0

    while True:
        try:
            if attempts >= 5:
                return
            response = requests.get(url=url, headers=getheaders, timeout=5)
            if not response.text:
                randomnumber = random.randint(10,120)
                print(MAGENTA + "[!] Could not grab information from website, rate limited, waiting %s seconds: %s" % (str(randomnumber), username))
                time.sleep(randomnumber)
                #time.sleep(1)
                attempts += 1
            else:
                try:
                    data = json.loads(str(response.text))
                    if data["reason"] == "taken":
                        return "N"
                    elif data["reason"] == "available":
                        return "Y"
                except:
                    return "S"
        except requests.ConnectionError:
            print(RED + "[>] Connection timed out. Most likley rate limited, sleeping for 2 minutes.")
            time.sleep(120)

#print(check("brandondies1", "twitter.txt"))
#exit()

# Grabs current username from header
def verifyaccount(file):
    url = "https://twitter.com/i/api/1.1/account/settings.json?include_mention_filter=true&include_nsfw_user_flag=true&include_nsfw_admin_flag=true&include_ranked_timeline=true&include_alt_text_compose=true&ext=ssoConnections&include_country_code=true&include_ext_dm_nsfw_media_filter=true&include_ext_sharing_audiospaces_listening_data_with_followers=true"
    getheaders = headers(file)
    try:
        response = requests.get(url=url, headers=getheaders, timeout=5)
        try:
            data = json.loads(str(response.text))
            return data["screen_name"]
        except:
            print(RED+"[>] Could not grab your account information. This could be because of rate limiting or bad headers.")
    except requests.ConnectionError:
        print(RED + "[>] Could not make connection to Twitter. This could be because of rate limiting or bad headers.")


def process():
    while True:
        username = getusernamefromlist()
        username = username.strip()
        username = username.replace("\n", "")
        checkusername = check(username, account_headers)
        if checkusername == "Y":
            print(GREEN+"[>] %s is available" % username)
            claimusername = claim(username, account_headers)
            if claimusername == "Y":
                print(GREEN + "[>] Changed to %s successfully" % username)
            elif claimusername == "S":
                print(YELLOW+"[>] Could not change username to %s. Most likely suspended account." % username)
            elif claimusername == "N":
                print(YELLOW+"[>] Could not change to %s" % username)
        elif checkusername == "S":
            print(YELLOW+"[>] Could not change username to %s. Most likely suspended account." % username)
        elif checkusername == "N":
            print(YELLOW +"[>] %s is not available" % username)

claimed = []

def swap(username, file, type):
    attempts = 1

    try:
        if claimed[0] == "1":
            print("Closed because we successfully claimed.")
            exit()
        else:
            pass
    except:
        pass


    if type == "1":
        print(YELLOW+"[>] Releasing " + username)
        time.sleep(2)
    elif type == "2":
        print(YELLOW+"[>] Swapping " + username)

    url = "https://twitter.com/i/api/1.1/account/settings.json"
    getheaders = headers(file)
    data1 = "screen_name=" + username

    while True:
        if attempts >= 5:
            print(CRED+"[!] Cancelled due to too many requests failing.")
            return
            exit()
        try:
            response = requests.post(url=url, data=data1, headers=getheaders, timeout=5)
            if not response.text:
                time.sleep(1)
                attempts += 1
            else:
                try:
                    data = json.loads(str(response.text))
                    if data["screen_name"] == username:
                        if type == "1":
                            print(GREEN+"[>] Successfully released %s" % username)
                            break
                            return
                        elif type == "2":
                            print(GREEN + "[>] Successfully claimed %s" % username)
                            claimed.append("1")
                            break
                            return
                    else:
                        if type == "1":
                            print("[>] Could not release %s" % username)
                            break
                            return
                        elif type == "2":
                            print("[>] Could not claim %s" % username)
                            break
                            return
                except:
                    if type == "1":
                        print("[>] Unexpected Error Releasing %s" % username)
                        break
                        return
                    elif type == "2":
                        print("[>] Unexpected Error Claiming %s" % username)
                        break
                        return

        except requests.ConnectionError:
            print(RED + "[>] Connection timed out. Most likley rate limited, sleeping for 2 minutes.")
            time.sleep(120)


def swapper():
    while True:
        account1 = input(YELLOW+"\n[>] Enter file name for headers of first account (Releasing Username): ")
        response1 = verifyaccount(account1)
        if not response1:
            print("")
        else:
            print(GREEN+"[>] Signed in, %s is going to be released." % response1)
            break
    
    while True:
        randomusername = input(YELLOW + "[>] Enter username to change this account to: ")
        checkifavailable = check(randomusername, account1)
        if checkifavailable == "Y":
            break
        else:
            print("The username you want to change %s to is unavailable. Please chose another." % account1)

    while True:
        account2 = input(YELLOW+"\n[>] Enter file name for headers of first account (Releasing Username): ")
        response2 = verifyaccount(account2)
        if not response2:
            print("")
        else:
            print(GREEN+"[>] Signed in, %s is going to claim %s." % (response2, response1))
            break

    question = input(YELLOW+"\n[>] Confirm this swap? (Y/N): ")
    if question == "y" or question == "Y":

        for x in range(int(1)):
            th = threading.Thread(target=swap, args=(randomusername, account1, "1"))
            th.start()
        th.join()

        for x in range(int(3)):
            th = threading.Thread(target=swap, args=(response1, account2, "2"))
            th.start()
        th.join()

    else:
        print(RED+ "[>] This swap has been cancelled." + WHITE)


def main():
    header()
    mode = input(YELLOW + "[>] Please choose one of the following\n[>] 1 = Turbo\n[>] 2 = Swapper\n[>] Selection: ")

    if mode == "1":
        while True:
            threads = input(YELLOW + "[>] Threads to open: ")
            if int(threads) >= 1 and  int(threads) <= 1000:
                for x in range(int(threads)):
                    th = threading.Thread(target=process)
                    th.start()
                th.join()
                break
            else:
                print(RED+"[!] Maximum threads is 500.")
    elif mode == "2":
        swapper()
    else:
        print(RED+"[!] Selection was not recognized, try again.")

main()
