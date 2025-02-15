import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_all_transcripts_urls():
    urls = []
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service,options=options)
    driver.get("https://nptel.ac.in/courses/106106184")
    driver.maximize_window()
    time.sleep(2)
    driver.find_element(By.XPATH, "//span[text()='downloads']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='course-downloads']/div/div/h3[text()='Transcripts']").click()
    time.sleep(2)
    def select_language():
        driver.find_element(By.XPATH, "//span[text()='Select Language']//parent::div").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[@class='pseudo-input darkBG selected']//following-sibling::ul/li").click()
        time.sleep(2)
    
    # Wait until the transcript buttons are present.
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='c-language']/following-sibling::div[1]/a/button")
        )
    )
    
    # Count the transcript buttons (each corresponding to a lecture)
    transcript_buttons = driver.find_elements(By.XPATH, "//div[@class='c-language']/following-sibling::div[1]/a/button")
    total = len(transcript_buttons)
    print("Total transcript buttons found:", total)
    
    for i in range(total):
        # If you need to select the language for each lecture, do it here:
        select_language()

        # Re-fetch the transcript button each time using its index.
        button_xpath = f"(//div[@class='c-language']/following-sibling::div[1]/a/button)[{i+1}]"
        transcript_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        transcript_button.click()  # make sure to use click() with parentheses
        time.sleep(3)  # Wait for the new window to open

        # Get the handle of the current (main) window.
        main_window = driver.current_window_handle
        all_windows = driver.window_handles

        # Look for the new window (it should be different from the main window).
        new_window = None
        for handle in all_windows:
            if handle != main_window:
                new_window = handle
                break

        if new_window:
            driver.switch_to.window(new_window)
            # Optionally wait a bit for the new window to load its URL.
            time.sleep(2)
            current_url = driver.current_url
            urls.append(current_url)
            print(f"Lecture {i+1} URL: {current_url}")
            driver.close()  # Close the transcript window.
            driver.switch_to.window(main_window)
        else:
            print(f"No new window found for transcript button {i+1}")
        
        # Optional pause between iterations.
        time.sleep(2)
    
    driver.quit()
    return urls

if __name__ == "__main__":
    transcript_urls = get_all_transcripts_urls()
    print("All Transcript URLs:", transcript_urls)





# lectures Urls 
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_video_id_from_player(driver):
    # Try using the YouTube IFrame API to get the video data.
    video_data = driver.execute_script(
        """
        if (window.YT && YT.get && YT.get('player')) {
            return YT.get('player').getVideoData();
        }
        return {};
        """
    )
    video_id = video_data.get('video_id', '')
    if video_id:
        return video_id

   
    try:
        iframe = driver.find_element(By.ID, "player")
        src = iframe.get_attribute("src")
        match = re.search(r'/embed/([^?&"/]+)', src)
        if match:
            return match.group(1)
    except Exception as e:
        print("Error extracting video id from iframe src:", e)
    return ''

def get_all_lectre_urls():
    youtube_urls = []

    # Set up WebDriver.
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    # Open the course page.
    driver.get("https://nptel.ac.in/courses/106106184")
    driver.maximize_window()
    time.sleep(5)  # Allow page to load.

    # Find all unit (week) sections.
    unit_titles = driver.find_elements(By.XPATH, "//div[contains(@class, 'unit-title')]")
    print("Found", len(unit_titles), "unit(s).")

    # Iterate over each unit.
    for unit_index in range(1, len(unit_titles) + 1):
        try:
            # Re-find the unit title element (DOM may update).
            unit_title = driver.find_element(By.XPATH, f"(//div[contains(@class, 'unit-title')])[{unit_index}]")
            driver.execute_script("arguments[0].scrollIntoView();", unit_title)
            unit_title.click()  # Expand the unit.
            print(f"Clicked unit {unit_index}")
            time.sleep(3)  # Wait for the unit to expand.

            # Locate the lessons list inside the expanded unit.
            lessons_xpath = f"(//div[contains(@class, 'unit-title')])[{unit_index}]/following-sibling::ul[contains(@class, 'lessons-list')]/li"
            lessons = driver.find_elements(By.XPATH, lessons_xpath)
            print(f"Found {len(lessons)} lesson(s) in unit {unit_index}.")

            # Iterate over each lesson in the current unit.
            for lesson_index in range(1, len(lessons) + 1):
                try:
                    # Re-find the lesson element (DOM may update).
                    lesson = driver.find_element(By.XPATH, f"({lessons_xpath})[{lesson_index}]")
                    driver.execute_script("arguments[0].scrollIntoView();", lesson)
                    lesson.click()  # Click the lesson to load the video.
                    print(f"Clicked lesson {lesson_index} in unit {unit_index}.")
                    time.sleep(7)  # Wait for the video to load.

                    # Extract the video ID from the YouTube player.
                    video_id = get_video_id_from_player(driver)
                    if video_id:
                        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                        print(f"Extracted URL for unit {unit_index}, lesson {lesson_index}: {youtube_url}")
                        youtube_urls.append(youtube_url)
                    else:
                        print(f"Video ID not found for unit {unit_index}, lesson {lesson_index}.")
                    time.sleep(2)  # Optional: wait a bit before the next lesson.
                except Exception as e:
                    print(f"Error processing lesson {lesson_index} in unit {unit_index}: {e}")
        except Exception as e:
            print(f"Error processing unit {unit_index}: {e}")

    driver.quit()
    return youtube_urls

