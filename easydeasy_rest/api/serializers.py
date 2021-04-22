from .models import Category, Feed, Site, Disease, Article, Model
from rest_framework.serializers import ModelSerializer, CharField
from easydeasy_rest import settings
import os
import random


class DiseaseSerializer(ModelSerializer):
    category = CharField()

    class Meta:
        model = Disease
        fields = '__all__'

    def create(self, validated_data):
        category_value = validated_data['category']

        kwargs = {'pk': int(category_value)} if category_value.isnumeric() else {'name': category_value}

        validated_data['category'] = Category.objects.get(**kwargs)

        return super().create(validated_data)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FeedSerializer(ModelSerializer):
    source_site = CharField()

    class Meta:
        model = Feed
        fields = '__all__'

    def create(self, validated_data):
        source_site_value = validated_data['source_site']

        kwargs = {'pk': int(source_site_value)} if source_site_value.isnumeric() else {'name': source_site_value}

        validated_data['source_site'] = Site.objects.get(**kwargs)

        return super().create(validated_data)


class SiteSerializer(ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class ArticleSerializer(ModelSerializer):

    def create(self, validated_data):

        # Updates the to generic image if possible
        if validated_data['img'] is None:
            # Gets First Disease in list
            disease: Disease = validated_data['diseases'][0]

            image_folder = f'/images/{disease.category.name}/'
            folder_path = f'{settings.MEDIA_ROOT}{image_folder}'

            # Selects random image
            random_image = random.choice(os.listdir(folder_path))

            validated_data['img'] = f'{image_folder}{random_image}'

        return super(ArticleSerializer, self).create(validated_data)

    class Meta:
        model = Article
        fields = '__all__'
