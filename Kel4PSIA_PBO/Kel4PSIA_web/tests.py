from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
# Create your tests here.
ContentType.objects.clear_cache()