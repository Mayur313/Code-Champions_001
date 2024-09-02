import streamlit as st
import Preprocessor  # Import the Preprocessor module
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Add a logo to the dashboard
col1, col2 = st.columns([1, 8])

with col1:
    st.image("static/IMG_20240827_193636-removebg-preview.png", width=200)

with col2:
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>E-Commerce Dashboard</h1>", unsafe_allow_html=True)



# Load datasets
file_names = [
    'olist_customers_dataset.csv',
    'olist_geolocation_dataset.csv',
    'olist_order_items_dataset.csv',
    'olist_order_payments_dataset.csv',
    'olist_order_reviews_dataset.csv',
    'olist_orders_dataset.csv',
    'olist_products_dataset.csv',
    'olist_sellers_dataset.csv',
    'product_category_name_translation.csv'
]

try:
    datasets = Preprocessor.load_datasets(file_names)
except Exception as e:
    st.error(f"Error loading datasets: {e}")

# Merge orders, items, payments, and seller datasets
merged_df = pd.merge(datasets['olist_orders_dataset'], datasets['olist_order_items_dataset'], on='order_id', how='left')
merged_df = pd.merge(merged_df, datasets['olist_order_payments_dataset'], on='order_id', how='left')
merged_df = pd.merge(merged_df, datasets['olist_sellers_dataset'], on='seller_id', how='left')

# Preprocess data and extract insights
datasets = Preprocessor.preprocess_and_insight(datasets)

# Sidebar filters
st.sidebar.header("Filter Options")

# Sidebar: Year Filter with Select/Deselect All
years = Preprocessor.multiselect("Select Year", datasets['olist_orders_dataset']['year'].unique().tolist())

# Sidebar: Month Filter with Select/Deselect All
months = Preprocessor.multiselect("Select Month", datasets['olist_orders_dataset']['month'].unique().tolist())

# Sidebar: Product Category Filter with Select/Deselect All
product_categories = Preprocessor.multiselect(
    "Select Product Category",
    datasets['product_category_name_translation']['product_category_name_english'].unique().tolist()
)

# # Sidebar: Seller State Filter with Select/Deselect All
# seller_states = Preprocessor.multiselect(
#     "Select Seller State",
#     datasets['olist_sellers_dataset']['seller_state'].unique().tolist()
# )

# Sidebar: Payment Type Filter with Select/Deselect All
payment_types = Preprocessor.multiselect(
    "Select Payment Type",
    datasets['olist_order_payments_dataset']['payment_type'].unique().tolist()
)

# Sidebar: Payment Type Filter with Select/Deselect All
selected_order_status = Preprocessor.multiselect(
    "Select Order Status",
    datasets['olist_orders_dataset']['order_status'].unique().tolist()
)


# Apply filters
filtered_df = datasets['olist_orders_dataset'][
    (datasets['olist_orders_dataset']['year'].isin(years)) &
    (datasets['olist_orders_dataset']['month'].isin(months)) &
    (datasets['olist_products_dataset']['product_category_name'].isin(product_categories)) &
    # (datasets['olist_sellers_dataset']['seller_state'].isin(seller_states)) &
    (datasets['olist_order_payments_dataset']['payment_type'].isin(payment_types)) &
    (datasets['olist_orders_dataset']['order_status'].isin(selected_order_status))
]

# Main dashboard layout
st.markdown("<h1 style='text-align: center;'>📊 Sales Overview</h1>", unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")

# Unique Insights (displayed in 4 columns)
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Number of unique customers
    unique_customers = datasets['olist_customers_dataset']['customer_id'].nunique()
    st.metric("Unique Customers", f"{unique_customers:,}")

# Load the dataset
file_path = 'olist_orders_dataset.csv'
df = pd.read_csv(file_path)

with col2:
    # Convert date columns to datetime format
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])

    # Calculate On-Time Delivery
    df['on_time'] = df['order_delivered_customer_date'] <= df['order_estimated_delivery_date']

    # Calculate On-Time Delivery Rate
    on_time_delivery_rate = df['on_time'].mean()

    # Display the metric
    st.metric("On-Time Delivery Rate", f"{on_time_delivery_rate * 100:.2f}%")
with col3:
    # Average freight value for orders
    avg_freight_value = datasets['olist_order_items_dataset']['freight_value'].mean()
    st.metric("Avg. Freight Value", f"${avg_freight_value:.2f}")

with col4:
    # Number of 5-star reviews
    five_star_reviews = datasets['olist_order_reviews_dataset'][datasets['olist_order_reviews_dataset']['review_score'] == 5].shape[0]
    st.metric("5-Star Reviews", f"{five_star_reviews:,}")

# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

# Visualization (6 columns layout)
col5, col6 = st.columns(2)

col7, col8 = st.columns(2)

col9, col10 = st.columns(2)


col11, col12 = st.columns(2)


col13, col14 = st.columns(2)
st.write("")
# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

# Column 5: Monthly Orders Line Chart
with col5:
    st.subheader("Monthly Orders")
    
    # Ensure you are grouping by the correct columns ('year' and 'month' should exist in filtered_df)
    monthly_orders = filtered_df.groupby(['year', 'month'])['order_id'].count().reset_index()
    
    # Use 'order_id' or whichever column represents unique orders
    fig1 = px.line(monthly_orders, x='month', y='order_id', color='year', title="Orders per Month")
    
    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig1, use_container_width=True)

