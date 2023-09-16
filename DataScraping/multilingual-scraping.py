import pandas as pd
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from googletrans import Translator

def send_dataframe_to_api(csv_file_path, api_endpoint):
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')

        for index, row in df.iterrows():
            heading = row['heading']
            body = row['body']

            api_data = {
                'heading': heading,
                'description': body,
            }

            try:
                response = requests.post(api_endpoint, json=api_data)
                response.raise_for_status()
                print(f'Data sent to API for Row {index + 1}')

                server_response = response.json() 
                print(f'Server Response for Row {index + 1}: {server_response}')

            except requests.exceptions.RequestException as e:
                print(f'Failed to send data to API for Row {index + 1}, Error: {str(e)}')

        print("All data sent to the API and processed.")

    except Exception as e:
        print(f'Error: {str(e)}')

def scrape_and_send_hindi_to_api(api_endpoint):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        url = "https://www.jagran.com/news/national-news-hindi.html?itm_medium=national&itm_source=dsktp&itm_campaign=navigation"
        driver.get(url)

        while True:
            try:
                load_more_button = driver.find_element(By.ID, "pagination-btn")
                if load_more_button.is_displayed():
                    load_more_button.click()
                    time.sleep(2)  
                else:
                    break
            except Exception as e:
                break

        hrefs = []
        div_elements = driver.find_elements(By.XPATH, "//ul[@class='ListingSide_listing__G0B28']/li[@class='ListingSide_CardStory__weOJf CardStory']")
        for div_element in div_elements:
            link = div_element.find_element(By.XPATH, ".//a").get_attribute("href")
            hrefs.append(link)

        driver.quit()

        def scrape_url(url):
            try:
                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                h1_heading = soup.find('h1').text.strip()

                article_body_div = soup.find('div', class_='ArticleBody')
                p_tags = article_body_div.find_all('p')
                paragraph_text = ' '.join([p.text.strip() for p in p_tags])

                return h1_heading, paragraph_text

            except requests.exceptions.RequestException as e:
                return None, str(e)
            except Exception as e:
                return None, str(e)

        def translate_text(text):
            try:
                if not text:
                    return "No text to translate" 
                translator = Translator()
                translation = translator.translate(text, src='auto', dest='en')
                if hasattr(translation, 'text'):
                    return translation.text
                else:
                    return "Translation failed"
            except Exception as e:
                return str(e)

        for url in hrefs:
            url = url.strip()
            h1, paragraph = scrape_url(url)

            if h1 is not None:
                h1_english = translate_text(h1)
                paragraph_english = translate_text(paragraph)

                api_data = {
                    'heading': h1_english,
                    'description': paragraph_english,
                }

                try:
                    response = requests.post(api_endpoint, json=api_data)
                    response.raise_for_status()
                    print(f'Data sent to API for URL: {url}')

                    server_response = response.json()  
                    print(f'Server Response: {server_response}')

                except requests.exceptions.RequestException as e:
                    print(f'Failed to send data to API for URL: {url}, Error: {str(e)}')

            else:
                print(f'Failed to scrape URL: {url}')

    except Exception as e:
        print(f'Error: {str(e)}')

def scrape_marathi_news(api_endpoint):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        url = "https://divyamarathi.bhaskar.com/national/"
        driver.get(url)

        def scroll_to_bottom():
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        anchor_tags = []

        for _ in range(3): 
            scroll_to_bottom()
            time.sleep(2)  

        li_elements = driver.find_elements(By.CSS_SELECTOR, "li.c7ff6507.db9a2680")

        hrefs = []

        for li_element in li_elements:
            a_elements = li_element.find_elements(By.TAG_NAME, "a")
            for a_element in a_elements:
                href_attribute = a_element.get_attribute("href")
                hrefs.append(href_attribute)

        driver.quit()

        def scrape_url_and_translate(url):
            try:
                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                heading_div = soup.find('div', class_='a88a1c42')
                h1_heading = heading_div.find('h1').text.strip()

                article_body_div = soup.find('div', class_='ba1e62a6')
                p_tags = article_body_div.find_all('p')
                paragraph_text = ' '.join([p.text.strip() for p in p_tags])

                translated_heading = translate_text(h1_heading)
                translated_paragraph = translate_text(paragraph_text)

                return translated_heading, translated_paragraph

            except requests.exceptions.RequestException as e:
                return None, str(e)
            except Exception as e:
                return None, str(e)

        def translate_text(text):
            try:
                if not text:
                    return "No text to translate"  
                translator = Translator()
                translation = translator.translate(text, src='auto', dest='en')
                if hasattr(translation, 'text'):
                    return translation.text
                else:
                    return "Translation failed"
            except Exception as e:
                return str(e)

        for url in hrefs:
            url = url.strip()
            translated_heading, translated_paragraph = scrape_url_and_translate(url)

            if translated_heading is not None:

                api_data = {
                    'heading': translated_heading,
                    'description': translated_paragraph,
                }

                try:
                    response = requests.post(api_endpoint, json=api_data)
                    response.raise_for_status()
                    print(f'Data sent to API for URL: {url}')

                    server_response = response.json()  
                    print(f'Server Response: {server_response}')

                except requests.exceptions.RequestException as e:
                    print(f'Failed to send data to API for URL: {url}, Error: {str(e)}')

            else:
                print(f'Failed to scrape URL: {url}')

    except Exception as e:
        print(f'Error: {str(e)}')

# Function to create a menu-driven program
def menu_driven_program():
    while True:
        print("Menu:")
        print("1. Forward regional data - Marathi")
        print("2. Forward regional data - Hindi")
        print("3. Forward data")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            marathi_api_endpoint = "https://c8ab-103-246-224-103.ngrok-free.app/predict"  
            scrape_marathi_news(marathi_api_endpoint)

        elif choice == '2':
            hindi_api_endpoint = "https://c8ab-103-246-224-103.ngrok-free.app/predict"  
            scrape_and_send_hindi_to_api(hindi_api_endpoint)

        elif choice == '3':
            csv_file_path = "english_data.csv"  
            api_endpoint = "https://c8ab-103-246-224-103.ngrok-free.app/predict"  
            send_dataframe_to_api(csv_file_path, api_endpoint)

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    menu_driven_program()
