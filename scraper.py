from selenium import webdriver
from private import cred
import time
import re
import os 
import sys

# extract assignment number
assignment = sys.argv[1]


# rename the file in a convenient way 
def rename_file(newname, download_dir, time_to_wait=30):
    time_counter = 0
    time.sleep(0.1)
    filename = max([f for f in os.listdir(download_dir)], key=lambda xa :   os.path.getctime(os.path.join(download_dir,xa)))
    print(filename)
    while 'crdownload' in filename:
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise Exception('Waited too long for file to download')
        filename = max([f for f in os.listdir(download_dir)], key=lambda xa :   os.path.getctime(os.path.join(download_dir,xa)))
    os.rename(os.path.join(download_dir, filename), os.path.join(download_dir, newname))



base_path = 'C:\\Users\\ASUS\\Uni\\work'

#create the folder for the downloads
download_path = base_path + '\\blatt' + str(assignment)
try:
    os.mkdir(download_path)
except OSError:
    print ("Creation of the directory %s failed" % download_path)
else:
    print ("Successfully created the directory %s " % download_path)




base_url = 'https://seafile.cloud.uni-hannover.de'
url = 'https://seafile.cloud.uni-hannover.de/sso'

#fix download path among others
options = webdriver.ChromeOptions()
config = {"plugins.always_open_pdf_externally": True, # Disable Chrome's PDF Viewer
               "download.default_directory": download_path , "download.extensions_to_open": "applications/pdf"}
options.add_experimental_option("prefs", config)
options.add_argument("--headless")

#start the web driver
driver = webdriver.Chrome("C:/Users/ASUS/Downloads/chromedriver.exe",chrome_options=options)

driver.get(url)

#authenticate 
driver.find_element_by_id("username").send_keys(cred['username'])
driver.find_element_by_id("password").send_keys(cred['password'])
driver.find_element_by_name('_eventId_proceed').click()

print('Login successfull')

'''

The following snippet of commented code is an alternative way to perform a sso login using the requests library.
However, you should manually adjust the parameters of the saml request and response. SAML is the intermediate that allows
the user to identify himself by the idp and then login into the sp. This snippet is inspired from "https://stackoverflow.com/questions/16512965/logging-into-saml-shibboleth-authenticated-server-using-python/23930373#23930373"
you need to adjust the headers according to the website you want to get or post as well as the saml response parameters.

On the other hand, the requets library does not support javascript. That's why I recommend using selenium following the above code.
Fortunately, you could switch from selenium driver to a request session at any time by doing the following:
import requests
cook = {i['name']: i['value'] for i in driver.get_cookies()}
driver.quit()
r = requests.get("your url", cookies=cook)

You can also use the mechanize library which is easy to handle but doesn't support javascript neither.


# start HTTP request session
s = requests.Session()

# Prepare for first request, change url1
url1 = "https://studip.uni-hannover.de/Shibboleth.sso/Login?target=https%3A%2F%2Fstudip.uni-hannover.de%2Fdispatch.php%2Fmy_courses%3Fsso%3Dshib%26again%3Dyes%26cancel_login%3D1&entityID=https%3A%2F%2Fsso.idm.uni-hannover.de%2Fidp%2Fshibboleth"
header_data = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

# Make first request
r1 = s.get(url1, headers = header_data)

# Prepare for second request - extract URL action for next POST from response, append header, and add login credentials
ss1 = re.search('action="', r1.text)

# this regular expression search is also very specific. You need to look at the html source of your website
ss2 = re.search('" method', r1.text)
print(r1.text[ss1.span(0)[1]:ss2.span(0)[0]])
#adjust first part...
url2 = 'https://sso.idm.uni-hannover.de' + r1.text[ss1.span(0)[1]:ss2.span(0)[0]]
header_data.update({'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/x-www-form-urlencoded'})
cred = {'j_username': 'your username', 'j_password':'your password', '_eventId_proceed' : 'Sign in'}

# Make second request
r2 = s.post(url2, data = cred)

# Prepare for third request - format and extract URL, RelayState, and SAMLResponse
ss3 = re.search('<form action="',r2.text) # expect only one instance of this pattern in string
ss4 = re.search('" method="post">',r2.text) # expect only one instance of this pattern in string
url3 = r2.text[ss3.span(0)[1]:ss4.span(0)[0]].replace('&#x3a;',':').replace('&#x2f;','/')

ss4 = re.search('name="RelayState" value="', r2.text) # expect only one instance of this pattern in string
ss5 = re.search('"/>', r2.text)
relaystate_value = r2.text[ss4.span(0)[1]:ss5.span(0)[0]].replace('&#x3a;',':')

ss6 = re.search('name="SAMLResponse" value="', r2.text)
ss7 = [m.span for m in re.finditer('"/>',r2.text)] # expect multiple matches with the second match being desired
saml_value = r2.text[ss6.span(0)[1]:ss7[1](0)[0]]

data = {'RelayState': relaystate_value, 'SAMLResponse': [saml_value, 'Continue']}
header_data.update({'Host': 'sso.idm.uni-hannover.de', 'Referer': 'https://sso.idm.uni-hannover.de', 'Connection': 'keep-alive'})

# Make third request
print(url3)
r3 = s.post(url3, headers=header_data, data = data)
soup = BeautifulSoup(r3.content,'html.parser')
print(soup.prettify())

'''




shared_libs_url = base_url + '/shared-libs/'
driver.get(shared_libs_url)
driver.get(base_url+ '/library/ab5502b7-3d56-45b2-8d65-24566eb2ee34/Ahmed_Korrekturen/')

# Not all queried html elements will be retrieved if page not fully loade, wait...
time.sleep(1)
lnks=driver.find_elements_by_tag_name("a")


driver.get('https://seafile.cloud.uni-hannover.de/library/ab5502b7-3d56-45b2-8d65-24566eb2ee34/Ahmed_Korrekturen/Blatt%20' + assignment)
time.sleep(1)
file_folders = driver.find_elements_by_tag_name('a')
file_folders_links = []

#store the links in an array to avoid stale element error when quering elemnts of a previous page
for folder in file_folders:
    file_folders_links.append(folder.get_attribute('href'))

#This is how I iterate through the pdf files and download them. Done conveneniently for me and is very website dependent.
for lnk in file_folders_links:
   if lnk != None and re.search('[0-9]{4}$',lnk):
    teamNumber = lnk[len(lnk)-4:len(lnk)]
    print(teamNumber)
    file_folder_url =str(lnk)
    driver.get(file_folder_url)
    time.sleep(1)
    links = driver.find_elements_by_tag_name("a")
    sub_file_folders_links = []
    for ln in links:
        sub_file_folders_links.append(ln.get_attribute('href'))
    for link in sub_file_folders_links:
        if link != None and re.search("_studip_",str(link)):
            url = link
            print(url)
            if 'pdf' in url:
                driver.get(url+"?dl=1")
                time.sleep(1)
                break
            
            #avoid irrelevant links
            elif  re.search('.*(repo.*[#]*.*|[#]+).*',url) == None:
                driver.get(url)
                time.sleep(1)
                links_before_pdf = driver.find_elements_by_tag_name("a")
                url_before_pdf = []
                for lnk in links_before_pdf:
                    url_before_pdf.append(lnk.get_attribute('href'))
                for link in url_before_pdf:
                    if link!= None and 'pdf' in str(link):
                            driver.get(link+"?dl=1")
                            rename_file(teamNumber+".pdf",download_path)

driver.close()