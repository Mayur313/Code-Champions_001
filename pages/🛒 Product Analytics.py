import streamlit as st
import Preprocessor  # Import the Preprocessor module
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Add a logo to the dashboard
col1, col2 = st.columns([1, 8])

with col1:
    st.image("static/IMG_20240827_193636-removebg-preview.png", width=200)

with col2:
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>E-Commerce Dashboard</h1>", unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")

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

# Sidebar: Seller State Filter with Select/Deselect All
seller_states = Preprocessor.multiselect(
    "Select Seller State",
    datasets['olist_sellers_dataset']['seller_state'].unique().tolist()
)

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
    (datasets['olist_sellers_dataset']['seller_state'].isin(seller_states)) &
    (datasets['olist_order_payments_dataset']['payment_type'].isin(payment_types)) &
    (datasets['olist_orders_dataset']['order_status'].isin(selected_order_status))
]


# Main dashboard layout
st.markdown("<h1 style='text-align: center;'>🛒Product Analytics</h1>", unsafe_allow_html=True)



st.write("")
st.write("")

# Unique Insights (displayed in 4 columns)
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Number of unique customers
    unique_customers = datasets['olist_customers_dataset']['customer_id'].nunique()
    st.metric("Unique Customers", f"{unique_customers:,}")

st.write("")
st.write("")

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
st.write("")
# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

col7, col8 = st.columns(2)
st.write("")
# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

col9, col10 = st.columns(2)
st.write("")
# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

col11, col12 = st.columns(2)
# # Add a horizontal line
# st.markdown("<hr>", unsafe_allow_html=True)

col13 = st.columns(1)
st.write("")
# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

col14 = st.columns(1)
st.write("")
# # Add a horizontal line
# st.markdown("<hr>", unsafe_allow_html=True)


products_df = pd.read_csv('olist_products_dataset.csv')


# Column 5: Number of Products By Photos Quantity
with col5:
    st.subheader("Number of Products By Photos Quantity")
    
    # Group by 'product_photos_qty' and count the number of unique products
    photo_counts = products_df.groupby('product_photos_qty')['product_id'].count().reset_index()
    
    # Create the bar chart
    fig1 = px.bar(photo_counts, 
                   x='product_photos_qty', 
                   y='product_id', 
                   title="Number of Products by Photos Quantity", 
                   labels={"product_photos_qty": "Number of Photos", "product_id": "Number of Products"})
    
    st.plotly_chart(fig1, use_container_width=True)

# Column 6: Customer less than 2 purchases

# Load the dataset (use the appropriate dataset that includes customer and order details)
purchase_df = pd.read_csv('olist_customers_dataset.csv')

# Calculate purchase frequency per customer
purchase_frequency = purchase_df.groupby('customer_unique_id')['customer_id'].count()

# Create a new DataFrame for segmentation
customer_segmentation = pd.DataFrame({
    'PurchaseFrequency': purchase_frequency
})

# Define dormant customers (those with less than 2 purchases)
dormant_customers = customer_segmentation[customer_segmentation['PurchaseFrequency'] < 2]

with col6:
    st.subheader("Customer Purchase Frequency Insights")

    # Visualize the distribution of purchase frequencies
    fig2 = px.histogram(customer_segmentation, 
                        x='PurchaseFrequency', 
                        nbins=30, 
                        title="Distribution of Customer Purchase Frequency", 
                        labels={"PurchaseFrequency": "Number of Purchases", "count": "Number of Customers"})
    
    st.plotly_chart(fig2, use_container_width=True)

    # Highlight the number of dormant customers
    num_dormant_customers = dormant_customers.shape[0]
    st.metric("Dormant Customers", f"{num_dormant_customers:,}", "Customers with less than 2 purchases")
    
    # Optional: Provide additional insight or action
    st.markdown("""
    <h1 style='font-size: 22px;'>Dormant customers are those who have made less than 2 purchases. Consider targeted marketing campaigns to re-engage these customers.</h1>
    """, unsafe_allow_html=True)

# Merge the 'olist_order_items_dataset' and 'olist_sellers_dataset'
merged_order_items_sellers = Preprocessor.merge_order_items_sellers(
    datasets['olist_order_items_dataset'], 
    datasets['olist_sellers_dataset']
)

