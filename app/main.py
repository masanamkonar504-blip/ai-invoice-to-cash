import streamlit as st
from sqlalchemy import text

from app.database import engine, Base
from app.models import Customer, Invoice, Payment, Dispute


# Create database tables
Base.metadata.create_all(bind=engine)


# Page configuration
st.set_page_config(
    page_title="AI Invoice-to-Cash",
    page_icon="💰",
    layout="wide"
)


# Title
st.title("💰 AI Invoice-to-Cash")
st.subheader(
    "Intelligent Billing, Payment Matching & Dispute Resolution"
)


# Dashboard metrics
with engine.connect() as connection:

    customer_count = connection.execute(
        text("SELECT COUNT(*) FROM customers")
    ).scalar()

    invoice_count = connection.execute(
        text("SELECT COUNT(*) FROM invoices")
    ).scalar()

    payment_count = connection.execute(
        text("SELECT COUNT(*) FROM payments")
    ).scalar()

    dispute_count = connection.execute(
        text("SELECT COUNT(*) FROM disputes")
    ).scalar()


# Display metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Customers", customer_count)

with col2:
    st.metric("Invoices", invoice_count)

with col3:
    st.metric("Payments", payment_count)

with col4:
    st.metric("Disputes", dispute_count)


# Project status
st.divider()

st.success("✅ Database connected successfully!")

st.info(
    "The AI Invoice-to-Cash platform is ready for customer, "
    "invoice and payment data."
)


# Modules
st.divider()

st.subheader("🚀 System Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("📄 **Invoice Processing**")
    st.write("Upload and validate invoices.")

with col2:
    st.write("💳 **Payment Matching**")
    st.write("Automatically match payments with invoices.")

with col3:
    st.write("⚠️ **Dispute Detection**")
    st.write("Detect mismatches and potential disputes.")
    
from app.payment_matching import match_payments
    
st.divider()

st.header("💳 Payment Matching")

st.write("Automatically match customer payments with invoices.")

if st.button("🔍 Match Payments"):
    results = match_payments()

    if results:
        st.success("Payment matching completed successfully!")
        st.dataframe(results, use_container_width=True)
    else:
        st.info("No payments found.")
