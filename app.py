from dotenv import load_dotenv
load_dotenv() ## load all the environment variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name TSHIRT and has the following columns - BRAND, COLOUR, 
    SIZE, PRICE, STOCK_QUANTITY \n\nFor example,
    \nExample 1 - How much is the price of the inventory for all small size t-shirts? 
    the SQL command will be something like this SELECT SUM(PRICE*STOCK_QUANTITY) FROM TSHIRT WHERE SIZE="S";
    \nExample 2 - How many t-shirts do we have left for nike in medium size and blue color? 
    the SQL command will be something like this SELECT STOCK_QUANTITY FROM TSHIRT WHERE BRAND="Nike" AND COLOUR="Blue" AND SIZE="M
    \nExample 3 - How many red color adidas's t shirts we have available?
    the SQL command will be something like this SELECT SUM(STOCK_QUANTITY) FROM TSHIRT WHERE BRAND = "Adidas" AND COLOUR = "Red"
    \nExample 4 - How many adidas tshirts are available?
    the SQL command will be something like this SELECT SUM(STOCK_QUANTITY) FROM TSHIRT WHERE BRAND = "Adidas"
    also the sql code should not have ``` in beginning or end and sql word in output

    """
]
prompt.extend([
    """
    What is the total stock quantity for all t-shirts?
    """,
    """
    How many t-shirts do we have in stock?
    """,
    """
    Show me all available t-shirt sizes.
    """,
    """
    What is the total price of all t-shirts in the inventory?
    """,
    """
    How many t-shirts of each color do we have?
    """,
    """
    How many t-shirts of each size do we have?
    """,
    """
    Show me the available brands of t-shirts.
    """
])

## Streamlit App
st.set_page_config(page_title="IntelliStock")
st.title("IntelliStock: Your AI buddy for Inventory Solutions")

st.markdown("<h5>Enter your question:</h5>", unsafe_allow_html=True)
question = st.text_input("")
submit = st.button("Submit")

if submit:
    response = get_gemini_response(question, prompt)
    response = read_sql_query(response ,"Tshirt.db")
    
    st.subheader("Results:")
    if response:
        if question.lower().startswith("how many") and "brands" in question.lower():
            num_brands = response[0][0]
            st.write(f"<span style='font-size:20px'>There are in total {num_brands} brands.</span>", unsafe_allow_html=True)  # Format the response for counting brands
        elif "price" in question.lower() and "inventory" in question.lower():
            total_price = response[0][0]
            st.write(f"<span style='font-size:20px'>The total price of the inventory is Rs.{total_price}.</span>", unsafe_allow_html=True)  # Format the response for inventory price
        elif "how much is the price of" in question.lower():
            brand_name = question.split("price of ")[1].capitalize()  # Extracting the brand name from the question
            query = f"SELECT PRICE FROM TSHIRT WHERE BRAND = '{brand_name}'"  # SQL query to fetch the price of the specified brand
            response = read_sql_query(query, "Tshirt.db")  # Execute the SQL query to fetch the price
            if response:
                price = response[0][0]
                st.write(f"<span style='font-size:20px'>The price of {brand_name} t-shirt is Rs.{price}.</span>", unsafe_allow_html=True)  # Format the response with the queried brand name and price
            else:
                st.write(f"<span style='font-size:20px'>No price found for {brand_name}.</span>", unsafe_allow_html=True)
        elif "total stock quantity of t-shirts" in question.lower():
            query = "SELECT SUM(STOCK_QUANTITY) FROM TSHIRT"  # SQL query to fetch the total stock quantity of all t-shirts
            response = read_sql_query(query, "Tshirt.db")  # Execute the SQL query to fetch the total stock quantity
            if response:
                total_stock_quantity = response[0][0]
                if total_stock_quantity:
                    st.write(f"<span style='font-size:20px'>The total stock quantity of t-shirts is {total_stock_quantity}.</span>", unsafe_allow_html=True)  # Display the total stock quantity of all t-shirts
                else:
                    st.write("<span style='font-size:20px'>No total stock quantity found for t-shirts.</span>", unsafe_allow_html=True)  # If no total stock quantity is found in the database for t-shirts
            else:
                st.write("<span style='font-size:20px'>No total stock quantity found for t-shirts.</span>", unsafe_allow_html=True)  # If no total stock quantity is found in the database for t-shirts
        elif "what is the price of" in question.lower():
            brand_name = question.split("price of ")[1].capitalize()  # Extracting the brand name from the question
            total_price = response[0][0]
            st.write(f"<span style='font-size:20px'>The price of {brand_name} t-shirt is Rs.{total_price}.</span>", unsafe_allow_html=True)  # Format the response with the queried brand name
        elif "how many" in question.lower() and "left" in question.lower():
            stock_quantity = response[0][0]
            st.write(f"<span style='font-size:20px'>There are {stock_quantity} items left.</span>", unsafe_allow_html=True)  # Format the response for items left
        elif "how many" in question.lower() and "available" in question.lower():
            brand_name = question.split()[2]  # Extracting the brand name from the question
            num_available = response[0][0]
            st.write(f"<span style='font-size:20px'>There are {num_available} {brand_name.capitalize()} t-shirts available.</span>", unsafe_allow_html=True)  # Format the response with the queried brand name
        elif "what colours are available in" in question.lower():
            brand_name = question.split("in ")[1].capitalize()  # Extracting the brand name from the question
            query = f"SELECT DISTINCT COLOUR FROM TSHIRT WHERE BRAND = '{brand_name}'"  # SQL query to fetch distinct colors for the specified brand
            response = read_sql_query(query, "Tshirt.db")  # Execute the SQL query to fetch the colors
            if response:
                colors = [row[0] for row in response]  # Extracting the colors from the response
                if colors:
                    colors_text = ", ".join(colors)  # Joining the colors into a comma-separated string
                    st.write(f"<span style='font-size:20px'>The available colours for {brand_name} are : {colors_text}.</span>", unsafe_allow_html=True)  # Display all available colors
                else:
                    st.write(f"<span style='font-size:20px'>No colours found for {brand_name}.</span>", unsafe_allow_html=True)  # If no colors are found in the database for the specified brand
            else:
                st.write(f"<span style='font-size:20px'>No colours found for {brand_name}.</span>", unsafe_allow_html=True)  # If no colors are found in the database for the specified brand
        elif "how much stock is left in" in question.lower():
            brand_name = question.split("in ")[1].capitalize()  # Extracting the brand name from the question
            query = f"SELECT SUM(STOCK_QUANTITY) FROM TSHIRT WHERE BRAND = '{brand_name}'"  # SQL query to fetch the total stock quantity for the specified brand
            response = read_sql_query(query, "Tshirt.db")  # Execute the SQL query to fetch the stock quantity
            if response:
                stock_quantity = response[0][0]
                st.write(f"<span style='font-size:20px'>The stock quantity left in {brand_name} is: {stock_quantity}.</span>", unsafe_allow_html=True)  # Display the stock quantity for the specified brand with increased font size
            else:
                st.write(f"<span style='font-size:20px'>No stock quantity found for {brand_name}.</span>", unsafe_allow_html=True)  # If no stock quantity is found in the database for the specified brand with increased font size
        elif "total stock price of" in question.lower():
            brand_name = question.split("of ")[1].capitalize()  # Extracting the brand name from the question
            query = f"SELECT SUM(STOCK_QUANTITY * PRICE) FROM TSHIRT WHERE BRAND = '{brand_name}'"  # SQL query to fetch the total stock price for the specified brand
            response = read_sql_query(query, "Tshirt.db")  # Execute the SQL query to fetch the total stock price
            if response:
                total_stock_price = response[0][0]
                if total_stock_price:
                    st.write(f"<span style='font-size:20px'>The total stock price of {brand_name} is Rs.{total_stock_price}.</span>", unsafe_allow_html=True)  # Display the total stock price for the specified brand
                else:
                    st.write(f"<span style='font-size:20px'>No total stock price found for {brand_name}.</span>", unsafe_allow_html=True)  # If no total stock price is found in the database for the specified brand
            else:
                st.write(f"<span style='font-size:20px'>No total stock price found for {brand_name}.</span>", unsafe_allow_html=True)  # If no total stock price is found in the database for the specified brand
        else:
            result_text = '\n'.join([', '.join(map(str, row)) for row in response])  # Joining results into text format
            st.write(result_text)  # Displaying the result text
    else:
        st.write("<span style='font-size:20px'>No results found.</span>", unsafe_allow_html=True)