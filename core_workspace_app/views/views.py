"""
    Workspace views.
"""
import copy

from django.http import HttpResponseBadRequest, HttpResponseForbidden

from core_main_app.utils.rendering import render
from core_main_app.commons.exceptions import DoesNotExist
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
    except DoesNotExist as e:
        return HttpResponseBadRequest("The workspace does not exist.")
    except:
        return HttpResponseBadRequest("Something wrong happened.")

    if workspace.owner != str(request.user.id):
        return HttpResponseForbidden("Only the workspace owner can edit the rights.")

    try:
        # Users
        users_read_workspace = workspace_api.get_list_user_can_read_workspace(workspace, request.user)
        users_write_workspace = workspace_api.get_list_user_can_write_workspace(workspace, request.user)

        users_access_workspace = list(set(users_read_workspace + users_write_workspace))
        detailed_users = []
        for user in users_access_workspace:
            detailed_users.append({'object_id': user.id,
                                   'object_name': user.username,
                                   'can_read': user in users_read_workspace,
                                   'can_write': user in users_write_workspace,
                                   })
    except:
        detailed_users = []

    try:
        # Groups
        groups_read_workspace = workspace_api.get_list_group_can_read_workspace(workspace, request.user)
        groups_write_workspace = workspace_api.get_list_group_can_write_workspace(workspace, request.user)

        groups_access_workspace = list(set(groups_read_workspace + groups_write_workspace))
        detailed_groups = []
        for group in groups_access_workspace:
            detailed_groups.append({'object_id': group.id,
                                    'object_name': group.name,
                                    'can_read': group in groups_read_workspace,
                                    'can_write': group in groups_write_workspace,
                                    })
    except:
        detailed_groups = []

    context = {
        'workspace': workspace,
        'user_data': detailed_users,
        'group_data': detailed_groups,
        'template': workspace_constants.EDIT_RIGHTS_TEMPLATE_TABLE,
        'action_read': workspace_constants.ACTION_READ,
        'action_write': workspace_constants.ACTION_WRITE,
        'user': workspace_constants.USER,
        'group': workspace_constants.GROUP,
    }

    assets = {
        "css": ['core_main_app/libs/datatables/1.10.13/css/jquery.dataTables.css',
                "core_main_app/libs/fSelect/css/fSelect.css"],

        "js": [{
                "path": 'core_main_app/libs/datatables/1.10.13/js/jquery.dataTables.js',
                "is_raw": True
                },
                {
                "path": "core_main_app/libs/fSelect/js/fSelect.js",
                "is_raw": False
                }]
    }

    assets['js'].extend(copy.deepcopy(workspace_constants.JS_TABLES))
    assets['js'].extend(copy.deepcopy(workspace_constants.JS_ADD_USER))
    assets['css'].extend(copy.deepcopy(workspace_constants.CSS_SWITCH))
    assets['js'].extend(copy.deepcopy(workspace_constants.JS_SWITCH_RIGHT))
    assets['js'].extend(copy.deepcopy(workspace_constants.JS_REMOVE_RIGHT))
    assets['js'].extend(copy.deepcopy(workspace_constants.JS_ADD_GROUP))
    assets['js'].extend(copy.deepcopy(workspace_constants.JS_INIT))

    modals = [workspace_constants.MODAL_ADD_USER,
              workspace_constants.MODAL_SWITCH_RIGHT,
              workspace_constants.MODAL_REMOVE_RIGHTS,
              workspace_constants.MODAL_ADD_GROUP]

    return render(request, workspace_constants.EDIT_RIGHTS_TEMPLATE,
                  context=context,
                  assets=assets,
                  modals=modals)
