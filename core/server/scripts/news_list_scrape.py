import requests
from bs4 import BeautifulSoup
import os
import re
from PIL import Image
from io import BytesIO
from django.shortcuts import render
from ..models import InfoSource

def scrape_nepal_news(request):
    url = "https://journalists.feedspot.com/nepal_news_websites/"
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <p> tags with class 'trow trow-wrap'
    rows = soup.find_all('p', class_='trow trow-wrap')

    # Create a directory to save images if it doesn't exist
    image_dir = os.path.join('media', 'images')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Loop through each row and scrape the data
    for row in rows:
        # Inside each 'trow trow-wrap', find the <a> tag with class 'ext'
        link = row.find('a', class_='ext')
        if link:
            title = link.get_text(strip=True)
            href = link.get('href')

            # Sanitize the title to create a valid filename
            sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)

            # Find the <img> tag with class 'thumb alignnone size-thumbnail wp-image-1243'
            img_tag = row.find('img', class_='thumb alignnone size-thumbnail wp-image-1243')
            img_path = None
            if img_tag:
                img_url = img_tag['src']
                img_extension = os.path.splitext(img_url)[1]  # Get the image extension

                # Download the image
                img_data = requests.get(img_url).content

                # Open image using Pillow
                img = Image.open(BytesIO(img_data))

                # Convert image to PNG format
                img_filename = f"{sanitized_title}.png"
                img_path = os.path.join('images', img_filename)  # Save path relative to 'media/' folder

                # Save the image in the desired format
                img.save(os.path.join('media', img_path), 'PNG')

            # Create or update the InfoSource object in the database
            InfoSource.objects.update_or_create(
                title=title,
                defaults={
                    'url': href,
                    'image': img_path,  # Save the relative image path (without 'media/')
                    'category': 'news_portal',  # Using 'news' as the category for all
                    'tags': 'news, samachar, khabar, Website'  # Use predefined tags
                }
            )

    return render(request, 'server/scrape_completed.html', {'message': 'Scraping completed and data saved to the database!'})