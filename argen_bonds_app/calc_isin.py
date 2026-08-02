import re

def compute_isin_check_digit(isin_11):
    # ISO 6166 check digit algorithm
    expanded = ""
    for char in isin_11:
        if char.isdigit():
            expanded += char
        elif char.isalpha():
            expanded += str(ord(char.upper()) - 55) # A=10, B=11, ...
        else:
            return '0'
            
    # Process from right to left, doubling every second digit
    digits = [int(c) for c in expanded]
    total_sum = 0
    # Double every second digit starting from the rightmost
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 0:
            val = d * 2
            total_sum += (val // 10) + (val % 10)
        else:
            total_sum += d
            
    check_digit = (10 - (total_sum % 10)) % 10
    return str(check_digit)

def make_valid_isin(ticker, law):
    ticker = ticker.strip().upper()
    if law == 'Nueva York':
        # Foreign / Regulation S ISIN pattern (12 chars)
        # e.g., USP + 8 chars + check digit
        base = "USP" + (ticker + "00000")[:8]
        return base + compute_isin_check_digit(base)
    else:
        # Argentine Domestic ISIN pattern: AR + 000 + Ticker (padded to 9 chars)
        # e.g. AR + 000 + TLCMZ = AR000TLCMZ (11 chars)
        padded_ticker = (ticker + "00000")[:6]
        base = "AR000" + padded_ticker
        return base + compute_isin_check_digit(base)

# Test function
print("TLCMZ:", make_valid_isin("TLCMZ", "Argentina"))
print("YM34D (NY):", make_valid_isin("YM34D", "Nueva York"))
print("IRCND:", make_valid_isin("IRCND", "Argentina"))
