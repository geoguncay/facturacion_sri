from datetime import datetime


def modulo11(key):

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


def generate_access_key(ruc, estab, pto_emision, secuencial):

    date = datetime.now().strftime("%d%m%Y")

    invoice_type = "01"
    ambiente = "1"
    number_code = "12345678"
    emision_type = "1"

    key = (
        date +
        invoice_type +
        ruc +
        ambiente +
        estab +
        pto_emision +
        secuencial +
        number_code +
        emision_type
    )

    digit = modulo11(key)

    return key + str(digit)