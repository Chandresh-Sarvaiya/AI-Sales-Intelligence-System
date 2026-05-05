def run():    
    import streamlit as st
    import pandas as pd
    import os

    st.set_page_config(
        page_title=" CLV Optimization & Customer Intelligence",
        layout="wide"
    )

    @st.cache_data
    def load_rfm_data():
        return pd.read_csv(r"data\rfm_analysis.csv")

    rfm = load_rfm_data()

    st.title(" CLV Optimization & Customer Intelligence")
    st.write(
        "This dashboard presents customer segmentation using RFM analysis "
        "to understand customer value and purchasing behavior."
    )

    st.markdown("---")
    
    st.markdown("## Business Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Customers",
        rfm['CustomerID'].nunique()
    )

    col2.metric(
        "Total Revenue",
        f"£{rfm['Monetary'].sum():,.0f}"
    )

    col3.metric(
        "Average Revenue per Customer",
        f"£{rfm['Monetary'].mean():.2f}"
    )

    
    st.markdown("---")

    st.markdown("##  RFM Intelligence Insights")

    st.info("""
    This module uses RFM analysis to identify customer value patterns.

    • Recency → How recently the customer purchased  
    • Frequency → How often the customer purchases  
    • Monetary → How much revenue the customer generates  

    Using these features, customers are automatically segmented into groups such as
    Champion, Loyal Customer, At Risk, and Lost Customer to support CLV optimization.
    """)

    st.markdown("---")

    st.markdown("## Business Summary")

    col1, col2, col3 = st.columns(3)

    high_value = rfm[rfm["Segment"].isin(["Champion", "Loyal Customer"])]

    at_risk = rfm[rfm["Segment"].isin(["At Risk", "Lost Customer"])]

    col1.metric(
        "High Value Customers",
        high_value.shape[0]
    )

    col2.metric(
        "At Risk Customers",
        at_risk.shape[0]
    )

    col3.metric(
        "Estimated Revenue Impact",
        f"£{high_value['Monetary'].sum():,.0f}"
    )


    st.markdown("---")

    st.markdown("## AI-Based Customer Segmentation Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Customers per Segment")
        segment_counts = rfm["Segment"].value_counts()
        st.bar_chart(segment_counts)

    with col2:
        st.markdown("### Revenue Contribution by Segment")
        revenue_by_segment = rfm.groupby("Segment")["Monetary"].sum()
        st.bar_chart(revenue_by_segment)

    st.markdown("---")

    st.markdown("## Segment Intelligence Explorer")

    segment = st.selectbox(
        "Select Customer Segment",
        sorted(rfm['Segment'].unique())
    )

    segment_df = rfm[rfm['Segment'] == segment]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Customers in Segment",
        segment_df.shape[0]
    )

    col2.metric(
        "Average Revenue",
        f"£{segment_df['Monetary'].mean():.2f}"
    )

    col3.metric(
        "Average Purchase Frequency",
        f"{segment_df['Frequency'].mean():.1f}"
    )

    st.markdown("### Business Recommendation")

    if segment == "Champion":
        st.success("Reward these customers with premium offers, loyalty perks, and upselling strategies.")

    elif segment == "Loyal Customer":
        st.info("Maintain engagement with personalized offers and early access campaigns.")

    elif segment == "Potential Customer":
        st.warning("Target with conversion campaigns and discounts to increase purchase frequency.")

    elif segment == "At Risk":
        st.error("Launch retention campaigns immediately. Consider win-back emails or special discounts.")

    elif segment == "Lost Customer":
        st.error("Re-engagement strategy needed. Offer strong incentives or remarketing campaigns.")

    st.markdown("### Top 5 Customers in this Segment")
    st.dataframe(
        segment_df.sort_values("Monetary", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )