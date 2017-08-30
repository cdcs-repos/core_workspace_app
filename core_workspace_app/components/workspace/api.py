"""
Workspace API
"""
from core_main_app.commons.exceptions import NotUniqueError
from core_main_app.components.group import api as group_api
from core_main_app.components.user import api as user_api
from core_main_app.utils.access_control.decorators import access_control
from core_workspace_app.components.workspace.access_control import can_delete_workspace, is_workspace_owner, \
    is_workspace_owner_to_perform_action_for_others
from core_workspace_app.components.workspace.models import Workspace
from core_workspace_app.permissions import api as permission_api


def create_and_save(owner_id, title):
    """ Create and save a workspace. It will also create permissions.

    Args:
        owner_id
        title

    Returns:
    """

    if Workspace.check_if_workspace_already_exists(title):
        raise NotUniqueError('A workspace with the same title already exists.')

    workspace = Workspace(title=title,
                          owner=str(owner_id),
                          read_perm_id=str(permission_api.create_read_perm(title).id),
                          write_perm_id=str(permission_api.create_write_perm(title).id))

    return workspace.save()


@access_control(can_delete_workspace)
def delete(workspace, user):
    """ Delete a workspace and its permissions.

    Args:
         workspace:

    Returns:
    """
    permission_api.delete_permission(workspace.read_perm_id)
    permission_api.delete_permission(workspace.write_perm_id)
    workspace.delete()


def set_title(workspace, new_title):
    """ Set the workspace's title.

    Args:
        workspace
        new_title

    Returns:
    """
    workspace.title = new_title
    workspace.save()


def get_all():
    """ Get all workspace.

    Returns:

    """
    return Workspace.get_all()


def get_all_by_owner(user):
    """ Get all workspaces created by the given user.

    Args:
        user

    Returns:

    """
    return Workspace.get_all_by_owner(str(user.id))


def get_by_id(workspace_id):
    """ Return the workspace with the given id.

    Args:
        workspace_id

    Returns:
        Workspace (obj): Workspace object with the given id

    """
    return Workspace.get_by_id(workspace_id)


def get_by_id_list(list_workspace_id):
    """ Return a list of workspaces with the given id list.

    Args:
        list_workspace_id

    Returns:
    """
    list_workspace = []
    for workspace_id in list_workspace_id:
        list_workspace.append(Workspace.get_by_id(workspace_id))
    return list_workspace


def get_all_workspaces_with_read_access_by_user(user):
    """ Get all workspaces with read access for the given user.

    Args:
        user

    Returns:

    """
    read_permissions = permission_api.get_all_workspace_permissions_user_can_read(str(user.id))
    return Workspace.get_all_workspaces_with_read_access_by_user_id(user.id, read_permissions)


def get_all_workspaces_with_write_access_by_user(user):
    """ Get all workspaces with write access for the given user.

    Args:
        user

    Returns:

    """
    write_permissions = permission_api.get_all_workspace_permissions_user_can_write(str(user.id))
    return Workspace.get_all_workspaces_with_write_access_by_user_id(user.id, write_permissions)


def get_all_workspaces_with_read_access_not_owned_by_user(user):
    """ Get the all workspaces with read access not owned by the given user.

    Args:
        user

    Returns:

    """
    read_permissions = permission_api.get_all_workspace_permissions_user_can_read(str(user.id))
    return Workspace.get_all_workspaces_with_read_access_not_owned_by_user_id(user.id, read_permissions)


def get_all_workspaces_with_write_access_not_owned_by_user_id(user):
    """ Get the all workspaces with write access not owned by the given user.

    Args:
        user

    Returns:

    """
    write_permissions = permission_api.get_all_workspace_permissions_user_can_write(str(user.id))
    return Workspace.get_all_workspaces_with_write_access_not_owned_by_user_id(user.id, write_permissions)


def get_all_other_public_workspaces(user):
    """ Get all other public workspaces.

    Args:
        user
    Returns:

    """
    public_permissions = permission_api.get_all_public_workspace_permission()
    return Workspace.get_all_other_public_workspaces(user.id, public_permissions)


