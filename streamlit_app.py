# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize with your smoothies :cup_with_straw: {st.__version__}")

st.write(
    """Choose the fruits you want in smoothie!"""
)
name_on_order = st.text_input("Name on Smoothie:")
# Connect to Snowflake
session = get_active_session()

# Get fruit names from table
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col('FRUIT_NAME'))

# Optional dataframe display
# st.dataframe(data=my_dataframe, use_container_width=True)

# Multiselect widget
ingredients = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)
time_to_insert = st.button('Submit Order')
# Process selections
if ingredients:

    ingredients_string = ''

    for fruit_chosen in ingredients:
        ingredients_string += fruit_chosen

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
                    values ('""" + name_on_order + """','""" + ingredients_string + """')"""

    st.write(my_insert_stmt)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(name_on_order + ', your Smoothie is ordered!', icon="✅")


