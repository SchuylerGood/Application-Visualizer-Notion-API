import requests
import matplotlib.pyplot as plt
from datetime import datetime
import os
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13",  # Adjust version if needed
}

def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=HEADERS)

    data = response.json()
    
    if "results" not in data:
        print("Error: No 'results' key found in the response JSON.")
        print("Response JSON:", data)
        return []

    results = data["results"]
    while data.get("has_more") and get_all:
        payload = {"page_size": page_size, "start_cursor": data.get("next_cursor")}
        response = requests.post(url, json=payload, headers=HEADERS)
        data = response.json()
        if "results" in data:
            results.extend(data["results"])

    return results

def get_graph_data(pages):
    data = []
    for page in pages:
        props = page["properties"]
        data.append(props.get('STATUS',{}).get('select',{}).get('name',{}))

    return data

def main():
    pages = get_pages()
    data = get_graph_data(pages)
    left = [1, 2, 3, 4]
    height = []
    tick_label = ['Applied', 'Rejected', 'Closed', 'Tech Assessment -> Rejected']


    height.append(data.count("Applied"))
    height.append(data.count("Rejected"))
    height.append(data.count("Closed"))
    height.append(data.count("Tech Assessment -> Rejected"))

    plt.bar(
        left, 
        height, 
        tick_label = tick_label,
        width = 0.8, 
        color = ['red', 'green']
    )
    # naming the x-axis
    plt.xlabel('Status')
    # naming the y-axis
    plt.ylabel('Number')
    # plot title
    plt.title('My bar chart!')
    
    # function to show the plot
    plt.show()
        

if __name__ == "__main__":
    main()
