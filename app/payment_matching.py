from app.database import SessionLocal
from app.models import Invoice, Payment


def match_payments():
    db = SessionLocal()
    results = []

    try:
        payments = db.query(Payment).all()
        invoices = db.query(Invoice).all()

        for payment in payments:

            # First: match using invoice reference
            invoice = None

            if payment.reference:
                invoice = (
                    db.query(Invoice)
                    .filter(
                        Invoice.invoice_number == payment.reference
                    )
                    .first()
                )

            # Second: fallback to customer name
            if invoice is None:
                invoice = (
                    db.query(Invoice)
                    .filter(
                        Invoice.customer_name == payment.customer_name
                    )
                    .first()
                )

            if invoice is None:
                payment.status = "Unmatched"

                results.append({
                    "payment_id": payment.id,
                    "invoice_number": "No Match",
                    "customer": payment.customer_name,
                    "payment_amount": payment.amount,
                    "invoice_amount": 0,
                    "difference": payment.amount,
                    "status": "Unmatched"
                })

                continue

            # Calculate difference
            difference = round(
                abs(invoice.total_amount - payment.amount), 2
            )

            # Exact payment
            if difference <= 0.01:
                payment.status = "Matched"

                if invoice.status != "Disputed":
                    invoice.status = "Paid"

                status = "Matched"

            # Partial payment
            else:
                payment.status = "Partial Match"

                if payment.amount < invoice.total_amount:
                    invoice.status = "Partially Paid"
                else:
                    invoice.status = "Disputed"

                status = "Partial Match"

            results.append({
                "payment_id": payment.id,
                "invoice_number": invoice.invoice_number,
                "customer": payment.customer_name,
                "payment_amount": payment.amount,
                "invoice_amount": invoice.total_amount,
                "difference": difference,
                "status": status
            })

        db.commit()

        return results

    finally:
        db.close()
