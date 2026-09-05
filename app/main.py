import streamlit as st
from sqlalchemy import text

from app.database import engine, Base, SessionLocal
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
        st.dataframe(results, width="stretch")
    else:
        st.info("No payments found.")
from app.dispute_detection import detect_disputes

st.divider()

st.header("⚠️ AI Dispute Detection")

st.write("Detect invoice and payment mismatches automatically.")

if st.button("🔎 Detect Disputes"):
    disputes = detect_disputes()

    if disputes:
        st.warning("Potential disputes detected!")
        st.dataframe(disputes, width="stretch")
    else:
        st.success("No payment disputes detected.")
from app.invoice_processing import validate_invoices

st.divider()

st.header("📄 Invoice Processing & Validation")

st.write("Validate invoices and detect calculation errors automatically.")

if st.button("✅ Validate Invoices"):
    invoices = validate_invoices()

    if invoices:
        st.success("Invoice validation completed!")

        st.dataframe(
            invoices,
            width="stretch"
        )
    else:
        st.info("No invoices found.")
st.divider()

st.divider()

st.header("📤 Invoice Upload")

st.write("Upload invoice data in CSV format.")

uploaded_file = st.file_uploader(
    "Choose an invoice CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    import pandas as pd

    invoice_data = pd.read_csv(uploaded_file)

    st.success("Invoice file uploaded successfully!")

    st.write("### 📋 Invoice Preview")

    st.dataframe(
        invoice_data,
        width="stretch"
    )

    st.write(f"Total records uploaded: {len(invoice_data)}")

    if st.button("💾 Save Valid Invoices"):

        required_columns = [
            "invoice_number",
            "customer_name",
            "amount",
            "tax",
            "total_amount",
            "status"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in invoice_data.columns
        ]

        if missing_columns:
            st.error(
                "Missing columns: "
                + ", ".join(missing_columns)
            )

        else:
            db = SessionLocal()

            saved_count = 0
            skipped_count = 0

            for _, row in invoice_data.iterrows():

                existing_invoice = (
                    db.query(Invoice)
                    .filter(
                        Invoice.invoice_number
                        == str(row["invoice_number"])
                    )
                    .first()
                )

                if existing_invoice:
                    skipped_count += 1
                    continue

                expected_total = round(
                    float(row["amount"]) + float(row["tax"]),
                    2
                )

                uploaded_total = round(
                    float(row["total_amount"]),
                    2
                )

                if abs(expected_total - uploaded_total) > 0.01:
                    skipped_count += 1
                    continue

                invoice = Invoice(
                    invoice_number=str(row["invoice_number"]),
                    customer_name=str(row["customer_name"]),
                    amount=float(row["amount"]),
                    tax=float(row["tax"]),
                    total_amount=float(row["total_amount"]),
                    status=str(row["status"])
                )

                db.add(invoice)
                saved_count += 1

            db.commit()
            db.close()

            st.success(
                f"✅ {saved_count} invoice(s) saved successfully!"
            )

            if skipped_count > 0:
                st.warning(
                    f"⚠️ {skipped_count} invoice(s) skipped."
                )
