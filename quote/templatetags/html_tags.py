import os
import codecs
from vatRate.models import VatRate
from quote.models import Quote, QuotedItem
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# @register.filter(name="read_html_file", takes_context=True)
# def read_html_file(html_field, organisation, *args, **kwargs):
#     html_path = html_field.path
#     print(html_path)
#     org = organisation
#     print(org)
#     if os.path.exists(html_path):
#         html_string = codecs.open(html_path, "r").read()
#         mark_safe_html_string = mark_safe(html_string)

#         return mark_safe_html_string
#     return None


def convert_rate(obj_vat_rate_id):
    vat_rate = 0
    if obj_vat_rate_id == None:
        vat_rate = 0
    else:
        vatRate = VatRate.objects.get(pk=obj_vat_rate_id)
        vat_rate = vatRate.rate
    return vat_rate


@register.simple_tag(name="read_html_file", takes_context=True)
def read_html_file(context, html_field):
    html_path = html_field.path
    pk = context["pk"]
    quote = Quote.objects.get(pk=pk)
    quotedItems = QuotedItem.objects.filter(quote=quote.pk)
    table_row_html = """<tr>
							<td class="text-center">{{seq}}</td>
							<td>{{item.item.name}}</td>
							<td class="text-right">{{item.quantity}}</td>
                            <td class="text-right">£{{item.amount}}</td>
							<td class="text-right">{{item.discount}}%</td>
							<td class="text-right">{{item.vat_rate}}%</td>
                            <td class="text-right">£{{item.line_total}}</td>
						</tr>"""
    quoted_items = ""
    i = 1
    for item in quotedItems:
        var_replaced_html = convert_html_to_python(
            variables={
                "seq": str(i),
                "item.item.name": item.item.name,
                "item.quantity": str(item.quantity),
                "item.amount": str(item.amount),
                "item.discount": str(item.discount),
                "item.vat_rate": str(convert_rate(item.vat_rate_id)),
                "item.line_total": str(item.line_total),
            },
            code=table_row_html,
        )
        quoted_items = quoted_items + var_replaced_html
        i = i + 1

    if os.path.exists(html_path):
        html_string = codecs.open(html_path, "r").read()
        html_string_formatted = convert_html_to_python(
            variables={
                "quote.organisation.work_org_name": quote.organisation.work_org_name,
                "quote.stage": quote.stage.status,
                "quote.quote_id": quote.quote_id,
                "quote.end_date": quote.end_date.strftime("%d-%b-%Y"),
                "quote.organisation.work_address_line1": quote.organisation.work_address_line1,
                "quote.organisation.work_address_line2": quote.organisation.work_address_line2,
                "quote.organisation.work_address_line3": quote.organisation.work_address_line3,
                "quote.organisation.work_address_line4": quote.organisation.work_address_line4,
                "quote.organisation.work_address_postcode": quote.organisation.work_address_postcode,
                "quote.owner.phone_number": quote.owner.phone_number,
                "quote.owner.mobile_number": quote.owner.mobile_number,
                "quote.owner.email": quote.owner.email,
                "quote.title": quote.title,
                "quote.first_name": quote.first_name,
                "quote.last_name": quote.last_name,
                "quote.work_org_name": quote.work_org_name,
                "quote.billing_address1": quote.billing_address1,
                "quote.billing_address2": quote.billing_address2,
                "quote.billing_address3": quote.billing_address3,
                "quote.billing_address4": quote.billing_address4,
                "quote.billing_address_city": quote.billing_address_city,
                "quote.billing_address_state_county": quote.billing_address_state_county,
                "quote.billing_address_postcode": quote.billing_address_postcode,
                "quote.phone": "415-676-3600",
                "quote.email": quote.email,
                "quote.quoted_items": quoted_items,
                "quote.sub_total_amount": str(quote.sub_total_amount),
                "quote.discount": str(quote.discount),
                "quote.shipping_charges": str(quote.shipping_charges),
                "quote.shipping_vat.rate": str(convert_rate(quote.shipping_vat_id)),
                "quote.adjustment": str(quote.adjustment),
                "quote.total_amount": str(quote.total_amount),
                "quote.notes": quote.notes,
                "quote.terms_conditions": quote.terms_conditions,
            },
            code=html_string,
        )
        print(str(quote.sub_total_amount))
        return mark_safe(html_string_formatted)
    return None


def convert_html_to_python(variables={}, code=""):
    for variable in variables:
        code = code.replace("{{" + str(variable) + "}}", variables[variable])
    return code
