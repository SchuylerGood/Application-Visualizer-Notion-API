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
import plotly.graph_objects as go

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

app = Flask(__name__)
CORS(app)

# @app.route('/', methods=['GET'])
# def retrieve_data():
#     pages = get_pages()
#     status_data = get_status_data(pages)
#     print(status_data)
#     return '{"results":"'+str(status_data)+'"}'

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
    left = [1,2,3,4,5]
    height = []
    tick_label = ['Added', 'Applied', 'Rejected', 'Closed', 'Coffee Chat']
    status_list = df_applications["STATUS"].tolist()

    need_to_apply = 0
    applied = 0
    rejected = 0
    closed = 0
    coffee_chat = 0

    for i in range(len(status_list)):
        try:
            val = status_list[i]
            if "Need to Apply" in val:
                need_to_apply += 1
            if "Applied" in val:
                applied += 1
            if "Rejected" in val:
                rejected += 1
            if "Closed" in val:
                closed += 1
            if "Coffee Chat" in val:
                coffee_chat += 1
        except:
            continue
    
    height.append(need_to_apply)
    height.append(applied)
    height.append(rejected)
    height.append(closed)
    height.append(coffee_chat)

    plt.bar(
        left, 
        height, 
        tick_label = tick_label,
        width = 0.8, 
        color = ['blue', 'green', 'red', 'orange', 'purple'],
    )

    for i, v in enumerate(height):
        plt.text(left[i], v + 0.1, str(v), ha='center', va='bottom')


    # naming the x-axis
    plt.xlabel('Job Application Status')
    # naming the y-axis
    plt.ylabel('Number')
    # plot title
    plt.title("Application Status Graph")
    
    # function to show the plot
    plt.show()

def applied_state_graph(df_applications):
    applied_df = df_applications[df_applications['STATUS'] == 'Applied']

    # Apply the function to each row and stack the resulting Series
    stacked_states = applied_df.apply(split_and_count_states, axis=1).stack()

    state_counts = stacked_states.value_counts()  # Count the occurrences of each state
    total_states = state_counts.shape[0]  # Get the number of unique states
    tick_labels = state_counts.index  # Get tick labels (state names)
    x_values = range(total_states)  # Create the range for x-axis

    # Create the bar chart
    plt.bar(
        x=x_values,
        height=state_counts.values,
        tick_label=tick_labels,
        width=0.8,
        color=['blue', 'red', 'orange', 'yellow']  # Adjust colors as needed
    )
    
    plt.xlabel('State')
    plt.ylabel('Number')
    plt.title("Applied State Graph")
    plt.xticks(x_values, tick_labels, rotation=45, ha='right')  # Rotate the labels for better readability
    plt.show()


def date_applied_line_graph(df_applications):
    df_applications['TIME_CREATED'] = pd.to_datetime(df_applications['TIME_CREATED'])
    df_applications.set_index('TIME_CREATED', inplace=True)

    # Resample the data to a weekly frequency and count the data points for each week
    weekly_counts = df_applications.resample('W').count()

    plt.plot(
        weekly_counts.index, 
        weekly_counts['URL'].values, 
        marker=',', 
        linestyle='-'
    )

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Set labels and title
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title("Date Applied Line Graph")

    # Display the plot
    plt.tight_layout()
    plt.show()

