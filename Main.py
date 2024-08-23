import streamlit as st
from streamlit_option_menu import option_menu
import Functions as fun
import plotly.express as px
from PIL import Image
import json
import pandas as pd
#streamlit app
conn = fun.create_connection()
st.set_page_config(page_icon=r"assets/images/logofinal.png",page_title="PhonePe Data Insights",layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
selected_page = option_menu(menu_title=None,
options=["Home", "State-Wise Analysis", "Interactive Map Viewer","District-Wise Analysis","Insights"],
icons=["house", "bar-chart-line", "geo-alt", "bar-chart-line","lightbulb"],
menu_icon="cast",default_index=0,orientation="horizontal")
if selected_page == "Home":
    col11,col22 = st.columns(2)
    with col11:
        st.write("""Welcome to the Phonepe Data Visualization and Exploration ! This site offers interactive tools to explore and visualize data related to PhonePe transactions and user metrics. Whether you want to analyze transaction trends, understand user behavior across regions, or explore overall performance metrics, this site provides valuable insights.""")
        st.header("Key Features")
        st.subheader("Overview Dashboard")
        st.markdown("""
    - **Total Transactions**: View trends in the total number of transactions over time.
    - **Total Users**: View trends in the total number of users over time.
    - **Total Insurance**: View trends in the total number of insurances over time.""")
        st.subheader("Geographic Insights")
        st.markdown("""
    - **State-wise Analysis**: Compare transaction volumes and user engagement across States.
    - **Charts and Graphs**: Utilize interactive visualizations like line plots, bar charts, and scatter plots.
    - **District-level Analysis**: Analyze performance metrics at the district level.
    """)
        st.subheader("Quarterly Performance")
        st.markdown("""
    - **Yearly Trends**: Analyze transaction trends and user behavior year wise.
    - **Quarterly Trends**: Analyze transaction trends and user behavior quarter by quarter.
    - **Comparison Tool**: Compare performance metrics across different quarters.
    """)
        st.subheader("Custom Filters")
        st.markdown("""
    - **Filter by Year**: Focus on specific years for detailed analysis.
    - **State and District Filters**: Select States and districts to tailor insights.
    - **Quarter Filter** : Focus on specific quarter for more comphrensive analysis.
    """)
    with col22:
        image_path_1 = r"assets/images/phonpe1.jpg"
        image_1 = Image.open(image_path_1)
        st.image(image_1, caption="Sample Image")
    with col22:
        image_path_2 = r"assets/images/phonepe3.png"
        image_2 = Image.open(image_path_2)
        st.image(image_2, caption="Sample Image")
        col1,col2,col3 = st.columns(3)
        with col2:
            image_path_3 = r"assets/images/phonemap1.jpg"
            image_3 = Image.open(image_path_3)
            st.image(image_3, caption="Sample Image")
    st.header("How to Use")
    st.markdown("""
    1. Navigation: Use the Option-Menu above to switch between the main sections: Home, State Wise Analysis, Interactive Map, and District Wise Analysis.
    2. Section Selection: Within each main section, use the radio buttons to toggle between User Analysis, Transaction Analysis, and Insurance Analysis.
    3. Interactive Elements: Utilize dropdowns and selection boxes to filter data by State, district, year, and quarter, providing you with the specific insights you need.
    We hope this platform enhances your understanding of PhonePe's impact across different regions and helps you leverage this data for strategic decision-making. Enjoy exploring the data!
    """)
    st.header("Getting Started")
    st.write("""
    Explore the power of data visualization and uncover actionable insights into PhonePe's performance and user behavior. Use the option-menu above to navigate through different sections, apply filters, and interact with visualizations to delve deeper into your datfun. Start exploring now!
    """)
if selected_page == "State-Wise Analysis":
    st.markdown("""State Wise Analysis section is to explore data at the State level. Select any State to view detailed user, transaction, and insurance metrics, helping you identify regional patterns and make data-driven decisions for specific States.""")
    selected_option= st.radio("Select:",["User Analysis","Transaction Analysis","Insurance Analysis"])
    if selected_option=="User Analysis":
        agg_user_data_path = r"data/data/aggregated/user/state/"
        Agg_Users = fun.agg_user_data(agg_user_data_path)
        Agg_Users['Year'] = Agg_Users['Year'].astype(str)
        Agg_Users["Percentage_of_Brand"] = Agg_Users["Percentage_of_Brand"].apply(lambda x: "{:.1f}%".format(x * 100) if pd.notnull(x) else None)
        col1, col2, col3,col4 = st.columns(4)
        with col1:
            year_filter_1 = st.selectbox("Select Year:", options=["All Years"] + Agg_Users["Year"].unique().tolist(), key="user_analysis_year")
        with col2:
            quarter_filter_1 = st.selectbox("Select Quarter:", options=["All Quarters"] + Agg_Users["Quarter"].unique().tolist(), key="user_analysis_quarter")
        with col3:
            State_filter_1 = st.selectbox("Select State:", options=["All States"] + Agg_Users["State"].unique().tolist(), key="user_analysis_State")
        with col4:
            brand_filter_1 = st.selectbox("Select Brand:", options=["All Brand"] + Agg_Users["Device_Brand"].unique().tolist(), key="user_analysis_brand")
        filtered_Agg_Users_1 = Agg_Users.copy()
        if State_filter_1 != "All States":
            filtered_Agg_Users_1 = filtered_Agg_Users_1[filtered_Agg_Users_1["State"] == State_filter_1]
        if year_filter_1 != "All Years":
            filtered_Agg_Users_1 = filtered_Agg_Users_1[filtered_Agg_Users_1["Year"] == year_filter_1]
        if quarter_filter_1 != "All Quarters":
            filtered_Agg_Users_1 = filtered_Agg_Users_1[filtered_Agg_Users_1["Quarter"] == quarter_filter_1]
        if brand_filter_1 != "All Brand":
            filtered_Agg_Users_1 = filtered_Agg_Users_1[filtered_Agg_Users_1["Device_Brand"] == brand_filter_1]
        st.info("The State-Wise User Details")
        filtered_Agg_Users_1['State'] = filtered_Agg_Users_1['State'].str.capitalize()
        st.dataframe(filtered_Agg_Users_1, use_container_width=True)
        if filtered_Agg_Users_1["Device_Brand"].isnull().any():
            st.error("Oops! Sorry. There is No Device Brand Details Available for Some Entries in the Filtered Datfun.")
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("TOP 10 StateS BY REGISTERED USERS COUNT")
        fun.get_top_States_with_highest_registered_users(conn)
        st.subheader("BOTTOM 10 StateS BY REGISTERED USERS COUNT")
        fun.get_bottom_States_with_lowest_registered_users(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("BRANDS USAGE BY State")
        fun.get_brand_counts1(conn)
        st.subheader("OVERALL BRANDS USAGE")
        fun.get_brand_counts2(conn)
        st.subheader("TOP 3 BRANDS MAXIMUM BRAND SHARE PERCENTAGE BY YEAR")
        fun.max_percentage_per_year(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("TOP 10 State BY APPS OPEN COUNT")
        fun.sum_app_opens_top_State(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("YEAR WISE HIGHEST REGISTRATION COUNT WITH State")
        fun.top_States_by_year(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader(" OVERALL YEAR WISE HIGHEST REGISTRATION COUNT")
        fun.top_States_by_year_1(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
    if selected_option == "Transaction Analysis":
        agg_transaction_data_path = r"D:\CAPSTONE\PHONEPE\CODE\SQLITE3\data\data\aggregated\transaction\state/"
        Agg_Trans = fun.agg_transaction_data(agg_transaction_data_path)
        Agg_Trans['Year'] = Agg_Trans['Year'].astype(str)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            year_filter_1 = st.selectbox("Select Year:", options=["All Years"] + Agg_Trans["Year"].unique().tolist(), key="user_analysis_year")
        with col2:
            quarter_filter_1 = st.selectbox("Select Quarter:", options=["All Quarters"] + Agg_Trans["Quarter"].unique().tolist(), key="user_analysis_quarter")
        with col3:
            State_filter_1 = st.selectbox("Select State:", options=["All States"] + Agg_Trans["State"].unique().tolist(), key="user_analysis_State")
        with col4:
            trans_type_filter_1 = st.selectbox("Select Transaction Type:",options=["All Types"] + Agg_Trans["Transaction_Type"].unique().tolist(),key="user_analysis_trans_type")
        filtered_Agg_Trans= Agg_Trans.copy()
        if State_filter_1 != "All States":
            filtered_Agg_Trans = filtered_Agg_Trans[filtered_Agg_Trans["State"] == State_filter_1]
        if year_filter_1 != "All Years":
            filtered_Agg_Trans = filtered_Agg_Trans[filtered_Agg_Trans["Year"] == year_filter_1]
        if quarter_filter_1 != "All Quarters":
            filtered_Agg_Trans = filtered_Agg_Trans[filtered_Agg_Trans["Quarter"] == int(quarter_filter_1)]
        if trans_type_filter_1 != "All Types":
            filtered_Agg_Trans = filtered_Agg_Trans[filtered_Agg_Trans["Transaction_Type"] == trans_type_filter_1]
        st.info("The State-Wise Transaction Detals")
        filtered_Agg_Trans['State'] = filtered_Agg_Trans['State'].str.capitalize()
        st.dataframe(filtered_Agg_Trans,use_container_width=True)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("TRANSACTION COUNT:")
        fun.get_top_10_States_with_highest_transaction_count(conn)
        fun.get_top_10_States_with_lowest_transaction_count(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("TRANSACTION AMOUNT:")
        fun.get_top_10_States_with_highest_transaction_amount(conn)
        fun.get_top_10_States_with_lowest_transaction_amount(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("TRANSACTION TYPE:")
        fun.transaction_type(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("YEARLY TRENDS IN TRANSACTION COUNTS")
        fun.total_count_highest_year(conn)
        st.subheader("YEARLY TRENDS IN TRANSACTION AMOUNTS")
        fun.total_amount_highest_year(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
    if selected_option == "Insurance Analysis":
        agg_insurance_data_path = r"D:\CAPSTONE\PHONEPE\CODE\SQLITE3\data\data\aggregated\insurance\state/"
        Agg_Ins = fun.agg_ins_data(agg_insurance_data_path)
        Agg_Ins['Year'] = Agg_Ins['Year'].astype(str)
        col1, col2, col3 = st.columns(3)
        with col1:
            year_filter_1 = st.selectbox("Select Year:", options=["All Years"] + Agg_Ins["Year"].unique().tolist(), key="user_analysis_year")
        with col2:
            quarter_filter_1 = st.selectbox("Select Quarter:", options=["All Quarters"] + Agg_Ins["Quarter"].unique().tolist(), key="user_analysis_quarter")
        with col3:
            State_filter_1 = st.selectbox("Select State:", options=["All States"] + Agg_Ins["State"].unique().tolist(), key="user_analysis_State")
        filtered_Agg_Ins= Agg_Ins.copy()
        if State_filter_1 != "All States":
            filtered_Agg_Ins = filtered_Agg_Ins[filtered_Agg_Ins["State"] == State_filter_1]
        if year_filter_1 != "All Years":
            filtered_Agg_Ins = filtered_Agg_Ins[filtered_Agg_Ins["Year"] == year_filter_1]
        if quarter_filter_1 != "All Quarters":
            filtered_Agg_Ins = filtered_Agg_Ins[filtered_Agg_Ins["Quarter"] == int(quarter_filter_1)]
        st.info("The State-Wise Insurance Details")
        filtered_Agg_Ins['State'] = filtered_Agg_Ins['State'].str.capitalize()
        st.dataframe(filtered_Agg_Ins,use_container_width=True)
        st.markdown('<hr>', unsafe_allow_html=True)
        col1, col2= st.columns(2)
        with col1 :
            st.subheader("State RANKINGS: INSURANCE COUNTS")
            fun.highest_ins_count(conn)
        with col2 :
            st.subheader("State RANKINGS: INSURANCE AMOUNTS")
            fun.highest_ins_amount(conn)
        st.markdown('<hr>', unsafe_allow_html=True)
        col1, col2= st.columns(2)
        with col1 :
            fun.lowest_ins_count(conn)
            st.markdown('<hr>', unsafe_allow_html=True)
        with col2:
            fun.lowest_ins_amount(conn)
            st.markdown('<hr>', unsafe_allow_html=True)

if selected_page == "Interactive Map Viewer":
    st.markdown("""Our Interactive Map feature allows you to visualize the data geographically. This visual representation helps in identifying regional disparities, growth opportunities, and areas needing attention. You can switch between User Analysis, Transaction Analysis, and Insurance Analysis to see different aspects of the data on the map.""")
    selected_option= st.radio("Select:",["User Analysis","Transaction Analysis","Insurance Analysis"])
    col1,col2,col3 = st.columns([1,1,4])
    if selected_option == "Insurance Analysis":
        with col1:
            filter_by_year = st.selectbox("Filter By Year :", ["2018", "2019", "2020", "2021", "2022", "2023", "2024"], key="year_filter")
            quarter_filter = st.selectbox("Select Quarter:", ["1", "2", "3", "4"], key="quarter_filter")
            st.info("Please Select Year and Quarter From 2020-2nd")
    else:
        with col1:
            filter_by_year = st.selectbox("Filter By Year :", ["2018", "2019", "2020", "2021", "2022", "2023", "2024"], key="year_filter")
            quarter_filter = st.selectbox("Select Quarter:", ["1", "2", "3", "4"], key="quarter_filter")
    geojson_path =r"D:\CAPSTONE\PHONEPE\india-State.geojson"
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    conn = fun.create_connection()
    if selected_option=="User Analysis":
        map_user_data_path = r"D:\CAPSTONE\PHONEPE\CODE\SQLITE3\data\data\map\user\state/"
        Map_User = fun.map_user_data(map_user_data_path)
        Map_User['Year'] = Map_User['Year'].astype(str)
        filtered_Map_User = Map_User.copy()
        filtered_Map_User['State'] = filtered_Map_User['State'].str.capitalize()
        df = fun.fetch_data_map_user(conn,filter_by_year, quarter_filter)
        fig = px.choropleth(df, 
                        geojson=geojson_data, 
                        locations="State", 
                        featureidkey="properties.NAME_1",
                        color="avg_registered_users", 
                        color_continuous_scale="Sunsetdark",
                        range_color=(df["avg_registered_users"].min(), df["avg_registered_users"].max()),
                        hover_name="State",
                        hover_data={"State": True, "avg_registered_users": True, "avg_app_opens": True}, 
                        title="Average Registered Users",
                        labels={"avg_registered_users": "Avg Registered Users", "avg_app_opens": "Avg App Opens"},width =1000,height=600)
        fig.update_geos(fitbounds="locations", visible=False)
        with col3:
            st.plotly_chart(fig,use_container_width=True)
    if selected_option == "Transaction Analysis":
        map_trans_data_path = r"D:\CAPSTONE\PHONEPE\CODE\SQLITE3\data\data\map\transaction\state"
        Map_Trans = fun.map_transaction_data(map_trans_data_path)
        filtered_Map_Trans = Map_Trans.copy()
        filtered_Map_Trans['State'] = filtered_Map_Trans['State'].str.capitalize()
        df1 = fun.fetch_data_map_trans(conn,filter_by_year, quarter_filter)
        fig1 = px.choropleth(df1, geojson=geojson_data, locations="State", featureidkey="properties.NAME_1",
                    color="Avg_Transaction_Count", color_continuous_scale="Sunsetdark",
                    range_color=(df1["Avg_Transaction_Count"].min(), df1["Avg_Transaction_Count"].max()),
                    hover_name="State",hover_data={"State": True, "Avg_Transaction_Count": True, "Avg_Total_Transaction_Amount": True}, 
                    title="Average Transaction ",
                    labels={"Avg_Transaction_Count": "Avg Transaction Count", "Avg_Total_Transaction_Amount": "Avg Transaction Amount"},width =1000,height=600)
        fig1.update_geos(fitbounds="locations", visible=False)
        with col3:
            st.plotly_chart(fig1,use_column_width=True)
    if selected_option == "Insurance Analysis":
        if (filter_by_year in {2020} and quarter_filter < 2) or (filter_by_year in {2018, 2019} and quarter_filter <=4) :
            st.info("Please Select Year and Quarter From 2020-2nd")
        else:
            map_ins_data_path = r"D:\CAPSTONE\PHONEPE\CODE\SQLITE3\data\data\map\insurance\state/"
            try:
                Map_Ins = fun.map_ins_data(map_ins_data_path)
                filtered_Map_Ins = Map_Ins.copy()
                filtered_Map_Ins['State'] = filtered_Map_Ins['State'].str.capitalize()
                df2 = fun.fetch_data_map_ins(conn, filter_by_year, quarter_filter)
                if not df2.empty:
                    fig2 = px.choropleth(df2, geojson=geojson_data, locations="State", featureidkey="properties.NAME_1",
                        color="Avg_Total_Count", 
                        color_continuous_scale="Sunsetdark",
                        range_color=(df2["Avg_Total_Count"].min(), df2["Avg_Total_Count"].max()),
                        hover_name="State",
                        hover_data={"State": True, "Avg_Total_Count": True, "Avg_Total_Amount": True}, 
                        title="Average Insurance",
                        labels={"Avg_Total_Count": "Avg Total Insurance Count", "Avg_Total_Amount": "Avg Total Insurance Amount"},width =1000,height=600)
                    fig2.update_geos(fitbounds="locations", visible=False)
                    with col3:
                        st.plotly_chart(fig2, use_column_width=True)
                else:
                    st.write("No data available for the selected filters.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
if selected_page == "District-Wise Analysis":
    st.markdown("""Dive deeper with the District Wise Analysis section. This feature provides granular insights at the district level, allowing for more localized analysis and understanding. This is particularly useful for planning district-specific strategies and interventions.""")
    selected_option= st.radio("Select:",["User Analysis","Transaction Analysis","Insurance Analysis"])
    if selected_option == "User Analysis":
        top_user_data_district_path = r"D:\CAPSTONE\PHONEPE\CODE\SQLITE3\data\data\top\user\state/"
        Top_User_District = fun.top_user_district_data(top_user_data_district_path)
        col1, col2, col3,col4 = st.columns(4)
        with col1:
            year_filter_1 = st.selectbox("Select Year:", options=["All Years"] + Top_User_District["Year"].unique().tolist(), key="user_analysis_year")
        with col2:
            quarter_filter_1 = st.selectbox("Select Quarter:", options=["All Quarters"] + Top_User_District["Quarter"].unique().tolist(), key="user_analysis_quarter")
        with col3:
            State_filter_1 = st.selectbox("Select State:", options=["All States"] + Top_User_District["State"].unique().tolist(), key="user_analysis_State")
        with col4:
            district_filter_1 = st.selectbox("Select District:", options=["All District"] + Top_User_District["District"].unique().tolist(), key="user_analysis_district")
        filtered_Top_Users = Top_User_District.copy()
        if State_filter_1 != "All States":
            filtered_Top_Users = filtered_Top_Users[filtered_Top_Users["State"] == State_filter_1]
        if year_filter_1 != "All Years":
            filtered_Top_Users = filtered_Top_Users[filtered_Top_Users["Year"] == year_filter_1]
        if quarter_filter_1 != "All Quarters":
            filtered_Top_Users = filtered_Top_Users[filtered_Top_Users["Quarter"] == int(quarter_filter_1)]
        if district_filter_1 != "All District":
            filtered_Top_Users = filtered_Top_Users[filtered_Top_Users["District"] == district_filter_1]
        st.info("The District-Wise User Details")
        filtered_Top_Users['State'] = filtered_Top_Users['State'].str.capitalize()
        filtered_Top_Users['District'] = filtered_Top_Users['District'].str.capitalize()
        st.dataframe(filtered_Top_Users,use_container_width=True)  
        col1,col2,col3,col4,col5 = st.columns([1,1,3,1,1])
        with col3:
            ques = st.selectbox("Registered Users", [
                        'District With Highest No.of Users in All States',
                        'Top 10 District With Highest No.of Users All over India',
                        'District With Lowest No.of Users in All States',
                        'Top 10 District With Lowest No.of Users All over India',
                        'District With Highest No.of Users in All Years with their State',
                        'District With Lowest No.of Users in All Years with their State'])
            if ques == 'District With Highest No.of Users in All States':
                fun.get_district_with_highest_users_in_States(conn)
            elif ques == 'Top 10 District With Highest No.of Users All over India':
                fun.get_top_10_districts_highest_users_all_over_india(conn)
            elif ques == 'District With Lowest No.of Users in All States':
                fun.get_district_with_lowest_users_in_States(conn)
            elif ques == 'Top 10 District With Lowest No.of Users All over India':
                fun.get_top_10_districts_lowest_users_all_over_india(conn)
            elif ques == 'District With Highest No.of Users in All Years with their State':
                fun.get_top_districts_with_highest_registered_users_in_all_year(conn)
            elif ques == 'District With Lowest No.of Users in All Years with their State':
                fun.get_top_districts_with_lowest_registered_users_in_all_year(conn)
    if selected_option == "Transaction Analysis":
        top_transaction_district_data_path = r"D:\CAPSTONE\PHONEPE\CODE\SQLITE3\data\data\top\transaction\state/"
        Top_Trans_District = fun.top_transaction_district_data(top_transaction_district_data_path)
        col1, col2, col3 = st.columns(3)
        with col1:
            year_filter_1 = st.selectbox("Select Year:", options=["All Years"] + Top_Trans_District["Year"].unique().tolist(), key="user_analysis_year")
        with col2:
            quarter_filter_1 = st.selectbox("Select Quarter:", options=["All Quarters"] + Top_Trans_District["Quarter"].unique().tolist(), key="user_analysis_quarter")
        with col3:
            State_filter_1 = st.selectbox("Select State:", options=["All States"] + Top_Trans_District["State"].unique().tolist(), key="user_analysis_State")
        filtered_Top_Trans = Top_Trans_District.copy()
        if State_filter_1 != "All States":
            filtered_Top_Trans = filtered_Top_Trans[filtered_Top_Trans["State"] == State_filter_1]
        if year_filter_1 != "All Years":
            filtered_Top_Trans = filtered_Top_Trans[filtered_Top_Trans["Year"] == year_filter_1]
        if quarter_filter_1 != "All Quarters":
            filtered_Top_Trans = filtered_Top_Trans[filtered_Top_Trans["Quarter"] == int(quarter_filter_1)]
        st.info("The District-Wise Transaction Details")
        filtered_Top_Trans['State'] = filtered_Top_Trans['State'].str.capitalize()
        st.dataframe(filtered_Top_Trans,use_container_width=True)  
        col1,col2, = st.columns(2)
        with col1:
            ques1 = st.selectbox("Transaction Count", [
                        'District With Highest Transaction Count in All States',
                        'Top 5 District With Highest Transaction Count All over India',
                        'District With Lowest Transaction Count in All States',
                        'Top 5 District With Lowest Transaction Count All over India',
                        'Highest Transaction Count All Years',
                        'Lowest Transaction Count All Years'])
            if ques1 == 'District With Highest Transaction Count in All States':
                fun.get_highest_transaction_count_all_States(conn)
            elif ques1 == 'Top 5 District With Highest Transaction Count All over India':
                fun.get_top5_highest_transaction_count(conn)
            elif ques1 == 'District With Lowest Transaction Count in All States':
                fun.get_lowest_transaction_count_all_States(conn)
            elif ques1 == 'Top 5 District With Lowest Transaction Count All over India':
                fun.get_top5_lowest_transaction_count(conn)
            elif ques1 == 'Highest Transaction Count All Years':
                fun.get_highest_transaction_count_all_years(conn)
            elif ques1 == 'Lowest Transaction Count All Years':
                fun.get_lowest_transaction_count_all_years(conn)
        with col2:
            query = st.selectbox("Transaction Amount",['District With Highest Transaction Amount in All States',
                    'Top 5 District With Highest Transaction Amount All over India',
                    'District With Lowest Transaction Amount in All States',
                    'Top 5 District With Lowest Transaction Amount All over India',
                    'Highest Transaction Amount All Years',
                    'Lowest Transaction Amount All Years'])
            if query == 'District With Highest Transaction Amount in All States':
                fun.get_highest_transaction_amount_all_States(conn)
            elif query == 'Top 5 District With Highest Transaction Amount All over India':
                fun.get_top5_highest_transaction_amount(conn)
            elif query == 'District With Lowest Transaction Amount in All States':
                fun.get_lowest_transaction_amount_all_States(conn)
            elif query == 'Top 5 District With Lowest Transaction Amount All over India':
                fun.get_top5_lowest_transaction_amount(conn)
            elif query == 'Highest Transaction Amount All Years':
                fun.get_highest_transaction_amount_all_years(conn)
            elif query == 'Lowest Transaction Amount All Years':
                fun.get_lowest_transaction_amount_all_years(conn)
    if selected_option == "Insurance Analysis":
        top_insurance_district_data_path = r"D:\CAPSTONE\PHONEPE\CODE\SQLITE3\data\data\top\insurance\state/"
        Top_Ins_District = fun.top_ins_dist_data(top_insurance_district_data_path)
        col1, col2, col3 = st.columns(3)
        with col1:
            year_filter_1 = st.selectbox("Select Year:", options=["All Years"] + Top_Ins_District["Year"].unique().tolist(), key="user_analysis_year")
        with col2:
            quarter_filter_1 = st.selectbox("Select Quarter:", options=["All Quarters"] + Top_Ins_District["Quarter"].unique().tolist(), key="user_analysis_quarter")
        with col3:
            State_filter_1 = st.selectbox("Select State:", options=["All States"] + Top_Ins_District["State"].unique().tolist(), key="user_analysis_State")
        filtered_Top_Ins = Top_Ins_District.copy()
        if State_filter_1 != "All States":
            filtered_Top_Ins = filtered_Top_Ins[filtered_Top_Ins["State"] == State_filter_1]
        if year_filter_1 != "All Years":
            filtered_Top_Ins = filtered_Top_Ins[filtered_Top_Ins["Year"] == year_filter_1]
        if quarter_filter_1 != "All Quarters":
            filtered_Top_Ins = filtered_Top_Ins[filtered_Top_Ins["Quarter"] == int(quarter_filter_1)]
        st.info("The District-Wise Transaction Details")
        filtered_Top_Ins['State'] = filtered_Top_Ins['State'].str.capitalize()
        st.dataframe(filtered_Top_Ins,use_container_width=True)  
        col1,col2=st.columns(2)
        with col1:
            ques = st.selectbox("Insurance Count", [
                    'Top 10 District With Highest Insurance Count in All India',
                    'Top 10 District With Lowest Insurance Count All over India'])
            if ques == 'Top 10 District With Highest Insurance Count in All India':
                fun.highest_ins_count_1(conn)
            elif ques == 'Top 10 District With Lowest Insurance Count All over India':
                fun.lowest_ins_count_1(conn)
        with col2:
            ques = st.selectbox("Insurance Amount", [
                    'Top 10 District With Highest Insurance Amount in All India',
                    'Top 10 District With Lowest Insurance Amount All over India'])
            if ques == 'Top 10 District With Highest Insurance Amount in All India':
                fun.highest_ins_amount_1(conn)
            elif ques == 'Top 10 District With Lowest Insurance Amount All over India':
                fun.lowest_ins_amount_1(conn)
if selected_page == "Insights":
    st.subheader("Statewise Summary")
    col1,col2 = st.columns(2)
    with col1:
        st.success("**__Maharashtra holds the highest number of Registered Users, App Opens, and Transaction Counts across ALL YEARS, securing the FIRST place in these categories.__**")
        st.success("**__TELANGANA has the Highest Transaction amount.__**")
    with col2:
        st.success("**__KARNATAKA has the Highest Insurance Count and Insurance Amount.__**")
        st.success("**__TAMILNADU has Consistently Ranked among the TOP 10 States in Registered Users, App Opens, Transaction Amount, Insurance Count, and Insurance Amount.__**")
    st.error("**__LAKSHWADEEP has the Lowest Metrics in All Categories.__**")
    st.subheader("Brand Analysis Report")
    st.success("**__XIAOMI | SAMSUNG | VIVO | OPPO are the Most Used Brands.__**")
    st.subheader("Districtwise Summary")
    col1,col2 = st.columns(2)
    with col1:
        st.success("**__BANGALORE URBAN has the Highest Number of Registered Users, Transaction Count, Transaction Amount, Insurance Count, and Insurance Amount in all years.__**")
    with col2:
        st.warning("**__TRICHY has the lowest usage in Tamil Nadu, while CHENNAI has the highest.__**")
    st.subheader("Overall Summary")
    col1,col2 = st.columns(2)
    with col1:
        st.info("**__The SOUTHERN AND CENTRAL PART of India has the Highest Usage of PhonePe.__**")
        st.info("**__The NORTH AND WEST PART of India has the Lowest Usage of PhonePe.__**")
    with col2:
        st.info("**__2023 has the Highest Registered Count till now, Nearly 72 Billion.__**")
        st.info("**__Registered Users Jumped from 2 trillion in 2021 to 10 trillion by 2023.__**")