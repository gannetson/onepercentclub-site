from onepercent_projects.models import OnePercentProject, ProjectPhases
from onepercent_projects.serializers import ProjectPreviewSerializer


def prepare_money_donated():
    projects = OnePercentProject.objects.filter(phase__in=[ProjectPhases.campaign, ProjectPhases.act,
                                                 ProjectPhases.results, ProjectPhases.realized]).all()

    for project in projects:
        try:
            project.projectcampaign.update_money_donated()
            project.update_popularity()
        except Exception:
            pass


def prepare_project_images():
    projects = OnePercentProject.objects.exclude(phase__in=[ProjectPhases.pitch, ProjectPhases.failed]).all()

    for project in projects:
        try:
            ProjectPreviewSerializer().to_native(project)
        except Exception:
            # Don't raise errors on corrupt or missing images
            pass

