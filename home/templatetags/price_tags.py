# home/templatetags/price_tags.py
from django import template

register = template.Library()

@register.simple_tag
def discounted_price(price, discount):
    """
    Calculate discounted price given original price and discount percent.
    Returns clean integer (no .0 if unnecessary).
    """
    try:
        price = float(price)
        discount = float(discount)
        if discount > 0:
            final_price = price - (price * discount / 100)
            return int(final_price) if final_price.is_integer() else round(final_price, 2)
        else:
            # 👇 Even if 0% discount, return clean price
            return int(price) if price.is_integer() else round(price, 2)
    except (TypeError, ValueError):
        return price
