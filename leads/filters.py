
from django import forms
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
import django_filters
from .models import Lead, Category
from django.contrib.auth import get_user_model

User = get_user_model()


def users_of_same_org(request):
    if request is None:
        print("request is empty")
        return User.objects.none()

    org = request.user.userorganization
    return User.objects.filter(userorganization=org)


class LeadFilter(django_filters.FilterSet):

    # team = CharFilter(method='my_custom_filter')
    assigned_to = django_filters.ModelMultipleChoiceFilter(
        queryset=users_of_same_org,
        widget=CheckboxSelectMultiple(attrs={'class': 'related-widget-wrapper', }),
        to_field_name="pk",
        label="Assigned to users",
        label_suffix="",

    )

    annual_revenue = django_filters.NumberFilter()
    annual_revenue__gt = django_filters.NumberFilter(field_name='annual_revenue', lookup_expr='gt')
    annual_revenue__lt = django_filters.NumberFilter(field_name='annual_revenue', lookup_expr='lt')

    nbr_of_employees = django_filters.NumberFilter()
    nbr_of_employees__gt = django_filters.NumberFilter(field_name='nbr_of_employees', lookup_expr='gt')
    nbr_of_employees__lt = django_filters.NumberFilter(field_name='nbr_of_employees', lookup_expr='lt')

    status = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple(attrs={'class': 'form-control', }),
        to_field_name="pk",
        label="Lead Status",
        label_suffix="",

    )

    dateTimeModified = django_filters.DateFromToRangeFilter(
        label='Worked/Reviewed in (Min and Max Modified Date range)',
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'dd/mm/yyyy',
                                                         'class': 'form-control-sm ',
                                                         'type': 'date'
                                                         })
    )

    dateTimeCreated = django_filters.DateFromToRangeFilter(
        label='Added on date (Min and Max Created Date range)',
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'dd/mm/yyyy',
                                                         'class': 'form-control-sm',
                                                         'type': 'date'
                                                         })
    )

    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending'),
    )

    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_ordering')

    class Meta:
        model = Lead
        # fields = {
        #     'team': ['icontains'],
        # }
        fields = [
            'team',
            'assigned_to',
            'source',
            'work_org_name',
            'work_Role',
            'industry',
            'annual_revenue__gt',
            'annual_revenue__lt',
            'nbr_of_employees__gt',
            'nbr_of_employees__lt',
            'preferred_contact_preference',
            'status',
            'lead_Ratings',
            'dateTimeModified',
            'dateTimeCreated',
        ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
            models.DateTimeField: {
                'filter_class': django_filters.DateFromToRangeFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput,
                },
            },

        }

    def filter_by_ordering(self, queryset, name, value):
        expression = 'dateTimeCreated' if value == 'ascending' else '-dateTimeCreated'
        return queryset.order_by(expression)

    # @property
    # def qs(self):
    #     parent = super().qs
    #     user = getattr(self.request, 'user', None)
    #     return parent.filter(organisation=user.userorganization)

    # def __init__(self, *args, **kwargs):
    #     super(LeadFilter, self).__init__(*args, **kwargs)
    #     instance = kwargs.get("instance")
    #     users_in_org = User.objects.none()
    #     if instance:
    #         users_in_org = User.objects.filter(userorganization_id=instance.organisation_id)
    #     self.fields['assigned_to'].queryset = users_in_org
