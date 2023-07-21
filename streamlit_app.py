import streamlit
streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list)

#Choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

#We'll add a user interactive widget called a Multi-select that will allow users to pick the fruits they want in their smoothies.
# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
#pre-populate the list to set an example for the customer
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#We'll ask our app to put the list of selected fruits into a variable called fruits_selected. 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#Then, we'll ask our app to use the fruits in our fruits_selected list to pull rows from the full data set (and assign that data to a variable called fruits_to_show). 
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
#Finally, we'll ask the app to use the data in fruits_to_show in the dataframe it displays on the page. 
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
#ask user for input, default to Kiwi fruit
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#change to split out fruit choice
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
#change to use variable from user input
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#http response
#streamlit.text(fruityvice_response)

#json output
#streamlit.text(fruityvice_response.json()) # just writes the data to the screen

# take the json response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it to the screen
streamlit.dataframe(fruityvice_normalized)

#use the streamlit secret file to connect
import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
#my_data_row = my_cur.fetchone()
#fetch all rows
my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
#streamlit.text("The fruit load list contains:")
#streamlit.text(my_data_row)
#changed to dataframe for nicer view
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#ask user for input to add fruit to the list, no default
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
#streamlit.write('The user entered ', add_my_fruit)
streamlit.write('Thanks for adding ', add_my_fruit)

#this should fail, but go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")

