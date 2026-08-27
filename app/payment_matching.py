from app.database import SessionLocal
from app.models import Invoice, Payment


def match_payments():
    db = SessionLocal()

    payments = db.query(Payment).all()
    invoices = db.query(Invoice).all()

    results = []

    for payment in payments:
        best_match = None

        for invoice in invoices:
            if (
                payment.customer_name == invoice.customer_name
                and payment.amount == invoice.total_amount
            ):
                best_match = invoice
                break

        if best_match:
            payment.status = "Matched"
            best_match.status = "Paid"

            results.append({
                "payment_id": payment.id,
                "invoice_number": best_match.invoice_number,
                "customer": payment.customer_name,
                "payment_amount": payment.amount,
                "status": "Matched"
            })
        else:
            results.append({
                "payment_id": payment.id,
                "invoice_number": "No Match",
                "customer": payment.customer_name,
                "payment_amount": payment.amount,
                "status": "Unmatched"
            })

    db.commit()
    db.close()

    return results
