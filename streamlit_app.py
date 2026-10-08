# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize with your smoothies :cup_with_straw: {st.__version__}")

st.write(
    """Choose the fruits you want in smoothie!"""
)

# Name input
name_on_order = st.text_input("Name on Smoothie:")

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit names from table
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col("FRUIT_NAME"))

# Multi-select
ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# Submit button
time_to_insert = st.button("Submit Order")

# Process selections
if ingredients:

    ingredients_string = ""

    st.header("SmoothieFroot Nutrition Information")

    for fruit_chosen in ingredients:

        ingredients_string += fruit_chosen + " "

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/watermelon"
        )

        if smoothiefroot_response.status_code == 200:

            st.subheader(fruit_chosen)

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
            name_on_order + ", your Smoothie is ordered!",
            icon="✅"
        )
