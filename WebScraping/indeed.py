from apify_client import ApifyClient
import csv
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_oVYa7W8ZTmcSDgwXqC5Vspn2Y4LQwr3hmIcX")

# Prepare the Actor input
def prepare_run_input(position, location):
    return {
        "position": position,
        "country": "DE",
        "location": location,
        "maxItems": 5000,
        "parseCompanyDetails": False,
        "saveOnlyUniqueItems": True,
        "followApplyRedirects": True,
        "maxConcurrency": 20,
    }

# Run the Actor and wait for it to finish
def run_actor(position, location):
    run_input = prepare_run_input(position, location)
    logging.info(f"Starting actor for position '{position}' in '{location}'")
    run = client.actor("hMvNSpz3JnHgl5jkh").call(run_input=run_input)
    return run

# Fetch and process results
def fetch_results(run, position, location):
    dataset_id = run["defaultDatasetId"]
    job_data = []
    
    for item in client.dataset(dataset_id).iterate_items():
        job_entry = {
            'search_keyword': position,
            'search_location': location,
            'company_name': item.get('company', ''),
            'date_posted': item.get('postingDateParsed', ''),
            'job_location': item.get('location', ''),
            'title': item.get('positionName', ''),
            'job_url': item.get('url', ''),
            'description': item.get('descriptionHTML', '')
        }
        job_data.append(job_entry)
    
    return job_data

# Main function to run the script
def main(keywords, locations):
    all_job_data = []

    for keyword in keywords:
        for location in locations:
            run = run_actor(keyword, location)
            job_data = fetch_results(run, keyword, location)
            all_job_data.extend(job_data)
            logging.info(f"Fetched {len(job_data)} jobs for keyword '{keyword}' in '{location}'")

    # Save data to CSV
    csv_file_name = 'indeed_jobs_final.csv'
    fieldnames = ['search_keyword', 'search_location', 'company_name', 'date_posted', 'job_location', 'title', 'job_url', 'description']

    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for job in all_job_data:
            writer.writerow(job)
    
    logging.info(f"Data extraction complete. Check the {csv_file_name} file.")

# Define your search keywords and locations as lists
search_keywords = [
    "Machine Learning Engineer",
    "Data Scientist",
    "AI Product Manager",
    "Robotics Engineer",
    "Reinforcement Learning Specialist",
    "Computer Vision Engineer",
    "AI Architect",
    "Natural Language Processing (NLP) Engineer",
    "Deep Learning Engineer",
    "AI Research Scientist",
    "AI Engineer",
    "Data Engineer",
    "AI Product Owner",
    "AI Technical Lead",
    "AI Program Manager",
    "AI Development Lead",
    "AI Implementation Specialist",
    "AI Platform Engineer",
    "AI Strategy Consultant",
    "AI Solutions Engineer",
    "AI Systems Engineer",
    "AI Quality Assurance Engineer",
    "AI Policy Advisor",
    "AI Trainer",
    "Director of AI",
    "Head of AI",
    "Postdoctoral Researcher",
    "Research Fellow",
    "AI Researcher (Academic)",
    "AI Professor",
    "AI Operations Specialist",
    "AI Infrastructure Engineer",
    "Big Data Engineer",
    "Data Analyst",
    "AI Software Developer",
    "AI Consultant",
    "Business Intelligence Developer",
    "AI Solution Architect",
    "Algorithm Engineer"
]

search_locations = [
    "Berlin",
    "München",
    "Dresden",
    "Hannover",
    "Nürnberg",
    "Leipzig",
    "Essen",
    "Düsseldorf",
    "Köln",
    "Bremen",
    "Stuttgart",
    "Dortmund",
    "Hamburg",
    "Duisburg",
    "Frankfurt"
]

# Run the main function
if __name__ == "__main__":
    main(search_keywords, search_locations)
