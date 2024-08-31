import streamlit as st


# Set page configuration to wide layout
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.markdown("<h1 style='font-size:60px;'>Welcome to the E-Commerce Dashboard</h1>", unsafe_allow_html=True)


st.write("")
st.write("")
st.write("")
# Add a logo to the dashboard
col1, col2 = st.columns([1, 13])

with col1:
    st.image("IMG_20240827_193636-removebg-preview.png", width=80)

with col2:
    st.markdown("## Your one-stop platform for all E-commerce analytics.")



