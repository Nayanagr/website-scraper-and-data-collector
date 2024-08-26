import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# # -------------------------------------------- CONSTANTS -----------------------------------------------------------#
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSfBIq5YI70-FgvwI19Bm9Od3eQo7o8guCBRmYWb0qzx2iRqfA/viewform'
URL = "https://www.zillow.com/san-francisco-ca/rentals"
PRICE_LIST = []
URL_LIST = []
ADDR_LIST = []
MASTER_LIST = [PRICE_LIST,URL_LIST,ADDR_LIST]

driver = webdriver.Chrome(options=webdriver.ChromeOptions().add_experimental_option('detach',True))
driver.get(url=URL)
time.sleep(20)
# next_page_button = driver.find_element(By.XPATH,'//a[@title="Next page"]')

# y=500
# for i in range(10):
#     try:
#         driver.execute_script("window.scrollTo(0,'+str(y)+');")
#         y+=500
#         print('Scroll action must have been performed')
#     except:
#         print('Error')
#         pass

data = driver.page_source

# for i in range():
#     next_page_button.click()
#     data = driver.page_source
#
# --------------------------------------- WEB SCRAPING ---------------------------------------------------------------#
soup = BeautifulSoup(data,features='lxml')

price_tags = soup.find_all('span',attrs={'data-test':"property-card-price"})
for tag in price_tags:
    try:
        price = tag.text.replace('/mo','')
        PRICE_LIST.append(price)
    except:
        print(f'PRICE NOT IDENTIFIED IN TAG{tag}')
        price = tag.text
        PRICE_LIST.append(price)

addr_tags = soup.find_all('address',attrs={'data-test':"property-card-addr"})
for tag in addr_tags:
    try:
        addr = tag.text.replace('/mo','')
        ADDR_LIST.append(addr)
    except:
        print(f'ADDR NOT IDENTIFIED IN TAG{tag}')
        addr = tag.text
        ADDR_LIST.append(addr)

url_tags = soup.find_all('a',attrs={'data-test':'property-card-link'})
for tag in url_tags:
    try:
        url = tag['href']
        if 'https://www.zillow.com/' not in url:
            url = 'https://www.zillow.com/'+url
        URL_LIST.append(url)
    except:
        print(f'URL NOT FOUND IN TAG{tag}')
        url = tag['href']
        URL_LIST.append(url)

# ---------------------------------Maintaining order and refining URL_LIST--------------------------------------------#
for url in URL_LIST:
    if url in URL_LIST:
        URL_LIST.remove(url)

for item in MASTER_LIST:
    print(len(item),item)
# ---------------------------------------- LOADING GOOGLE FORM--------------------------------------------------------#
driver2 = webdriver.Chrome(options=webdriver.ChromeOptions().add_experimental_option('detach',True))
driver2.get(FORM)
time.sleep(2)
addr_box = None
price_box =None
link_box = None
submit_button = None
# ======================================= FILLING GOOGLE FORM ========================================================#
def finding_boxes():
    global addr_box,price_box,link_box,submit_button
    input_boxes = driver2.find_elements(By.XPATH,'//input[@type="text"]')
    addr_box = input_boxes[0]
    price_box = input_boxes[1]
    link_box = input_boxes[2]
    submit_button = driver2.find_elements(By.XPATH,'//div[@role="button"]')[0]

for (addr,price,link) in zip(ADDR_LIST,PRICE_LIST,URL_LIST):
    finding_boxes()
    print(addr,price,link)
    addr_box.send_keys(addr)
    price_box.send_keys(price)
    link_box.send_keys(link)
    time.sleep(1)
    submit_button.click()
    time.sleep(2)
    driver2.get(FORM)
    time.sleep(3)
