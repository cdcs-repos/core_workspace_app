""" Workspace models
"""
from django.db import models


class Workspace(models.Model):
    class Meta:
        verbose_name = 'core_workspace_app'
        default_permissions = ()
