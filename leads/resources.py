from django.conf import settings
from teams.models import Team
from organisation.models import Organisation
from import_export import fields, resources
from leads.models import Category, Industry, Lead
from import_export.widgets import ForeignKeyWidget
from allauth.account.models import EmailAddress
from firstcontact_crm.users.models import User


class LeadResource(resources.ModelResource):
    organisation = fields.Field(
        column_name="organisation",
        attribute="organisation",
        widget=ForeignKeyWidget(Organisation, "work_org_name"),
    )
    team = fields.Field(
        column_name="team", attribute="team", widget=ForeignKeyWidget(Team, "name")
    )
    assigned_to = fields.Field(
        column_name="assigned_to",
        attribute="assigned_to",
        widget=ForeignKeyWidget(User, "username"),
    )
    created_by = fields.Field(
        column_name="created_by",
        attribute="created_by",
        widget=ForeignKeyWidget(User, "username"),
    )
    industry = fields.Field(
        column_name="industry",
        attribute="industry",
        widget=ForeignKeyWidget(Industry, "title"),
    )
    status = fields.Field(
        column_name="status",
        attribute="status",
        widget=ForeignKeyWidget(Category, "status"),
    )

    class Meta:
        model = Lead
        # fields = ('id', 'organisation', 'team', 'assigned_to', 'status', 'industry', 'dateTimeModified')
        # exclude = ('created_by', )
        # import_id_fields = ("organisation", "team", "assigned_to", "industry", "status")
        skip_unchanged = True
        report_skipped = True
        widgets = {
            "dateTimeModified": {"format": "%d.%m.%Y"},
        }
