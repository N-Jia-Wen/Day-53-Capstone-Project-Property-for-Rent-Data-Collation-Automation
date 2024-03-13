from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import os


PROPERTY_PRICE_URL = "https://appbrewery.github.io/Zillow-Clone/"
# Your own Google form to key in the property's address, price, and link:
GOOGLE_FORM_URL = os.environ["GOOGLE_FORM_URL"]

response = requests.get(PROPERTY_PRICE_URL)
contents = response.text

soup = BeautifulSoup(contents, "html.parser")

listing_elements = soup.select(".StyledPropertyCardDataArea-anchor")
price_elements = soup.select(".PropertyCardWrapper__StyledPriceLine")
address_elements = soup.find_all("address")

listing_links = [listing.get("href") for listing in listing_elements]
# Obtains the price in the form $X,XXX (accounts for price being presented as e.g. $2,095+/mo and $2,494+ 1 bd:
listing_prices = [price.text.split("/")[0].split(" ")[0].replace("+", "") for price in price_elements]
listing_addresses = [address.text.strip().replace("|", "") for address in address_elements]


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

for num in range(len(listing_links)):
    driver.get(GOOGLE_FORM_URL)
    time.sleep(3)

    input_elements = driver.find_elements(By.CSS_SELECTOR, ".whsOnd.zHQkBf")

    address_input = input_elements[0]
    address_input.send_keys(listing_addresses[num])

    price_input = input_elements[1]
    price_input.send_keys(listing_prices[num])

    link_input = input_elements[2]
    link_input.send_keys(listing_links[num])

    submit_button = driver.find_element(By.CSS_SELECTOR, ".l4V7wb.Fxmcue")
    submit_button.click()
