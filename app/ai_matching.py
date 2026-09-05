from difflib import SequenceMatcher


def calculate_confidence(
    payment_customer,
    invoice_customer,
    payment_amount,
    invoice_amount,
    reference_match
):
    score = 0

    # Invoice reference match
    if reference_match:
        score += 50

    # Customer name similarity
    similarity = SequenceMatcher(
        None,
        payment_customer.lower().strip(),
        invoice_customer.lower().strip()
    ).ratio()

    if similarity >= 0.95:
        score += 30
    elif similarity >= 0.80:
        score += 20
    elif similarity >= 0.60:
        score += 10

    # Amount match
    difference = abs(payment_amount - invoice_amount)

    if difference <= 0.01:
        score += 20
    elif difference <= 100:
        score += 10

    # Confidence level
    if score >= 90:
        level = "High"
    elif score >= 70:
        level = "Medium"
    else:
        level = "Low"

    return score, level
