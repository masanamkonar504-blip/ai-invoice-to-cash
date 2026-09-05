import numpy as np
from sklearn.ensemble import RandomForestClassifier


def train_model():
    # Training features:
    # reference_match, customer_match, amount_difference

    X = np.array([
        [1, 1, 0],
        [1, 1, 10],
        [1, 1, 50],
        [1, 1, 100],
        [1, 1, 500],
        [1, 1, 1000],
        [0, 1, 0],
        [0, 1, 50],
        [0, 1, 500],
        [0, 0, 1000],
        [0, 0, 5000],
        [1, 0, 500],
        [1, 0, 2000],
    ])

    # 0 = Matched
    # 1 = Partial Match
    # 2 = Mismatch

    y = np.array([
        0,
        0,
        0,
        1,
        1,
        2,
        0,
        1,
        1,
        2,
        2,
        1,
        2,
    ])

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def predict_payment(
    reference_match,
    customer_match,
    amount_difference
):
    model = train_model()

    features = np.array([[
        int(reference_match),
        int(customer_match),
        amount_difference
    ]])

    prediction = model.predict(features)[0]

    if prediction == 0:
        return "Matched"

    elif prediction == 1:
        return "Partial Match"

    else:
        return "Mismatch"
