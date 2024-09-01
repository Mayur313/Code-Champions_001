import streamlit as st


# Fixed font size for the title
font_size = 60  # You can change this value to adjust the size

# Use the fixed font size in the HTML
st.markdown(
    f"<h1 style='text-align: center; color: #003366; font-size: {font_size}px;'>Welcome to the E-Commerce Dashboard</h1>",
    unsafe_allow_html=True
)

st.write("")

# Fixed font size for the subtitle
font_size_subtitle = 38  # You can adjust this size as needed

# Use the fixed font size in the HTML for the subtitle
st.markdown(
    f"<h3 style='text-align: center; color: #666666; font-size: {font_size_subtitle}px;'>Your one-step platform for all E-commerce analytics.</h3>",
    unsafe_allow_html=True
)

st.write("")
st.write("")
st.write("")
# Add a logo to the dashboard
col1, col2  = st.columns([1, 1.5])

with col1:
    st.image("static/IMG_20240827_193636-removebg-preview.png", width=300)

with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
        # Define the font sizes for question and answers
    font_size_question = 40  # Larger size for the question
    font_size_answers = 29    # Smaller size for the answers

    # Display the formatted text with sizes applied
    st.markdown(
        f"""
        <h4 style='color: #4D4D4D; font-size: {font_size_question}px;'>What we will see ahead ?</h4>
        <ol>
            <li style='color: #000080; font-size: {font_size_answers}px;'>Detailed Sales Analysis</li>
            <li style='color: #000080; font-size: {font_size_answers}px;'>Product Profitability and Price Impact</li>
        </ol>
        
        """, 
        unsafe_allow_html=True
    )

