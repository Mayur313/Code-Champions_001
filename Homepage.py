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
    st.image("static/IMG_20240827_193636-removebg-preview.png", width=80)

with col2:
    st.markdown("## Your one-stop platform for all E-commerce analytics.")

# Page 2 content
page_2_content = """
    <h2>Analyze Daily and Monthly Sales Trends</h2>
    <p>Analyze daily and monthly sales trends to identify peak periods and performance patterns.</p>
"""

# Page 3 content
page_3_content = """
    <h2>Explore Pricing Strategies</h2>
    <p>Explore how pricing strategies impact profitability and uncover insights for optimizing returns.</p>
"""

# Display content in Streamlit
st.markdown(page_2_content, unsafe_allow_html=True)
st.markdown(page_3_content, unsafe_allow_html=True)

# Additional call to action
st.markdown("<h2>Stay Ahead of the Curve with Our Data-Driven Insights!</h2>", unsafe_allow_html=True)

