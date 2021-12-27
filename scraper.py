from selenium import webdriver
import time
import re
import os 
import sys

assignment = sys.argv[1]

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
download_path = base_path + '\\blatt' + str(assignment)
try:
    os.mkdir(download_path)
except OSError:
    print ("Creation of the directory %s failed" % download_path)
else:
    print ("Successfully created the directory %s " % download_path)

payload = {
    'username' : 'HWR-CKL',
    'password' : 'antimageForever'
}
base_url = 'https://seafile.cloud.uni-hannover.de'
url = 'https://seafile.cloud.uni-hannover.de/sso'

options = webdriver.ChromeOptions()
config = {"plugins.always_open_pdf_externally": True, # Disable Chrome's PDF Viewer
               "download.default_directory": download_path , "download.extensions_to_open": "applications/pdf"}
options.add_experimental_option("prefs", config)
#options.add_argument("--headless")
driver = webdriver.Chrome("C:/Users/ASUS/Downloads/chromedriver.exe",chrome_options=options)

driver.get(url)

driver.find_element_by_id("username").send_keys(payload['username'])
driver.find_element_by_id("password").send_keys(payload['password'])
driver.find_element_by_name('_eventId_proceed').click()

print('logged in')

shared_libs_url = base_url + '/shared-libs/'
driver.get(shared_libs_url)
driver.get(base_url+ '/library/ab5502b7-3d56-45b2-8d65-24566eb2ee34/Ahmed_Korrekturen/')
driver.implicitly_wait(10)
time.sleep(1)
lnks=driver.find_elements_by_tag_name("a")


driver.get('https://seafile.cloud.uni-hannover.de/library/ab5502b7-3d56-45b2-8d65-24566eb2ee34/Ahmed_Korrekturen/Blatt%20' + assignment)
time.sleep(1)
file_folders = driver.find_elements_by_tag_name('a')
file_folders_links = []
for folder in file_folders:
    file_folders_links.append(folder.get_attribute('href'))
for lnk in file_folders_links:
   # get_attribute() to get all href
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
                #rename_file(teamNumber+".pdf",download_path)
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