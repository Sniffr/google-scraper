from bs4 import BeautifulSoup
import requests
import re

import dbscript
from threading import Thread

keywords = ["Sports", "Lottery", "slot", "casino", "sports lottery India", "Horse Racing bet"]

results = []


# Define a function that takes a keyword as a parameter
def get_headers_and_links(keyword):
    url = f'https://www.google.com/search?q={keyword}'
    # Get the HTML from the website
    html = requests.get(url).text
    # Create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')
    # Find all a tags on the page
    a_tags = soup.find_all('a')
    # Print the h3 tags that are children of the tags
    for a in a_tags:
        h3 = a.find('h3')
        if h3:
            result = re.search(r'https?://[a-z0-9.-]+\.[a-z]{2,4}[/a-z0-9._-]*', a['href']).group(0) if re.search(
                r'https?://[a-z0-9.-]+\.[a-z]{2,4}[/a-z0-9._-]*', a['href']) else "No URL found in string"
            if result != "No URL found in string":
                results.append({'header': h3.text, 'url': result})


def group_urls(urls):
    # Define a dictionary to store the URL groups
    groups = {
        "blog": [],
        "social_media": [],
        "website": [],
        "news": [],
        "betting_site": [],
        "other": []
    }

    # Iterate over the URLs
    for url_dict in urls:
        # Use a regular expression to check if the URL is a blog
        if re.search(r'blog\.[a-z0-9.-]+\.[a-z]{2,4}[/a-z0-9._-]*', url_dict['url']):
            groups["blog"].append(url_dict)
        # Use a regular expression to check if the URL is a social media site
        elif re.search(r'(facebook|twitter|linkedin|instagram|pinterest)\.[a-z0-9.-]+\.[a-z]{2,4}[/a-z0-9._-]*',
                       url_dict['url']):
            groups["social_media"].append(url_dict)
        # Use a regular expression to check if the URL is a news site
        elif re.search(r'news\.[a-z0-9.-]+\.[a-z]{2,4}[/a-z0-9._-]*', url_dict['url']):
            groups["news"].append(url_dict)
        # Use a regular expression to check if the URL is a betting site
        elif re.search(r'bet\.[a-z0-9.-]+\.[a-z]{2,4}[/a-z0-9._-]*', url_dict['url']):
            groups["betting_site"].append(url_dict)
        else:
            groups["other"].append(url_dict)

    # Return the dictionary of URL groups
    return groups


# Create a new thread for each keyword
threads = []

# Start a thread for each keyword
for keyword in keywords:
    thread = Thread(target=get_headers_and_links, args=(keyword,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    print("waiting for threads to finish ")
    thread.join()

print("size of results dictionary", results.__sizeof__())

group = group_urls(results)

dbscript.save_to_db(group)
