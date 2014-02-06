from django.contrib.contenttypes.models import ContentType


from rest_framework import serializers


from bluebottle.accounts.serializers import UserPreviewSerializer
from bluebottle.bluebottle_drf2.serializers import (SorlImageField, SlugGenericRelatedField, PolymorphicSerializer, EuroField,
                                              TagSerializer, ImageSerializer, TaggableSerializerMixin)
from bluebottle.geo.models import Country
from bluebottle.utils.serializers import MetaField


from fund.models import Donation
from onepercent_projects.models import ProjectPitch, ProjectPlan, ProjectCampaign, ProjectTheme
from wallposts.models import TextWallPost, MediaWallPost
from wallposts.serializers import TextWallPostSerializer, MediaWallPostSerializer

from .models import OnePercentProject


class ProjectCountrySerializer(serializers.ModelSerializer):

    subregion = serializers.CharField(source='subregion.name')

    class Meta:
        model = Country
        fields = ('id', 'name', 'subregion')


class ProjectPitchSerializer(serializers.ModelSerializer):

    project = serializers.SlugRelatedField(source='project', slug_field='slug', read_only=True)
    country = ProjectCountrySerializer()
    # This can be writable with the version of DRF that we're using.
    tags = TagSerializer()
    image = ImageSerializer(required=False)

    class Meta:
        model = ProjectPitch
        fields = ('id', 'project', 'title', 'pitch', 'theme', 'tags', 'description', 'country', 'latitude', 'longitude',
                  'need', 'status', 'image')


class ManageProjectPitchSerializer(TaggableSerializerMixin, ProjectPitchSerializer):

    country = serializers.PrimaryKeyRelatedField(required=False)
    status = serializers.ChoiceField(choices=ProjectPitch.PitchStatuses.choices, required=False)

    def validate_status(self, attrs, source):
        value = attrs.get(source, None)
        if value and value not in [ProjectPitch.PitchStatuses.submitted, ProjectPitch.PitchStatuses.new]:
            raise serializers.ValidationError("You can only change status into 'submitted'")
        return attrs


class ProjectPlanSerializer(TaggableSerializerMixin, serializers.ModelSerializer):

    project = serializers.SlugRelatedField(source='project', slug_field='slug', read_only=True)
    country = ProjectCountrySerializer()
    theme = serializers.PrimaryKeyRelatedField()
    tags = TagSerializer()
    organization = serializers.PrimaryKeyRelatedField(source="organization", required=False)
    image = ImageSerializer(required=False)

    class Meta:
        model = ProjectPlan
        fields = ('id', 'project', 'title', 'pitch', 'theme', 'tags', 'description', 'country', 'latitude', 'longitude',
                  'need', 'effects', 'future', 'for_who', 'reach', 'status', 'image', 'organization','money_needed', 'campaign')


class ManageProjectPlanSerializer(ProjectPlanSerializer):

    country = serializers.PrimaryKeyRelatedField(required=False)

    def validate_status(self, attrs, source):
        value = attrs[source]
        if value not in [ProjectPlan.PlanStatuses.submitted, ProjectPlan.PlanStatuses.new, ProjectPlan.PlanStatuses.needs_work]:
            raise serializers.ValidationError("You can only change status into 'submitted'")
        return attrs


