from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings

from django_countries import CountryField
from djchoices import DjangoChoices, ChoiceItem
from django_extensions.db.fields import (
    ModificationDateTimeField, CreationDateTimeField
)

from sorl.thumbnail import ImageField


class Project(models.Model):
    """ The base Project model """

    class ProjectPhases(DjangoChoices):
        idea = ChoiceItem('idea', label=_("Idea"))
        plan = ChoiceItem('plan', label=_("Plan"))
        act = ChoiceItem('act', label=_("Act"))
        results = ChoiceItem('results', label=_("Results"))

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)

    image = ImageField(max_length=255, blank=True,
        upload_to='project_images/',
        help_text=_('Main project picture'))

    organization = models.ForeignKey('organizations.Organization')
    owner = models.ForeignKey('auth.User')

    phase = models.CharField(max_length=20, choices=ProjectPhases.choices,
        help_text=_('Phase this project is in right now.')
    )

    created = CreationDateTimeField(
        help_text=_('When was this project created')
    )

    country = CountryField(null=True)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    """ Location of this project """

    project_language = models.CharField(max_length=6,
        choices=settings.LANGUAGES,
        help_text=_('Project main language')
    )

    def __unicode__(self):
        if self.title:
            return self.title
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        """ Get the URL for the current project.. """

        return ('project_detail', (), {
            'slug': self.slug
        })

    class Meta:
        ordering = ['title']


class AbstractPhase(models.Model):
    """ Abstract base class for project phases. """

    class PhaseStatuses(DjangoChoices):
        hidden = ChoiceItem('hidden', label=_("Hidden"))
        progress = ChoiceItem('progress', label=_("Progress"))
        completed = ChoiceItem('completed', label=_("Completed"))

    project = models.OneToOneField(Project)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    startdate = models.DateField(null=True)
    enddate = models.DateField(null=True)
    """ Date the phase has started/ended """

    status = models.CharField(max_length=20, choices=PhaseStatuses.choices)

    class Meta:
        abstract = True


class IdeaPhase(AbstractPhase):
    """ IdeaPhase: Got a nice idea here """

    pass


class PlanPhase(AbstractPhase):
    """ PlanPhase: fill out some forms for project plan """

    class PhaseStatuses(DjangoChoices):
        hidden = ChoiceItem('hidden', label=_("Hidden"))
        progress = ChoiceItem('progress', label=_("Progress"))
        feedback = ChoiceItem('feedback', label=_("Feedback"))
        waiting = ChoiceItem('waiting', label=_("Waiting"))
        completed = ChoiceItem('completed', label=_("Completed"))

    money_total = models.DecimalField(max_digits=9, decimal_places=2,
        help_text=_('Total amount needed for this project.')
    )
    money_asked = models.DecimalField(max_digits=9, decimal_places=2,
        help_text=_('Amount asked for from this website.')
    )

    what = models.TextField(
        blank=True,
        help_text=_("What do you want to do?")
    )
    goal = models.TextField(
        blank=True,
        help_text=_("What is your goal?")
    )
    who = models.TextField(
        blank=True,
        help_text=_("Who are you helping?")
    )
    how = models.TextField(
        blank=True,
        help_text=_("In which way?")
    )
    sustainability = models.TextField(
        blank=True,
        help_text=_("How can next generations profit from this?")
    )
    target = models.TextField(
        blank=True,
        help_text=_("What is your target?")
    )

    needed_expertise = models.TextField(blank=True)
    needed_volunteers = models.TextField(blank=True)

    budget_description = models.TextField(blank=True)
    money_other_sources = models.TextField(blank=True)



class ActPhase(AbstractPhase):
    """ ActPhase Funding complete lets DO it! """

    planning = models.TextField(blank=True)
    planned_start_date = models.DateField(null=True)
    planned_end_date = models.DateField(null=True)


class ResultsPhase(AbstractPhase):
    """ ResultsPhase: Tell about how things worked out """

    what = models.TextField(
        help_text=_("What and how?"),
        blank=True
    )
    tips = models.TextField(
        help_text=_("Tips and tricks?"),
        blank=True
    )
    change = models.TextField(
        help_text=_("What has changed for the target group?"),
        blank=True
    )
    financial = models.TextField(
        help_text=_("How was the money spend?"),
        blank=True
    )
    next = models.TextField(
        help_text=_("What's next?"),
        blank=True
    )
    """ Five questions that get asked after the project is done """


class BudgetCategory(models.Model):
    """ BudgetCategory: Categories for BudgetLines """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ordering = models.IntegerField(max_length=3)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['ordering']
        verbose_name_plural = 'Budget Categories'


class BudgetLine(models.Model):
    """
    BudgetLine: Entries to the Project Budget sheet.
    This is the budget for the amount asked from this
    website.
    """

    project = models.ForeignKey(Project)
    category = models.ForeignKey(BudgetCategory)
    description = models.TextField(blank=True)
    money_amount = models.DecimalField(max_digits=9, decimal_places=2)


class OtherSourcesLines(models.Model):
    """
    Other sources of money to fund this project.
    Every entry is an application (-to apply-)
    for a grant or other probable source of money.
    """

    class Statuses(DjangoChoices):
        progress = ChoiceItem('progress', label=_("Progress"))
        applied = ChoiceItem('applied', label=_("Applied"))
        granted = ChoiceItem('granted', label=_("Granted"))
        received = ChoiceItem('received', label=_("Received"))

    project = models.ForeignKey(Project)
    source = models.CharField(max_length=255)
    """ Who's giving the money """
    description = models.TextField(blank=True)
    money_amount = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=20, choices=Statuses.choices)


# Now some stuff connected to Projects
# Can we think of a better place to put this??

class Link(models.Model):
    """ Links (urls) connected to a Project """

    project = models.ForeignKey(Project)
    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)
    ordering = models.IntegerField()
    created = CreationDateTimeField()

    class Meta:
        ordering = ['ordering']


class Testimonial(models.Model):
    """ Any user can write something nice about a project """

    project = models.ForeignKey(Project)
    user = models.ForeignKey('auth.User')
    description = models.TextField()
    created = CreationDateTimeField()
    updated = ModificationDateTimeField()

    class Meta:
        ordering = ['-created']


class Message(models.Model):
    """ Message by a user on the Project wall """

    project = models.ForeignKey(Project)
    user = models.ForeignKey('auth.User')
    body = models.TextField()
    created = CreationDateTimeField()
    deleted = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'%s : %s...' % (
            self.created.date(), self.body[:20]
        )

    class Meta:
        ordering = ['-created']


class Category(models.Model):
    """ Categories for Projects """

    name = models.CharField(max_length=255)
    description = models.TextField()
    ordering = models.IntegerField()

    class Meta:
        ordering = ['ordering']




