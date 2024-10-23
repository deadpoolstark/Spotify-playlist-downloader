import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Path to your geckodriver
driver_path = ''

# Path to the Firefox binary
firefox_binary_path = ''
# URL template for Lucida.to
base_url = "https://lucida.to/?url={}&country=US"

# Path to the text file containing the Spotify track URLs
txt_file = 'spotify_song_links.txt'

def format_url(spotify_url):
    return base_url.format(spotify_url)

def download_tracks():
    # Setup Firefox options
    options = Options()
    options.headless = False  # Set to True if you do not need a UI
    options.binary_location = firefox_binary_path

    # Initialize the Firefox WebDriver
    service = Service(executable_path=driver_path)
    driver = webdriver.Firefox(service=service, options=options)
    
    with open(txt_file, 'r') as file:
        spotify_urls = [line.strip() for line in file.readlines()]

    for spotify_url in spotify_urls:
        # Format the URL for Lucida.to
        formatted_url = format_url(spotify_url)
        
        # Visit the Lucida.to page
        driver.get(formatted_url)
        
        try:
            # Wait until the button is present and visible
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, '//button[contains(@class, "download-button")]'))
            )
            
            # Locate the download button using XPath
            download_button = driver.find_element(By.XPATH, '//button[contains(@class, "download-button")]')
            
            # Use JavaScript to click the button directly
            driver.execute_script("arguments[0].click();", download_button)
            print(f"Clicked download for: {spotify_url}")            
        except (TimeoutException, NoSuchElementException):
            print(f"Download button was not found or not clickable for {spotify_url}")
        except Exception as e:
            print(f"Failed to click download for: {spotify_url}. Error: {e}")
        time.sleep(60)
    
    # Close the WebDriver
    driver.quit()

if __name__ == '__main__':
    download_tracks()