# packages :
import pandas as pd
import psycopg2
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json

                                   # creating tables :

#connecting to sql :
mydb = psycopg2.connect(host = "localhost",
                       user = "postgres",
                       port = "5432",
                       database = "Phonepe",
                       password = "1234"
                       )
cursor = mydb.cursor()

#agg transcation df :
cursor.execute("select * from aggregated_trans")
mydb.commit()
table1 = cursor.fetchall()

agg_trans_df = pd.DataFrame(table1, columns=('State', 'Year', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount'))

#agg user df :
cursor.execute("select * from aggregated_user")
mydb.commit()
table2 = cursor.fetchall()

agg_user_df = pd.DataFrame(table2, columns=('State', 'Year', 'Quarter', 'brand', 'Transaction_count', 'percentage'))

#map trans df :
cursor.execute("select * from map_trans")
mydb.commit()
table3 = cursor.fetchall()

map_trans_df = pd.DataFrame(table3, columns=('State', 'Year', 'Quarter', 'Districts', 'Transaction_count', 'Transaction_amount'))

#map user df :
cursor.execute("select * from map_user")
mydb.commit()
table4 = cursor.fetchall()
 
map_user_df = pd.DataFrame(table4, columns=('State', 'Year', 'Quarter', 'Districts', 'Registereduser', 'AppOpens'))

#top trans df :
cursor.execute("select * from top_trans")
mydb.commit()
table5 = cursor.fetchall()

top_trans_df = pd.DataFrame(table5, columns=('State', 'Year', 'Quarter', 'Pincode', 'Transaction_count', 'Transaction_amount'))

#top user df :
cursor.execute("select * from top_user")
mydb.commit()
table6 = cursor.fetchall()

top_user_df = pd.DataFrame(table6, columns=('State', 'Year', 'Quarter', 'Pincode', 'Registereduser'))

#aggregate transcation year wise :

def Transaction_amount_count_y(df, year):

    tacy = df[df["Year"] == year]
    tacy.reset_index(drop =True, inplace = True)

    tacyg = tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)
    
    return tacy

#aggregate transcation quarter wise :
                                                             # Bar plots :
        
def Transaction_amount_count_y_q(df, Quarteryear):
    tacy = df[df["Quarter"] == Quarteryear]
    tacy.reset_index(drop =True, inplace = True)

    tacyg = tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2,col3 = st.columns(3)
    with col1:
        fig_amount = px.bar(tacyg, x = "State", y = "Transaction_amount", title = f" YEAR {tacy['Year'].min()} QUARTER  {Quarteryear} TRANSACTION AMOUNT",
                            color_discrete_sequence = px.colors.sequential.RdBu, height = 400, width = 400)
        st.plotly_chart(fig_amount)
    with col3:
        fig_count = px.bar(tacyg, x = "State", y = "Transaction_count", title = f" YEAR {tacy['Year'].min()} QUARTER {Quarteryear} TRANSACTION COUNT",
                        color_discrete_sequence = px.colors.sequential.Agsunset, height = 400, width = 400)
        st.plotly_chart(fig_count)

                                                          
                                                        #india geo map:
        
    col1, col2,col3 = st.columns(3)
    with col1:
        url ="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        res =requests.get(url)
        coordinates = json.loads(res.content)

        st_names = []
        for i in coordinates["features"]:
            st_names.append(i["properties"]["ST_NM"])

        st_names.sort()
        fig_ind1 = px.choropleth(tacyg, geojson = coordinates, locations = "State", featureidkey = "properties.ST_NM",
                                color='Transaction_amount',
                                color_continuous_scale='Brwnyl',
                                range_color = (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name = "State",
                                title = f" YEAR {tacy['Year'].min()} QUARTER {Quarteryear} TRANSACTION AMOUNT", fitbounds = "locations", height = 700, width = 500,
                                )
        
        fig_ind1.update_geos(visible = False)
        st.plotly_chart(fig_ind1)

    with col3:

        fig_ind2 = px.choropleth(tacyg, geojson = coordinates, locations = "State", featureidkey = "properties.ST_NM",
                                color='Transaction_count',
                                color_continuous_scale='Brwnyl',
                                range_color = (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name = "State",
                                title = f" YEAR {tacy['Year'].min()} QUARTER {Quarteryear} TRANSACTION COUNT", fitbounds = "locations", height = 700, width = 500,
                                )
        
        fig_ind2.update_geos(visible = False)
        st.plotly_chart(fig_ind2)

    return tacy
    
#piechart for Aggregated transaction types :

def agg_trans_transaction_type(df, state):
    tacy = df[df["State"] == state]
    tacy.reset_index(drop =True, inplace = True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2,col3 = st.columns(3)
    with col1:
        fig_pie_1 = px.pie(data_frame = tacyg, names = "Transaction_type", values =  "Transaction_amount", 
                        width = 500, title = f"{state.upper()} TRANSACTION AMOUNT", hole = 0.7)
        st.plotly_chart(fig_pie_1)

    with col3:
        fig_pie_2 = px.pie(data_frame = tacyg, names = "Transaction_type", values =  "Transaction_count", 
                        width = 500, title = f"{state.upper()} TRANSACTION COUNT", hole = 0.7)
        st.plotly_chart(fig_pie_2)

# Aggregated user :

def agg_user_plot(df, year):    
    aguy = df[df["Year"] == year]
    aguy.reset_index(drop =True, inplace = True)

    aguy_g = aguy.groupby("brand")[["Transaction_count"]].sum()
    aguy_g.reset_index(inplace = True)

    return aguy

#Agg transaction quarter wise :
def agg_user_plot_q(df, quarter):
    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop =True, inplace = True)

    aguyq_g = aguyq.groupby("brand")[["Transaction_count"]].sum()
    aguyq_g.reset_index(inplace = True)

    fig_bar_2 = px.bar(aguyq_g, x = "brand", y = "Transaction_count", title = f"{quarter} QUARTER, BRANDS and TRANSACTION COUNT",
                        color_discrete_sequence = px.colors.sequential.Redor, width = 800)
    st.plotly_chart(fig_bar_2)
    return aguyq

#agg user brand and quarter wise line chart :
def agg_user_state(df, state):
    auy_q_state = df[df["State"] == state].head(10)
    auy_q_state.reset_index(drop = True, inplace = True)

    fig_line_1 = px.line(auy_q_state, x = "brand", y = "Transaction_count", hover_data = "percentage",
                        title = f"{state.upper()} TRANSACTION COUNT and PERCENTAGE VALUES of BRANDS", 
                        color_discrete_sequence = px.colors.sequential.Oryel_r, width = 1000,
                        markers = "True")


    st.plotly_chart(fig_line_1)

# map trans year wise:
        
def Map_Transaction_amount_count_y(df, year):
    mtacy = df[df["Year"] == year]
    mtacy.reset_index(drop =True, inplace = True)

    mtacyg = mtacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    mtacyg.reset_index(inplace = True)
    return mtacy

#barchart for map district types :

def map_trans_district(df, state):
    mdtacy = map_trans_df[map_trans_df["State"] == state]
    mdtacy.reset_index(drop =True, inplace = True)

    mdacyg = mdtacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    mdacyg.reset_index(inplace = True)

    
    fig_bar_1 = px.bar(mdacyg, x = "Transaction_amount", y = "Districts", 
                        orientation = "h", title = f"{state.upper()} DISTRICT WISE TRANSACTION AMOUNT",
                        color_discrete_sequence = px.colors.sequential.Redor,height = 850)
    st.plotly_chart(fig_bar_1)


    fig_bar_2 = px.bar(mdacyg, x = "Transaction_count", y = "Districts", 
                        orientation = "h", title = f"{state.upper()} DISTRICT WISE TRANSACTION COUNT",
                        color_discrete_sequence = px.colors.sequential.Greys,height = 850)
    st.plotly_chart(fig_bar_2)

#map user year wise :

def map_user_lineplot(df, year):    
    mpuy = df[df["Year"] == year]
    mpuy.reset_index(drop =True, inplace = True)

    mpuy_g = mpuy.groupby("State")[["Registereduser", "AppOpens"]].sum()
    mpuy_g.reset_index(inplace = True)

#map user quarter wise :

def map_user_lineplot_q(df, quarter):    
    mpuyq = df[df['Quarter'] == quarter]
    mpuyq.reset_index(drop =True, inplace = True)

    mpuyq_g = mpuyq.groupby("State")[["Registereduser", "AppOpens"]].sum()
    mpuyq_g.reset_index(inplace = True)

    figure_line_1 = px.line(mpuyq_g, x = "State", y = ["Registereduser", "AppOpens"],
                    title = f"{quarter} Quarter Registered user & AppOpens",
                    color_discrete_sequence = px.colors.sequential.Rainbow, 
                    width = 850, height = 750, markers = True)
    st.plotly_chart(figure_line_1)

    #map user district wise quarter :

def map_user_bar_q(df, state):
    mpduyq = df[df["State"] == state]
    mpduyq.reset_index(drop =True, inplace = True)

    col1, col2,col3 = st.columns(3)
    with col1:
        fig_map_bar_1 = px.bar(mpduyq, x = "Registereduser", y = "Districts", 
                            orientation = "h", title = f"{state.upper()} Registereduser",
                            color_discrete_sequence = px.colors.sequential.Redor, width = 500, height = 500)
        st.plotly_chart(fig_map_bar_1)

    with col3:
        fig_map_bar_2 = px.bar(mpduyq, x = "AppOpens", y = "Districts", 
                            orientation = "h", title = f"{state.upper()} AppOpens",
                            color_discrete_sequence = px.colors.sequential.Redor_r, width = 500, height = 500)
        st.plotly_chart(fig_map_bar_2)
    
#top transacton quarter wise:

def top_trans_bar_q(df, states):    
    tty_q = df[df["State"] == states]
    tty_q.reset_index(drop =True, inplace = True)

    col1, col2,col3 = st.columns(3)
    with col1:
        fig_top_bar_1 = px.bar(tty_q, x = "Quarter", y = "Transaction_amount", hover_data = "Pincode",
                                title = f"{states.upper()} QUARTER WISE TRANSACTION AMOUNT",
                                color_discrete_sequence = px.colors.sequential.YlGnBu, width = 500, height = 500)
        st.plotly_chart(fig_top_bar_1)

    with col3:
        fig_top_bar_2 = px.bar(tty_q, x = "Quarter", y = "Transaction_count", hover_data = "Pincode",
                                title = f"{states.upper()} QUARTER WISE TRANSACTION COUNT",
                                color_discrete_sequence = px.colors.sequential.Teal_r, width = 500, height = 500)
        st.plotly_chart(fig_top_bar_2)


# top user year wise:

def top_user_plot(df, year):    
   tuy = df[df["Year"] == year]
   tuy.reset_index(drop =True, inplace = True)

   tuy_g = tuy.groupby(["State", "Quarter"])[["Registereduser"]].sum()
   tuy_g.reset_index(inplace = True)

   fig_bar_1 = px.bar(tuy_g, x = "State", y = "Registereduser", title = f"{year} REGISTEREDUSER",
                  color = "Quarter", color_discrete_sequence = px.colors.sequential.Blugrn, width = 700,height = 600)
   st.plotly_chart(fig_bar_1)

   return tuy

#top user bar2 :

def top_user_plot_s(df, state):
    tuys = df[df["State"] == state]
    tuys.reset_index(drop =True, inplace = True)

    fig_top_s = px.bar(tuys, x = "Quarter", y = "Registereduser", title = f"{state.upper()} QUARTER & PINCODE WISE REGISTEREDUSER", hover_data = "Pincode", 
                    color = "Registereduser", color_continuous_scale = px.colors.sequential.haline_r, width = 700,height = 600)
    st.plotly_chart(fig_top_s)

#connecting to sql :

def topc_transamt(tb_name):
    mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "Phonepe",
                        password = "1234")
                        
    cursor = mydb.cursor()

#for transaction amount :
    #Ascending order :
    query1 = f'''select state,sum(transaction_amount) as transaction_amount
                from {tb_name}
                group by state
                order by transaction_amount limit(10)'''

    cursor.execute(query1)
    mydb.commit()
    tb1 = cursor.fetchall()

    df1 = pd.DataFrame(tb1, columns = ('States' ,'Transaction Amount'))

    fig_amount1 = px.bar(df1, x = "States", y = "Transaction Amount", title = "TRANSACTION AMOUNT FOR LEAST 10 STATES",
                            color_discrete_sequence = px.colors.sequential.RdBu_r, height = 500, width = 550)
    st.plotly_chart(fig_amount1)

    #Discending order :
    query2 = f'''select state,sum(transaction_amount) as transaction_amount
                from {tb_name}
                group by state
                order by transaction_amount desc limit(10)'''

    cursor.execute(query2)
    mydb.commit()
    tb2 = cursor.fetchall()

    df2 = pd.DataFrame(tb2, columns = ('States' ,'Transaction Amount'))

    fig_amount2 = px.bar(df2, x = "States", y = "Transaction Amount", title = "TRANSACTION AMOUNT FOR TOP 10 STATES",
                            color_discrete_sequence = px.colors.sequential.Sunsetdark, height = 500, width = 550)
    st.plotly_chart(fig_amount2)

    #Average order :
    query3 = f'''select state,avg(transaction_amount) as transaction_amount
                from {tb_name}
                group by state
                order by transaction_amount'''

    cursor.execute(query3)
    mydb.commit()
    tb3 = cursor.fetchall()

    df3 = pd.DataFrame(tb3, columns = ('States' ,'Transaction Amount'))

    fig_amount3 = px.bar(df3, x = "States", y = "Transaction Amount", title = "AVERAGE FOR TRANSACTION AMOUNT",
                            color_discrete_sequence = px.colors.sequential.Oranges, height = 700, width = 700)
    st.plotly_chart(fig_amount3)

#connecting to sql :

def topc_transcount(tb_name):
    mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "Phonepe",
                        password = "1234")
                        
    cursor = mydb.cursor()
#for transaction count :
    #Ascending order :
    query1 = f'''select state,sum(transaction_count) as transaction_count
                from {tb_name}
                group by state
                order by transaction_count limit(10)'''

    cursor.execute(query1)
    mydb.commit()
    tb1 = cursor.fetchall()

    df1 = pd.DataFrame(tb1, columns = ('States' ,'Transaction Count'))

    fig_amount = px.bar(df1, x = "States", y = "Transaction Count", title = "TRANSACTION COUNT FOR LEAST 10 STATES",
                            color_discrete_sequence = px.colors.sequential.RdBu_r, height = 500, width = 550)
    st.plotly_chart(fig_amount)

    #Discending order :
    query2 = f'''select state,sum(transaction_count) as transaction_count
                from {tb_name}
                group by state
                order by transaction_count desc limit(10)'''

    cursor.execute(query2)
    mydb.commit()
    tb2 = cursor.fetchall()

    df2 = pd.DataFrame(tb2, columns = ('States' ,'Transaction Count'))

    fig_amount2 = px.bar(df2, x = "States", y = "Transaction Count", title = "TRANSACTION COUNT FOR TOP 10 STATES",
                            color_discrete_sequence = px.colors.sequential.Sunsetdark, height = 500, width = 550)
    st.plotly_chart(fig_amount2)

    #Average order :
    query3 = f'''select state,avg(transaction_count) as transaction_count
                from {tb_name}
                group by state
                order by transaction_count'''

    cursor.execute(query3)
    mydb.commit()
    tb3 = cursor.fetchall()

    df3 = pd.DataFrame(tb3, columns = ('States' ,'Transaction Count'))

    fig_amount3 = px.bar(df3, x = "States", y = "Transaction Count", title = "AVERAGE FOR TRANSACTION COUNT",
                            color_discrete_sequence = px.colors.sequential.Oranges, height = 700, width = 700)
    st.plotly_chart(fig_amount3)    

#connecting to sql :

def topc_regmp(tb_name, state):
    mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "Phonepe",
                        password = "1234")
                        
    cursor = mydb.cursor()
