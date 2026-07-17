# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  
import pandas as pd

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

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()


pd_df= my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()



options = st.multiselect(
    "CHOOSE UP  TO 5 INGREDIENTS: ",
     my_dataframe,
    max_selections=5
)
if options :
    #st.write(options)
    #st.text(options)
    ingredients_string = ", ".join(options)

    for fruits_chosen in options:
      search_on = pd_df.loc[
        pd_df['FRUIT_NAME'] == fruits_chosen,
        'SEARCH_ON'
      ].iloc[0]

     #st.write(f"The search value for {fruits_chosen} is {search_on}")

      st.subheader(f"{fruits_chosen} Nutrition Information")

      smoothiefroot_response = requests.get(
        f"https://my.smoothiefroot.com/api/fruit/{search_on}"
      )

      fruit_df = pd.json_normalize(smoothiefroot_response.json())

      st.dataframe(fruit_df, use_container_width=True)
      

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '"""+ name_on_order+ """')"""
    
    time_to_insert = st. button('submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")


