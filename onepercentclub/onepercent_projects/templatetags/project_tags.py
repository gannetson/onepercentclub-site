from django import template


register = template.Library()


@register.assignment_tag
def get_project(project_id):
    from onepercent_projects.models import OnePercentProject
    return OnePercentProject.objects.get(pk=int(project_id))
