import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    p {
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5, h6 {
        color: #6e6d78;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col2:
    st.image("img/auto.png")
    
st.markdown("# Discover the AutoInsight Universe")

st.markdown("### Your solution for Stock Management Optimization")
    
st.write("""
    Welcome to **AutoInsight**, the ultimate tool designed to help car resellers, manufacturers, and automotive brands **optimize stock management**, **boost sales performance**, and **reduce losses** caused by overproduction or stockouts. Provide an overview of the sales data analyzed to help you make informed decisions. Your solution to balancing stock management in the automotive sector.
    
    Car dealerships often face the challenge of either overstocking, leading to high storage costs, or stockouts, which result in lost sales opportunities. Our goal is to help dealerships find the right balance by analyzing sales data, identifying trends, and providing strategic recommendations.
    
    This application will utilize data from over 34,000 car sales across the United States, considering various factors such as sales trends, demographics, and regional performance.
    
    ### Why AutoInsight?
    
    The automotive industry is more competitive than ever, and maximizing profitability requires precise planning and strategic decisions. **AutoInsight** brings advanced data analysis and predictive modeling to help you find the perfect balance between supply and demand, ensuring you are always prepared to meet your customers' needs without overcommitting resources.
    
    ### For Car Resellers:
    - 🏆 **Boost Sales Performance**: Identify top-selling models and the best times to stock them to ensure availability when customers are ready to buy.
    - 📊 **Analyze Market Trends**: Understand seasonal trends and regional differences to fine-tune your inventory strategy and increase profitability.
    - 🎯 **Targeted Marketing**: Use demographic insights to attract the right customers by focusing marketing efforts on what sells best in your area.
    
    ### For Factories
    - 🏭 **Optimize Production Planning**: Avoid costly overproduction by understanding which models are in demand and when.
    - 📦 **Efficient Stock Management**: Reduce storage costs and inventory waste by producing the right amount of vehicles at the right time.
    - 🔄 **Streamline Supply Chains**: Adjust production based on real-time data, ensuring a smooth and efficient supply chain process.
    
    ### For Automotive Brands
    - 🚀 **Expand Market Reach**: Discover which regions show the most potential for growth and focus resources strategically to maximize brand presence.
    - 📉 **Minimize Losses**: Prevent overproduction and stockouts by accurately forecasting demand and adapting to market changes.
    - 📍 **Benchmarking & Strategy**: Compare performance across regions and dealerships to identify where to invest in marketing and distribution.
    
    ## What We Offer
    
    Our platform analyzes data from over **34,000 sales** across the United States, providing insights on:
    - **Top-selling models** by season, region, and customer segment.
    - **Sales performance trends** across different periods and demographics.
    - **Detailed benchmarks** between dealerships and regions to help you identify the best strategies for success.
    
    With **AutoInsight**, you can confidently plan your sales, production, and marketing strategies, ensuring that you stay ahead of the competition while minimizing costs and maximizing profits. Let’s drive your success together!
    
    ---
    
    Ready to see how AutoInsight can transform your business? Navigate through the menu on the left and start exploring our powerful tools.
    """)