class ProjectCampaignSerializer(serializers.ModelSerializer):

    project = serializers.SlugRelatedField(source='project', slug_field='slug', read_only=True)
    money_asked = EuroField()
    money_donated = EuroField()
    money_needed = EuroField()

    class Meta:
        model = ProjectCampaign
        fields = ('id', 'project', 'money_asked', 'money_donated', 'money_needed', 'deadline', 'status')


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug', read_only=True)

    owner = UserPreviewSerializer()
    coach = UserPreviewSerializer()

    plan = ProjectPlanSerializer(source='projectplan')
    campaign = ProjectCampaignSerializer(source='projectcampaign')

    task_count = serializers.IntegerField(source='task_count')

    meta_data = MetaField(
            title = 'get_meta_title',
            fb_title = 'get_fb_title',
            description = 'projectplan__pitch',
            keywords = 'projectplan__tags',
            image_source = 'projectplan__image',
            tweet = 'get_tweet',
            )

    def __init__(self, *args, **kwargs):
        super(ProjectSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = OnePercentProject
        fields = (
            'id', 'created', 'title', 'owner', 'coach', 'plan', 'campaign', 'phase', 'popularity',
            'task_count', 'meta_data', 'is_campaign',
        )


class ProjectPreviewSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug', read_only=True)
    image = SorlImageField('projectplan.image', '400x300', crop='center')
    country = ProjectCountrySerializer(source='projectplan.country')
    pitch = serializers.CharField(source='projectplan.pitch')

    #plan = ProjectPlanSerializer(source='projectplan')
    campaign = ProjectCampaignSerializer(source='projectcampaign')
    task_count = serializers.IntegerField(source='task_count')

    class Meta:
        model = OnePercentProject
        fields = ('id', 'title', 'image', 'phase', 'campaign', 'pitch', 'popularity', 'country', 'task_count',
                  'is_campaign')


class ProjectSupporterSerializer(serializers.ModelSerializer):
    """
    For displaying donations on project and member pages.
    """
    member = UserPreviewSerializer(source='user')
    project = ProjectPreviewSerializer(source='project') # NOTE: is this really necessary?
    date_donated = serializers.DateTimeField(source='ready')

    class Meta:
        model = Donation
        fields = ('date_donated', 'project',  'member',)


class ProjectDonationSerializer(serializers.ModelSerializer):
    member = UserPreviewSerializer(source='user')
    date_donated = serializers.DateTimeField(source='ready')
    amount = EuroField(source='amount')

    class Meta:
        model = Donation
        fields = ('member', 'date_donated', 'amount',)


class ManageProjectSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='slug', read_only=True)

    url = serializers.HyperlinkedIdentityField(view_name='project-manage-detail')
    phase = serializers.CharField(read_only=True)

    pitch = serializers.PrimaryKeyRelatedField(source='projectpitch', read_only=True)
    plan = serializers.PrimaryKeyRelatedField(source='projectplan', read_only=True)
    campaign = serializers.PrimaryKeyRelatedField(source='projectcampaign', read_only=True)
    result = serializers.PrimaryKeyRelatedField(source='projectresult', read_only=True)

    coach = serializers.PrimaryKeyRelatedField(source='coach', read_only=True)

    class Meta:
        model = OnePercentProject
        fields = ('id', 'created', 'title', 'url', 'phase', 'pitch', 'plan', 'campaign', 'coach')


# Serializers for ProjectWallPosts:

class ProjectTextWallPostSerializer(TextWallPostSerializer):
    """ TextWallPostSerializer with project specific customizations. """

    project = SlugGenericRelatedField(to_model=OnePercentProject)
    url = serializers.HyperlinkedIdentityField(view_name='project-textwallpost-detail')

    class Meta(TextWallPostSerializer.Meta):
        # Add the project slug field.
        fields = TextWallPostSerializer.Meta.fields + ('project',)

    def save(self, **kwargs):
        # Save the project content type on save.
        project_type = ContentType.objects.get_for_model(OnePercentProject)
        self.object.content_type_id = project_type.id
        return super(ProjectTextWallPostSerializer, self).save(**kwargs)


class ProjectMediaWallPostSerializer(MediaWallPostSerializer):
    """ MediaWallPostSerializer with project specific customizations. """

    project = SlugGenericRelatedField(to_model=OnePercentProject)
    url = serializers.HyperlinkedIdentityField(view_name='project-mediawallpost-detail')

    class Meta(MediaWallPostSerializer.Meta):
        # Add the project slug field.
        fields = MediaWallPostSerializer.Meta.fields + ('project',)

    def save(self, **kwargs):
        # Save the project content type on save.
        project_type = ContentType.objects.get_for_model(OnePercentProject)
        self.object.content_type_id = project_type.id
        return super(ProjectMediaWallPostSerializer, self).save(**kwargs)


class ProjectWallPostSerializer(PolymorphicSerializer):
    """ Polymorphic WallPostSerializer with project specific customizations. """

    class Meta:
        child_models = (
            (TextWallPost, ProjectTextWallPostSerializer),
            (MediaWallPost, ProjectMediaWallPostSerializer),
        )


class ProjectThemeSerializer(serializers.ModelSerializer):
    title = serializers.Field(source='name')

    class Meta:
        model = ProjectTheme
        fields = ('id', 'title')