# Column 6: Revenue by Year Bar Chart
with col6:
    st.subheader("Yearly Revenue")
    yearly_revenue = filtered_df.groupby(['year'])['payment_value'].sum().reset_index()
    fig2 = px.bar(yearly_revenue, x='year', y='payment_value', title="Revenue by Year", labels={"payment_value": "Revenue"})
    st.plotly_chart(fig2, use_container_width=True)

# Column 7:

st.subheader('The Distribution of Sellers')

# # Load the data
# df_geolocation = Preprocessor.load_geolocation_data()

# # Ensure the column 'geolocation_state' exists and isn't empty
# if 'geolocation_state' in df_geolocation.columns:
#     # Sidebar filter for geolocation states
#     selected_geolocation_states = Preprocessor.multiselect(
#         "Select Geolocation States",
#         df_geolocation['geolocation_state'].unique().tolist()
#     )

#     @st.cache_data
#     def filter_and_downsample_data(states, df, sample_size=100000):
#         # Apply the filter
#         df_filtered = df[df['geolocation_state'].isin(states)]
#         # Downsample if necessary
#         if len(df_filtered) > sample_size:
#             df_filtered = df_filtered.sample(sample_size, random_state=1)
#         return df_filtered
        
#     if selected_geolocation_states:
        
#         # Apply the filter
#         df_geolocation_filtered = df_geolocation[df_geolocation['geolocation_state'].isin(selected_geolocation_states)]

#         # Downsample if necessary
#         if len(df_geolocation_filtered) > 100000:
#             df_geolocation_filtered = df_geolocation_filtered.sample(100000, random_state=1)

#         # Ensure there is data to plot
#         if not df_geolocation_filtered.empty:
#             # Create scatter plot using Plotly
#             fig_geolocation = px.scatter(
#                 df_geolocation_filtered,
#                 x='geolocation_lng',
#                 y='geolocation_lat',
#                 color='geolocation_state',
#                 title='Geolocation of Customers and Sellers',
#                 labels={
#                     'geolocation_lng': 'Longitude',
#                     'geolocation_lat': 'Latitude',
#                     'geolocation_state': 'State'
#                 },
#                 color_continuous_scale='Spectral'
#             )

#             # Customize the layout
#             fig_geolocation.update_layout(
#                 xaxis_title="Longitude",
#                 yaxis_title="Latitude",
#                 title_x=0.5,
#                 coloraxis_colorbar=dict(title="State"),
#                 height=500
#             )

#             # Display the plot in Streamlit
#             st.plotly_chart(fig_geolocation, use_container_width=True)
#         else:
#             st.warning("No data available for the selected states.")
#     else:
#         st.warning("Please select at least one state.")
# else:
#     st.error("The 'geolocation_state' column is missing in the dataset.")

# Load the data
merged_df = Preprocessor.load_data()

# Sidebar filters for state and city
state_filter = st.sidebar.multiselect(
    "Select State(s)", merged_df['seller_state'].unique()
)
select_all_states = st.sidebar.checkbox("Select All States", value=True)
if select_all_states:
    state_filter = merged_df['seller_state'].unique()

city_filter = st.sidebar.multiselect(
    "Select City/Cities", merged_df['seller_city'].unique()
)
select_all_cities = st.sidebar.checkbox("Select All Cities", value=True)
if select_all_cities:
    city_filter = merged_df['seller_city'].unique()

# Filter the data
filtered_df = Preprocessor.filter_data(merged_df, state_filter, city_filter)

# Get map data and display the map
map_data = Preprocessor.get_map_data(filtered_df)
st.map(map_data)

# Optionally, show the filtered data table
st.dataframe(filtered_df[['seller_id', 'seller_city', 'seller_state']])

st.markdown("""
    ## Logic to Increase Purchases:
    - ##### **Segmented Campaigns** : Develop segmented marketing campaigns that address specific regional needs and preferences.
    - ##### **Customer Feedback** : Collect and analyze feedback from different regions to refine products and services.
    - ##### **Strategic Investment** : Invest in regions showing promising growth potential or underserved markets.
    """)

# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

# Column 8 :

# Assuming 'order_items' is already loaded as a DataFrame
order_items = pd.read_csv('olist_order_items_dataset.csv')

# Calculate the number of products sold per seller
products_per_seller = order_items.groupby('seller_id')['order_item_id'].count().reset_index()
products_per_seller.columns = ['Seller ID', 'Number of Products Sold']

# Plot the top 20 sellers by the number of products sold
top_sellers = products_per_seller.sort_values(by='Number of Products Sold', ascending=False).head(20)

# Create a Plotly bar chart
fig = px.bar(
    top_sellers,
    x='Number of Products Sold',
    y='Seller ID',
    orientation='h',  # Horizontal bar chart
    title='Top 20 Sellers by Number of Products Sold',
    color='Number of Products Sold',
    color_continuous_scale='inferno'
)

# Customize the layout for better presentation
fig.update_layout(
    xaxis_title="Number of Products Sold",
    yaxis_title="Seller ID",
    yaxis=dict(autorange="reversed"),  # Reverse y-axis to show top sellers at the top
    template="plotly_white"
)

# Streamlit container to display the chart
st.container()
st.subheader("Top 20 Sellers by Number of Products Sold")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
    ### This plot identifies the top-performing sellers, which can be beneficial for partnership or inventory strategies.
    """)

# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

##########################################################################
