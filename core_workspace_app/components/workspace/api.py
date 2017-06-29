"""
Workspace API
"""

from core_main_app.components.group import api as group_api
from core_workspace_app.components.workspace.models import Workspace
from core_workspace_app.permissions import api as permission_api


def create_and_save(owner_id, title="Default workspace"):
    """ Create and save a workspace. It will also create permissions.

    Args:
        owner_id
        title

    Returns:
    """

    workspace = Workspace(title=title,
                          owner=str(owner_id),
                          read_perm_id=str(permission_api.create_read_perm(title).id),
                          write_perm_id=str(permission_api.create_write_perm(title).id))

    return workspace.save()


def delete(workspace):
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
