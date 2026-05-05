import streamlit as st
import streamlit.components.v1 as components

def run():

    st.set_page_config(page_title="Executive Dashboard", layout="wide")

    st.title("Business Dashboard")

    power_bi_url = "https://app.powerbi.com/groups/me/reports/71843a3e-69bf-4e7e-98c9-814a4d730b26/ReportSection"

    st.markdown("---")

    st.image(r"E:\SEM 8\Sales_Intelligence_System\Code_Implementation\Integrated_system\data\executive_dashboard.png")

    st.link_button("Open Full Dashboard", power_bi_url)

    st.markdown("---")

    st.subheader("Download Dashboard File")

    with open("executive_dashboard.pbix", "rb") as file:
        st.download_button(
            label="Download PBIX File",
            data=file,
            file_name="Eexecutive_Dashboard.pbix"
        )