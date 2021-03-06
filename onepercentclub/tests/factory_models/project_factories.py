from datetime import timedelta
from django.utils import timezone
from bluebottle.test.factory_models.projects import ProjectFactory
import factory

from apps.projects.models import Project



class OnePercentProjectFactory(ProjectFactory):

    FACTORY_FOR = Project
    deadline = timezone.now() + timedelta(days=30)
    amount_needed = 100
    amount_asked = 100
    allow_overfunding = True