# Apply filters to merged_order_items_sellers
filtered_order_items_sellers = merged_order_items_sellers[
    (merged_order_items_sellers['order_id'].isin(filtered_df['order_id'])) &
    (merged_order_items_sellers['seller_state'].isin(seller_states))
]

# Group orders by state and calculate total order count
state_order_counts = filtered_order_items_sellers.groupby('seller_state')['order_id'].count().reset_index()

# Sort the DataFrame by 'order_id' in ascending order
state_order_counts = state_order_counts.sort_values(by='order_id', ascending=True)

with col7:
    st.subheader("Purchase Behavior by State: Products Sold")
    
    # Plot a bar chart to show geographic trends using Plotly
    fig3 = px.bar(
        state_order_counts, 
        x='seller_state', 
        y='order_id', 
        labels={'seller_state': 'State', 'order_id': 'Total Order Count'},
        title="Purchase Behavior by State"
    )
    
    fig3.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)


with col8:
    st.markdown("""
    ### Key Insights from the Graph
    
    - **Top-performing State:** SP (São Paulo) Indicating a significantly larger customer base compared to other regions.
    - **Moderate Growth:** States like RJ (Rio de Janeiro) and MG (Minas Gerais) show moderate purchase behavior, which can be optimized further.
    
    ### Strategies to Increase Purchase
    
    - **Targeted Marketing:** 
        - Implement localized marketing campaigns focusing on the lower-performing states. Consider special promotions or regional discounts to attract customers from those areas.
    - **Product Variety Expansion:**
        - In underperforming regions, explore expanding the product categories based on regional preferences or localized needs.
    """)


with col9:
    st.markdown("""
    ## Strategies to Improve Purchase Behavior
    
    - ### Promote Alternative Payment Options:  
        Encourage the use of alternate payment methods, like debit cards or vouchers, by offering incentives such as discounts or cashback to diversify payment methods.
    - ### Trust Building for Digital Payments: 
        Launch campaigns to build trust around digital payment methods, particularly targeting regions or customers who might still be hesitant about online transactions.
    """)



# Assuming filtered_df already contains the relevant columns from merged datasets
# First, ensure filtered_df is constructed properly to include 'payment_type'

# Calculate the count of each payment type from the filtered payments dataset
payment_methods = datasets['olist_order_payments_dataset'][datasets['olist_order_payments_dataset']['order_id'].isin(filtered_df['order_id'])]['payment_type'].value_counts().reset_index()
payment_methods.columns = ['payment_type', 'count']

with col10:
    st.subheader("Payment Method Distribution")

    # Create a pie chart using Plotly
    fig4 = px.pie(
        payment_methods, 
        names='payment_type', 
        values='count', 
        title="Distribution of Payment Methods",
        labels={'payment_type': 'Payment Method', 'count': 'Number of Transactions'}
    )

    # Optionally, highlight the selected payment type if you want to emphasize a specific one
    # For example, highlight 'credit_card'
    fig4.update_traces(
        pull=[0.1 if method == 'credit_card' else 0 for method in payment_methods['payment_type']],
        marker=dict(line=dict(color='#000000', width=2))
    )

    st.plotly_chart(fig4, use_container_width=True)


# Load the datasets
df_orders = pd.read_csv('olist_orders_dataset.csv')  # Ensure you have the correct file names
df_payments = pd.read_csv('olist_order_payments_dataset.csv')

# Use Preprocessor to merge orders and payments
df_order_payment = Preprocessor.merge_orders_payments(datasets['olist_orders_dataset'], datasets['olist_order_payments_dataset'])
# Create filters for order status and payment type
unique_order_statuses = df_order_payment['order_status'].unique()

# Insight: Analyze the distribution of payment methods by order status
payment_by_status = df_order_payment.groupby(['order_status', 'payment_type']).size().unstack().fillna(0)

# Reshape the DataFrame for Plotly
payment_by_status = payment_by_status.reset_index()
payment_by_status = payment_by_status.melt(id_vars='order_status', var_name='payment_type', value_name='number_of_payments')

