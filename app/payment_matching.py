from app.database import SessionLocal
from app.models import Invoice, Payment
from app.ai_matching import calculate_confidence
from app.ml_model import predict_payment


def match_payments():
    db = SessionLocal()
    results = []

    try:
        payments = db.query(Payment).all()
        invoices = db.query(Invoice).all()

        for payment in payments:

            invoice = None
            reference_match = False
            customer_match = False

            # 1. Try invoice reference
            if payment.reference:
                invoice = (
                    db.query(Invoice)
                    .filter(
                        Invoice.invoice_number == payment.reference
                    )
                    .first()
                )

                if invoice:
                    reference_match = True

            # 2. Fallback to customer name
            if invoice is None:
                invoice = (
                    db.query(Invoice)
                    .filter(
                        Invoice.customer_name == payment.customer_name
                    )
                    .first()
                )

            # No invoice found
            if invoice is None:
                payment.status = "Unmatched"

                results.append({
                    "payment_id": payment.id,
                    "invoice_number": "No Match",
                    "customer": payment.customer_name,
                    "payment_amount": payment.amount,
                    "invoice_amount": 0,
                    "difference": payment.amount,
                    "confidence": 0,
                    "confidence_level": "Low",
                    "ml_prediction": "Mismatch",
                    "status": "Unmatched"
                })

                continue

            # Check customer match
            if (
                payment.customer_name.strip().lower()
                == invoice.customer_name.strip().lower()
            ):
                customer_match = True

            # Calculate difference
            difference = round(
                abs(invoice.total_amount - payment.amount), 2
            )

            # Calculate confidence
            confidence, confidence_level = calculate_confidence(
                payment.customer_name,
                invoice.customer_name,
                payment.amount,
                invoice.total_amount,
                reference_match
            )

            # ML prediction
            ml_prediction = predict_payment(
                reference_match,
                customer_match,
                difference
            )

            # Final payment status
            if difference <= 0.01:
                payment.status = "Matched"

                if invoice.status != "Disputed":
                    invoice.status = "Paid"

                status = "Matched"

            elif payment.amount < invoice.total_amount:
                payment.status = "Partial Match"
                invoice.status = "Partially Paid"
                status = "Partial Match"

            else:
                payment.status = "Mismatch"
                invoice.status = "Disputed"
                status = "Amount Mismatch"

            results.append({
                "payment_id": payment.id,
                "invoice_number": invoice.invoice_number,
                "customer": payment.customer_name,
                "payment_amount": payment.amount,
                "invoice_amount": invoice.total_amount,
                "difference": difference,
                "confidence": confidence,
                "confidence_level": confidence_level,
                "ml_prediction": ml_prediction,
                "status": status
            })

        db.commit()

        return results

    finally:
        db.close()
