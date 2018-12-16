#!/srkim/anaconda2/bin/python
# -*- coding: utf-8 -*-

'''
  Author   : Kim, Seongrae
  Filename : send_mail.py
  Release  : 1
  Date     : 2018-12-11

  Description : Mail Simulator Main module

  Notes :
  ===================
  History
  ===================
  2018/12/11  created by Kim, Seongrae
'''
import os
import sys
import select
import socket
import threading
from time import sleep
from email.base64mime import body_encode as encode_base64

# common package import
from common import *


BUFFER_SIZE = 1000

class SendMail:
    def __init__(self, mail_from, mail_to, ipaddr="127.0.0.1", port=25, pwd=None, uid=None):
        self.isRun = True
        self.ipaddr = ipaddr;
        self.uid = mail_from if uid == None else uid
        self.pwd = pwd
        self.port = port
        self.sock = None
        self.ehlo = mail_from.split("@")[1]
        self.mail_to = mail_to
        self.mail_from = mail_from
        self.asw_command = []
        local_lock     = threading.Semaphore(1)

    def __del__(self):
        self.isRun = False
        self.__smtp_disconnection()

    def __th_main(self):
        sBuffer         = ""
        select_timer    = 0.01
        while self.isRun == True:
            if self.sock != None:
                input_list = [self.sock]
                input_ready, write_ready, except_ready = select.select(input_list, [], input_list, select_timer)
                if len(input_ready) <= 0:
                    continue

                data = self.sock.recv(65536)

                if len(data) == 0:
                    continue

                ch = data.decode('ascii')
                sBuffer += ch

                if ch[-1] != '\n':
                    continue

                sBuffer = sBuffer.split("\n")

                for line in sBuffer:
                    if len(line) == 0:
                        continue
                    print("%sS%s < %s" % (C_RED,C_END,line))
                    line = line.replace("-", "")
                    line = line.split(" ")
                    self.asw_command.append(line[0])
                sBuffer = ""

    def __smtp_wait_command(self):
        while True:
            if len(self.asw_command) > self.ch_idx:
                nRet = self.asw_command[self.ch_idx]
                self.ch_idx += 1
                return nRet
            sleep(0.01)

    def __mime_replace_user_info(self, line, mail_from=None, mail_to=None):
        if mail_from==None and mail_to==None:
            return line

        if get_param(("--exchange-username","-e")) == "False":
            return line

        tag=line.split(":")[0].upper()

        if tag == "FROM" and mail_from != None:
            if len(line.split("<")) != 1:
                return "%s<%s>" % (line.split("<")[0], mail_from)
            else:
                return "From: %s" % (mail_from)

        if tag == "TO" and mail_to != None:
            if len(line.split("<")) != 1:
                return "%s<%s>" % (line.split("<")[0], mail_to)
            else:
                return "To: %s" % (mail_to)

        return line


    def __smtp_connection(self):

        self.ch_idx = 0
        self.isRun = True
        self.asw_command = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ipaddr, self.port))

        self.hThread = threading.Thread(target=self.__th_main)
        self.hThread.daemon = True
        self.hThread.start() 

    def __smtp_disconnection(self):
        self.isRun = False
        self.ch_idx = 0
        self.asw_command = []
        sleep(0.03)
        if self.sock != None:
            self.sock.close()
            self.sock = None


    def __send_mail_from_log(self, eml_path):

        smtp_hdr=[]
        smtp_hdr.append("mail FROM:<%s>\r\n" % (self.mail_from))
        smtp_hdr.append("rcpt TO:<%s>\r\n" % (self.mail_to))
        smtp_hdr.append("data\r\n")

        for hdr_it in smtp_hdr:
            sys.stdout.write("%sC%s > %s" % (C_GREEN,C_END,hdr_it))
            self.sock.send(hdr_it.encode())
            sleep(0.05)

        for line in open(eml_path, 'r').readlines():
            line = line.split('\n')[0]
            line = self.__mime_replace_user_info(line, self.mail_from, self.mail_to)
            line += "\r\n"
            sys.stdout.write("%sC%s > %s" % (C_GREEN,C_END,line))
            #bin_line = self.sock.send(line.encode())
            try:
                bin_line = line.decode('utf-8').encode('utf-8')
            except UnicodeDecodeError as e:
                continue

            self.sock.send(bin_line)

        sleep(0.5)

        smtp_hdr=[]
        smtp_hdr.append(".\r\n")

        for hdr_it in smtp_hdr:
            sys.stdout.write("%sC%s > %s" % (C_GREEN,C_END,hdr_it))
            sleep(0.05)
            self.sock.send(hdr_it.encode())
 

        for i in range(2500):
            if self.asw_command[-1] == "250":
                break
            sleep(0.001)

 
    def send_mail(self, eml_path):
        self.__smtp_connection()
        smtp_hdr=[]
        smtp_hdr.append("ehlo %s\r\n" % (self.ehlo))
        if self.uid != None and self.pwd != None and get_param(("--auth","-a")) == "True":
            auth_key = b""
            auth_key += '\x00'
            auth_key += self.uid.encode('ascii')
            auth_key += '\x00'
            auth_key += self.pwd.encode('ascii')
            smtp_hdr.append("AUTH PLAIN %s\r\n" % (encode_base64(auth_key, eol='')))

        for hdr_it in smtp_hdr:
            sys.stdout.write("%sC%s > %s" % (C_GREEN,C_END,hdr_it))
            self.sock.send(hdr_it.encode())
            sleep(0.05)

        smtp_hdr=[]
        smtp_hdr.append("quit\r\n")

        if type(eml_path) != list:
            eml_path = [eml_path,]

        for item in eml_path:
            if os.path.exists(item) == False:
                continue
            self.__send_mail_from_log(item)

        for hdr_it in smtp_hdr:
            sys.stdout.write("%sC%s > %s" % (C_GREEN,C_END,hdr_it))
            sleep(0.05)
            self.sock.send(hdr_it.encode())
 

        for i in range(2500):
            if self.asw_command[-1] == "221":
                break
            sleep(0.001)

        self.__smtp_disconnection()
       

def test_case1(): # ./send_mail.py aaa.eml bbb.eml ...
    if len(sys.argv) == 1:
        return 
    e = SendMail(mail_from="test2@do.test.com", mail_to="test100@do.test.com", ipaddr="192.168.56.130")
    for idx, item in enumerate(sys.argv):
        if os.path.exists(item) == False or idx == 0:
            continue
        e.send_mail(item)

def test_case2(): # ./send_mail.py aaa.eml bbb.eml ...
    if len(sys.argv) == 1:
        return 
    #e = SendMail(mail_from="test2@do.test.com", mail_to="test100@do.test.com", ipaddr="192.168.56.130", pwd="qwe123")
    #e = SendMail(mail_from="srkim@eluon.com", mail_to="shshrka001@gmail.com", ipaddr="192.168.56.130", uid="test2@do.test.com", pwd="qwe123")
    e = SendMail(mail_from="test2@do.test.com", mail_to="test100@do.test.com", ipaddr="192.168.56.130", pwd="qwe123")
    #e = SendMail(mail_from="shshrka001@gmail.com", mail_to="test100@do.test.com", ipaddr="192.168.56.130", pwd="qwe123")
    e.send_mail(sys.argv[1:])



if __name__ == "__main__":
    test_case2()

