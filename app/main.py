import streamlit as st

st.set_page_config(
    page_title="AI Invoice-to-Cash",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Invoice-to-Cash")
st.subheader("Intelligent Billing, Payment Matching & Dispute Resolution")

st.info("Project foundation is ready. AI modules will be added next.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Invoices", 0)

with col2:
    st.metric("Payments Received", 0)

with col3:
    st.metric("Matched", 0)

with col4:
    st.metric("Disputes", 0)
