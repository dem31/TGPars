#!/bin/env python3
from email.mime.image import MIMEImage
from tkinter import Image

from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import time
from email.message import EmailMessage

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
SLEEP_TIME = 60


class main():

    def banner():

        print(f"""
    {re}╔╦╗{cy}┌─┐┌─┐┌─┐┌─┐┬─┐{re}╔═╗
    {re} ║ {cy}├─┐├┤ ├─┘├─┤├┬┘{re}╚═╗
    {re} ╩ {cy}└─┘└─┘┴  ┴ ┴┴└─{re}╚═╝
    by https://github.com/elizhabs
            """)

    def send_sms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            os.system('clear')
            main.banner()
            print(re + "[!] run python3 setup.py first !!\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)

        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))

        os.system('clear')
        main.banner()
        input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        # print(gr + "[1] send sms by user ID\n[2] send sms by username ")
        # mode = int(input(gr + "Input : " + re))  # 5211085083

        #message = input(gr + "[+] Enter Your Message : " + re)
        message = EmailMessage()
        message = open('tst', 'r', encoding='UTF-8').read()
        #message.set_content(open('tst', 'r', encoding='UTF-8').read())
        #attachment = 'dos.jpg'
        #image_data = open(attachment, "rb")
        #image_mime = MIMEImage(image_data.read())
        #image_data.close()
        #message.add_attachment(image_mime)
        print(gr + "HAS " + message + re)

        for user in users:
            if user['username'] != "":
                receiver = client.get_input_entity(user['username'])
            else:
                receiver = InputPeerUser(user['id'], user['access_hash'])
            try:
                print(gr + "[+] Sending Message to:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                # client.send_message(receiver, message)
                # print(gr + "[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
            except PeerFloodError:
                print(
                    re + "[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re + "[!] Error:", e)
                print(re + "[!] Trying to continue...")
                continue
        client.disconnect()
        print("Done. Message sent to all users.")


main.send_sms()
