from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
from server.models import InfoSource

class Command(BaseCommand):
    help = 'Search YouTube and save results'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str)

    def handle(self, *args, **kwargs):
        keyword = kwargs['keyword']
        results = self.search_youtube(keyword)
        self.save_to_model(results, 'youtube', keyword)  # Pass the keyword for tags
        self.stdout.write(self.style.SUCCESS('Successfully saved YouTube search results.'))

    def search_youtube(self, keyword):
        driver = webdriver.Chrome()  # or specify path: webdriver.Chrome('/path/to/chromedriver')
        try:
            driver.get("https://www.youtube.com")
            search_box = driver.find_element(By.NAME, 'search_query')
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)

            # Apply filters: 'This year' and 'Channel'
            filter_button = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/div/ytd-search-header-renderer/div[3]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
            filter_button.click()
            rev_button = driver.find_element(By.XPATH, '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-search-filter-options-dialog-renderer/div[2]/ytd-search-filter-group-renderer[5]/ytd-search-filter-renderer[1]/a/div/yt-formatted-string')
            rev_button.click()
            time.sleep(2)
            channel_filter = driver.find_element(By.XPATH, '//yt-formatted-string[text()="Channel"]')
            channel_filter.click()
            time.sleep(3)
            results = []
            seen_urls = set()  # To keep track of already processed URLs

            while len(results) < 10:
                channel_elements = driver.find_elements(By.XPATH, '//ytd-channel-renderer')
                for channel in channel_elements:
                    try:
                        title_element = channel.find_element(By.XPATH, './/*[@id="text"]')
                        title = title_element.text
                        link_element = channel.find_element(By.XPATH, './/*[@id="main-link"]')
                        url = link_element.get_attribute('href')
                        thumbnail_element = channel.find_element(By.XPATH, './/*[@id="img"]')
                        thumbnail = thumbnail_element.get_attribute('src')

                        subscriber_count_element = channel.find_element(By.XPATH, './/*[@id="video-count"]')
                        subscriber_count = subscriber_count_element.text
                        if 'K' in subscriber_count or 'M' in subscriber_count:
                            if title and url and thumbnail and url not in seen_urls:
                                seen_urls.add(url)
                                sanitized_keyword = keyword.replace(' ', '_').replace('/', '_')
                                file_name = os.path.join('media/images', f"{sanitized_keyword}_thumbnail_{len(results)+1}.jpg")
                                self.download_thumbnail(thumbnail, file_name)
                                print("xxxxxxxxxxxxxxxxxxxx",subscriber_count)
                                subscriber_count1 = subscriber_count
                                results.append({'title': title, 'url': url, 'thumbnail': file_name,'subscriber_count':subscriber_count1})

                            if len(results) >= 15:
                                break
                    except Exception as e:
                        print(f"Skipping a channel due to error: {e}")
                        continue

                if len(results) < 10:
                    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                    time.sleep(5)

            return results
        finally:
            driver.quit()

        
    def download_thumbnail(self, url, file_name):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Ensure directory exists
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
                with open(file_name, 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    
    def save_to_model(self, data, category, keyword):
        from django.conf import settings
        for item in data:
            # Compute the relative path
            image_path = os.path.relpath(item['thumbnail'], settings.MEDIA_ROOT)
            
            # Add keyword as a tag
            tags = f"{item['title']},{keyword}"  # Combine title and keyword as tags, separated by a comma
            
            InfoSource.objects.create(
                title=item['title'],
                url=item['url'],
                image=image_path,  # Store relative path
                category=category,
                tags=tags , # Store the combined tags
                subscribers_count=item['subscriber_count']
            )