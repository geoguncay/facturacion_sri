from app.database import models


def calculate_total(details):

    total = 0

    for d in details:

        subtotal = d["quantity"] * d["price"]
        total += subtotal

    return total