#for reg user of map user :
    #Ascending order :
    query1 = f'''select districts, sum(registereduser) as registereduser from {tb_name}
                where state = '{state}'
                group by districts
                order by registereduser limit(10)'''

    cursor.execute(query1)
    mydb.commit()
    tb1 = cursor.fetchall()

    df1 = pd.DataFrame(tb1, columns = ('Districts' ,'Registered User'))

    fig_amount = px.bar(df1, x = "Districts", y = "Registered User", title = "REGISTERED USER FOR LEAST 10 STATES",
                            color_discrete_sequence = px.colors.sequential.RdBu_r, height = 500, width = 550)
    st.plotly_chart(fig_amount)

    #Discending order :
    query2 = f'''select districts, sum(registereduser) as registereduser from {tb_name}
                where state = '{state}'
                group by districts
                order by registereduser desc limit(10)'''

    cursor.execute(query2)
    mydb.commit()
    tb2 = cursor.fetchall()

    df2 = pd.DataFrame(tb2, columns = ('Districts' ,'Registered User'))

    fig_amount2 = px.bar(df2, x = "Districts", y = "Registered User", title = "REGISTERED USER FOR TOP 10 STATES",
                            color_discrete_sequence = px.colors.sequential.Sunsetdark, height = 500, width = 550)
    st.plotly_chart(fig_amount2)

    #Average order :
    query3 = f'''select districts, avg(registereduser) as registereduser from {tb_name}
                where state = '{state}'
                group by districts
                order by registereduser'''

    cursor.execute(query3)
    mydb.commit()
    tb3 = cursor.fetchall()

    df3 = pd.DataFrame(tb3, columns = ('Districts' ,'Registered User'))

    fig_amount3 = px.bar(df3, x = "Districts", y = "Registered User", title = "AVERAGE FOR REGISTERED USER",
                            color_discrete_sequence = px.colors.sequential.Oranges, height = 700, width = 700)
    st.plotly_chart(fig_amount3)

