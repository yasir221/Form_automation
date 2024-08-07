from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Function to initialize and configure the webdriver
def init_driver():
    # Change the path to the location of your webdriver executable
    driver = webdriver.Chrome()
    driver.maximize_window()  # Maximize the browser window
    return driver

# Function to search for a keyword on Amazon
def search_keyword(driver, keyword):
    driver.get("https://www.amazon.com")
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for the page to load
    except Exception as e:
        print("Error searching on Amazon:", e)
        driver.quit()

# Function to scrape product links from search results
def scrape_product_links(driver):
    product_links = []
    try:
        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-item"))
        )
        
        # Find all product elements on the page
        product_elements = driver.find_elements(By.CSS_SELECTOR, ".s-result-item")
        for product_element in product_elements:
            # Extract link to the product
            try:
                product_link = product_element.find_element(By.CSS_SELECTOR, "a.a-link-normal.a-text-normal").get_attribute("href")
                product_links.append(product_link)
            except:
                pass
    except Exception as e:
        print("Error scraping product links:", e)
    return product_links

# Function to scrape store name from product page
def scrape_store_name(driver, product_link):
    try:
        driver.get(product_link)
        # Wait for the store name to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "bylineInfo"))
        )
        store_name = driver.find_element(By.ID, "bylineInfo").text.strip()
        return store_name
    except Exception as e:
        print("Error scraping store name:", e)
        return None

# Function to save data to CSV file
def save_to_csv(store_names, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Store Name"])  # Header row
        for store_name in store_names:
            writer.writerow([store_name])

def main():
    keyword = input("Enter the keyword to search on Amazon: ")
    filename = input("Enter the filename to save the data (e.g., output.csv): ")

    # Initialize the webdriver
    driver = init_driver()

    try:
        # Search for the keyword on Amazon
        search_keyword(driver, keyword)

        # Scrape product links from search results
        product_links = scrape_product_links(driver)

        # Scrape store names from each product page
        store_names = []
        for product_link in product_links:
            store_name = scrape_store_name(driver, product_link)
            if store_name and not(store_name.__contains__('Brand:')) and not(store_names.__contains__(store_name)):
                store_names.append(store_name)
                save_to_csv(store_names, filename)


        # Save data to CSV file
        # save_to_csv(store_names, filename)

        print(f"Data saved to {filename}")
    finally:
        # Close the browser window
        driver.quit()

if __name__ == "__main__":
    main()
