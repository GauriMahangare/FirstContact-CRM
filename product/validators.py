from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_image(value):
    return value


def validate_code(value):
    from product.models import Product

    # product = Product.objects.filter(code=value)
    # if product:
    #     raise ValidationError(_("This product code exists in the table."))

    return value


def validate_name(value):
    return value


def validate_sale_start_date(value):
    return value


def validate_sale_end_date(value):
    return value
