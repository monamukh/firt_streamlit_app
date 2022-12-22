import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites ')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale Spinach and Rocket Smoothie')
streamlit.text(' 🐔 Hard-bolied Free-Range Egg') 
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create repetable code (function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"  + fruit_choice) 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    
#New Section to display api response
streamlit.header("Fruityvice Fruit Advice!")
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)  
      
except URLError as e:
    streamlit.error()
    
streamlit.write('The user entered ', fruit_choice)
#import requests

#streamlit.text(fruityvice_response.json()) # writes data to screen
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"  + fruit_choice) 
#normalize json response
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#puts the normalize datainto table
#streamlit.dataframe(fruityvice_normalized)

#don't run anything past here   
#streamlit.stop()
#import snowflake.connector

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("select * from fruit_load_list") 
#my_data_row = my_cur.fetchone()
#my_data_row = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
#streamlit.text("The fruit load list contains:")
#streamlit.text(my_data_row)
#streamlit.dataframe(my_data_row)
streamlit.header("The fruit load list contains:")
#Snowflake-related-function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()  
 
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    streamlit.dataframe(my_data_row)
    

#add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
#streamlit.write('Thanks for adding ', add_my_fruit)
#my_cur.execute("insert into fruit_load_list values('from streamlit')") 

#Allow end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values('from streamlit')") 
         return  "Thanks for adding" + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like to add?')    
if streamlit.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)     
    
