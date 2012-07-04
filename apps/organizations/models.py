from django.db import models
from django_countries import CountryField
from django_extensions.db.fields import ModificationDateTimeField, CreationDateTimeField, AutoSlugField
from djchoices import DjangoChoices, ChoiceItem
from django.utils.translation import ugettext as _


class Organization(models.Model):
    """ 
        Organizations can run Projects. 
        Organization has one or more members 
    """

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    legal_status = models.TextField(null=True)
    """ The legal status of the organization (e.g. Foundation) """

    street = models.CharField(max_length=255, blank=True)
    street_number = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = CountryField(null=True)

    phone_number = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    website = models.CharField(max_length=255, blank=True)

    created = CreationDateTimeField()
    updated = ModificationDateTimeField()
    deleted = models.DateTimeField(null=True)

    partner_organisations = models.TextField(blank=True)

    account_bank_name = models.CharField(max_length=255, blank=True)
    account_bank_address = models.CharField(max_length=255, blank=True)
    account_bank_country = CountryField(blank=True)
    account_iban = models.CharField(max_length=255, blank=True)
    account_bicswift = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=255, blank=True)
    account_name = models.CharField(max_length=255, blank=True)
    account_city = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']


class OrganizationMember(models.Model):
    """ Members from a Organization """

    class MemberFunctions(DjangoChoices):
        owner = ChoiceItem('owner', label=_('owner'))
        admin = ChoiceItem('admin', label=_('admin'))
        editor = ChoiceItem('editor', label=_('editor'))
        member = ChoiceItem('member', label=_('member'))


    organization = models.ForeignKey(Organization)
    member = models.ForeignKey('auth.User')
    function = models.CharField(max_length=20, choices=MemberFunctions.choices)
    """ Function might determine Role later on """

