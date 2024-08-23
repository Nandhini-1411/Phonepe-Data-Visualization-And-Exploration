# import needed libraries
import os
import json
import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px
#Aggregated User
@st.cache_data(show_spinner=False)
def agg_user_data(path):
    agg_State_list = os.listdir(path)
    colm = {'State': [], 'Year': [], 'Quarter': [], 'Total_Registered_Users': [], 'Total_App_Opens': [], 'Device_Brand': [], 'Reg_User_Count_By_Brand': [], 'Percentage_of_Brand': []}
    for i in agg_State_list:
        p_i = os.path.join(path, i) 
        agg_yr = os.listdir(p_i) 
        for j in agg_yr:
            p_j = os.path.join(p_i, j) 
            agg_yr_list = os.listdir(p_j) 
            for k in agg_yr_list:
                p_k = os.path.join(p_j, k) 
                with open(p_k, 'r') as Data:
                    D = json.load(Data) 
                    aggregated = D.get('data', {}).get('aggregated', {})
                    Total_Registered_Users = aggregated.get('registeredUsers')
                    Total_App_Opens = aggregated.get('appOpens')
                    users_by_device = D.get('data', {}).get('usersByDevice', [])
                    if users_by_device: 
                        for device in users_by_device: 
                            Device_Brand = device.get('brand')
                            Reg_User_Count_By_Brand = device.get('count')
                            Percentage_of_Brand = device.get('percentage')
                            colm['Device_Brand'].append(Device_Brand)
                            colm['Reg_User_Count_By_Brand'].append(Reg_User_Count_By_Brand)
                            colm['Percentage_of_Brand'].append(Percentage_of_Brand)
                            colm['Total_Registered_Users'].append(Total_Registered_Users)
                            colm['Total_App_Opens'].append(Total_App_Opens)
                            colm['State'].append(i)
                            colm['Year'].append(int(j))
                            colm['Quarter'].append(int(k.strip('.json')))
                    else :
                        colm['Device_Brand'].append(None)
                        colm['Reg_User_Count_By_Brand'].append(None)
                        colm['Percentage_of_Brand'].append(None)
                        colm['Total_Registered_Users'].append(Total_Registered_Users)
                        colm['Total_App_Opens'].append(Total_App_Opens)
                        colm['State'].append(i)
                        colm['Year'].append(int(j))
                        colm['Quarter'].append(int(k.strip('.json')))
    Agg_Users = pd.DataFrame(colm)
    Agg_Users = Agg_Users.fillna({'Device_Brand': 'Unknown','Reg_User_Count_By_Brand': 0,'Percentage_of_Brand': 0.0})
    conn = create_connection()
    cursor = conn.cursor()  
    aggregated_user_table = '''CREATE TABLE IF NOT EXISTS agg_user (
                                State VARCHAR(50),
                                Year VARCHAR(5),
                                Quarter INT,
                                Total_Registered_Users INTEGER,
                                Total_App_Opens INTEGER,
                                Device_Brand VARCHAR(50) NULL,
                                Percentage_of_Brand DECIMAL(5,2),
                                Reg_User_Count_By_Brand INTEGER,
                                UNIQUE (State, Year, Quarter,Device_Brand,Total_Registered_Users, Total_App_Opens,Reg_User_Count_By_Brand, Percentage_of_Brand))'''
    cursor.execute(aggregated_user_table)
    insert_query1 = '''INSERT OR IGNORE INTO  agg_user (State, Year, Quarter, Total_Registered_Users, Total_App_Opens, Device_Brand, Reg_User_Count_By_Brand, Percentage_of_Brand)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    for index, row in Agg_Users.iterrows():
        values = (row['State'],row['Year'],row['Quarter'],row['Total_Registered_Users'],row['Total_App_Opens'],row['Device_Brand'],row['Reg_User_Count_By_Brand'],row['Percentage_of_Brand'])
        cursor.execute(insert_query1, values)
    conn.commit()
    return Agg_Users   
#Aggregated Transaction
@st.cache_data(show_spinner=False)
def agg_transaction_data(path):
    agg_State_list = os.listdir(path)
    colm = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_Type': [], 'Transaction_Count': [], 'Transaction_Amount': []}
    for i in agg_State_list:
        p_i = os.path.join(path, i)
        agg_yr = os.listdir(p_i)
        for j in agg_yr:
            p_j = os.path.join(p_i, j)
            agg_yr_list = os.listdir(p_j)
            for k in agg_yr_list:
                p_k = os.path.join(p_j, k)
                with open(p_k, 'r') as Data:
                    D = json.load(Data)
                    for x in D.get('data', {}).get('transactionData', []):
                        Name = x.get('name')
                        Count = x.get('paymentInstruments', [])[0].get('count')
                        Amount = x.get('paymentInstruments', [])[0].get('amount')
                        colm['Transaction_Type'].append(Name)
                        colm['Transaction_Count'].append(Count)
                        colm['Transaction_Amount'].append(Amount)
                        colm['State'].append(i)
                        colm['Year'].append(int(j))
                        colm['Quarter'].append(int(k.strip('.json')))
    Agg_Trans = pd.DataFrame(colm)
    conn = create_connection()
    cursor = conn.cursor()
    aggregated_transaction_table = '''CREATE TABLE IF NOT EXISTS aggregated_transaction (
        State VARCHAR(50),
        Year VARCHAR(5),
        Quarter INT,
        Transaction_Type VARCHAR(50),
        Transaction_Count INTEGER,
        Transaction_Amount INTEGER,
        UNIQUE (State, Year, Quarter,Transaction_Type, Transaction_Count, Transaction_Amount))'''
    cursor.execute(aggregated_transaction_table)
    insert_query2 = '''INSERT OR IGNORE INTO aggregated_transaction (State, Year, Quarter, Transaction_Type, Transaction_Count, Transaction_Amount)
    VALUES (?, ?, ?, ?, ?, ?)'''
    for index, row in Agg_Trans.iterrows():
        values = (row['State'],row['Year'],row['Quarter'],row['Transaction_Type'],row['Transaction_Count'],row['Transaction_Amount'])
        cursor.execute(insert_query2, values)
    conn.commit()
    return Agg_Trans
#Aggregated Insurance
@st.cache_data(show_spinner=False)
def agg_ins_data(path):
    agg_State_list = os.listdir(path)
    colm = {'State': [], 'Year': [], 'Quarter': [], 'Total_Count': [], 'Total_Amount': []}
    for i in agg_State_list:
        p_i = os.path.join(path, i)
        agg_yr = os.listdir(p_i)
        for j in agg_yr:
            p_j = os.path.join(p_i, j)
            agg_yr_list = os.listdir(p_j)
            for k in agg_yr_list:
                p_k = os.path.join(p_j, k)
                with open(p_k, 'r') as Data:
                    D = json.load(Data)
                    transactionData = D.get('data', {}).get('transactionData', [])   
                    for item in transactionData:
                        Total_Count = item.get('paymentInstruments', [{}])[0].get('count')
                        Total_Amount = item.get('paymentInstruments', [{}])[0].get('amount')
                        colm['Total_Count'].append(Total_Count)
                        colm['Total_Amount'].append(Total_Amount)
                        colm['State'].append(i)
                        colm['Year'].append(int(j.strip(',')))
                        colm['Quarter'].append(int(k.strip('.json')))
    Agg_Ins = pd.DataFrame(colm)
    conn = create_connection()
    cursor = conn.cursor()
    aggregate_insurance_table = '''CREATE TABLE IF NOT EXISTS aggregated_insurance(
        State VARCHAR(50),
        Year VARCHAR(5),
        Quarter INT,
        Total_Count INTEGER,
        Total_Amount INTEGER,
        UNIQUE (State, Year, Quarter, Total_Count, Total_Amount))'''
    cursor.execute(aggregate_insurance_table)
    insert_query4 = '''INSERT OR IGNORE INTO aggregated_insurance (State, Year, Quarter, Total_Count, Total_Amount)
    VALUES (?, ?, ?, ?,?)'''
    for index, row in Agg_Ins.iterrows():
        values = (row['State'],row['Year'],row['Quarter'],row['Total_Count'],row['Total_Amount'])
        cursor.execute(insert_query4, values)
    conn.commit()
    return Agg_Ins
#Map Users
@st.cache_data(show_spinner=False)
def map_user_data(path):
    agg_State_list = os.listdir(path)
    colm = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Total_Registered_users': [], 'Total_App_Opens': []}
    for i in agg_State_list:
        p_i = os.path.join(path, i)
        agg_yr = os.listdir(p_i)
        for j in agg_yr:
            p_j = os.path.join(p_i, j)
            agg_yr_list = os.listdir(p_j)
            for k in agg_yr_list:
                p_k = os.path.join(p_j, k)
                with open(p_k, 'r') as Data:
                    D = json.load(Data)
                    hoverDataList = D.get('data', {}).get('hoverData', {})   
                    for district, data in hoverDataList.items():
                        Total_Registered_users = data.get('registeredUsers')
                        Total_App_Opens = data.get('appOpens')
                        colm['State'].append(i)
                        colm['Year'].append(int(j))
                        colm['Quarter'].append(int(k.strip('.json')))
                        colm['District'].append(district)
                        colm['Total_Registered_users'].append(Total_Registered_users)
                        colm['Total_App_Opens'].append(Total_App_Opens)
        Map_Users = pd.DataFrame(colm)     
    conn = create_connection()
    cursor = conn.cursor()
    map_user_table = '''CREATE TABLE IF NOT EXISTS map_user (
        State VARCHAR(50),
        Year VARCHAR(5),
        Quarter INT,
        District VARCHAR(50),
        Total_Registered_User INTEGER,
        Total_App_Opens INTEGER,
        UNIQUE (State, Year, Quarter, District, Total_Registered_User, Total_App_Opens))'''
    cursor.execute(map_user_table)
    insert_query3 = '''INSERT OR IGNORE INTO map_user (State, Year, Quarter, District, Total_Registered_User, Total_App_Opens)
    VALUES (?, ?, ?, ?, ?,?)'''
    for index, row in Map_Users.iterrows():
        values = (row['State'],row['Year'],row['Quarter'],row['District'],row['Total_Registered_users'],row['Total_App_Opens'])
        cursor.execute(insert_query3, values)
    conn.commit()
    return Map_Users
#Map Transaction
@st.cache_data(show_spinner=False)
def map_transaction_data(path):
    agg_State_list = os.listdir(path)
    colm = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_Count': [], 'Total_Transaction_Amount': []}
    for i in agg_State_list:
        p_i = os.path.join(path, i)
        agg_yr = os.listdir(p_i)
        for j in agg_yr:
            p_j = os.path.join(p_i, j)
            agg_yr_list = os.listdir(p_j)
            for k in agg_yr_list:
                p_k = os.path.join(p_j, k)
                with open(p_k, 'r') as Data:
                    D = json.load(Data)
                    hoverDataList = D.get('data', {}).get('hoverDataList', [])   
                    for item in hoverDataList:
                        District = item.get('name')
                        Transaction_Count = item.get('metric', [{}])[0].get('count')
                        Total_Transaction_Amount = item.get('metric', [{}])[0].get('amount')
                        colm['District'].append(District)
                        colm['Transaction_Count'].append(Transaction_Count)
                        colm['Total_Transaction_Amount'].append(Total_Transaction_Amount)
                        colm['State'].append(i)
                        colm['Year'].append(int(j))
                        colm['Quarter'].append(int(k.strip('.json')))
    Map_Trans= pd.DataFrame(colm)
    conn = create_connection()
    cursor = conn.cursor()
    map_transaction_table = '''CREATE TABLE IF NOT EXISTS map_transaction (
        State VARCHAR(50),
        Year VARCHAR(5),
        Quarter INT,
        District VARCHAR(50),
        Transaction_Count INTEGER,
        Total_Transaction_Amount INTEGER,
        UNIQUE (State, Year, Quarter, District, Transaction_Count, Total_Transaction_Amount))'''
    cursor.execute(map_transaction_table)
    insert_query4 = '''INSERT OR IGNORE INTO map_transaction (State, Year, Quarter, District, Transaction_Count, Total_Transaction_Amount)
    VALUES (?, ?, ?, ?, ?,?)'''
    for index, row in Map_Trans.iterrows():
        values = (row['State'],row['Year'],row['Quarter'],row['District'],row['Transaction_Count'],row['Total_Transaction_Amount'])
        cursor.execute(insert_query4, values)
    conn.commit()
    return Map_Trans
#Map Insurance
@st.cache_data(show_spinner=False)
def map_ins_data(path):
    agg_State_list = os.listdir(path)
    colm = {'State': [], 'Year': [], 'Quarter': [],'District': [], 'Total_Count': [], 'Total_Amount': []}
    for State_folder in agg_State_list:
        State_path = os.path.join(path, State_folder)
        years_list = os.listdir(State_path)
        for year_folder in years_list:
            year_path = os.path.join(State_path, year_folder)
            quarter_files = os.listdir(year_path)
            for quarter_file in quarter_files:
                quarter_path = os.path.join(year_path, quarter_file)
                with open(quarter_path, 'r') as data_file:
                    data = json.load(data_file)
                    hoverDataList = data.get('data', {}).get('hoverDataList', [{}])
                    for item in hoverDataList:
                        District = item.get('name')
                        total_count=item.get('metric',[{}])[0].get('count')
                        total_amount = item.get('metric',[{}])[0].get('amount')
                        colm["District"].append(District)
                        colm['Total_Count'].append(total_count)
                        colm['Total_Amount'].append(total_amount)
                        colm['State'].append(State_folder)
                        colm['Year'].append(int(year_folder))
                        colm['Quarter'].append(int(quarter_file.strip('.json')))
    Map_Ins = pd.DataFrame(colm)
    conn = create_connection()
    cursor = conn.cursor()
    map_insurance_table = '''CREATE TABLE IF NOT EXISTS map_insurance (
            State VARCHAR(50),
            Year VARCHAR(5),
            Quarter INT,
            District VARCHAR(100),
            Total_Count INTEGER,
            Total_Amount INTEGER,
            UNIQUE (State, Year, Quarter, District, Total_Count, Total_Amount))'''
    cursor.execute(map_insurance_table)
    insert_query = '''INSERT OR IGNORE INTO map_insurance (State, Year, Quarter,District, Total_Count, Total_Amount)
    VALUES (?, ?, ?, ?, ?,?)'''
    for index, row in Map_Ins.iterrows():
        values = (row['State'],row['Year'],row['Quarter'],row["District"],row['Total_Count'],row['Total_Amount'])
        cursor.execute(insert_query, values)
    conn.commit()
    return Map_Ins
#Top User District Wise
@st.cache_data(show_spinner=False)
def top_user_district_data(path):
    agg_State_list = os.listdir(path)
    colm = {'State': [],'Year': [],'Quarter': [],'Registered_Users': [],'District': []}
    for State_folder in agg_State_list:
        State_path = os.path.join(path, State_folder)
        years_list = os.listdir(State_path)
        for year_folder in years_list:
            year_path = os.path.join(State_path, year_folder)
            quarter_files = os.listdir(year_path)
            for quarter_file in quarter_files:
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for district_data in data['data']['districts']:
                        district_name = district_data['name']
                        registered_users = district_data['registeredUsers']
                        colm['State'].append(State_folder)
                        colm['Year'].append(year_folder)
                        colm['Quarter'].append(int(quarter_file.strip('.json')))
                        colm['Registered_Users'].append(registered_users)
                        colm['District'].append(district_name) 
    Top_User_District = pd.DataFrame(colm)
    conn = create_connection()
    cursor = conn.cursor()
    top_user_table = '''CREATE TABLE IF NOT EXISTS top_user (
                        State VARCHAR(50),
                        Year VARCHAR(5),
                        Quarter INT,
                        District VARCHAR(50),
                        RegisteredUser INTEGER,
                        UNIQUE (State, Year, Quarter, District, RegisteredUser))'''
    cursor.execute(top_user_table)
    insert_query = '''INSERT OR IGNORE INTO top_user (State, Year, Quarter, District, RegisteredUser)
                        VALUES (?, ?, ?, ?,?)'''
    for index, row in Top_User_District.iterrows():
        values = (row['State'],row['Year'],row['Quarter'],row['District'],row['Registered_Users'])
        cursor.execute(insert_query, values)
    conn.commit()
    return Top_User_District
#Top Transaction District Wise
@st.cache_data(show_spinner=False)
def top_transaction_district_data(path):
    agg_State_list = os.listdir(path)
    colm = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Total_Transaction_Count': [], 'Total_Transaction_Amount': []}
    for State_folder in agg_State_list:
        State_path = os.path.join(path, State_folder)
        years_list = os.listdir(State_path)
        for year_folder in years_list:
            year_path = os.path.join(State_path, year_folder)
            quarter_files = os.listdir(year_path)
            for quarter_file in quarter_files:
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as Data:
                    D = json.load(Data)
                    for x in D['data']['districts']:
                        District = x["entityName"]
                        Total_Count = x['metric']['count']
                        Total_Amount = x['metric']['amount']
                        colm['Total_Transaction_Count'].append(Total_Count)
                        colm['Total_Transaction_Amount'].append(int(Total_Amount))
                        colm['District'].append(District)
                        colm['State'].append(State_folder)
                        colm['Year'].append(year_folder)
                        colm['Quarter'].append(int(quarter_file.strip('.json')))
    Top_Trans_District = pd.DataFrame(colm)
    conn = create_connection()
    cursor = conn.cursor()
    top_transaction_table = '''CREATE TABLE IF NOT EXISTS top_transaction (
        State VARCHAR(50),
        Year VARCHAR(5),
        Quarter INT,
        District VARCHAR(150),
        Total_Transaction_Count INTEGER,
        Total_Transaction_Amount INTEGER,
        UNIQUE (State, Year, Quarter, District, Total_Transaction_Count, Total_Transaction_Amount))'''
    cursor.execute(top_transaction_table)
    insert_query = '''INSERT OR IGNORE INTO top_transaction(State, Year, Quarter, District, Total_Transaction_Count, Total_Transaction_Amount)
                        VALUES (?, ?, ?, ?, ?, ?)'''
    for index, row in Top_Trans_District.iterrows():
        values = (row['State'],row['Year'],row['Quarter'],row['District'],row['Total_Transaction_Count'],row['Total_Transaction_Amount'])
        cursor.execute(insert_query, values)
    conn.commit()
    return Top_Trans_District
#Top Insurance District Wise
@st.cache_data(show_spinner=False)
def top_ins_dist_data(path):
    agg_State_list = os.listdir(path)
    colm = {'State': [],'Year': [],'Quarter': [],'District': [],'Total_Count': [],'Total_Amount': []}
    for State_folder in agg_State_list:
        State_path = os.path.join(path, State_folder)
        years_list = os.listdir(State_path)
        for year_folder in years_list:
            year_path = os.path.join(State_path, year_folder)
            quarter_files = os.listdir(year_path)
            for quarter_file in quarter_files:
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for district_data in data['data']['districts']:
                        District = district_data['entityName']
                        Total_Count = district_data['metric']['count']
                        Total_Amount = district_data['metric']["amount"]
                        colm['State'].append(State_folder)
                        colm['Year'].append(year_folder)
                        colm['Quarter'].append(int(quarter_file.strip('.json')))
                        colm['District'].append(District) 
                        colm['Total_Count'].append(Total_Count)
                        colm['Total_Amount'].append(Total_Amount)
    Top_Ins_Dist = pd.DataFrame(colm)
    conn = create_connection()
    cursor = conn.cursor()
    top_ins_dist_table = '''CREATE TABLE IF NOT EXISTS top_ins_dist (
                        State VARCHAR(50),
                        Year VARCHAR(5),
                        Quarter INT,
                        District VARCHAR(50),
                        Total_Count INTEGER,
                        Total_Amount INTEGER,
                        UNIQUE (State, Year, Quarter, District, Total_Count,Total_Amount))'''
    cursor.execute(top_ins_dist_table)
    insert_query = '''INSERT OR IGNORE INTO top_ins_dist (State, Year, Quarter, District, Total_Count,Total_Amount)
                        VALUES (?, ?, ?, ?, ?, ?)'''
    for index, row in Top_Ins_Dist.iterrows():
        values = (row['State'],row['Year'], row['Quarter'],row['District'], row['Total_Count'],row['Total_Amount'])
        cursor.execute(insert_query, values)
    conn.commit()
    return Top_Ins_Dist
#charts question function
#1 - AGG-USERS
def get_top_States_with_highest_registered_users(conn):
    query = """SELECT State, SUM(Total_Registered_Users) AS Total_Users 
                FROM agg_user
                GROUP BY State
                ORDER BY Total_Users DESC
                LIMIT 10;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#4B0082', '#6A5ACD', '#9932CC', '#800080', '#9400D3', '#663399', '#C9A0DC', '#483D8B', '#C8A2C8', '#CCCCFF']
    fig = px.bar(df, x='State', y='Total_Users',color = 'State',color_discrete_sequence=colors,
                     hover_name='State',
                     text="Total_Users",
                     labels={'Registered_Users': 'Number of Registered Users', 'State': 'State'})
    fig.update_traces(textposition='inside', textangle=90)
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",
    font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#2
def get_bottom_States_with_lowest_registered_users(conn):
    query = """SELECT State, SUM(Total_Registered_Users) AS Total_Users
            FROM agg_user
            GROUP BY State
            ORDER BY Total_Users ASC
            LIMIT 10;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#82008B', '#CD5A6A', '#CC3299', '#800080', '#D30094', '#993366', '#DCA0C9', '#8B3D48', '#C8A2C8', '#FFCCCC']
    fig = px.bar(df, x='State', y='Total_Users',color = 'State',color_discrete_sequence=colors,
                     hover_name='State',
                     text="Total_Users",
                     labels={'Registered_Users': 'Number of Registered Users', 'State': 'State'})
    fig.update_layout(xaxis_tickangle=30)
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#3
def get_brand_counts1(conn):
    query = """SELECT State, Device_Brand, COUNT(*) AS Reg_User_Count_By_Brand
                FROM agg_user
                GROUP BY State, Device_Brand
                ORDER BY State, Reg_User_Count_By_Brand DESC;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["Device_Brand"] = df["Device_Brand"].str.capitalize()
    colors = {'Xiaomi': '#9966CC','Vivo': '#D1C6E6','Samsung': '#5500AA'}
    fig = px.bar(df, y='Reg_User_Count_By_Brand', x='State', color='Device_Brand',
                 color_discrete_map=colors,
                 labels={'State': 'State', 'Reg_User_Count_By_Brand': 'Brand Usage Count', 'Device_Brand': 'Brand'},
                 orientation='v')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#4
def get_brand_counts2(conn):
    query = """SELECT Device_Brand, COUNT(*) AS Brand_Usage_Count
                FROM agg_user
                WHERE Device_Brand IS NOT NULL
                GROUP BY Device_Brand;"""
    df = pd.read_sql(query, conn)
    df["Device_Brand"] = df["Device_Brand"].str.capitalize()
    colors = ['#DDA0DD', '#9370DB','#800080',"#E6E6FA"]
    fig = px.pie(df, values='Brand_Usage_Count', names='Device_Brand',
             labels={'Brand_Usage_Count': 'Count', 'Brand': 'Brand'},
             color_discrete_sequence=colors)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True) 
#5
def max_percentage_per_year(conn):
    query = """SELECT Year, Device_Brand, Max_Brand_Share_Percentage
FROM (
    SELECT Year, Device_Brand, MAX(Percentage_of_Brand) AS Max_Brand_Share_Percentage,
           ROW_NUMBER() OVER (PARTITION BY Year ORDER BY MAX(Percentage_of_Brand) DESC) AS row_num
    FROM agg_user
    WHERE Percentage_of_Brand != 'None'
    GROUP BY Year, Device_Brand
) AS ranked_brands
WHERE row_num <= 5;"""
    df = pd.read_sql(query, conn)
    df["Max_Brand_Share_Percentage"] = (df["Max_Brand_Share_Percentage"] * 100).round().astype(str) + '%'
    colors = ['#DDA0DD', '#9370DB', '#800080','#E6E6FA','#663399']
    df["Device_Brand"] = df["Device_Brand"].str.capitalize()
    fig = px.bar(df, x='Year', y='Max_Brand_Share_Percentage', color='Device_Brand',text="Max_Brand_Share_Percentage",
             hover_name='Year', color_discrete_sequence=colors,
             labels={'Max_Brand_Share_Percentage': 'Max Brand Share Percentage', 'Year': 'Year'})
    fig.update_layout(xaxis={'categoryorder':'category descending'})
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#6
def sum_app_opens_top_State(conn):
    query = """SELECT SUM(Total_App_Opens) AS Sum_App_opens, State
                FROM agg_user
                GROUP BY State
                ORDER BY Sum_App_opens DESC
                LIMIT 10;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#CCCCFF', '#C8A2C8', '#8B3D48', '#DCA0C9', '#993366', '#D30094', '#800080', '#CC3299', '#CD5A6A', '#82008B']
    fig = px.bar(df, x='State', y='Sum_App_opens',color = "State", color_discrete_sequence=colors,text="Sum_App_opens",
                 labels={'State': 'State', 'Sum_App_opens': 'Sum of App Opens'},hover_name="State")
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#7
def top_States_by_year(conn):
    query = """SELECT year, State, total_registered_count
    FROM (SELECT year, State, SUM(Total_Registered_Users) AS total_registered_count
        FROM agg_user
        GROUP BY year, State
    ) AS yearly_counts
    WHERE total_registered_count = (SELECT MAX(total_registered_count)
        FROM (SELECT year, State, SUM(Total_Registered_Users) AS total_registered_count
            FROM agg_user
            GROUP BY year, State
        ) AS max_counts
        WHERE yearly_counts.year = max_counts.year)
    ORDER BY year;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    fig = px.area(df, x='year', y='total_registered_count',color= "State",text="total_registered_count",color_discrete_sequence=["#C9A0DC"],
                 hover_name="year",
                 labels={'State': 'State', 'Sum_App_opens': 'Sum of App Opens'})
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#8
def top_States_by_year_1(conn):
    query = """SELECT year, total_registered_count
    FROM (
        SELECT year, SUM(Total_Registered_Users) AS total_registered_count
        FROM agg_user
        GROUP BY year
    ) AS yearly_counts
    WHERE total_registered_count = (
        SELECT MAX(total_registered_count)
        FROM (
            SELECT year, SUM(Total_Registered_Users) AS total_registered_count
            FROM agg_user
            GROUP BY year
        ) AS max_counts
        WHERE yearly_counts.year = max_counts.year
    )ORDER BY year;"""
    df = pd.read_sql(query, conn)
    fig = px.area(df, x='year', y='total_registered_count', text='total_registered_count', 
                  color_discrete_sequence=["#C9A0DC"],
                  labels={'total_registered_count': 'Total Registered Count'})
    fig.update_layout(
        hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New", font=dict(color="white")),
        xaxis_title='Year',
        yaxis_title='Total Registered Count')
    st.plotly_chart(fig, use_container_width=True)
#1 -AGG-TRANS (Charts)
def get_top_10_States_with_highest_transaction_count(conn):
    query = """WITH State_yearly_counts AS (
    SELECT State, SUM(Transaction_count) AS yearly_count
    FROM aggregated_transaction
    GROUP BY State, year)
    SELECT State, SUM(yearly_count) AS total_count_sum
    FROM State_yearly_counts
    GROUP BY State
    ORDER BY total_count_sum DESC
    LIMIT 10;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#4B0082', '#6A5ACD', '#9932CC', '#800080', '#9400D3', '#663399', '#C9A0DC', '#483D8B', '#C8A2C8', '#CCCCFF']
    fig = px.bar(df, x='State', y='total_count_sum', color = "State",color_discrete_sequence=colors,
                 title='Top 10 States with Highest Total Transaction Count',text="total_count_sum",hover_name="State",
                 labels={'total_count_sum': 'Total Transaction Count', 'State': 'State'})
    fig.update_traces(textposition='inside')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#2
def get_top_10_States_with_lowest_transaction_count(conn):
    query = """WITH State_yearly_counts AS (
        SELECT State, SUM(Transaction_count) AS yearly_count
        FROM aggregated_transaction
        GROUP BY State, year)
        SELECT State, SUM(yearly_count) AS total_count_sum
        FROM State_yearly_counts
        GROUP BY State
        ORDER BY total_count_sum ASC
        LIMIT 10;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#82008B', '#CD5A6A', '#CC3299', '#800080', '#D30094', '#993366', '#DCA0C9', '#8B3D48', '#C8A2C8', '#FFCCCC']
    fig = px.bar(df, x='State', y='total_count_sum', color='State',color_discrete_sequence=colors,
                 title='Top 10 States with Lowest Total Transaction Count',text="total_count_sum",hover_name="State",
                 labels={'total_count_sum': 'Total Transaction Count', 'State': 'State'})
    fig.update_layout(hoverlabel=dict(bgcolor='black',font_size=16,font_family='Courier New',font=dict(color="white"))) 
    st.plotly_chart(fig,use_container_width=True)
#3
def get_top_10_States_with_highest_transaction_amount(conn):
    query = """WITH State_yearly_counts AS (
    SELECT State, SUM(Transaction_Amount) AS yearly_count
    FROM aggregated_transaction
    GROUP BY State, year)
    SELECT State, SUM(yearly_count) AS total_Amount_sum
    FROM State_yearly_counts
    GROUP BY State
    ORDER BY total_Amount_sum DESC LIMIT 10;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#4B0082', '#6A5ACD', '#9932CC', '#800080', '#9400D3', '#663399', '#C9A0DC', '#483D8B', '#C8A2C8', '#CCCCFF']
    fig = px.bar(df, x='State', y='total_Amount_sum', color = "State",color_discrete_sequence=colors,text="total_Amount_sum",
                 title='Top 10 States with Highest Total Transaction Amount',hover_name="State",
                 labels={'total_count_sum': 'Total Transaction Amount', 'State': 'State'})
    fig.update_layout(hoverlabel=dict(bgcolor='black',font_size=16,font_family='Courier New',font=dict(color="white"))) 
    st.plotly_chart(fig,use_container_width=True)
#4
def get_top_10_States_with_lowest_transaction_amount(conn):
    query = """WITH State_yearly_counts AS (
    SELECT State, SUM(Transaction_amount) AS yearly_count
    FROM aggregated_transaction
    GROUP BY State, year)
    SELECT State, SUM(yearly_count) AS total_amount_sum
    FROM State_yearly_counts
    GROUP BY State
    ORDER BY total_amount_sum ASC
    LIMIT 10;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#82008B', '#CD5A6A', '#CC3299', '#800080', '#D30094', '#993366', '#DCA0C9', '#8B3D48', '#C8A2C8', '#FFCCCC']
    fig = px.bar(df, x='State', y='total_amount_sum', color = "State",color_discrete_sequence=colors,
                 title='Top 10 States with lowest Total Transaction Amount',text="total_amount_sum",hover_name="State",
                 labels={'total_count_sum': 'Total Transaction Amount', 'State': 'State'})
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#5
def transaction_type(conn):
    query = """SELECT Transaction_Type, COUNT(*) AS Transaction_Count
               FROM aggregated_transaction
               GROUP BY Transaction_Type;"""
    df =pd.read_sql(query,conn)
    df["Transaction_Type"] = df["Transaction_Type"].str.capitalize()
    colors = ['#DDA0DD', '#9370DB','#800080',"#E6E6FA","#F5E1FF"]
    fig = px.pie(df,values="Transaction_Count",names="Transaction_Type",labels={'Transaction_Type_Count': 'Transaction Count', 'Transaction_Type': 'Transaction Type'}
             ,hover_name="Transaction_Type",color_discrete_sequence=colors)
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#6
def total_count_highest_year(conn):
    query = """SELECT year, State, SUM(Transaction_Count) AS Highest_Transaction_Total
               FROM aggregated_transaction
               GROUP BY year, State
               HAVING SUM(Transaction_Count) = (
              SELECT MAX(total_transactions)
              FROM (
                SELECT year, SUM(Transaction_Count) AS total_transactions
                FROM aggregated_transaction
                GROUP BY year, State
                   ) AS subquery
             WHERE subquery.year = aggregated_transaction.year)
            ORDER BY year;"""
    df =pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    fig = px.line(df,x="Year",y="Highest_Transaction_Total",labels={'Transaction_Count': 'Transaction Count', 'State': 'State'},
             color_discrete_sequence=["purple"],markers=True)
    fig.update_traces(line=dict(width=3))
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#7
def total_amount_highest_year(conn):
    query = """SELECT year, State, Total_Transactions AS Highest_Transaction_Total
    FROM (
        SELECT year, State, SUM(Transaction_Amount) AS Total_Transactions
        FROM aggregated_transaction
        GROUP BY year, State
    ) AS subquery
    WHERE (year, Total_Transactions) IN (
        SELECT year, MAX(Total_Transactions) AS Highest_Transaction_Total
    FROM (
        SELECT year, SUM(Transaction_Amount) AS Total_Transactions
        FROM aggregated_transaction
        GROUP BY year, State
    ) AS year_totals
    GROUP BY year)ORDER BY year;"""
    df =pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    fig = px.line(df,x="year",y="Highest_Transaction_Total",labels={'Transaction_Amount': 'Transaction Amount', 'State': 'State'},
             color_discrete_sequence=["violet"],markers=True,width=10)
    fig.update_traces(line=dict(width=3))
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#1 - AGG-INS (CHARTS)
def highest_ins_count(conn):
    query = """SELECT State, SUM(Total_Count) AS Total_Insurance_Count
                FROM aggregated_insurance
                GROUP BY State
                ORDER BY Total_Insurance_Count DESC LIMIT 10;"""
    df = pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#4B0082', '#6A5ACD', '#9932CC', '#800080', '#9400D3', '#663399', '#C9A0DC', '#483D8B', '#C8A2C8', '#CCCCFF']
    fig = px.bar(df,x="State",y="Total_Insurance_Count",color ="State",text="Total_Insurance_Count",color_discrete_sequence=colors,title="Top 10 State with Highest Insurance Count")
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#2
def lowest_ins_count(conn):
    query = """SELECT State, SUM(Total_Count) AS Total_Insurance_Count
            FROM aggregated_insurance
            GROUP BY State
            ORDER BY Total_Insurance_Count ASC LIMIT 10;"""
    df = pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#82008B', '#CD5A6A', '#CC3299', '#800080', '#D30094', '#993366', '#DCA0C9', '#8B3D48', '#C8A2C8', '#FFCCCC']
    fig = px.bar(df,x="State",y="Total_Insurance_Count",color ="State",color_discrete_sequence=colors,text="Total_Insurance_Count",title="Top 10 State with Lowest Insurance Count")
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#3
def highest_ins_amount(conn):
    query = """SELECT State, SUM(Total_Amount) AS Total_Insurance_Amount
                FROM aggregated_insurance
                GROUP BY State
                ORDER BY Total_Insurance_Amount DESC LIMIT 10;"""
    df = pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#4B0082', '#6A5ACD', '#9932CC', '#800080', '#9400D3', '#663399', '#C9A0DC', '#483D8B', '#C8A2C8', '#CCCCFF']
    fig = px.bar(df,x="State",y="Total_Insurance_Amount",color ="State",color_discrete_sequence=colors,text="Total_Insurance_Amount",title="Top 10 State with Highest Insurance Amount")
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#4
def lowest_ins_amount(conn):
    query = """SELECT State, SUM(Total_Amount) AS Total_Insurance_Amount
                FROM aggregated_insurance
                GROUP BY State
                ORDER BY Total_Insurance_Amount ASC LIMIT 10;"""
    df = pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    colors = ['#82008B', '#CD5A6A', '#CC3299', '#800080', '#D30094', '#993366', '#DCA0C9', '#8B3D48', '#C8A2C8', '#FFCCCC']
    fig = px.bar(df,x="State",y="Total_Insurance_Amount",color ="State",text="Total_Insurance_Amount",color_discrete_sequence=colors,title="Top 10 State with Lowest Insurance Amount")
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#1 TOP-DISTRICT-USERS (CHARTS)
def get_district_with_highest_users_in_States(conn):
    query = """ SELECT State, District, RegisteredUser
                FROM top_user
                WHERE (State, RegisteredUser) IN (
                SELECT State, MAX(RegisteredUser) as MaxRegisteredUser
                FROM top_user
                GROUP BY State);"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["District"] = df["District"].str.capitalize()
    fig = px.pie(df, values='RegisteredUser', names='District',hover_name="District",
                 title='District with Highest Number of Registered Users in Each State',
                 labels={'RegisteredUser': 'Number of Registered Users', 'State': 'State'},
                 hole=0.4)
    fig.update_layout(height=800, width=1000)
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#2
def get_top_10_districts_highest_users_all_over_india(conn):
    query = """SELECT DISTINCT State, District, RegisteredUser
                FROM top_user
                WHERE (State, RegisteredUser) IN (
                    SELECT State, MAX(RegisteredUser) as MaxRegisteredUser
                    FROM top_user
                    GROUP BY State) ORDER BY RegisteredUser DESC LIMIT 10;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["District"] = df["District"].str.capitalize()
    fig = px.scatter(df, x='District', y='RegisteredUser', color='State',
                  title='Top 10 Districts with Highest Number of Registered Users in India',
                  size='RegisteredUser',hover_name="District",
                  labels={'RegisteredUser': 'Number of Registered Users', 'District': 'District', 'State': 'State'})
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#3
def get_district_with_lowest_users_in_States(conn):
    query = """SELECT DISTINCT State, District, RegisteredUser
                FROM top_user
                WHERE (State, RegisteredUser) IN (
                    SELECT State, MIN(RegisteredUser) as MinRegisteredUser
                    FROM top_user
                    GROUP BY State);"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["District"] = df["District"].str.capitalize()
    fig = px.bar(df, x='State', y='RegisteredUser', color='District',hover_name="District",
                 title='District with Lowest Number of Registered Users in Each State',
                 labels={'RegisteredUser': 'Number of Registered Users', 'State': 'State', 'District': 'District'})
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#4
def get_top_10_districts_lowest_users_all_over_india(conn):
    query = """SELECT DISTINCT State, District, RegisteredUser
                FROM top_user
                WHERE (State, RegisteredUser) IN (
                    SELECT State, MIN(RegisteredUser) as MaxRegisteredUser
                    FROM top_user
                    GROUP BY State) ORDER BY RegisteredUser ASC
                     LIMIT 10;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["District"] = df["District"].str.capitalize()
    fig = px.scatter(df, y='RegisteredUser', x='District', color='State',
                title='Top 10 Districts with Lowest Number of Registered Users in India',
                size='RegisteredUser',hover_name="District",
                labels={'RegisteredUser': 'Number of Registered Users', 'District': 'District', 'State': 'State'})
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#5
def get_top_districts_with_highest_registered_users_in_all_year(conn):
    query_top_districts = """WITH yearly_totals AS (SELECT year, District, State, SUM(RegisteredUser) AS total_users
                                FROM top_user
                                GROUP BY year, District, State),
                            ranked_totals AS (
                                SELECT year,District,State,total_users,
                                    ROW_NUMBER() OVER (PARTITION BY year ORDER BY total_users DESC) AS rnk
                                FROM yearly_totals)
                            SELECT year,State,total_users,District
                            FROM ranked_totals
                            WHERE rnk = 1
                            ORDER BY year;"""
    df = pd.read_sql(query_top_districts, conn)
    df["State"] = df["State"].str.capitalize()
    df["District"] = df["District"].str.capitalize()
    colors=["violet"]
    fig = px.bar(df, x="year", y="total_users", color="District",
                               hover_name="State", barmode="stack",color_discrete_sequence=colors,
                               title='Districts with Highest Number of Registered Users by Year',
                               labels={'TotalRegisteredUser': 'Number of Registered Users', 'District': 'District', 'State': 'State'})
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#6
def get_top_districts_with_lowest_registered_users_in_all_year(conn):
    query_top_districts = """WITH yearly_totals AS (SELECT year, District, State, SUM(RegisteredUser) AS total_users
                                FROM top_user
                                GROUP BY year, District, State),
                            ranked_totals AS (
                                SELECT year,District,State,total_users,
                                    ROW_NUMBER() OVER (PARTITION BY year ORDER BY total_users ASC) AS rnk
                                FROM yearly_totals)
                            SELECT year,District,State,total_users
                            FROM ranked_totals
                            WHERE rnk = 1
                            ORDER BY year;"""
    df = pd.read_sql(query_top_districts, conn)
    df["State"] = df["State"].str.capitalize()
    df["District"] = df["District"].str.capitalize()
    colors = ['#82008B', '#CD5A6A', '#CC3299',]
    fig = px.bar(df, x="year", y="total_users", color="District",
                               hover_name="State", barmode="stack",color_discrete_sequence=colors,
                               title='Districts with Lowest Number of Registered Users by Year',
                               labels={'TotalRegisteredUser': 'Number of Registered Users', 'District': 'District', 'State': 'State'})
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#1 TOP-DISTRICT-TRANS-COUNT (CHARTS)
def get_highest_transaction_count_all_States(conn):
    query = """WITH ranked_totals AS (
    SELECT State,District,SUM(Total_Transaction_Count) AS total_transaction_count,
    ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Transaction_Count) DESC) AS rnk
    FROM top_transaction
    GROUP BY State, District)
    SELECT State,District,total_transaction_count
    FROM ranked_totals
    WHERE rnk = 1
    ORDER BY State;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["District"] = df["District"].str.capitalize()
    fig = px.bar(df, x='District', y='total_transaction_count',color ="District",
                 labels={"total_transaction_count":"Total Transaction Count","State":"State","district":"District"},
                 hover_name="State", title='District With Highest Transaction Count in All States')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#2
def get_top5_highest_transaction_count(conn):
    query = """WITH ranked_totals AS (
    SELECT State,district,SUM(Total_Transaction_Count) AS total_transaction_count,
    ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Transaction_Count) DESC) AS rnk
    FROM top_transaction
    GROUP BY State, district)
    SELECT State,district,total_transaction_count
    FROM ranked_totals
    WHERE rnk = 1
    ORDER BY total_transaction_count DESC LIMIT 5;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    colors = ['#DDA0DD', '#9370DB','#800080',"#E6E6FA","#663399"]
    fig = px.pie(df, values='total_transaction_count', names='district',color ="district",color_discrete_sequence=colors,
                 labels={"total_transaction_count":"Total Transaction Count","State":"State","district":"District"},
                 hover_name="State", title='Top 5 District With Highest Transaction Count')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#3
def get_lowest_transaction_count_all_States(conn):
    query = """WITH ranked_totals AS (
    SELECT State,district,SUM(Total_Transaction_Count) AS total_transaction_count,
    ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Transaction_Count) ASC) AS rnk
    FROM top_transaction
    GROUP BY State, district)
    SELECT State,district,total_transaction_count
    FROM ranked_totals
    WHERE rnk = 1
    ORDER BY State;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.bar(df, x='district', y='total_transaction_count',color ="district",hover_name="State",
                 labels={"total_transaction_count":"Total Transaction Count","State":"State","district":"District"},
                  title='District With Lowest Transaction Count in All States')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#4
def get_top5_lowest_transaction_count(conn):
    query = """WITH ranked_totals AS (
    SELECT State,district,SUM(Total_Transaction_Count) AS total_transaction_count,
    ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Transaction_Count) ASC) AS rnk
    FROM top_transaction
    GROUP BY State, district)
    SELECT State,district,total_transaction_count
    FROM ranked_totals
    WHERE rnk = 1
    ORDER BY total_transaction_count DESC LIMIT 5;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    colors = ['#DDA0DD', '#9370DB','#800080',"#E6E6FA","#663399"]
    fig = px.pie(df, values='total_transaction_count', names='district',color ="district",color_discrete_sequence=colors,hover_name="State", 
                 labels={"total_transaction_count":"Total Transaction Count","State":"State","district":"District"},
                 title='Top 5 District With Lowest Transaction Count')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#5
def get_highest_transaction_count_all_years(conn):
    query = """WITH yearly_totals AS (
            SELECT year, district, State, SUM(Total_Transaction_Count) AS total_transactions
            FROM top_transaction
            GROUP BY year, district, State),
        ranked_totals AS (
            SELECT year, district, State, total_transactions,
                   ROW_NUMBER() OVER (PARTITION BY year ORDER BY total_transactions DESC) AS rnk
            FROM yearly_totals)
        SELECT year, district, State, total_transactions
        FROM ranked_totals
        WHERE rnk = 1
        ORDER BY year;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    colors = ["violet"]
    fig = px.line(df, x='year', y='total_transactions',color_discrete_sequence=colors,
                hover_name="State",color="district", labels={"total_transactions":"Total Transaction","State":"State","district":"District"},markers=True,
                title='District With Highest Transaction Count in All Years with their State')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True)
#6
def get_lowest_transaction_count_all_years(conn):
    query = """WITH yearly_totals AS (
            SELECT year, district, State, SUM(Total_Transaction_Count) AS total_transactions
            FROM top_transaction
            GROUP BY year, district, State),
        ranked_totals AS (
            SELECT year, district, State, total_transactions,
                   ROW_NUMBER() OVER (PARTITION BY year ORDER BY total_transactions ASC) AS rnk
            FROM yearly_totals)
        SELECT year, district, State, total_transactions
        FROM ranked_totals
        WHERE rnk = 1
        ORDER BY year;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.line(df, x='year', y='total_transactions', 
                  hover_name="State",markers=True,color="district", labels={"total_transactions":"Total Transaction","State":"State","district":"District"},
                  title='District With Lowest Transaction Count in All Years with their State')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True)
#1 TOP-DISTRICT-TRANS-AMOUNT
def get_highest_transaction_amount_all_States(conn):
    query = """WITH ranked_totals AS (
    SELECT State,district,SUM(Total_Transaction_Amount) AS total_transaction_amount,
    ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Transaction_Amount) DESC) AS rnk
    FROM top_transaction
    GROUP BY State, district)
    SELECT State,district,total_transaction_amount
    FROM ranked_totals
    WHERE rnk = 1
    ORDER BY State;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.bar(df, x='district', y='total_transaction_amount',color ="district",hover_name="State", 
                 labels={"total_transaction_amount":"Total Transaction Amount","State":"State","district":"District"},
                 title='District With Highest Transaction Amount in All States')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#2
def get_top5_highest_transaction_amount(conn):
    query = """WITH ranked_totals AS (
    SELECT State,district,SUM(Total_Transaction_Amount) AS total_transaction_amount,
    ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Transaction_Amount) DESC) AS rnk
    FROM top_transaction
    GROUP BY State, district)
    SELECT State,district,total_transaction_amount
    FROM ranked_totals
    WHERE rnk = 1
    ORDER BY total_transaction_amount DESC LIMIT 5;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    colors = ['#DDA0DD', '#9370DB','#800080',"#E6E6FA","#663399"]
    fig = px.pie(df, values='total_transaction_amount', names='district',color ="district",
                 color_discrete_sequence=colors,hover_name="State",labels={"total_transaction_amount":"Total Transaction Amount","State":"State","district":"District"},
                   title='Top 5 District With Highest Transaction Count')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#3
def get_lowest_transaction_amount_all_States(conn):
    query = """WITH ranked_totals AS (
    SELECT State,district,SUM(Total_Transaction_Amount) AS total_transaction_amount,
    ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Transaction_Amount) ASC) AS rnk
    FROM top_transaction
    GROUP BY State, district)
    SELECT State,district,total_transaction_amount
    FROM ranked_totals
    WHERE rnk = 1
    ORDER BY State;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.bar(df, x='district', y='total_transaction_amount',color ="district",hover_name="State",labels={"total_transaction_amount":"Total Transaction Amount","State":"State","district":"District"},
                  title='District With Lowest Transaction Amount in All States')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#4
def get_top5_lowest_transaction_amount(conn):
    query = """WITH ranked_totals AS (
    SELECT State,district,SUM(Total_Transaction_Amount) AS total_transaction_amount,
    ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Transaction_Amount) ASC) AS rnk
    FROM top_transaction
    GROUP BY State, district)
    SELECT State,district,total_transaction_amount
    FROM ranked_totals
    WHERE rnk = 1
    ORDER BY total_transaction_amount DESC LIMIT 5;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    colors = ['#DDA0DD', '#9370DB','#800080',"#E6E6FA","#663399"]
    fig = px.pie(df, values='total_transaction_amount', names ='district',color ="district",hover_name="State",color_discrete_sequence=colors,
                 labels={"total_transaction_amount":"Total Transaction Amount","State":"State","district":"District"} ,title='Top 5 District With Lowest Transaction Amount')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig, use_container_width=True)
#5
def get_highest_transaction_amount_all_years(conn):
    query = """WITH yearly_totals AS (
            SELECT year, district, State, SUM(Total_Transaction_Amount) AS total_transactions
            FROM top_transaction
            GROUP BY year, district, State),
        ranked_totals AS (
            SELECT year, district, State, total_transactions,
                   ROW_NUMBER() OVER (PARTITION BY year ORDER BY total_transactions DESC) AS rnk
            FROM yearly_totals)
        SELECT year, district, State, total_transactions
        FROM ranked_totals
        WHERE rnk = 1
        ORDER BY year;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.line(df, x='year', y='total_transactions',markers=True,hover_name="State",color ="district",labels={'district':'District',"State":"State","total_transactions":"Total Transactions"}, 
                    title='District With Highest Transaction Amount in All Years with their State')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True)
#6
def get_lowest_transaction_amount_all_years(conn):
    query = """WITH yearly_totals AS (
            SELECT year, district, State, SUM(Total_Transaction_Amount) AS total_transactions
            FROM top_transaction
            GROUP BY year, district, State),
        ranked_totals AS (
            SELECT year, district, State, total_transactions,
                   ROW_NUMBER() OVER (PARTITION BY year ORDER BY total_transactions ASC) AS rnk
            FROM yearly_totals)
        SELECT year, district, State, total_transactions
        FROM ranked_totals
        WHERE rnk = 1
        ORDER BY year;"""
    df = pd.read_sql(query, conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.line(df, x='year', y='total_transactions',hover_name="State",markers=True,color="district",
                  labels={"district":"District","total_transactions":"Total Transactions","State":"State"}, title='District With Lowest Transaction Amount in All Years with their State')
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True)
#1 - TOP-INS (CHARTS)
def highest_ins_count_1(conn):
    query = """WITH ranked_totals AS (SELECT State,district,SUM(Total_Count) AS Total_Insurance_Count,
            ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Count) DESC) AS rnk
            FROM top_ins_dist
            GROUP BY State, district)
            SELECT State,district,Total_Insurance_Count,rnk
            FROM ranked_totals
            ORDER BY Total_Insurance_Count DESC
            LIMIT 10;"""
    df = pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.bar(df,x="State",y="Total_Insurance_Count",labels={"district":"District"},color ="district",hover_name="State",title="Top 10 District with Highest Insurance Count")
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#2
def lowest_ins_count_1(conn):
    query = """WITH ranked_totals AS (SELECT State,district,SUM(Total_Count) AS Total_Insurance_Count,
            ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Count) ASC) AS rnk
            FROM top_ins_dist
            GROUP BY State, district)
            SELECT State,district,Total_Insurance_Count,rnk
            FROM ranked_totals
            ORDER BY Total_Insurance_Count ASC
            LIMIT 10;"""
    df = pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.bar(df,x="State",y="Total_Insurance_Count",labels={"district":"District"},color ="district",hover_name="State",title="Top 10 District with Lowest Insurance Count")
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#3
def highest_ins_amount_1(conn):
    query = """WITH ranked_totals AS (SELECT State,district,SUM(Total_Amount) AS Total_Insurance_Amount,
            ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Amount) DESC) AS rnk
            FROM top_ins_dist
            GROUP BY State, district)
            SELECT State,district,Total_Insurance_Amount,rnk
            FROM ranked_totals
            ORDER BY Total_Insurance_Amount DESC
            LIMIT 10;"""
    df = pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.bar(df,x="State",y="Total_Insurance_Amount",labels={"district":"District"},color ="district",hover_name="State",title="Top 10 District with Highest Insurance Amount")
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#4
def lowest_ins_amount_1(conn):
    query = """WITH ranked_totals AS (SELECT State,district,SUM(Total_Amount) AS Total_Insurance_Amount,
            ROW_NUMBER() OVER (PARTITION BY State ORDER BY SUM(Total_Amount) ASC) AS rnk
            FROM top_ins_dist
            GROUP BY State, district)
            SELECT State,district,Total_Insurance_Amount,rnk
            FROM ranked_totals
            ORDER BY Total_Insurance_Amount ASC
            LIMIT 10;"""
    df = pd.read_sql(query,conn)
    df["State"] = df["State"].str.capitalize()
    df["district"] = df["district"].str.capitalize()
    fig = px.bar(df,x="State",y="Total_Insurance_Amount",color ="district",hover_name="State",
                 labels={'Total_Insurance_Amount':'Total InsuranceAmount',"State":"State","district":"District"},title="Top 10 District with Lowest Insurance Amount")
    fig.update_layout(hoverlabel=dict(bgcolor="black", font_size=16, font_family="Courier New",font=dict(color="white")))
    st.plotly_chart(fig,use_container_width=True)
#1 - map_user (CHARTS)
def fetch_data_map_user(conn,year, quarter):
    query = """SELECT quarter, year, State, AVG(Total_registered_user) AS avg_registered_users,
       AVG(Total_App_Opens) AS avg_app_opens
        FROM map_user
        WHERE year = ? AND quarter = ?
        GROUP BY quarter, year, State"""
    params = (year, quarter)
    df = pd.read_sql(query, conn, params=params)
    State_mapping = {
        'Andaman-&-nicobar-islands': 'Andaman and Nicobar',
        'Andhra-pradesh': 'Andhra Pradesh',
        'Arunachal-pradesh': 'Arunachal Pradesh',
        'dadra-&-nagar-haveli': 'Dadra and Nagar Haveli',
        'daman-&-diu':'Daman and Diu',
        'Himachal-pradesh': 'Himachal Pradesh',
        'Jammu-&-kashmir': 'Jammu and Kashmir',
        'Madhya-pradesh': 'Madhya Pradesh',
        'Tamil-nadu': 'Tamil Nadu',
        'Uttar-pradesh': 'Uttar Pradesh',
        'West-bengal': 'West Bengal'
    }
    df['State'] = df['State'].str.capitalize().replace(State_mapping)
    df["avg_registered_users"] = df["avg_registered_users"].round()
    df["avg_app_opens"] = df["avg_app_opens"].round()
    return df
#2
def fetch_data_map_trans(conn,year, quarter):
    query = """SELECT quarter,year,State,AVG(Transaction_Count) AS Avg_Transaction_Count,
    AVG(Total_Transaction_Amount) AS Avg_Total_Transaction_Amount
    FROM map_transaction 
    WHERE year = ? AND quarter = ?
    GROUP BY quarter, year, State"""
    params = (year, quarter)
    df = pd.read_sql(query, conn, params=params)
    State_mapping = {
        'Andaman-&-nicobar-islands': 'Andaman and Nicobar',
        'Andhra-pradesh': 'Andhra Pradesh',
        'Arunachal-pradesh': 'Arunachal Pradesh',
        'dadra-&-nagar-haveli': 'Dadra and Nagar Haveli',
        'daman-&-diu':'Daman and Diu',
        'Himachal-pradesh': 'Himachal Pradesh',
        'Jammu-&-kashmir': 'Jammu and Kashmir',
        'Madhya-pradesh': 'Madhya Pradesh',
        'Tamil-nadu': 'Tamil Nadu',
        'Uttar-pradesh': 'Uttar Pradesh',
        'West-bengal': 'West Bengal'
    }
    df['State'] = df['State'].str.capitalize().replace(State_mapping)
    df["Avg_Transaction_Count"] = df["Avg_Transaction_Count"].round()
    df["Avg_Total_Transaction_Amount"] = df["Avg_Total_Transaction_Amount"].round()
    return df
#3
def fetch_data_map_ins(conn,year, quarter):
    query = """SELECT quarter,year,State,AVG(Total_Count) AS Avg_Total_Count,
    AVG(Total_Amount) AS Avg_Total_Amount
    FROM map_insurance 
    WHERE year = ? AND quarter = ?
    GROUP BY quarter, year, State"""
    params = (year, quarter)
    df = pd.read_sql(query, conn, params=params)
    State_mapping = {
        'Andaman-&-nicobar-islands': 'Andaman and Nicobar',
        'Andhra-pradesh': 'Andhra Pradesh',
        'Arunachal-pradesh': 'Arunachal Pradesh',
        'dadra-&-nagar-haveli': 'Dadra and Nagar Haveli',
        'daman-&-diu':'Daman and Diu',
        'Himachal-pradesh': 'Himachal Pradesh',
        'Jammu-&-kashmir': 'Jammu and Kashmir',
        'Madhya-pradesh': 'Madhya Pradesh',
        'Tamil-nadu': 'Tamil Nadu',
        'Uttar-pradesh': 'Uttar Pradesh',
        'West-bengal': 'West Bengal'}
    df['State'] = df['State'].str.capitalize().replace(State_mapping)
    df["Avg_Total_Count"] = df["Avg_Total_Count"].round()
    df["Avg_Total_Amount"] = df["Avg_Total_Amount"].round()
    return df
#connect to database
db_path = st.secrets["database"]["path"]
def create_connection():
    conn = sqlite3.connect('db_path')  
    return conn