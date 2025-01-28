from bs4 import BeautifulSoup
import requests
import pandas as pd

################################ FOR SPOOFING HEADERS ###############################

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", 
  }

try:
    current_page = 1
    proceed = True
    data = []

    while proceed:
        print(f'Currently scraping page: {current_page}')

        ################### FETCHING THE PAGE ###################

        url = f'https://books.toscrape.com/catalogue/page-{current_page}.html'

        response = requests.get(url, headers=headers)
        
        ################## Check for 404 before proceeding further ##############
        if response.status_code == 404:
            proceed = False
            break
        
        response.raise_for_status()  # Throw an error if the request fails

        ################## PARSING THE PAGE #####################

        soup = BeautifulSoup(response.text, 'html.parser')
        all_books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

        ################# LOOPING THRU EVERY ELEMENT ON THE PAGE #################

        for book in all_books:
            item = {}
            item['Title'] = book.find('img').attrs['alt']
            item['Link'] = "https://books.toscrape.com/catalogue/"+book.find('a').attrs['href']
            item['Price'] = book.find('p', class_='price_color').text[2:]
            item['Stock'] = book.find('p', class_='instock availability').text.strip()

            data.append(item)

        current_page += 1
        # proceed = False


except Exception as e:
    print(f"An error occurred: {e}")

finally:
    ################# SAVING RESULT INTO CSV FILE #################
    if data:
        df = pd.DataFrame(data)
        df.to_csv("books.csv", index=False)
        print("Data saved to books.csv")
    else:
        print("No data to save.")