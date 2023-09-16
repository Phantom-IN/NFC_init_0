from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

url = "https://pib.gov.in/AllReleasem.aspx"
driver.get(url)

for year in range(2022, 2024): 
    year_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlYear"))
    year_dropdown.select_by_value(str(year))

    for month in range(1, 13): 
        month_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlMonth"))
        month_dropdown.select_by_value(str(month))

        for day in range(1, 32): 
            day_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlday"))
            day_dropdown.select_by_value(str(day))

            import time
            time.sleep(2)

            anchor_tags = driver.find_elements(By.CLASS_NAME, "col-md-12.col-sm-9.col-xs-12 a")

            with open("news.txt", "a", encoding="utf-8") as file:
                for anchor_tag in anchor_tags:
                    href_attribute = anchor_tag.get_attribute("href")
                    file.write(f"Date {day}, Month {month}, Year {year}, Href Attribute: {href_attribute}\n")

# Close the WebDriver
driver.quit()
