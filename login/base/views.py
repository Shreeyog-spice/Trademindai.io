from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Wallet
from datetime import date, timedelta
from decimal import Decimal
import random
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

def home(request):
    return render(request, 'registration/home.html')

def authView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the new user
            wallet = Wallet.objects.create(user=user)  # Create a wallet for the new user
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful signup
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

@require_POST
@login_required
def get_login_reward(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    today = date.today()
    reward_details = {
        "amount": 0,
        "currency": "",
        "message": "",
        "streak": wallet.login_streak,
        "upcoming_rewards": [],
    }

    # Check if the user has already received their reward today
    if wallet.last_reward_date == today:
        reward_details['message'] = "You have already received your login reward today."
    else:
        # Update streak based on last reward date
        if wallet.last_reward_date == today - timedelta(days=1):
            wallet.login_streak += 1
        else:
            wallet.login_streak = 1

        wallet.last_reward_date = today

        # Generate a random reward
        currency = random.choice(['cash', 'btc', 'usdt'])

        if currency == 'cash':
            amount = Decimal(str(round(random.uniform(5, 15), 2)))
            wallet.cash_balance += amount
            reward_details['currency'] = 'Cash'
        elif currency == 'btc':
            amount = Decimal(str(round(random.uniform(0.00001, 0.0001), 6)))
            wallet.btc_balance += amount
            reward_details['currency'] = 'BTC'
        elif currency == 'usdt':
            amount = Decimal(str(round(random.uniform(2, 10), 2)))
            wallet.usdt_balance += amount
            reward_details['currency'] = 'USDT'

        reward_details['amount'] = float(amount)
        wallet.save()

        # Construct the message for the user
        reward_details['message'] = f"Login reward: {amount} {reward_details['currency']} (Streak: {wallet.login_streak})"
        reward_details['streak'] = wallet.login_streak

    # Predict the next 5 days of rewards (not stored in DB, for display purposes)
    for i in range(1, 6):
        streak = wallet.login_streak + i
        currency = random.choice(['cash', 'btc', 'usdt'])

        if currency == 'cash':
            amount = round(random.uniform(5, 15), 2)
            symbol = 'Cash'
        elif currency == 'btc':
            amount = round(random.uniform(0.00001, 0.0001), 6)
            symbol = 'BTC'
        else:
            amount = round(random.uniform(2, 10), 2)
            symbol = 'USDT'

        reward_details['upcoming_rewards'].append({
            'day': str(today + timedelta(days=i)),
            'amount': amount,
            'currency': symbol,
            'streak': streak
        })

    return JsonResponse(reward_details)

def check_balance(request):
    if request.user.is_authenticated:
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        return render(request, 'check_balance.html', {
            'cash_balance': wallet.cash_balance,
            'btc_balance': wallet.btc_balance,
            'usdt_balance': wallet.usdt_balance,
        })
    else:
        return redirect('login')
