from selenium import webdriver


driver = webdriver.Firefox()
driver.get('https://www.python.org')
driver.save_full_page_screenshot('fullpage_gecko_firefox.png')
driver.quit()
