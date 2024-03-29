import django

version = "3.0.0"

if django.VERSION < (4, 2):
    default_app_config = "jazzmin.apps.JazzminConfig"
