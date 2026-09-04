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
from app.database import SessionLocal
from app.models import Invoice, Payment, Dispute

TOLERANCE = 0.01


def detect_disputes():
    db = SessionLocal()
    results = []

    try:
        invoices = db.query(Invoice).all()
        payments = db.query(Payment).all()

        for invoice in invoices:

            # 1. First try to find payment using invoice reference
            payment = (
                db.query(Payment)
                .filter(Payment.reference == invoice.invoice_number)
                .order_by(Payment.id.desc())
                .first()
            )

            # 2. If reference is unavailable, match using customer name
            if payment is None:
                payment = (
                    db.query(Payment)
                    .filter(Payment.customer_name == invoice.customer_name)
                    .order_by(Payment.id.desc())
                    .first()
                )

            # No payment found
            if payment is None:
                continue

            # Calculate difference
            difference = round(
                abs(invoice.total_amount - payment.amount), 2
            )

            # Payment matches invoice
            if difference <= TOLERANCE:
                continue

            # Priority
            if difference >= 1000:
                priority = "High"
            elif difference >= 500:
                priority = "Medium"
            else:
                priority = "Low"

            reason = "Payment amount does not match invoice amount"

            # 3. Check whether dispute already exists
            existing = (
                db.query(Dispute)
                .filter(
                    Dispute.invoice_number == invoice.invoice_number,
                    Dispute.status == "Open"
                )
                .first()
            )

            if existing:
                # Update existing dispute instead of creating duplicate
                existing.difference = difference
                existing.reason = reason
                existing.priority = priority

            else:
                # Create new dispute
                dispute = Dispute(
                    invoice_number=invoice.invoice_number,
                    difference=difference,
                    reason=reason,
                    priority=priority,
                    status="Open"
                )

                db.add(dispute)

            results.append({
                "invoice_number": invoice.invoice_number,
                "customer": invoice.customer_name,
                "invoice_amount": invoice.total_amount,
                "payment_amount": payment.amount,
                "difference": difference,
                "priority": priority,
                "status": "Open"
            })

        db.commit()

        return results

    finally:
        db.close()
