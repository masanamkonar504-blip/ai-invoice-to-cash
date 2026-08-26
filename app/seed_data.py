from app.database import engine, Base, SessionLocal
from app.models import Customer, Invoice, Payment, Dispute


# Create database tables
Base.metadata.create_all(bind=engine)

# Open database session
db = SessionLocal()


# -----------------------------
# Customers
# -----------------------------

customers = [
    Customer(
        name="ABC Technologies",
        country="India",
        currency="INR"
    ),
    Customer(
        name="Global Solutions Ltd",
        country="USA",
        currency="USD"
    ),
    Customer(
        name="Euro Systems GmbH",
        country="Germany",
        currency="EUR"
    ),
    Customer(
        name="Dubai Trading LLC",
        country="UAE",
        currency="AED"
    ),
    Customer(
        name="Singapore Digital Pte Ltd",
        country="Singapore",
        currency="SGD"
    )
]


# -----------------------------
# Invoices
# -----------------------------

invoices = [
    Invoice(
        invoice_number="INV-1001",
        customer_name="ABC Technologies",
        amount=50000,
        tax=9000,
        total_amount=59000,
        status="Paid"
    ),
    Invoice(
        invoice_number="INV-1002",
        customer_name="Global Solutions Ltd",
        amount=1000,
        tax=180,
        total_amount=1180,
        status="Paid"
    ),
    Invoice(
        invoice_number="INV-1003",
        customer_name="Euro Systems GmbH",
        amount=2500,
        tax=475,
        total_amount=2975,
        status="Partially Paid"
    ),
    Invoice(
        invoice_number="INV-1004",
        customer_name="Dubai Trading LLC",
        amount=75000,
        tax=3750,
        total_amount=78750,
        status="Pending"
    ),
    Invoice(
        invoice_number="INV-1005",
        customer_name="Singapore Digital Pte Ltd",
        amount=5000,
        tax=450,
        total_amount=5450,
        status="Disputed"
    )
]


# -----------------------------
# Payments
# -----------------------------

payments = [
    Payment(
        customer_name="ABC Technologies",
        amount=59000,
        reference="INV-1001",
        status="Matched"
    ),
    Payment(
        customer_name="Global Solutions Ltd",
        amount=1180,
        reference="INV-1002",
        status="Matched"
    ),
    Payment(
        customer_name="Euro Systems GmbH",
        amount=2500,
        reference="INV-1003",
        status="Partial Match"
    ),
    Payment(
        customer_name="Dubai Trading LLC",
        amount=78750,
        reference="INV-1004",
        status="Unmatched"
    ),
    Payment(
        customer_name="Singapore Digital Pte Ltd",
        amount=5000,
        reference="INV-1005",
        status="Disputed"
    )
]


# -----------------------------
# Disputes
# -----------------------------

disputes = [
    Dispute(
        invoice_number="INV-1003",
        difference=475,
        reason="Tax/payment mismatch",
        priority="Medium",
        status="Open"
    ),
    Dispute(
        invoice_number="INV-1005",
        difference=450,
        reason="Payment amount mismatch",
        priority="High",
        status="Open"
    )
]


# Add data to database
db.add_all(customers)
db.add_all(invoices)
db.add_all(payments)
db.add_all(disputes)

db.commit()

db.close()

print("Sample data inserted successfully!")
