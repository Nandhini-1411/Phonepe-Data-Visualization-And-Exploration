# Phonepe-Data-Visualization-And-Exploration

Collect and analyze PhonePe Pulse data, including data processing and storage. 

Built a Streamlit app to fetch and display data from a Sqlite3 database for visualization and exploration.

-------------------------------------------------------------------------------------------------------
1.Import Libraries:
 
 -Import necessary libraries for connecting to SQLITE3, pandas, Streamlit,plotly , json and os.The Libraries are,
   - sqlite3 – For Connecting the Database and performing Operations
   - pandas – For Working with Dataframes
   - streamlit – To Build a web app
   - plotly - To Visualize Charts
   - json - To read json files such as data and map coordinates file.
   - os - For interacting with the operating system (e.g., file paths)

2.Functions to Json Data to Dataframe and Store it in a sqlite3 DB:
Define functions to get
  - Database Connection
  - Aggregated User,Transaction and Insurance Data
  - Map User,Transaction and Insurance Data
  - Top User,Transaction and Insurance Data
  - To get details of the charts from the database to display in Streamlit app
       - Highest and Lowest Users State and District Wise
       - Highest and Lowest Transactions State and District Wise
       - Highest and Lowest Insurances State and District Wise
       - Brand Usage etc,...

3.Streamlit User Interface:
  - Set up the Streamlit user interface with a title,header,subheader,option_menu for selecting the types of options (Districtwise,Statewise,Insights,Interactive map viewer,Insights).

 STATE-WISE AND DISTRICT-WISE
 - Prompt the user to select the Mode of Retriveal for DataFrame display (User,Transaction,Insurance).
 - Use charts to explain the Usage of PhonePe all over India in the Year(2018-2024) - (Scatter Chart, Bar Chart, Line Chart, Pie Chart).

INTERACTIVE MAP VIEWER:
 - User can filter the year and qaurter after selecting the Mode of Retrival. They Can See the Indian Geograpgical Map with the corresponding Analysis by hover over the State.


- The data is from anothe github account.

INSIGHTS:
 - Using Status Messages for Provide insights from the analysis at the Insights Option, to keep the client user informed and engaged.
