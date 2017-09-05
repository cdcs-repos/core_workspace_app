"""
    Url router for the workspace
"""
from django.conf.urls import url
from core_workspace_app.views import ajax as workspace_ajax, views as workspace_views

urlpatterns = [
    # Ajax
    url(r'^create-workspace', workspace_ajax.create_workspace, name='core_workspace_create_workspace'),
    url(r'^change-workspace', workspace_ajax.load_form_change_workspace, name='core_workspace_change_workspace'),
    url(r'^assign-workspace', workspace_ajax.assign_workspace, name='core_workspace_assign_workspace'),
    url(r'^public-workspace', workspace_ajax.set_public_workspace, name='core_workspace_public_workspace'),
    url(r'^edit-rights/(?P<workspace_id>\w+)$', workspace_views.edit_rights,
        name='core_workspace_edit_rights_workspace'),
    url(r'^add-user-form', workspace_ajax.load_add_user_form, name='core_workspace_edit_rights_users_form'),
    url(r'^add-user-right-to-workspace', workspace_ajax.add_user_right_to_workspace,
        name='core_workspace_add_user_right_to_workspace'),
    url(r'^switch-right', workspace_ajax.switch_right, name='core_workspace_switch_right'),
    url(r'^remove-rights', workspace_ajax.remove_user_or_group_rights, name='core_workspace_remove_rights'),
    url(r'^add-group-form', workspace_ajax.load_add_group_form, name='core_workspace_edit_rights_groups_form'),
    url(r'^add-group-right-to-workspace', workspace_ajax.add_group_right_to_workspace,
        name='core_workspace_add_group_right_to_workspace'),

]
