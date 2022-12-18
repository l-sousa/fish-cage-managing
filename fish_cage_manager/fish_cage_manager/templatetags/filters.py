from django import template

from backend.tables import months

register = template.Library()


@register.filter
def return_latest_num_fishes(queryset):
    return sorted(queryset,
                  key=lambda x: (x.year, months.index(x.month_name)),
                  reverse=True)[0].num_fishes


@register.filter
def return_latest_monthstat_id(queryset):
    return sorted(queryset,
                  key=lambda x: (x.year, months.index(x.month_name)),
                  reverse=True)[0].id


@register.filter
def divide_by_30(val):
    return round(val / 30, 4)
