import streamlit as st

df = session_state.df
row_id = st.session_state.selected_id

row = df[df["id"] == row_id].iloc[0]

name = st.text_input("Name", value = row["name"])

if st.button["Save"]:
    idx = df[df["id"] == row_id].index[0]
    st.session_state.df.loc[idx, "name"] = name

    st.success("Updated")