#connecting to sql :

def topc_apomp(tb_name, state):
    mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "Phonepe",
                        password = "1234")
                        
    cursor = mydb.cursor()
#for APPOPEN :
    #Ascending order :
    query1 = f'''select districts, sum(appopens) as appopens from {tb_name}
                where state = '{state}'
                group by districts
                order by appopens limit(10)'''

    cursor.execute(query1)
    mydb.commit()
    tb1 = cursor.fetchall()

    df1 = pd.DataFrame(tb1, columns = ('Districts' ,'appopens'))

    fig_amount = px.bar(df1, x = "Districts", y = "appopens", title = "APPOPENS FOR LEAST 10 STATES",
                            color_discrete_sequence = px.colors.sequential.RdBu_r, height = 500, width = 550)
    st.plotly_chart(fig_amount)

    #Discending order :
    query2 = f'''select districts, sum(appopens) as appopens from {tb_name}
                where state = '{state}'
                group by districts
                order by appopens desc limit(10)'''

    cursor.execute(query2)
    mydb.commit()
    tb2 = cursor.fetchall()

    df2 = pd.DataFrame(tb2, columns = ('Districts' ,'appopens'))

    fig_amount2 = px.bar(df2, x = "Districts", y = "appopens", title = "APPOPENS FOR TOP 10 STATES",
                            color_discrete_sequence = px.colors.sequential.Sunsetdark, height = 500, width = 550)
    st.plotly_chart(fig_amount2)

    #Average order :
    query3 = f'''select districts, avg(appopens) as appopens from {tb_name}
                where state = '{state}'
                group by districts
                order by appopens'''

    cursor.execute(query3)
    mydb.commit()
    tb3 = cursor.fetchall()

    df3 = pd.DataFrame(tb3, columns = ('Districts' ,'appopens'))

    fig_amount3 = px.bar(df3, x = "Districts", y = "appopens", title = "AVERAGE FOR APPOPENS",
                            color_discrete_sequence = px.colors.sequential.Oranges, height = 700, width = 700)
    st.plotly_chart(fig_amount3)

