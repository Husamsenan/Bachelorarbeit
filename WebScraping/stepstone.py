import requests
import csv
import time
from bs4 import BeautifulSoup
import json

# Define the base URL and payload template
base_url = "https://www.stepstone.de/public-api/resultlist/unifiedResultlist"
payload_template = {
    "lang": "en",
    "siteId": 250,
    "userData": {
        "isUserLoggedIn": False,
        "candidateId": "",
        "userHashId": "2be9ad08-c3b0-4977-b598-ac3084824fab"
    },
    "isNonEUUser": False,
    "isBotCrawler": False,
    "uiLanguage": "en",
    "fields": [
        "items",
        "pagination",
        "unifiedPagination"
    ]
}

# Define the headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def fetch_page_data(keyword, location, page):
    payload = payload_template.copy()
    payload["url"] = f"https://www.stepstone.de/work/{keyword}/in-{location}?whereType=autosuggest&radius=30&page={page}"
    response = requests.post(base_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def extract_description(job_url):
    response = requests.get(job_url, headers={"User-Agent": headers["User-Agent"]})
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', type='application/ld+json')
    if script_tag:
        ld_json = json.loads(script_tag.string)
        return ld_json.get('description', '')
    return ''

def extract_data(item, keyword, location):
    job_url = f"https://www.stepstone.de{item['url']}"
    description = extract_description(job_url)
    return {
        'search_keyword': keyword,
        'search_location': location,
        'company_name': item['companyName'],
        'date_posted': item['datePosted'],
        'job_location': item['location'],
        'title': item['title'],
        'job_url': job_url,
        'description': description
    }

def fetch_all_data(keywords_list, locations_list):
    all_data = []
    for keyword in keywords_list:
        for location in locations_list:
            print(f"Fetching data for '{keyword}' in '{location}'...")
            # Fetch data from the first page to determine the total number of pages
            initial_data = fetch_page_data(keyword, location, 1)
            total_pages = initial_data['pagination']['pageCount']
            
            for page in range(1, total_pages + 1):
                print(f"    Fetching page {page}...")
                page_data = fetch_page_data(keyword, location, page)
                items = page_data.get('items', [])
                
                for item in items:
                    all_data.append(extract_data(item, keyword, location))
                
                # Delay to avoid making too many requests in a short period
                time.sleep(1)
    
    return all_data

# Define your search keywords and locations as lists
search_keywords = [
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Research Scientist",
    "Data Engineer",
    "AI Engineer",
    "Deep Learning Engineer",
    "AI Product Manager",
    "AI Ethicist",
    "Algorithm Engineer",
    "AI Consultant",
    "AI Solution Architect",
    "Business Intelligence Developer",
    "AI Sentiment Analysis Specialist"
]

search_locations = [
    "Berlin",
    "Hamburg",
    "München",
    "Köln",
    "Frankfurt",
    "Stuttgart",
    "Düsseldorf",
    "Dortmund",
    "Essen",
    "Leipzig",
    "Bremen",
    "Dresden",
    "Hannover",
    "Nürnberg",
    "Duisburg"
]

# Fetch all data
job_data = fetch_all_data(search_keywords, search_locations)

# Open a CSV file for writing
with open('stepstone_jobs_final.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['search_keyword', 'search_location', 'company_name', 'date_posted', 'job_location', 'title', 'job_url', 'description'])
    writer.writeheader()
    
    for job in job_data:
        writer.writerow(job)

print("Data extraction complete. Check the stepstone_jobs_final.csv file.")
