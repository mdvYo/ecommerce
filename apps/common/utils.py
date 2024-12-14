import secrets

from apps.comments.models import Review
from apps.common.managers import IsDeletedQuerySet
from apps.common.models import BaseModel


def generate_unique_code(model: BaseModel, field: str) -> str:
    """
    Generate a unique code for a specified model and field.

    Args:
        model (BaseModel): The model class to check for uniqueness.
        field (str): The field name to check for uniqueness.

    Returns:
        str: A unique code.
    """
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    unique_code = "".join(secrets.choice(allowed_chars) for _ in range(12))
    code = unique_code
    similar_object_exists = model.objects.filter(**{field: code}).exists()
    if not similar_object_exists:
        return code
    return generate_unique_code(model, field)


def set_dict_attr(obj, data):
    for attr, value in data.items():
        setattr(obj, attr, value)   # Или obj.attr = value для каждого атрибута
    return obj


def get_average_rating(data: dict, product: IsDeletedQuerySet):
    ''' Adding information about average rating of the product to serializer.data '''

    reviews = Review.objects.filter(product=product)

    data['average_rating'] = sum(review.rating for review in reviews) / reviews.count()