#connecting to sql :

def topc_regmpusers(tb_name):
    mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "Phonepe",
                        password = "1234")
                        
    cursor = mydb.cursor()
#for REGISTER USER :
    #Ascending order :
    query1 = f'''select state,sum(registeredusers) as registeredusers from {tb_name}
                group by state
                order by registeredusers 
                limit 10;'''

    cursor.execute(query1)
    mydb.commit()
    tb1 = cursor.fetchall()

    df1 = pd.DataFrame(tb1, columns = ('State' ,'Registereduser'))

    fig_amount = px.bar(df1, x = "State", y = "Registereduser", title = "REGISTERED USER FOR LEAST 10 STATES",
                            color_discrete_sequence = px.colors.sequential.RdBu_r, height = 500, width = 550)
    st.plotly_chart(fig_amount)

    #Discending order :
    query2 = f'''select state,sum(registeredusers) as registeredusers from {tb_name}
                group by state
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query2)
    mydb.commit()
    tb2 = cursor.fetchall()

    df2 = pd.DataFrame(tb2, columns = ('State' ,'Registereduser'))

    fig_amount2 = px.bar(df2, x = "State", y = "Registereduser", title = "REGISTERED USER FOR TOP 10 STATES",
                            color_discrete_sequence = px.colors.sequential.Sunsetdark, height = 500, width = 550)
    st.plotly_chart(fig_amount2)

    #Average order :
    query3 = f'''select state,avg(registeredusers) as registeredusers from {tb_name}
                group by state
                order by registeredusers desc'''

    cursor.execute(query3)
    mydb.commit()
    tb3 = cursor.fetchall()

    df3 = pd.DataFrame(tb3, columns = ('State' ,'Registereduser'))

    fig_amount3 = px.bar(df3, x = "State", y = "Registereduser", title = "AVERAGE FOR REGISTERED USER",
                            color_discrete_sequence = px.colors.sequential.Oranges, height = 700, width = 700)
    st.plotly_chart(fig_amount3)

                                     #streamlit setup:
 
st.set_page_config(layout = "wide")
st.title(":violet[Phonepe] Pulse Data Visualization and Exploration")

with st.sidebar:
    select = option_menu("Main menu", ["Home", "Explore Data", "Top Charts"])

if select == "Home":
    
    st.header("PhonePe is a popular digital payments platform in India. Here are some key details about PhonePe")

    
    st.subheader(":orange[Ownership:]")
    st.divider()
    st.write("PhonePe was founded in December 2015 by Sameer Nigam, Rahul Chari, and Burzin Engineer. In 2016, it was acquired by Flipkart, an Indian e-commerce company, which is itself owned by Walmart.")
    st.subheader(":orange[Services:]")
    st.divider()
    st.write("PhonePe offers a wide range of services including mobile recharge, bill payments, money transfers, online shopping, and more. It allows users to link their bank accounts and make transactions securely.")
    st.subheader(":orange[UPI Integration:]")
    st.divider()
    st.write("One of its notable features is its integration with Unified Payments Interface (UPI), a real-time payment system in India. This allows users to make instant bank-to-bank transfers using their smartphones.")
    st.subheader(":orange[Wallet]")
    st.divider()
    st.write(" PhonePe also has a digital wallet feature, where users can store money and use it for various transactions. Additionally, users can earn rewards and cashback offers through transactions on the platform.")
    st.subheader(":orange[Partnerships:]")
    st.divider()
    st.write("PhonePe has partnered with various merchants and businesses to enable seamless transactions and offers cashback incentives to users for using PhonePe for payments at these partner outlets.")
    st.subheader(":orange[User Base:]")    
    st.write("As of recent data, PhonePe has a significant user base and is one of the leading digital payment platforms in India, competing closely with other players like Google Pay, Paytm, etc.")

elif select == "Explore Data":   
    col1, col2 = st.columns(2)
    with col1: 
        tab1,tab2,tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
   
    with tab1:
        method1 = st.selectbox("Select the method", ("Aggregated Transactions", "Aggregated Users"))
        if method1 ==  "Aggregated Transactions":
            col1, col2,col3 = st.columns(3)
            with col1:
                years = st.slider("Select the years" ,agg_trans_df["Year"].min(), agg_trans_df["Year"].max(), agg_trans_df["Year"].min())
            agg_tac_year = Transaction_amount_count_y(agg_trans_df, years)

            col1, col2, col3 = st.columns(3)
            with col1:
                quarters = st.slider("Select the quarter year" ,agg_tac_year["Quarter"].min(), agg_tac_year["Quarter"].max(), agg_tac_year["Quarter"].min())
            agg_tac_year_q = Transaction_amount_count_y_q(agg_tac_year, quarters)

            col1, col2, col3 = st.columns(3)
            with col1:
                state = st.selectbox("Select the State by Quarter year", agg_tac_year["State"].unique())
            agg_trans_transaction_type(agg_tac_year_q, state)   

        elif method1 ==  "Aggregated Users":
            col1, col2,col3 = st.columns(3)
            with col1:
                years = st.slider("Select the years" ,agg_user_df["Year"].min(), agg_user_df["Year"].max(), agg_user_df["Year"].min())
            agg_user_y = agg_user_plot(agg_user_df, years)

            col1, col2,col3 = st.columns(3)
            with col1:
                quarters = st.slider("Select the quarter" ,agg_user_y["Quarter"].min(), agg_user_y["Quarter"].max(), agg_user_y["Quarter"].min())
            agg_user_y_q = agg_user_plot_q(agg_user_y, quarters)

            col1, col2, col3 = st.columns(3)
            with col1:
                District = st.selectbox("Select the State by Quarter wise", agg_user_y_q["State"].unique())   
            map_trans_district(agg_user_y_q, District)
    with tab2:
        method2 = st.selectbox("Select the method", ["Map Transactions", "Map Users"])
        if method2 ==  "Map Transactions":
            col1, col2,col3 = st.columns(3)
            with col1:
                Year = st.slider("Select the year" ,map_trans_df["Year"].min(), map_trans_df["Year"].max(), map_trans_df["Year"].min())            
            map_tac_year = Map_Transaction_amount_count_y(map_trans_df, Year)

            col1, col2, col3 = st.columns(3)
            with col1:
                Quarter = st.selectbox("Select the year by Quarter", map_tac_year["Quarter"].unique())            
            map_tac_year_q = Transaction_amount_count_y_q(map_tac_year, Quarter)

            col1, col2, col3 = st.columns(3)
            with col1:
                States = st.selectbox("Select the State", map_tac_year["State"].unique())
            map_trans_district(map_tac_year_q, States)   

        elif method2 ==  "Map Users":
            col1, col2,col3 = st.columns(3)
            with col1:
                YEARs = st.slider("Select the year" ,map_user_df["Year"].min(), map_user_df["Year"].max(), map_user_df["Year"].min())
            map_user_y = map_user_lineplot(map_user_df, YEARs)

            col1, col2,col3 = st.columns(3)
            with col1:
                quart = st.slider("select the quarters" ,1,4,1)
            map_user_y_q = map_user_lineplot_q(map_user_df, quart)

            col1, col2,col3 = st.columns(3)
            with col1:
                states = st.selectbox("Select the state", map_user_df["State"].unique())
            map_user_bar_q(map_user_df, states)            

    with tab3:
        method3 = st.selectbox("Select the method", ["Top Transactions", "Top Users"])
        if method3 ==  "Top Transactions":
            col1, col2,col3 = st.columns(3)
            with col1:
                Year = st.slider("select the year" ,top_trans_df["Year"].min(), top_trans_df["Year"].max(), top_trans_df["Year"].min())            
            top_tac_year = Map_Transaction_amount_count_y(top_trans_df, Year)

            col1, col2,col3 = st.columns(3)
            with col1:
                quart = st.slider("Select the quarters" ,1,4,1)
            top_tac_year_q = Transaction_amount_count_y_q(top_tac_year, 3)

            col1, col2,col3 = st.columns(3)
            with col1:
                states = st.selectbox("Select the state ", top_trans_df["State"].unique())
            top_user_q = top_trans_bar_q(top_tac_year, states)


        elif method3 ==  "Top Users":
            col1, col2,col3 = st.columns(3)
            with col1:
                Year = st.slider("select the year" ,top_trans_df["Year"].min(), top_trans_df["Year"].max(), top_trans_df["Year"].min())            
            top_user_y = top_user_plot(top_user_df ,Year)

            col1, col2,col3 = st.columns(3)
            with col1:
                states = st.selectbox("select the state", top_user_df["State"].unique())
            top_user_plot_s(top_user_y, states)

elif select == "Top Charts":
    
    quest = st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Transaction",
                                                "2. Transaction Amount and Count of Map Transaction",
                                                "3. Transaction Amount and Count of Top Transaction",
                                                "4. Transaction Count of Aggregated User",
                                                "5. Register User of Map User",
                                                "6. App opens of map user",
                                                "7. Register User of Top User"
                                               ])
    if quest == "1. Transaction Amount and Count of Aggregated Transaction":
        topc_transamt("aggregated_trans")
        topc_transcount("aggregated_trans")

    elif quest == "2. Transaction Amount and Count of Map Transaction":
        topc_transamt("map_trans")
        topc_transcount("map_trans")

    elif quest == "3. Transaction Amount and Count of Top Transaction":
        topc_transamt("top_trans")
        topc_transcount("top_trans")

    elif quest == "4. Transaction Count of Aggregated User":
        topc_transcount("aggregated_User")

    elif quest == "5. Register User of Map User":
        state = st.selectbox("Select the states", map_user_df["State"].unique())
        topc_regmp("map_user", state)

    elif quest == "6. App opens of map user":
        state = st.selectbox("Select the states:", map_user_df["State"].unique())
        topc_apomp("map_user", state)    
    
    elif quest == "7. Register User of Top User":
        topc_regmpusers("top_user") 