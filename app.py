import streamlit as st

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
button[data-baseweb="tab"] {
    font-size: 22px;
    font-weight: 700;
    padding: 14px 28px;
    margin-right: 10px;
    border-radius: 12px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #ff4b4b !important;
    color: white !important;
    box-shadow: 0px 4px 12px rgba(255,75,75,0.4);
    border-bottom: none !important;
}

div[data-baseweb="tab-highlight"] {
    display: none !important;
}

button[data-baseweb="tab"]:hover {
    background-color: rgba(255, 75, 75, 0.15);
    color: #ff4b4b;
}


div[data-baseweb="tab-list"] {
    gap: 12px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="AI Sales Intelligence System",
    layout="wide",
    initial_sidebar_state="collapsed"

)

st.title("AI Sales Intelligence Platform")

st.markdown("### Transforming Data into Business Decisions")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    " Lead Scoring",
    " Customer Intelligence",
    " CLV Prediction",
    "Executive Power BI Dashboard"
])

with tab1:
    import pages.lead_scoring as lead
    lead.run()

with tab2:
    import pages.rfm_analysis as rfm
    rfm.run()
   

with tab3:
    import pages.clv_prediction as clv
    clv.run()
        
with tab4:
    import pages.dashboard as dash
    dash.run()