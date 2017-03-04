from selenium import webdriver
from bs4 import BeautifulSoup

import Tkinter
import tkMessageBox

class myClass:
  baseurl = ""
  username = ""
  password = ""
  mac = ""
  other = ''
  found = 0
  xpaths = ""
  mydriver = "";
  def initialize(self):
        self.baseurl = "http://192.168.0.1/"
        self.username = "admin"
        self.password = "9446025244"
        self.mac = "<td>38-A4-ED-E1-C2-7D</td>"
        self.other = '<td class="ListB" id="t_mac_address">MAC Address</td>'
        self.found = 0
        self.xpaths = { 'usernameTxtBox' : "//*[@id='userName']",
                        'passwordTxtBox' : "//*[@id='pcPassword']",
                        'submitButton' :   "//*[@id='loginBtn']"
                      }
  def launchDriver(self, url):
        self.mydriver=webdriver.Chrome(executable_path=r"C:\Chrome\chromedriver.exe")
        self.mydriver.get(url)
  def gotoFrame(self, frame):
        self.mydriver.switch_to_frame(self.mydriver.find_element_by_name(frame))
  def login(self, path, user, passw):
        self.mydriver.find_element_by_xpath(path['usernameTxtBox']).send_keys(user)
        self.mydriver.find_element_by_xpath(path['passwordTxtBox']).send_keys(passw)
        self.mydriver.find_element_by_xpath(path['submitButton']).click()
  def selectTab(self, tab, subtab):
        self.gotoFrame("bottomLeftFrame")
        self.mydriver.find_element_by_link_text(tab).click()
        self.mydriver.find_element_by_link_text(subtab).click()
        self.mydriver.switch_to_default_content()
  def closeDriver(self):
        self.mydriver.close()
  def getIP(self):
        self.gotoFrame("mainFrame")
        soup = BeautifulSoup(self.mydriver.page_source,"html.parser")
        self.closeDriver()
        rows = soup.findAll('tr')
        for row in rows:
            cols = row.find_all('td')
            for col in cols:
             if ((self.mac == str(col)) and (self.other != str(col))):
               ip = cols[3]
               self.found = self.found +1
               break
            if self.found == 2:
             break
        return str(ip)[4:17]
  def findIP(self):
        quit()
        self.launchDriver(self.baseurl)
        self.login(self.xpaths, self.username, self.password)
        self.selectTab("DHCP","- DHCP Client List")
        ip = self.getIP()
        self.launchDriver("ftp://"+ip+":2121")

        
def quit():
    root.destroy()
def buttonclick():
    obj.findIP()

obj = myClass()
root = Tkinter.Tk()

obj.initialize()
B = Tkinter.Button(root,text = "Click",command = buttonclick)

B.pack()

root.mainloop()