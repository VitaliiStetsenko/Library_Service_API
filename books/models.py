from django.db import models


class Book(models.Model):
    class BookChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=200)
    cover = models.CharField(max_length=4, choices=BookChoices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
