"""
Edenred Payment Optimization Module
This module provides calculations for edenred, where employer pays for food as salary"""

minimum_lunch_card_payment = 8.60
maximum_lunch_card_payment = 13.70
maximum_card_payment_times_per_day = 5

def calculate_optimal_payment(total_price):
    """
    Calculate the best way to pay for food to minimize cash payments.
    
    Args:
        total_price: Total price of food to pay
        
    Returns:
        dict: Contains card_payments, cash_payments, and total_cash_amount
    """
    card_payments = []
    remaining_price = total_price
    card_uses = 0
    
    # Use maximum card payments first to minimize cash
    while (card_uses < maximum_card_payment_times_per_day and 
           remaining_price >= minimum_lunch_card_payment):
        
        # Pay maximum allowed amount with card
        card_payment = min(maximum_lunch_card_payment, remaining_price)
        
        # Only use card if payment meets minimum requirement
        if card_payment >= minimum_lunch_card_payment:
            card_payments.append(card_payment)
            remaining_price -= card_payment
            card_uses += 1
        else:
            break
    
    cash_amount = remaining_price
    total_card_amount = sum(card_payments)
    
    return {
        'card_payments': [round(payment, 2) for payment in card_payments],
        'cash_payment': round(cash_amount, 2),
        'total_cash_amount': round(cash_amount, 2),
        'total_card_amount': round(total_card_amount, 2),
        'card_uses': len(card_payments),
        'total_amount': round(total_price, 2)
    }