import requests
import matplotlib.pyplot as plt
from collections import Counter
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

def get_status_data(pages):
    data = []
    for page in pages:
        props = page["properties"]
        data.append(props.get('STATUS',{}).get('select',{}).get('name',{}))

    return data

def get_state_data_applied(pages):
    data = []
    for page in pages:
        props = page["properties"]
        if props.get('STATUS',{}).get('select',{}).get('name',{}) == "Applied":
            cur_row = props.get('STATE',{}).get('multi_select',{})
            for i in range(len(cur_row)):
                data.append(cur_row[i].get('name'))

    return data

def get_state_data_completed(pages):
    data = []
    acceptable_status = ["Applied", "Rejected"]
    for page in pages:
        props = page["properties"]
        if props.get('STATUS',{}).get('select',{}).get('name',{}) in acceptable_status:
            cur_row = props.get('STATE',{}).get('multi_select',{})
            for i in range(len(cur_row)):
                data.append(cur_row[i].get('name'))

    return data

def graph1(data):
    left = [1,2,3,4]
    height = []
    tick_label = ['Applied', 'Rejected', 'Closed', 'Tech Assessment -> Rejected']


    height.append(data.count("Applied"))
    height.append(data.count("Rejected"))
    height.append(data.count("Closed"))
    # height.append(data.count("Tech Assessment -> Scheduled"))
    # height.append(data.count("Tech Assessment -> Complete"))
    height.append(data.count("Tech Assessment -> Rejected"))
    # height.append(data.count("Interview 1 -> Scheduled"))
    # height.append(data.count("Interview 1 -> Complete"))
    # height.append(data.count("Interview 1 -> Rejected"))

    plt.bar(
        left, 
        height, 
        tick_label = tick_label,
        width = 0.8, 
        color = ['blue', 'red', 'orange', 'yellow']
    )
    # naming the x-axis
    plt.xlabel('Status')
    # naming the y-axis
    plt.ylabel('Number')
    # plot title
    plt.title('Applications overview')
    
    # function to show the plot
    plt.show()

def applied_state_graph(title, data):
    state_data = dict(Counter(data))
    x_values = range(len(state_data))

    plt.bar(
        x = x_values,
        height = list(state_data.values()), 
        tick_label = list(state_data.keys()),
        width = 0.8, 
        color = ['blue', 'red', 'orange', 'yellow']
    )
    # naming the x-axis
    plt.xlabel('State')
    # naming the y-axis
    plt.ylabel('Number')
    # plot title
    plt.title(title)
    
    # Adjust labels
    plt.xticks(x_values, state_data.keys(), rotation=45, ha='right')  # Rotate the labels for better readability

    # function to show the plot
    plt.show()

def main():
    pages = get_pages()
    # status_data = get_status_data(pages)
    # graph1(status_data)

    # location_data = get_state_data_applied(pages)
    # applied_state_graph('Applications Location - Applied', location_data)

    location_data = get_state_data_completed(pages)
    applied_state_graph('Applications Location - Applied + Rejected', location_data)


if __name__ == "__main__":
    main()
