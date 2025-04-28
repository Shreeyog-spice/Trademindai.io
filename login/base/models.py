from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    btc_balance = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    usdt_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    login_streak = models.IntegerField(default=0)
    last_reward_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Wallet of {self.user.username}"
