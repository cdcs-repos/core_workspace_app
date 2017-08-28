"""
    Workspace views.
"""
import copy

from core_main_app.utils.rendering import render
from core_workspace_app import constants as workspace_constants
from core_workspace_app.components.workspace import api as workspace_api


def edit_rights(request, workspace_id):
    """ Load page to edit the rights.

    Args:   request
            workspace_id
    Returns:
    """

    try:
        workspace = workspace_api.get_by_id(workspace_id)
        # Users
        users_access_workspace = workspace_api.get_list_user_can_access_workspace(workspace, request.user)
        detailed_users = []
        for user in users_access_workspace:
            detailed_users.append({'user': user,
                                   'can_read': workspace_api.can_user_read_workspace(workspace, user),
                                   'can_write': workspace_api.can_user_write_workspace(workspace, user),
                                   'is_public': workspace_api.is_workspace_public(workspace)
                                   })
    except:
        detailed_users = []
        workspace = None

    # Groups
    detailed_groups = []

    context = {
        'workspace': workspace,
        'user_data': detailed_users,
        'group_data': detailed_groups,
        'template': workspace_constants.EDIT_RIGHTS_TEMPLATE_TABLE,
        'action_read': workspace_constants.ACTION_READ,
        'action_write': workspace_constants.ACTION_WRITE
    }

    assets = {
        "css": ['core_main_app/libs/datatables/1.10.13/css/jquery.dataTables.css'],

        "js": [{
                "path": 'core_main_app/libs/datatables/1.10.13/js/jquery.dataTables.js',
                "is_raw": True
                }]
    }

    assets['js'].extend(copy.deepcopy(workspace_constants.JS_TABLES))
    assets['js'].extend(copy.deepcopy(workspace_constants.JS_INIT))
    assets['js'].extend(copy.deepcopy(workspace_constants.JS_ADD_USER))
    assets['css'].extend(copy.deepcopy(workspace_constants.CSS_SWITCH))
    assets['js'].extend(copy.deepcopy(workspace_constants.JS_SWITCH_RIGHT))
    assets['js'].extend(copy.deepcopy(workspace_constants.JS_REMOVE_RIGHT))
    assets['css'].extend(copy.deepcopy(workspace_constants.CSS_FORM))

    modals = [workspace_constants.MODAL_ADD_USER,
              workspace_constants.MODAL_SWITCH_RIGHT,
              workspace_constants.MODAL_REMOVE_RIGHTS]

    return render(request, workspace_constants.EDIT_RIGHTS_TEMPLATE,
                  context=context,
                  assets=assets,
                  modals=modals)
