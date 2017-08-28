""" Ajax API
"""
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader

import core_workspace_app.constants as workspace_constants
from core_main_app.commons.exceptions import DoesNotExist, NotUniqueError
from core_main_app.components.data import api as data_api
from core_main_app.components.user import api as user_api
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_workspace_app import constants
from core_workspace_app.components.data import api as data_workspace_api
from core_workspace_app.components.workspace import api as workspace_api
from core_workspace_app.forms import ChangeWorkspaceForm, UserRightForm


def set_public_workspace(request):
    """ Set a workspace public.

    Args:
        request:

    Returns:
    """
    workspace_id_list = request.POST.getlist('workspace_id[]', [])
    try:
        list_workspace = workspace_api.get_by_id_list(workspace_id_list)
    except DoesNotExist, dne:
        return HttpResponseBadRequest(dne.message)
    try:
        for workspace in list_workspace:
            workspace_api.set_workspace_public(workspace)
    except:
        return HttpResponseBadRequest("Something wrong happened.")

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def assign_workspace(request):
    """ Assign the record to a workspace.

    Args:
        request:

    Returns:
    """
    document_ids = request.POST.getlist('document_id[]', [])
    workspace_id = request.POST.get('workspace_id', None)

    for data_id in document_ids:
        try:
            data_workspace_api.assign(data_api.get_by_id(data_id, request.user),
                                      workspace_api.get_by_id(str(workspace_id)),
                                      request.user)
        except Exception, exc:
            return HttpResponseBadRequest(exc.message)

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def load_form_change_workspace(request):
    """ Load the form to list the workspaces.

    Args:
        request:

    Returns:
    """
    document_ids = request.POST.getlist('document_id[]', [])
    list_workspace = set()
    try:
        list_data = data_api.get_by_id_list(document_ids, request.user)
        for data in list_data:
            if hasattr(data, 'workspace') and data.workspace is not None:
                list_workspace.add(data.workspace)
    except:
       pass

    try:
        form = ChangeWorkspaceForm(request.user, list(list_workspace))
    except DoesNotExist, dne:
        return HttpResponseBadRequest(dne.message)
    except:
        return HttpResponseBadRequest("Something wrong happened.")

    context = {
        "assign_workspace_form": form
    }

    return HttpResponse(json.dumps({'form': loader.render_to_string(constants.MODAL_ASSIGN_WORKSPACE_FORM, context)}),
                        'application/javascript')


def create_workspace(request):
    """ Create a workspace.

    Args:
        request

    Returns:
    """
    name_workspace = request.POST.get('name_workspace', None)
    try:
        workspace_api.create_and_save(request.user.id, name_workspace)
    except NotUniqueError:
        return HttpResponseBadRequest("A workspace called "
                                      + name_workspace +
                                      " already exists. Please change the name and try again.")
    except Exception:
        return HttpResponseBadRequest("A problem occurred while creating the workspace.")
    return HttpResponse(json.dumps({}), content_type='application/javascript')


def load_add_user_form(request):
    """ Load the form to list the users with no access to the workspace.

    Args:
        request:

    Returns:
    """
    workspace_id = request.POST.get('workspace_id', None)
    try:
        workspace = workspace_api.get_by_id(str(workspace_id))
    except Exception, exc:
        return HttpResponseBadRequest(exc.message)

    try:
        # We retrieve all users with no access
        users_with_no_access = list(workspace_api.get_list_user_with_no_access_workspace(workspace, request.user))

        # We remove the owner of the workspace
        users_with_no_access.remove(user_api.get_user_by_id(workspace.owner))

        if len(users_with_no_access) == 0:
            return HttpResponseBadRequest("There is no users that can be added.")

        form = UserRightForm(users_with_no_access)
    except AccessControlError, ace:
        return HttpResponseBadRequest(ace.message)
    except DoesNotExist, dne:
        return HttpResponseBadRequest(dne.message)
    except:
        return HttpResponseBadRequest("Something wrong happened.")

    context = {
        "add_user_form": form
    }

    return HttpResponse(json.dumps({'form': loader.render_to_string(constants.MODAL_ADD_USER_FORM, context)}),
                        'application/javascript')


def add_user_right_to_workspace(request):
    """ Add rights to user for the workspace.

    Args:
        request

    Returns
    """
    workspace_id = request.POST.get('workspace_id', None)
    users_ids = request.POST.getlist('users_id[]', [])
    is_read_checked = request.POST.get('read', None)
    is_write_checked = request.POST.get('write', None)

    if len(users_ids) == 0:
        return HttpResponseBadRequest("You need to select at least one user.")
    if is_read_checked == 'false' and is_write_checked == 'false':
        return HttpResponseBadRequest("You need to select at least one permission (read and/or write).")

    try:
        workspace = workspace_api.get_by_id(str(workspace_id))
        for user in user_api.get_all_users_by_list_id(users_ids):
            if is_read_checked == 'true':
                workspace_api.add_user_read_access_to_workspace(workspace, user, request.user)
            if is_write_checked == 'true':
                workspace_api.add_user_write_access_to_workspace(workspace, user, request.user)
    except AccessControlError, ace:
        return HttpResponseBadRequest(ace.message)
    except DoesNotExist, dne:
        return HttpResponseBadRequest(dne.message)
    except Exception, exc:
        return HttpResponseBadRequest('Something wrong happened.')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def switch_right(request):
    """ Switch user's right for the workspace.

    Args:
        request

    Returns
    """

    workspace_id = request.POST.get('workspace_id', None)
    user_id = request.POST.get('user_id', None)
    action = request.POST.get('action', None)
    value = request.POST.get('value', None)

    try:
        workspace = workspace_api.get_by_id(str(workspace_id))
        user = user_api.get_user_by_id(user_id)

        if action == workspace_constants.ACTION_READ:
            if value == 'true':
                workspace_api.add_user_read_access_to_workspace(workspace, user, request.user)
            else:
                workspace_api.remove_user_read_access_to_workspace(workspace, user, request.user)
        elif action == workspace_constants.ACTION_WRITE:
            if value == 'true':
                workspace_api.add_user_write_access_to_workspace(workspace, user, request.user)
            else:
                workspace_api.remove_user_write_access_to_workspace(workspace, user, request.user)

    except AccessControlError, ace:
        return HttpResponseBadRequest(ace.message)
    except DoesNotExist, dne:
        return HttpResponseBadRequest(dne.message)
    except Exception, exc:
        return HttpResponseBadRequest('Something wrong happened.')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def remove_user_rights(request):
    """ Remove user's right for the workspace.

    Args:
        request

    Returns
    """

    workspace_id = request.POST.get('workspace_id', None)
    user_id = request.POST.get('user_id', None)

    try:
        workspace = workspace_api.get_by_id(str(workspace_id))
        user = user_api.get_user_by_id(user_id)
        workspace_api.remove_user_read_access_to_workspace(workspace, user, request.user)
        workspace_api.remove_user_write_access_to_workspace(workspace, user, request.user)
    except AccessControlError, ace:
        return HttpResponseBadRequest(ace.message)
    except DoesNotExist, dne:
        return HttpResponseBadRequest(dne.message)
    except Exception, exc:
        return HttpResponseBadRequest('Something wrong happened.')

    return HttpResponse(json.dumps({}), content_type='application/javascript')