from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """
    Set up the ChromeDriver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode, if preferred
    options.add_argument('--disable-gpu')  # Disable GPU acceleration

    # Specify the path to your ChromeDriver if needed
    driver = webdriver.Chrome(options=options)  
    return driver

def search_reddit_communities(driver, search_prompt, limit=10):
    """
    Scrapes Reddit communities based on a search prompt using Selenium.
    
    :param driver: Selenium WebDriver instance.
    :param search_prompt: The query for searching subreddits.
    :param limit: Number of communities to return (default: 10).
    :return: List of subreddit details.
    """
    search_url = f"https://www.reddit.com/search/?q={search_prompt}&type=sr"
    driver.get(search_url)

    # Wait for the subreddit search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="search-community"]'))
    )

    communities = []
    
    # Find all subreddit listings
    community_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="search-community"]')

    for community in community_elements[:limit]:
        try:
            # Extract community details
            name = community.find_element(By.CSS_SELECTOR, 'h2 span').text
            url = community.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            members = community.find_element(By.CSS_SELECTOR, 'div.text-12 span').text
            description = community.find_element(By.CSS_SELECTOR, 'p[data-testid="search-subreddit-desc-text"]').text
            
            communities.append({
                'name': name,
                'url': url,
                'members': members,
                'description': description
            })
        except Exception as e:
            print(f"Error extracting community data: {e}")
            continue  # Skip in case of missing data

    return communities

if __name__ == '__main__':
    search_prompt = input("Enter a search query for Reddit communities: ")

    # Set up the ChromeDriver
    driver = setup_driver()

    # Scrape Reddit communities based on the search query
    results = search_reddit_communities(driver, search_prompt)

    # Print the results
    if results:
        for i, community in enumerate(results, start=1):
            print(f"Community {i}: {community['name']}")
            print(f"URL: {community['url']}")
            print(f"Members: {community['members']}")
            print(f"Description: {community['description']}\n")
    else:
        print("No communities found.")
    
    # Quit the driver
    driver.quit()
