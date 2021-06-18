from import_export import resources
from leads.models import Lead


class LeadResource(resources.ModelResource):

    class Meta:
        model = Lead
        # fields = ('id', 'organisation', 'team', 'assigned_to', 'status', 'industry', 'dateTimeModified')
        # exclude = ('created_by', )
        widgets = {
            'dateTimeModified': {'format': '%d.%m.%Y'},
        }

    # In order to turn complicated data model into a (generally simpler) processed data structure on export

    def dehydrate_organisation(self, lead):
        if lead.organisation:
            return '%s' % (lead.organisation.work_org_name)
        else:
            return ''

    def dehydrate_team(self, lead):
        if lead.team:
            return '%s' % (lead.team.name)
        else:
            return ''

    def dehydrate_assigned_to(self, lead):
        if lead.assigned_to:
            return '%s' % (lead.assigned_to.username)
        else:
            return ''

    def dehydrate_status(self, lead):
        if lead.status:
            return '%s' % (lead.status.status)
        else:
            return ''

    def dehydrate_industry(self, lead):
        if lead.industry:
            return '%s' % (lead.industry.title)
        else:
            return ''

    def dehydrate_emailOptin(self, lead):
        if lead.emailOptIn:
            return '%s' % ('TRUE')
        else:
            return '%s' % ('FALSE')

    def dehydrate_created_by(self, lead):
        if lead.created_by:
            return '%s' % (lead.assigned_to.username)
        else:
            return ''
