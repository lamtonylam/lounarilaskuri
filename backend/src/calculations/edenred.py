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
    if total_price < minimum_lunch_card_payment:
        return {
            'card_payments': [],
            'cash_payment': round(total_price, 2),
            'total_cash_amount': round(total_price, 2),
            'total_card_amount': 0.0,
            'card_uses': 0,
            'total_amount': round(total_price, 2)
        }
    
    best_cash_amount = total_price
    best_card_payments = []
    
    # Try different numbers of card uses to find the optimal solution
    max_possible_uses = min(maximum_card_payment_times_per_day, int(total_price / minimum_lunch_card_payment))
    
    for num_uses in range(1, max_possible_uses + 1):
        # Calculate the optimal card total for this number of uses
        max_card_total = min(num_uses * maximum_lunch_card_payment, total_price)
        
        # Try to distribute payments as evenly as possible
        if max_card_total == total_price:
            # We can pay everything with cards
            avg_payment = total_price / num_uses
            if avg_payment >= minimum_lunch_card_payment and avg_payment <= maximum_lunch_card_payment:
                # Handle rounding to ensure total matches exactly
                card_payments = [round(avg_payment, 2)] * num_uses
                # Adjust the last payment to account for rounding differences
                total_rounded = sum(card_payments)
                if total_rounded != total_price:
                    card_payments[-1] += round(total_price - total_rounded, 2)
                cash_amount = 0
            else:
                # Need mixed payments
                card_payments = []
                remaining = total_price
                
                for i in range(num_uses):
                    if i == num_uses - 1:  # Last payment
                        payment = remaining
                    else:
                        payment = min(maximum_lunch_card_payment, remaining / (num_uses - i))
                        payment = max(minimum_lunch_card_payment, payment)
                    
                    if payment >= minimum_lunch_card_payment and payment <= maximum_lunch_card_payment and remaining >= payment:
                        card_payments.append(payment)
                        remaining -= payment
                    else:
                        break
                
                cash_amount = remaining
        else:
            # Some amount will be paid in cash
            card_total = max_card_total
            cash_amount = total_price - card_total
            
            # Distribute card payments optimally
            avg_payment = card_total / num_uses
            if avg_payment >= minimum_lunch_card_payment and avg_payment <= maximum_lunch_card_payment:
                # Handle rounding to ensure total matches exactly
                card_payments = [round(avg_payment, 2)] * num_uses
                # Adjust the last payment to account for rounding differences
                total_rounded = sum(card_payments)
                if total_rounded != card_total:
                    card_payments[-1] += round(card_total - total_rounded, 2)
            else:
                # Create mixed payments
                card_payments = []
                remaining_card = card_total
                
                for i in range(num_uses):
                    if i == num_uses - 1:
                        payment = remaining_card
                    else:
                        payment = min(maximum_lunch_card_payment, remaining_card / (num_uses - i))
                        payment = max(minimum_lunch_card_payment, payment)
                    
                    if payment >= minimum_lunch_card_payment and payment <= maximum_lunch_card_payment:
                        card_payments.append(payment)
                        remaining_card -= payment
                    else:
                        break
                
                if remaining_card > 0:
                    cash_amount += remaining_card
        
        # Check if this solution is better
        if cash_amount < best_cash_amount and len(card_payments) == num_uses:
            best_cash_amount = cash_amount
            best_card_payments = card_payments
    
    total_card_amount = sum(best_card_payments)
    
    return {
        'card_payments': [round(p, 2) for p in best_card_payments],
        'cash_payment': round(best_cash_amount, 2),
        'total_cash_amount': round(best_cash_amount, 2),
        'total_card_amount': round(total_card_amount, 2),
        'card_uses': len(best_card_payments),
        'total_amount': round(total_price, 2)
    }