def sanky_graph(df):
    # Step 1: Identify all unique status values
    unique_statuses = set(['Need to Apply','Applied','Closed','Rejected','Coffee Chat','Tech Assessment -> Complete','Interview 1 -> Complete','Interview 2 -> Complete','Interview 3 -> Complete','Referral'])

    # Step 2: Create new columns for each unique status
    for status in unique_statuses:
        df[status.strip()] = False

    # Step 3: Check if each status is present in the 'STATUS' column for each row
    for index, row in df.iterrows():
        if isinstance(row['STATUS'], str):
            for status in row['STATUS'].split(','):
                df.at[index, status.strip()] = True

    # Step 4: Count the number of occurrences of each status and store in a dictionary
    status_counts = {}
    for status in unique_statuses:
        status_counts[status.strip()] = df[status.strip()].sum()

    # =-=-=-=-=-=-=-=-= Counting Values =-=-=-=-=-=-=-=-=

    # All apps that needed to apply and added to database
    need_to_apply = ((df['Need to Apply'] == True)).sum()

    # All apps that had a coffee chat
    coffee_chat = ((df['Coffee Chat'] == True)).sum()

    # All apps that were needed to apply and then closed
    closed = ((df['Need to Apply'] == True) & (df['Closed'] == True)).sum()

    # All apps 
    cold_applied = ((df['Need to Apply'] == True) & (df['Closed'] == True)).sum()

    # All apps that were Closed
    rejected = ((df['Need to Apply'] == True) & (df['Closed'] == True)).sum()

    # All apps that had compete Tech Assessments
    tech_assessment = ((df['Need to Apply'] == True) & (df['Closed'] == True)).sum()

    # All apps that completed an interview
    interview_1 = ((df['Interview 1 -> Complete'] == True)).sum()

    # All apps that completed a second interview
    interview_2 = ((df['Interview 2 -> Complete'] == True)).sum()

    # All apps that completed a third interview
    interview_3 = ((df['Interview 3 -> Complete'] == True)).sum()

    # All apps that were rejected
    coffee_chat_referral = ((df['Coffee Chat'] == True) & (df['Referral'] == True)).sum()        
    
    referral_applied = ((df['Referral'] == True) & (df['Applied'] == True)).sum()
    
    print(status_counts)
    print(df.columns)
    print("BOTH:",cold_applied)

    fig = go.Figure(data=[go.Sankey(
    node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = [
            "Need to Apply: ("+str(need_to_apply)+")", # 0
            "Coffee Chat: ("+str(coffee_chat)+")", # 1
            "Closed: ("+str(closed)+")", # 2
            "Applied: ("+str(cold_applied)+")", # 3
            "Rejected: ("+str(rejected)+")", # 4
            "Tech Assessment: ("+str(tech_assessment)+")", # 5
            "First Round Interview: ("+str(interview_1)+")", # 6
            "Second Round Interview: ("+str(interview_2)+")", # 7
            "Third Round Interview: ("+str(interview_3)+")", # 8
            "Referral: ("+str(coffee_chat_referral)+")", # 9
            "Applied with Refferal: ("+str(referral_applied)+")", # 10
        ],
        color = "red"
    ),
    
    link = dict(
        source = [0, 0, 1, 9, 3], # indices correspond to labels, eg A1, A2, A1, B1, ...
        target = [3, 2, 9, 10, 4],
        value = [cold_applied, closed, coffee_chat_referral, referral_applied, rejected]
    ))])

    fig.update_layout(title_text="Applications", font_size=22)
    fig.show()

def split_and_count_states(row):
    try:
        states = row['STATE'].split(', ')  # Split the string by comma and space
    except:
        states = None
    return pd.Series(states)

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
            "TIME_CREATED":pages[page_num]["created_time"].split("T")[0]
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
            "TIME_CREATED":[],
        }
    )
    
    # Iterate for every piece of data in the database
    for page_num in range(len(pages)):        
        applications_datagrame.loc[len(applications_datagrame)] = get_row_data(pages, page_num)
        applications_datagrame = applications_datagrame.reset_index(drop=True)

    return applications_datagrame
        
def cli_program():
    
    continue_flag = 0
    while continue_flag == 0:
        print("Load Application Data from Spreadsheet? [Y/N]")
        csv_val = input()
        if csv_val == "N" or csv_val == "n":
            print("Loading data from API...\n")
            pages = get_pages()
            df_applications = data_to_dataframe(pages)
            print("Data Succesfully loaded from the Notion API!\n")
            df_applications.to_csv('application_data.csv')
            print("Data Saved to csv file\n")
            continue_flag = 1
        elif csv_val == "Y" or csv_val == "y":
            print("Loading data from previous session...\n")
            df_applications = pd.read_csv('application_data.csv')
            continue_flag = 1
        else:
            print("\nThat option did not work, please try again:\n")
            continue_flag = 0
    
    exit_flag = 0
    while exit_flag == 0:
        
        print("choose which graph to view:")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("[ 1 ] Date Applied Line Graph")
        print("[ 2 ] Jobs Applied by Status")
        print("[ 3 ] Jobs Applied by State")
        print("[ 4 ] Sanky Graph")
        print("[ Q ] Quit the program")
        
        choice = input()
        
        match choice:
            case "1":
                date_applied_line_graph(df_applications)
            case "2":
                application_status_graph(df_applications)
            case "3":
                applied_state_graph(df_applications)
            case "4":
                sanky_graph(df_applications)
            case "Q":
                exit_flag = 1
            case "q":
                exit_flag = 1
            case _:
                print("\nThat option did not work, please try again:\n")

def testing():
    # TESTING ONLY
    # pages = get_pages()
    df_applications = pd.read_csv('application_data.csv')
    # applied_state_graph(df_applications)
    # date_applied_line_graph(df_applications)
    sanky_graph(df_applications)
    # application_status_graph(df_applications)
    # print(df.head(100))

    
    # rejected_count = (df['STATUS'] == 'Rejected').sum()
    
    # print("Total 'Applied' count:", applied_count)


def main():
    # cli_program()
    testing()
    

if __name__ == "__main__":
    main()
    # app.run(port=5328)
