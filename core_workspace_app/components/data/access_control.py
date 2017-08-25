""" Data workspace access control
"""
from core_main_app.components.data.access_control import _check_can_write_data
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_workspace_app.components.workspace import api as workspace_api


def can_write_data_workspace(func, data, workspace, user):
    """ Can user write data in workspace.

    Args:
        func:
        data:
        workspace:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(data, workspace, user)

    _check_can_write_data(data, user)
    _check_can_write_workspace(workspace, user)
    return func(data, workspace, user)


def _check_can_write_workspace(workspace, user):
    """ Check that user can write in the workspace.

    Args:
        workspace:
        user:

    Returns:

    """
    accessible_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)
    if workspace not in accessible_workspaces:
        raise AccessControlError("The user does not have the permission to write into this workspace.")
