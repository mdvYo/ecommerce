from django.db import models

from apps.accounts.models import User
from apps.common.models import IsDeletedModel
from apps.shop.models import Product


# Create your models here.


class Review(IsDeletedModel):

    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    text = models.TextField()
