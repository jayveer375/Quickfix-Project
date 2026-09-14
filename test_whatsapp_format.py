"""
Test script to verify WhatsApp phone number formatting
"""

def whatsapp_format(phone_number):
    """
    Format phone number for WhatsApp link
    Removes all non-digit characters
    For 10-digit numbers, adds India country code (+91)
    For numbers with +, preserves the country code
    """
    if not phone_number:
        return ''
    
    original = str(phone_number).strip()
    # Remove all non-digit characters
    clean_number = ''.join(filter(str.isdigit, original))
    
    # If original had + and resulted in 10 digits, user likely entered country code separately
    # Example: "+95 1 210 8880" -> "9512108880" (10 digits)
    # In this case, we should NOT add 91
    if original.startswith('+'):
        # User explicitly provided country code, use as-is
        return clean_number
    
    # If number is exactly 10 digits and no + was present, assume India (+91)
    if len(clean_number) == 10:
        clean_number = '91' + clean_number
    
    return clean_number

# Test cases
test_numbers = [
    '+95 1 210 8880',      # Myanmar number - should be 9512108880
    '951 210 8880',        # Without + - 10 digits
    '9512108880',          # 10 digits
    '1234567890',          # 10 digits
    '+91 98765 43210',     # India number - should be 919876543210
    '(951) 210-8880',      # 10 digits
    '951-210-8880',        # 10 digits
    '+1 234 567 8900',     # US number - should be 12345678900
]

print("WhatsApp Phone Number Formatting Test\n")
print("-" * 60)

for number in test_numbers:
    formatted = whatsapp_format(number)
    clean = ''.join(filter(str.isdigit, str(number)))
    print(f"Input:  {number:20} (digits: {clean}, len: {len(clean)})")
    print(f"Output: {formatted}")
    print(f"WhatsApp Link: https://wa.me/{formatted}")
    print("-" * 60)
