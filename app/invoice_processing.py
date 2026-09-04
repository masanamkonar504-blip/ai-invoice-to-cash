from app.database import SessionLocal
from app.models import Invoice


def validate_invoices():
    db = SessionLocal()
    results = []

    try:
        invoices = db.query(Invoice).all()

        for invoice in invoices:

            errors = []

            # Check invoice number
            if not invoice.invoice_number:
                errors.append("Missing invoice number")

            # Check customer
            if not invoice.customer_name:
                errors.append("Missing customer name")

            # Check amount
            if invoice.amount is None or invoice.amount < 0:
                errors.append("Invalid invoice amount")

            # Check tax
            if invoice.tax is None or invoice.tax < 0:
                errors.append("Invalid tax")

            # Check total amount
            if invoice.total_amount is None or invoice.total_amount < 0:
                errors.append("Invalid total amount")

            # Check calculation
            if (
                invoice.amount is not None
                and invoice.tax is not None
                and invoice.total_amount is not None
            ):
                expected_total = round(
                    invoice.amount + invoice.tax, 2
                )

                if abs(expected_total - invoice.total_amount) > 0.01:
                    errors.append("Invoice total calculation mismatch")

            # Validation result
            if errors:
                status = "Invalid"
                message = "; ".join(errors)
            else:
                status = "Valid"
                message = "Invoice passed validation"

            results.append({
                "invoice_number": invoice.invoice_number,
                "customer": invoice.customer_name,
                "amount": invoice.amount,
                "tax": invoice.tax,
                "total_amount": invoice.total_amount,
                "status": status,
                "message": message
            })

        return results

    finally:
        db.close()
