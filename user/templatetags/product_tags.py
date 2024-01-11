from django import template
import math
register = template.Library()

@register.simple_tag

def call_sellprice(price,Discount):
    if Discount is None or Discount is 0:
        return price
    sellprice = price
    sellprice = price -(price*Discount/100)
    return math.floor(sellprice)

@register.simple_tag

def progress_bar(total_quantity,Availablity):
    progress_bar =   Availablity
    progress_bar = Availablity *(100/total_quantity)
    return math.floor(progress_bar)