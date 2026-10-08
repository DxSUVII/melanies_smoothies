# Import python packages
import streamlit as st
import pandas as pd
import requests

from snowflake.snowpark.functions import col

# App title
st.title(f"Customize with your smoothies :cup_with_straw: {st.__version__}")

st.write(
    """Choose the fruits you want in smoothie!"""
)

# Name on smoothie
name_on_order = st.text_input("Name on Smoothie:")

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit data including SEARCH_ON
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)

# Convert to pandas dataframe
pd_df = my_dataframe.to_pandas()

# Fruit picker
ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

# Submit button
time_to_insert = st.button("Submit Order")

if ingredients:

    ingredients_string = ''

    for fruit_chosen in ingredients:

        ingredients_string += fruit_chosen + ' '

        search_on = pd_df.loc[
            pd_df['FRUIT_NAME'] == fruit_chosen,
            'SEARCH_ON'
        ].iloc[0]

        st.subheader(fruit_chosen + ' Nutrition Information')

        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        if smoothiefroot_response.status_code == 200:

            st.dataframe(
                data=smoothiefroot_response.json(),
                use_container_width=True
            )

        else:

            st.error(
                f"SmoothieFroot API unavailable. Status code: {smoothiefroot_response.status_code}"
            )

    st.write(ingredients_string)

    my_insert_stmt = """
        insert into smoothies.public.orders(name_on_order, ingredients)
        values ('""" + name_on_order + """','""" + ingredients_string + """')
    """

    st.write(my_insert_stmt)

    if time_to_insert:

        session.sql(my_insert_stmt).collect()

        st.success(
            name_on_order + ', your Smoothie is ordered!',
            icon="✅"
        )
