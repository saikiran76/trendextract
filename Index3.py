from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import datetime
import requests
import time

def get_new_proxy():
    proxy_auth = ('Korada76', '2b435ztp.H@9wqL')
    proxy_url = 'https://www.pyproxy.com/login/'
    
    try:
        response = requests.get(proxy_url, auth=proxy_auth)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching proxy: {e}")
        raise Exception("Failed to get new proxy")


client = MongoClient('mongodb+srv://korada:Korada76105@initial.duq9qjd.mongodb.net/')
db = client['twitter_trends']
collection = db['trends']


def fetch_trending_topics():
    try:
        proxy_ip = get_new_proxy()
    except Exception as e:
        print(f"Error in get_new_proxy: {e}")
        return

    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy_ip}')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://twitter.com/login")
        
       
        driver.find_element(By.XPATH, "//span[text()='Sign in with Google']").click()
     
        input("Please log in through Google in the opened browser window. Press Enter here once you have logged in.")
      
        driver.get("https://twitter.com/explore/tabs/trending")
        time.sleep(5)  
        
        trends = driver.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='accessible-list-0'] div span")
        trending_topics = [trend.text for trend in trends[:5]]
        
        end_time = datetime.datetime.now()
        
        trend_data = {
            "trend1": trending_topics[0],
            "trend2": trending_topics[1],
            "trend3": trending_topics[2],
            "trend4": trending_topics[3],
            "trend5": trending_topics[4],
            "timestamp": end_time,
            "ip_address": proxy_ip
        }
        result = collection.insert_one(trend_data)
        
        driver.quit()
        return result.inserted_id, trend_data
    except Exception as e:
        driver.quit()
        print(f"Error during Selenium execution: {e}")
        raise e

if __name__ == "__main__":
    fetch_trending_topics()
