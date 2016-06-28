#!/usr/bin/python

# *****************************************************************************************
# use selenium and paramiko module
# command line:
# sudo pip install -U selenium
# sudo pip install paramiko
# *****************************************************************************************

import paramiko
import socket
import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# *****************************************************************************************
# set selenium and paramiko version
# *****************************************************************************************

paramikoVersion = '2.0.0'
seleniumVersion = '2.53.2'

# *****************************************************************************************
# set environment variable
# *****************************************************************************************

hostname = '140.92.27.96'
port = 22
username = 'root'
password = '!123456'
installRStudioCmd = 'wget https://download2.rstudio.org/rstudio-server-rhel-0.99.892-x86_64.rpm && chmod 777 /root/rstudio-server-rhel-0.99.892-x86_64.rpm && yum install --nogpgcheck /root/rstudio-server-rhel-0.99.892-x86_64.rpm'
createRStudioUserID = 'rstudio'
setRStudioUserPWD = 'rstudio'
rstudioServerPort = '8787'
chromeWebdriverPath = '/Users/Archer/Desktop/React Native/selenium/chromedriver'

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):

        # *****************************************************************************************
        # install RStudio Server
        # *****************************************************************************************

        paramiko.util.log_to_file('install_rstudio.log')
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "creating " + hostname + " connection"
        s.connect(hostname, port, username, password)
        print "connected " + hostname + " connection"
        print "download and install rstudio-server"
        stdin, stdout, stderr = s.exec_command(installRStudioCmd)
        stdin.write('Y\n')
        stdin.flush()
        error = stderr.read()
        output = stdout.read()
        print("download & install rstudio err:" + error)
        print("download & install rstudio out:" + output)
        #stdin, stdout, stderr = s.exec_command('useradd rstudio && passwd rstudio')
        stdin, stdout, stderr = s.exec_command('useradd ' + createRStudioUserID +' && passwd ' + createRStudioUserID)
        #stdin.write('rstudio\n')
        stdin.write(setRStudioUserPWD + '\n')
        stdin.flush()
        #stdin.write('rstudio\n')
        stdin.write(setRStudioUserPWD + '\n')
        stdin.flush()
        error = stderr.read()
        output = stdout.read()
        print("create user and change password err:" + error)
        print("create user and change password out:" + output)
        #stdin, stdout, stderr = s.exec_command('rstudio-server stop')
        stdin, stdout, stderr = s.exec_command('rstudio-server start')
        error = stderr.read()
        output = stdout.read()
        print("start rstudio-server err:" + error)
        print("start rstudio-server out:" + output)
        s.close()

        # *****************************************************************************************
        # set browser type
        # *****************************************************************************************

        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome(chromeWebdriverPath)

    def test_search_in_python_org(self):

        browser = self.driver

        # *****************************************************************************************
        # open url
        # *****************************************************************************************

        rstudioWeb = 'http://' + hostname + ':' + rstudioServerPort
        print "RStudioWeb: " + rstudioWeb
        browser.get(rstudioWeb)

        # *****************************************************************************************
        # input value & click ESCAPE & click RETURN button
        # *****************************************************************************************

        browser.find_element_by_id('username').send_keys(createRStudioUserID)
        browser.find_element_by_id('password').send_keys(setRStudioUserPWD + Keys.RETURN)

        assert "No results found." not in browser.page_source
        print "title: " + browser.title
        print "current_url: " + browser.current_url

    def tearDown(self):

        # *****************************************************************************************
        # close all browser
        # *****************************************************************************************

        time.sleep(30)

if __name__ == "__main__":

    if paramiko.__version__ == paramikoVersion and webdriver.__version__ == seleniumVersion:
        unittest.main()
    else:
        print "no install or verion error \nparamiko: " + paramikoVersion + "\nselenium: " + seleniumVersion
