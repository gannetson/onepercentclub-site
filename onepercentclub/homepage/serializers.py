from banners.serializers import SlideSerializer
from campaigns.serializers import CampaignSerializer
from fundraisers.serializers import FundRaiserSerializer
from onepercent_projects.serializers import ProjectPreviewSerializer
from quotes.serializers import QuoteSerializer
from statistics.serializers import StatisticSerializer

from rest_framework import serializers


class HomePageSerializer(serializers.Serializer):
    quotes = QuoteSerializer(source='quotes')
    slides = SlideSerializer(source='slides')
    impact = StatisticSerializer(source='stats')
    projects = ProjectPreviewSerializer(source='projects')
    campaign = CampaignSerializer(source='campaign')
    fundraisers = FundRaiserSerializer(source='fundraisers')
