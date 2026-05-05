def run():
    import streamlit as st
    import pandas as pd
    import joblib
    import os
    import numpy as np

    st.set_page_config(page_title="Lead Scoring System")

    st.title("Lead Scoring System")
    st.write("Predict customer lead potential using ML models")

    lr_model = joblib.load("models/linear_regression_model.pkl")
    rf_model = joblib.load("models/random_forest_model.pkl")
    gb_model = joblib.load("models/gradient_boosting_model.pkl")

    FEATURE_ORDER = [
        'Recency',
        'Frequency',
        'Monetary',
        'ProductDiversity',
        'Customer_active_days',
        'email_click_rate',
        'website_visits',
        'time_on_site',
        'discount_response'
    ]

    MODEL_ASSETS = {
        "Linear Regression": {
            "model": lr_model,
            "folder": "assets/logistic_reg",
            "metrics": "lr_regression_metrics.csv",
            "importance": "feature_importance_lr.csv",
            "plots": ["actual_vs_pred_lr.png", "residual_plot_lr.png"]
        },
        "Random Forest": {
            "model": rf_model,
            "folder": "assets/random_forest",
            "metrics": "rf_regression_metrics.csv",
            "importance": "feature_importance_rf.csv",
            "plots": ["actual_vs_pred_rf.png", "residual_plot_rf.png"]
        },
        "Gradient Boosting": {
            "model": gb_model,
            "folder": "assets/gradient_boost",
            "metrics": "gb_regression_metrics.csv",
            "importance": "feature_importance_gb.csv",
            "plots": ["actual_vs_pred_gb.png", "residual_plot_gb.png"]
        }
    }

    model_name = st.selectbox(
        "Select Machine Learning Model",
        list(MODEL_ASSETS.keys()),
        key="lead_model_select"
    )

    selected_model = MODEL_ASSETS[model_name]["model"]

    st.markdown("---")

    st.subheader("Customer Inputs")

    recency = st.number_input("Recency (days)", min_value=0)
    frequency = st.number_input("Frequency", min_value=1)
    monetary = st.number_input("Monetary Value", min_value=0.0)

    product_diversity = st.number_input(
        "Product Diversity",
        min_value=1,
        help="Number of unique products purchased"
    )

    customer_active_days = st.number_input("Customer Active Days",min_value=1)
    email_click_rate = st.slider("Engagement Score", 0, 10)
    website_visits = st.number_input("Website Visits", min_value=1)
    time_on_site = st.number_input("Time on Site (seconds)", min_value=1)
    discount_response = st.selectbox("Discount Response", [0, 1], key="discount_select")


    input_df = pd.DataFrame([{
        "Recency": recency,
        "Frequency": frequency,
        "Monetary": monetary,
        "ProductDiversity": product_diversity,
        "Customer_active_days": customer_active_days,
        "email_click_rate": email_click_rate,
        "website_visits": website_visits,
        "time_on_site": time_on_site,
        "discount_response": discount_response
    }])

    input_df = input_df[FEATURE_ORDER]

    if st.button("Predict Lead Score", key="predict_btn"):

        prediction = selected_model.predict(input_df)[0]
        lead_score = max(0, min(100, prediction))

        X = input_df[FEATURE_ORDER]
        input_df['predicted_score'] = selected_model.predict(X)
        input_df['predicted_score'] = input_df['predicted_score'].clip(0, 100)

        min_score = input_df['predicted_score'].min()
        max_score = input_df['predicted_score'].max()

        if max_score != min_score:
            lead_score = (lead_score - min_score) / (max_score - min_score) * 100
        else:
            lead_score = lead_score
    
        lead_score = round(lead_score, 2)


        st.subheader("Prediction Result")
        st.metric("Lead Score", f"{lead_score}")

        # Step 5: Classification
        if lead_score >= 70:
            st.success("High Value Lead")
        elif lead_score >= 40:
            st.warning("Medium Value Lead")
        else:
            st.error("Low Value Lead")
            st.markdown("---")

        st.subheader("Model Comparison")

        comparison_data = []

        for name, assets in MODEL_ASSETS.items():
            path = os.path.join(assets["folder"], assets["metrics"])

            if os.path.exists(path):
                df = pd.read_csv(path)
                df["Model"] = name
                comparison_data.append(df.iloc[0])

        if comparison_data:
            comp_df = pd.DataFrame(comparison_data)
            st.dataframe(comp_df, use_container_width=True)

            if "R2 Score" in comp_df.columns:
                best_model = comp_df.sort_values("R2 Score", ascending=False).iloc[0]["Model"]
            else:
                best_model = comp_df.sort_values("RMSE").iloc[0]["Model"]

        else:
            st.warning("No metrics files found")

        st.markdown("---")
        
        st.subheader("Feature Importance")

        imp_path = os.path.join(
            MODEL_ASSETS[model_name]["folder"],
            MODEL_ASSETS[model_name]["importance"]
        )

        if os.path.exists(imp_path):
            imp_df = pd.read_csv(imp_path)

            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            ax.barh(imp_df["Feature"], imp_df["Importance"])
            ax.invert_yaxis()
            ax.set_title("Feature Importance")

            st.pyplot(fig)

            top_feature = imp_df.iloc[0]["Feature"]

        else:
            st.warning("Feature importance file not found")

        st.markdown("---")


        st.subheader(f"{model_name} Visual Analysis")

        plots = MODEL_ASSETS[model_name]["plots"]
        folder = MODEL_ASSETS[model_name]["folder"]

        col1, col2 = st.columns(2)

        if len(plots) > 0:
            path1 = os.path.join(folder, plots[0])
            if os.path.exists(path1):
                with col1:
                    st.image(path1, caption="Actual vs Predicted")
                    
        if len(plots) > 1:
            path2 = os.path.join(folder, plots[1])
            if os.path.exists(path2):
                with col2:
                    st.image(path2, caption="Residual Plot")