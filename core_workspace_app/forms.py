"""
    Workspace Form
"""
from django import forms

from core_main_app.commons.exceptions import DoesNotExist
from core_workspace_app.components.workspace import api as workspace_api


class UserRightForm(forms.Form):
    """
    Form to select user to add rights.
    """
    users = forms.MultipleChoiceField(label='', required=True, widget=forms.SelectMultiple(attrs={'class': 'right-form'}))
    USERS_OPTIONS = []

    def __init__(self, users_with_no_access):
        self.USERS_OPTIONS = []

        # We sort by username, case sensitive
        sort_users = sorted(users_with_no_access, key=lambda s: s.username.lower())

        # We add them
        for user in sort_users:
            self.USERS_OPTIONS.append((user.id, user.username))

        super(UserRightForm, self).__init__()
        self.fields['users'].choices = []
        self.fields['users'].choices = self.USERS_OPTIONS


class WorkspaceForm(forms.Form):
    """
    Form to create the workspace.
    """
    workspace_name = forms.CharField( max_length=100)


class ChangeWorkspaceForm(forms.Form):
    """
    Form to select a workspace.
    """
    workspaces = forms.ChoiceField(label='', required=True, widget=forms.Select(attrs={"class": "form-control"}))
    WORKSPACES_OPTIONS = []

    def __init__(self, user, list_current_workspace=[]):
        self.WORKSPACES_OPTIONS = []
        self.WORKSPACES_OPTIONS.append(('', '-----------'))

        # We retrieve all workspaces with write access
        all_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)

        if len(all_workspaces) == 0:
            raise DoesNotExist("You don't have access to any workspaces with sufficient rights to assign a document.")

        # We sort by title, case insensitive
        sort_workspaces = sorted(all_workspaces, key=lambda s: s.title.lower())

        # We add them
        for workspace in sort_workspaces:
            if list_current_workspace == [] or\
                    (len(list_current_workspace) > 0 and workspace not in list_current_workspace):
                self.WORKSPACES_OPTIONS.append((workspace.id, workspace.title))

        super(ChangeWorkspaceForm, self).__init__()
        self.fields['workspaces'].choices = []
        self.fields['workspaces'].choices = self.WORKSPACES_OPTIONS
