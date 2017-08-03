""" Ajax API
"""
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader

from core_main_app.commons.exceptions import DoesNotExist, NotUniqueError
from core_main_app.components.data import api as data_api
from core_workspace_app.components.workspace import api as workspace_api
from core_workspace_app.forms import ChangeWorkspaceForm
from core_workspace_app import constants
from core_workspace_app.components.data import api as data_workspace_api


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
    workspace_id = request.POST['workspace_id']

    for data_id in document_ids:
        data_workspace_api.assign(data_api.get_by_id(data_id, request.user),
                                  workspace_api.get_by_id(str(workspace_id)),
                                  request.user)

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
    try:
        workspace_api.create_and_save(request.user.id, request.POST['name_workspace'])
    except NotUniqueError:
        return HttpResponseBadRequest("A workspace called "
                                      + request.POST['name_workspace'] +
                                      " already exists. Please change the name and try again.")
    except Exception:
        return HttpResponseBadRequest("A problem occurred while creating the workspace.")
    return HttpResponse(json.dumps({}), content_type='application/javascript')