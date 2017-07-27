""" Data workspace api
"""
from core_main_app.utils.access_control.decorators import access_control
from core_workspace_app.components.data.access_control import can_write_data_workspace


@access_control(can_write_data_workspace)
def assign(data, workspace, user):
    """ Assign data to a workspace.

    Args:
        data:
        workspace:
        user:

    Returns:

    """
    data.workspace = workspace
    return data.save()