# Visualization for payment methods by order status
with col11:
    st.subheader('Payment Methods by Order Status')

    # Ensure 'filtered_df' contains relevant columns from merged datasets for filtering
    # Merging orders and payments with the filters applied
    df_order_payment = Preprocessor.merge_orders_payments(
        datasets['olist_orders_dataset'], 
        datasets['olist_order_payments_dataset']
    )

    # Apply filters to df_order_payment
    filtered_order_payment = df_order_payment[
        (df_order_payment['order_id'].isin(filtered_df['order_id'])) &
        (df_order_payment['payment_type'].isin(payment_types)) &
        (df_order_payment['order_status'].isin(selected_order_status))
    ]

    # Calculate the distribution of payment methods by order status
    payment_by_status = filtered_order_payment.groupby(['order_status', 'payment_type']).size().unstack().fillna(0)
    
    # Reshape the DataFrame for Plotly
    payment_by_status = payment_by_status.reset_index()
    payment_by_status = payment_by_status.melt(id_vars='order_status', var_name='payment_type', value_name='number_of_payments')

    # Create a Plotly bar chart for payment methods by order status
    fig5 = px.bar(
        payment_by_status,
        x='order_status',
        y='number_of_payments',
        color='payment_type',
        title='Payment Methods by Order Status',
        labels={'order_status': 'Order Status', 'number_of_payments': 'Number of Payments'},
        text='number_of_payments'
    )

    fig5.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig5.update_layout(barmode='stack')

    # Display the plot in Streamlit
    st.plotly_chart(fig5, use_container_width=True)

    
with col12:
    st.markdown("""
    ## Key Insights from Payment Methods by Order Status
    - ### Cancelled Orders: 
      A very small number of payments were processed for cancelled orders. This suggests that most customers who start a purchase process generally complete their transactions successfully.
    
    ## Strategies to Improve Purchase Rates
    
    - ### Promote Underutilized Payment Methods:
      Consider offering discounts or promotions for customers using less popular payment methods (like debit cards or vouchers) to encourage their adoption and increase overall transaction volume.
    - ### Order Process Improvement:  
      Investigate any pain points in the order processing or payment phase to further reduce cancelled or unprocessed orders. Streamlining the checkout experience can significantly improve the conversion rate.
    """)



with st.container():
    st.subheader("Shipping Cost (Delivery Charges) vs. Product Price")

    # Ensure filtered_df has the necessary columns from the merged datasets
    # Merging with `order_items` to get `price` and `freight_value`
    filtered_order_items = pd.merge(
        filtered_df[['order_id']],  # Filtered orders based on the applied filters
        datasets['olist_order_items_dataset'], 
        on='order_id', 
        how='inner'
    )

    # Plot the scatter plot if filtered_order_items is not empty
    if not filtered_order_items.empty:
        # Create scatter plot using Plotly
        fig8 = px.scatter(
            filtered_order_items,
            x='price',
            y='freight_value',
            color='freight_value',
            color_continuous_scale='viridis',
            labels={'price': 'Product Price', 'freight_value': 'Shipping Cost (Freight Value)'},
            title='Shipping Cost vs. Product Price',
            opacity=0.9
        )

        # Customize the layout (optional)
        fig8.update_layout(
            xaxis_title="Product Price",
            yaxis_title="Shipping Cost (Delivery Charges)",
            title_x=0.1  # Center the title
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig8, use_container_width=True)
    else:
        st.write("No data available for the selected filters.")
    # Display the text with increased size
    st.markdown(
        """
        <p style="font-size:22px;">
        Companies might optimize their shipping strategy by analyzing products that are outliers (high shipping cost for relatively low price)
        </p>
        """,
        unsafe_allow_html=True
    )

# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

###########################################

orders = pd.read_csv('olist_orders_dataset.csv')

# Calculate delivery time in days
orders['delivery_time'] = (pd.to_datetime(orders['order_delivered_customer_date']) - pd.to_datetime(orders['order_purchase_timestamp'])).dt.days

# Create Plotly histogram
fig = px.histogram(orders, x='delivery_time', nbins=30, title='Distribution of Delivery Times', labels={'delivery_time': 'Delivery Time (days)'})

# Customize the layout (optional)
fig.update_layout(
    xaxis_title='Delivery Time (days)',
    yaxis_title='Frequency',
    template='plotly_white'
)

# Streamlit app
st.title('Distribution of Delivery Times')
st.plotly_chart(fig)

# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
