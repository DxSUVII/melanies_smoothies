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
time_to_insert = st.
