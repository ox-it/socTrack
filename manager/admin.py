from django.contrib import admin
from django.db.models import get_app, get_models

"""
Iterates through models in an app and adds them to Admin UI
"""

for model in get_models(get_app("manager")):
	admin.site.register(model)
