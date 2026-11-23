import secrets


def generate_pnr() -> str:
    """
    Generates a unique 10-digit PNR number formatted like standard Indian Railway PNRs.
    First digit 2-8, followed by 9 random digits.
    """
    first_digit = str(secrets.randbelow(7) + 2)  # 2 to 8
    remaining_digits = "".join(str(secrets.randbelow(10)) for _ in range(9))
    return f"{first_digit}{remaining_digits}"
