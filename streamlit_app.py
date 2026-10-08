st.header("SmoothieFroot Nutrition Information")

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

if smoothiefroot_response.status_code == 200:
    sf_df = st.dataframe(
        data=smoothiefroot_response.json(),
        use_container_width=True
    )
else:
    st.error(
        f"SmoothieFroot API unavailable. Status code: {smoothiefroot_response.status_code}"
    )
