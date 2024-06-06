from selenium import webdriver
import time

# Set up the web driver
driver = webdriver.Chrome()

# Navigate to Twitter
driver.get('https://twitter.com/explore')

# Wait for the page to load
time.sleep(2)

# Fetch trending topics
trending_topics = driver.find_element("xpath",'//span[@class="css-901oao css-16my406 r-1n1174f r-1efd50x r-5kkj8d r-9qu9m4"]')
for topic in trending_topics:
    print(topic.text)

# Close the web driver
driver.quit()