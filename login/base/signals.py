from django.db import transaction
from django.utils import timezone
import random
from datetime import date, timedelta
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from decimal import Decimal  # Import Decimal
from .models import Wallet

@receiver(user_logged_in)
def give_login_reward(sender, request, user, **kwargs):
    wallet = Wallet.objects.get(user=user)
    today = date.today()

    reward_details = {
        "amount": 0,
        "currency": "",
        "message": "",
    }

    # Only give a reward if the user hasn't already been rewarded today
    if wallet.last_reward_date == today:
        return reward_details  # Already rewarded today, return without any changes

    # Handle streaks
    if wallet.last_reward_date == today - timedelta(days=1):
        wallet.login_streak += 1
    else:
        wallet.login_streak = 1

    wallet.last_reward_date = today

    # Pick a random currency and reward amount
    currency = random.choice(['cash', 'btc', 'usdt'])
    if currency == 'cash':
        amount = Decimal(str(round(random.uniform(5, 15), 2)))  # Convert to Decimal
        wallet.cash_balance += amount
        reward_details['currency'] = 'Cash'
        reward_details['amount'] = float(amount)  # Convert to float for the response
    elif currency == 'btc':
        amount = Decimal(str(round(random.uniform(0.00001, 0.0001), 6)))  # Convert to Decimal
        wallet.btc_balance += amount
        reward_details['currency'] = 'BTC'
        reward_details['amount'] = float(amount)  # Convert to float for the response
    elif currency == 'usdt':
        amount = Decimal(str(round(random.uniform(2, 10), 2)))  # Convert to Decimal
        wallet.usdt_balance += amount
        reward_details['currency'] = 'USDT'
        reward_details['amount'] = float(amount)  # Convert to float for the response

    wallet.save()

    # Set the message for the pop-up
    reward_details['message'] = f"Login reward given: {reward_details['amount']} {reward_details['currency']} (streak: {wallet.login_streak})"

    # Send the reward details to the frontend (can be handled by views or AJAX)
    return reward_details
