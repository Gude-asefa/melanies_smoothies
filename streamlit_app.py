# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark import when_matched

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothies :cup_with_straw:")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)


name_on_order = st.text_input("Name on Smoothie", "Enter here")
st.write("Name on Smoothie will be : ", name_on_order)

#option = st.selectbox(
    #"What is your favorite fruit?",
   # ("banana", "strawberries", "peaches"),
#)

#st.write("Your favorite fruit is :", option)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)



options = st.multiselect(
    "CHOOSE UP  TO 5 INGREDIENTS: ",
     my_dataframe,
    max_selections=5
)
if options :
    #st.write(options)
    #st.text(options)
    ingredients_string = ''

    for fruits_chosen in options:
        ingredients_string += fruits_chosen

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '"""+ name_on_order+ """')"""
    
    time_to_insert = st. button('submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
