import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
from collections import defaultdict
from datetime import datetime
import os
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def retrieve_data():
    pages = get_pages()
    status_data = get_status_data(pages)
    print(status_data)
    return '{"results":"'+str(status_data)+'"}'



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
        if props.get('STATUS',{}).get('select',{}).get('name',{}) == "Applied" or props.get('STATUS',{}).get('select',{}).get('name',{}) == "Rejected":
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

def graph1(title, data):
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
    plt.title(title)
    
    # function to show the plot
    plt.show()

def applied_state_graph(title, data):

    # Aggregate counts into buckets of months
    state_data = dict(Counter(data))

    # Sort the dictionary by values
    sorted_dict = sorted(state_data.items(), key=lambda x: x[1], reverse=True) 
    
    # Extract the state names and counts into their own lists
    height = [i[1] for i in sorted_dict]
    tick_labels = [i[0] for i in sorted_dict]

    # Create the bar chart values
    x_values = range(len(state_data))

    # Create the bar chart
    plt.bar(
        x = x_values,
        height = height, 
        tick_label = tick_labels,
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
    plt.xticks(x_values, tick_labels, rotation=45, ha='right')  # Rotate the labels for better readability

    # function to show the plot
    plt.show()

def get_dates(pages):
    dates = []
    for page in pages:
        dates.append(page["created_time"].split("T")[0])
    return dict(Counter(dates))

def added_to_notion_graph(title, data):
    # Aggregate counts into buckets of months
    monthly_counts = defaultdict(int)
    for date_str, count in data.items():
        date = datetime.strptime(date_str, '%Y-%m-%d')
        month_year = date.strftime('%Y-%m')
        monthly_counts[month_year] += count
    months = list(monthly_counts.keys())[::-1]
    counts = list(monthly_counts.values())


    plt.plot(months, counts, marker=',', linestyle='-')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Set labels and title
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title(title)

    # Display the plot
    plt.tight_layout()
    plt.show()

def main():
    # Gets the data in the form of pages
    pages = get_pages()
    
    # dates_data = get_dates(pages)
    # added_to_notion_graph("Dates applied", dates_data)
    
    status_data = get_status_data(pages)
    print(status_data)
    # graph1('Applications Status Overview',status_data)

    # location_data = get_state_data_applied(pages)
    # applied_state_graph('Applications Location - Applied', location_data)


if __name__ == "__main__":
    # main()
    app.run(port=5328)
