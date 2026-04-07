from datetime import datetime


def module11(key):

    factor = 2
    total = 0
    for num in reversed(key):
        total += int(num) * factor
        factor += 1
        if factor > 7:
            factor = 2

    mod = total % 11
    digit = 11 - mod
    if digit == 11:
        digit = 0
    if digit == 10:
        digit = 1
    return digit


def generate_access_key(ruc, estab, emission_point, sequential):

    date = datetime.now().strftime("%d%m%Y")
    invoice_type = "01"
    ambient = "1"
    number_code = "12345678"
    emission_type = "1"

    key = (
        date +
        invoice_type +
        ruc +
        ambient +
        estab +
        emission_point +
        sequential +
        number_code +
        emission_type
    )

    digit = module11(key)

    return key + str(digit)