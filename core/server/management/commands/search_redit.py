import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.core.management.base import BaseCommand
from server.models import InfoSource  # Adjust this import based on your project structure

class Command(BaseCommand):
    help = 'Scrape Reddit communities and save results'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str)

    def handle(self, *args, **kwargs):
        keyword = kwargs['keyword']
        driver = self.setup_driver()
        results = self.search_reddit(driver, keyword)
        self.save_to_model(results, 'reddit', keyword)
        self.stdout.write(self.style.SUCCESS('Successfully saved Reddit community results.'))

    def setup_driver(self):
        driver = webdriver.Chrome()  # or specify path to chromedriver
        return driver

    def search_reddit(self, driver, keyword):
        search_url = f"https://www.reddit.com/search/?q={keyword}&type=sr"
        driver.get(search_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.flex.p-md.rounded.hover\\:bg-neutral-background-hover'))
        )

        communities = []
        community_elements = driver.find_elements(By.CSS_SELECTOR, 'div.flex.p-md.rounded.hover\\:bg-neutral-background-hover')

        seen_urls = set()  # Track processed URLs
        for community in community_elements:
            try:
                name = community.find_element(By.CSS_SELECTOR, 'h2 span').text
                url = "https://www.reddit.com" + community.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                thumbnail = community.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')  # Adjust selector for image
                members = community.find_element(By.XPATH, './/faceplate-number').text  # Adjust for members count
                description = community.find_element(By.CSS_SELECTOR, 'p.text-ellipsis').text

                if url not in seen_urls:
                    seen_urls.add(url)
                    sanitized_keyword = keyword.replace(' ', '_').replace('/', '_')
                    file_name = os.path.join('media/images', f"{sanitized_keyword}_thumbnail.jpg")
                    self.download_thumbnail(thumbnail, file_name)

                    communities.append({
                        'name': name,
                        'url': url,
                        'thumbnail': file_name,
                        'members': members,
                        'description': description,
                    })

            except Exception as e:
                print(f"Error processing community: {e}")

        return communities

    def download_thumbnail(self, url, file_name):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
                with open(file_name, 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    def save_to_model(self, data, category, keyword):
        from django.conf import settings
        for item in data:
            image_path = os.path.relpath(item['thumbnail'], settings.MEDIA_ROOT)
            tags = f"{item['description']},{keyword}"  # Combine description and keyword as tags
            
            InfoSource.objects.create(
                title=item['name'],
                url=item['url'],
                image=image_path,  # Store relative path
                category=category,
                tags=tags,  # Store the combined tags
                subscribers_count=item['members'],  # Map members to subscribers_count
            )
