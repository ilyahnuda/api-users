from django.db import models
from django.contrib.auth.models import AbstractUser

STANDARD_CATEGORIES = ["Забота о себе", "Зарплата", "Здоровье и фитнес", "Кафе и рестораны", "Машина",
                       "Образование",
                       "Отдых и развлечения", "Платежи, комиссии", "Покупки: одежда, техника", "Продукты", "Проезд"]


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    payments_balance = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        self.categories.set(Category.objects.filter(name__in=STANDARD_CATEGORIES))


class Transaction(models.Model):
    date_creation = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    summary = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    description = models.TextField(null=False, blank=False)
    organization = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.pk

    def save(self, *args, **kwargs):
        if self.category.name == 'Зарплата':
            self.user.payments_balance += self.summary
        else:
            self.user.payments_balance -= self.summary
        self.user.save()
        super(Transaction, self).save(*args, **kwargs)