def get_non_public_workspace_owned_by_user(user):
    """ Get the non public workspaces owned by the given user.

    Args:
        user:

    Returns:

    """
    public_permissions = permission_api.get_all_public_workspace_permission()
    return Workspace.get_non_public_workspace_owned_by_user_id(user.id, public_permissions)


def get_public_workspaces_owned_by_user(user):
    """ Get the public workspaces owned the given user.

    Args:
        user

    Returns:

    """
    public_permissions = permission_api.get_all_public_workspace_permission()
    return Workspace.get_public_workspaces_owned_by_user_id(user.id, public_permissions)


def is_workspace_public(workspace):
    """ Check if the workspace is public.

    Args:
        workspace

    Return:
    """
    return permission_api.is_workspace_public(workspace.read_perm_id)


def set_workspace_public(workspace):
    """ Set the workspace to public.

    Args:
        workspace

    Return:
    """
    permission_api.add_permission_to_group(group_api.get_anonymous_group().id, workspace.read_perm_id)
    permission_api.add_permission_to_group(group_api.get_default_group().id, workspace.read_perm_id)


def can_user_read_workspace(workspace, user):
    """ Check if user has read permission on workspace.

    Args:
        workspace
        user

    Return:
    """
    permission_label = permission_api.get_permission_label(workspace.read_perm_id)
    return str(workspace.owner) == str(user.id) or user.has_perm(permission_label)


def can_user_write_workspace(workspace, user):
    """ Check if user has write permission on workspace.

    Args:
        workspace
        user

    Return:
    """
    permission_label = permission_api.get_permission_label(workspace.write_perm_id)
    return str(workspace.owner) == str(user.id) or user.has_perm(permission_label)


@access_control(is_workspace_owner)
def get_list_user_can_access_workspace(workspace, user):
    """ Get the list of users that have either read or write access to workspace.

    Args:
        workspace
        user

    Returns:
    """

    # Get read permission of the workspace
    read_permission = permission_api.get_by_id(workspace.read_perm_id)

    # Get write permission of the workspace
    write_permission = permission_api.get_by_id(workspace.write_perm_id)

    # List all users that have the read permission of the workspace
    all_users_read = list(read_permission.user_set.all())

    # List all users that have the write permission of the workspace
    all_users_write = list(write_permission.user_set.all())

    # Return the union without doublons of the two lists.
    return list(set(all_users_read + all_users_write))


@access_control(is_workspace_owner)
def get_list_user_with_no_access_workspace(workspace, user):
    """ Get list of users that don't have any access to the workspace.

    Args:
         workspace
         user

    Returns:
    """
    return user_api.get_all_users_except_list(get_list_user_can_access_workspace(workspace, user))


@access_control(is_workspace_owner_to_perform_action_for_others)
def add_user_read_access_to_workspace(workspace, new_user, user):
    """ Add to new user the read access to workspace.

    Args:
          workspace
          new_user
          user
    Returns:
    """
    permission_api.add_permission_to_user(new_user, workspace.read_perm_id)


@access_control(is_workspace_owner_to_perform_action_for_others)
def add_user_write_access_to_workspace(workspace, new_user, user):
    """ Add to new user the write access to workspace.

    Args:
          workspace
          new_user
          user
    Returns:
    """
    permission_api.add_permission_to_user(new_user, workspace.write_perm_id)


@access_control(is_workspace_owner_to_perform_action_for_others)
def remove_user_read_access_to_workspace(workspace, new_user, user):
    """ Remove to new user the read access to workspace.

    Args:
          workspace
          new_user
          user
    Returns:
    """
    permission_api.remove_permission_to_user(new_user, workspace.read_perm_id)


@access_control(is_workspace_owner_to_perform_action_for_others)
def remove_user_write_access_to_workspace(workspace, new_user, user):
    """ Remove to new user the write access to workspace.

    Args:
          workspace
          new_user
          user
    Returns:
    """
    permission_api.remove_permission_to_user(new_user, workspace.write_perm_id)
