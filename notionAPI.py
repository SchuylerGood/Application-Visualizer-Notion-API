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

def application_status_graph(df_applications):
    left = [1,2,3,4]
    height = []
    tick_label = ['Applied', 'Rejected', 'Closed', 'Tech Assessment -> Rejected']

    status_list = df_applications["STATUS"].tolist()
    
    height.append(status_list.count("Applied"))
    height.append(status_list.count("Rejected"))
    height.append(status_list.count("Closed"))
    # height.append(status_list.count("Tech Assessment -> Scheduled"))
    # height.append(status_list.count("Tech Assessment -> Complete"))
    height.append(status_list.count("Tech Assessment -> Rejected"))
    # height.append(status_list.count("Interview 1 -> Scheduled"))
    # height.append(status_list.count("Interview 1 -> Complete"))
    # height.append(status_list.count("Interview 1 -> Rejected"))

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
    plt.title("Application Status Graph")
    
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

# def date_applied_line_graph():
    
#     # Aggregate counts into buckets of months
#     monthly_counts = defaultdict(int)
#     for date_str, count in data.items():
#         date = datetime.strptime(date_str, '%Y-%m-%d')
#         month_year = date.strftime('%Y-%m')
#         monthly_counts[month_year] += count
#     months = list(monthly_counts.keys())[::-1]
#     counts = list(monthly_counts.values())


#     plt.plot(months, counts, marker=',', linestyle='-')

#     # Rotate x-axis labels for better readability
#     plt.xticks(rotation=45, ha='right')

#     # Set labels and title
#     plt.xlabel('Date')
#     plt.ylabel('Count')
#     plt.title(title)

#     # Display the plot
#     plt.tight_layout()
#     plt.show()


def get_row_data(pages, page_num):
        # Iterate over each status tag
        status_list = pages[page_num]["properties"]["STATUS"]["multi_select"]
        new_status_list = []
        for i in status_list:
            new_status_list.append(i["name"])
        status_string = ','.join(str(e) for e in new_status_list)


        # Iterate over each category tag
        category_list = pages[page_num]["properties"]["CATEGORY"]["multi_select"]
        new_category_list = []
        for i in category_list:
            new_category_list.append(i["name"])
        category_string = ','.join(str(e) for e in new_category_list)


        # Iterate over each state tag
        state_list = pages[page_num]["properties"]["STATE"]["multi_select"]
        new_state_list = []
        for i in state_list:
            new_state_list.append(i["name"])
        state_string = ','.join(str(e) for e in new_state_list)

        # Try to access company name
        try:
            company = pages[page_num]["properties"]["COMPANY"]["rich_text"][0]["text"]["content"]
        except IndexError:
            company = ""

        # Try to access title
        try:
            title = pages[page_num]["properties"]["TITLE"]["title"][0]["text"]["content"]
        except IndexError:
            title = ""

        # Try to access City
        try:
            city = pages[page_num]["properties"]["CITY"]["rich_text"][0]["text"]["content"]
        except IndexError:
            city = ""

        # Try to access Type
        try:
            type = pages[page_num]["properties"]["TYPE"]["select"]["name"]
        except KeyError:
            type = ""

        # Try to access Country
        try:
            country = pages[page_num]["properties"]["COUNTRY"]["select"]["name"]
        except KeyError:
            country = ""
            
        # Try to access URL
        try:
            url = pages[page_num]["properties"]["URL"]["url"]
        except KeyError:
            url = ""

        # Define the new row
        new_row = {
            "STATUS":status_string,
            "SIMPLIFY":pages[page_num]["properties"]["SIMPLIFY"]["checkbox"],
            "COMPANY":company,
            "CATEGORY":category_string,
            "TITLE":title,
            "TYPE":type,
            "URL":url,
            "CITY":city,
            "STATE":state_string,
            "COUNTRY":country,
        }
        
        return new_row

def data_to_dataframe(pages):
    applications_datagrame = pd.DataFrame(
        {
            "STATUS":[],
            "SIMPLIFY":[],
            "COMPANY":[],
            "CATEGORY":[],
            "TITLE":[],
            "TYPE":[],
            "URL":[],
            "CITY":[],
            "STATE":[],
            "COUNTRY":[],
        }
    )
    
    # Iterate for every piece of data in the database
    for page_num in range(len(pages)):        
        applications_datagrame.loc[len(applications_datagrame)] = get_row_data(pages, page_num)
        applications_datagrame = applications_datagrame.reset_index(drop=True)

    return applications_datagrame
        
def console_program():
    print("Load Application Data from Spreadsheet? [Y/N]")
    csv_val = input()
    
    if csv_val == "N":
        print("Loading data from API...\n")
        pages = get_pages()
        df_applications = data_to_dataframe(pages)
        print("Data Succesfully loaded from the Notion API!\n")
        df_applications.to_csv('application_data.csv')
        print("Data Saved to csv file\n")
        

    else:
        print("Loading data from previous session...\n")
        df_applications = pd.read_csv('application_data.csv')
    
    exit_flag = 0
    while exit_flag == 0:
        
        print("choose which graph to view:")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("[ 1 ] Date Applied Line Graph")
        print("[ 2 ] application_status_graph")
        print("[ 3 ] Date Applied Line Graph")
        print("[ Q ] Quit the program")
        
        choice = input()
        
        match choice:
            case "1":
                # date_applied_line_graph()
                exit_flag = 0
            case "2":
                application_status_graph(df_applications)
            case "3":
                applied_state_graph('Applications Location - Applied')
            case "Q":
                exit_flag = 1
            case "q":
                exit_flag = 1
            case _:
                print("\nThat option did not work, please try again:\n")

def main():
    console_program()

if __name__ == "__main__":
    main()
    # app.run(port=5328)
