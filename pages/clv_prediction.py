def run():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import joblib
    import os

    st.set_page_config(
        page_title="Customer Lifetime Value",
        layout="centered"
    )

    st.title("Customer Lifetime Value")
    st.write("Predict the future revenue contribution of a customer.")

    MODEL_PATH = "models"
    DATA_PATH = "data"

    lr_model = joblib.load(os.path.join(MODEL_PATH, "linear_rig.joblib"))
    rf_model = joblib.load(os.path.join(MODEL_PATH, "random_for.joblib"))
    gb_model = joblib.load(os.path.join(MODEL_PATH, "gradient_boost.joblib"))

    MODEL_ASSETS = {
        "Linear Regression": {
            "model": lr_model,
            "txt": os.path.join(DATA_PATH, "lr_model_results.txt"),
            "plot": os.path.join(DATA_PATH, "lr_actual_vs_pred.png")
        },
        "Random Forest": {
            "model": rf_model,
            "txt": os.path.join(DATA_PATH, "rf_model_results.txt"),
            "plot": os.path.join(DATA_PATH, "rf_actual_vs_pred.png")
        },
        "Gradient Boosting": {
            "model": gb_model,
            "txt": os.path.join(DATA_PATH, "xg_model_results.txt"),
            "plot": os.path.join(DATA_PATH, "xg_actual_vs_pred.png")
        }
    }

    feature_img = os.path.join(DATA_PATH, "clv_feature_importance.png")
    comparison_csv = os.path.join(DATA_PATH, "clv_model_comparison.csv")

    model_name = st.selectbox(
        "Select Machine Learning Model",
        list(MODEL_ASSETS.keys()),
        key='clv_model_select'
    )

    selected_model = MODEL_ASSETS[model_name]["model"]

    st.subheader("Customer Details")

    recency = st.slider("Recency (Days Since Last Purchase)", 0, 600, 30)

    active_days = st.slider(
        "Active Days (Customer Lifetime So Far)",
        0, 600, 100
    )

    frequency = st.slider(
        "Purchase Frequency",
        1, 300, 5
    )

    monetary = st.number_input(
        "Total Monetary Value (Past Spending)",
        0.0, 450000.0,
        1000.0
    )

    avg_order = st.number_input(
        "Average Order Value",
        0.0, 10000.0,
        200.0
    )

    input_df = pd.DataFrame([{
        "Recency": recency,
        "ActiveDays": active_days,
        "Frequency": frequency,
        "Monetary": monetary,
        "AverageOrderValue": avg_order
    }])


    if st.button("Predict Customer Lifetime Value"):

        pred_log = selected_model.predict(input_df)[0]
        predicted_clv = np.expm1(pred_log)

        st.subheader("Prediction Result")
        st.metric("Predicted CLV", f"£{predicted_clv:,.2f}")

        if predicted_clv >= 174:
            st.success("High Value Customer")
            st.info("Actions: Loyalty programs, premium offers, retention strategies")

        elif predicted_clv >= 65:
            st.warning("Medium Value Customer")
            st.info("Actions: Upselling & personalized marketing")

        else:
            st.error("Low Value Customer")
            st.info("Actions: Discounts & re-engagement campaigns")

    st.subheader("Model Performance")

    if os.path.exists(comparison_csv):
        st.dataframe(pd.read_csv(comparison_csv), use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Feature Importance")
        if os.path.exists(feature_img):
            st.image(feature_img, use_container_width=True)

    with col2:
        st.markdown("### Selected Model Metrics")
        txt_path = MODEL_ASSETS[model_name]["txt"]

        if os.path.exists(txt_path):
            with open(txt_path, "r") as f:
                st.text(f.read())

    st.subheader("Actual vs Predicted Comparison")
    st.caption("Closer alignment = better performance")

    for model, assets in MODEL_ASSETS.items():
        if os.path.exists(assets["plot"]):
            st.image(assets["plot"], caption=model, width=500)