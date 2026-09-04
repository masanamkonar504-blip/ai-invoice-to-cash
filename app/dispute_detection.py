from app.database import SessionLocal
from app.models import Invoice, Payment, Dispute


def detect_disputes():
    db = SessionLocal()

    invoices = db.query(Invoice).all()
    payments = db.query(Payment).all()

    results = []

    for invoice in invoices:
        matching_payment = None

        for payment in payments:
            if payment.customer_name == invoice.customer_name:
                matching_payment = payment
                break

        if matching_payment:
            difference = round(
                invoice.total_amount - matching_payment.amount, 2
            )

            if difference != 0:
                if abs(difference) >= 1000:
                    priority = "High"
                elif abs(difference) >= 500:
                    priority = "Medium"
                else:
                    priority = "Low"

                dispute = Dispute(
                    invoice_number=invoice.invoice_number,
                    difference=abs(difference),
                    reason="Payment amount does not match invoice amount",
                    priority=priority,
                    status="Open"
                )

                db.add(dispute)

                results.append({
                    "invoice_number": invoice.invoice_number,
                    "customer": invoice.customer_name,
                    "invoice_amount": invoice.total_amount,
                    "payment_amount": matching_payment.amount,
                    "difference": abs(difference),
                    "priority": priority,
                    "status": "Open"
                })

    db.commit()
    db.close()

    return results
