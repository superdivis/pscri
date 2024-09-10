import pandas as pd
import streamlit as st

default_value = "A"

if st.sidebar.button("A"):
    default_value = "A"

if st.sidebar.button("B"):
    default_value = "B"

if st.sidebar.button("C"):
    default_value = "C"


df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9], "D": [10, 11, 12]})


choices = ["A", "B", "C"]
selected = st.selectbox("Select an object", choices, index=choices.index(default_value))

st.write(f"You selected {selected}")

st.line_chart(df, x="D", y=selected, use_container_width=True)