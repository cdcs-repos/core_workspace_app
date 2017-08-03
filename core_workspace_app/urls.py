"""
    Url router for the workspace
"""
from django.conf.urls import url
from core_workspace_app.views import ajax as workspace_ajax

urlpatterns = [
    # Ajax
    url(r'^create-workspace', workspace_ajax.create_workspace, name='core_workspace_create_workspace'),
    url(r'^change-workspace', workspace_ajax.load_form_change_workspace, name='core_workspace_change_workspace'),
    url(r'^assign-workspace', workspace_ajax.assign_workspace, name='core_workspace_assign_workspace'),
    url(r'^public-workspace', workspace_ajax.set_public_workspace, name='core_workspace_public_workspace'),
]
