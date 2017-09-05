"""
    Workspace constants
"""

GROUP = "group"
USER = "user"

ACTION_READ = "action_read"
ACTION_WRITE = "action_write"

EDIT_RIGHTS_TEMPLATE_TABLE = "core_workspace_app/list/edit_rights_table.html"
EDIT_RIGHTS_TEMPLATE = "core_workspace_app/edit_rights.html"

JS_CREATE_WORKSPACE = [{
                            "path": 'core_workspace_app/user/js/create_workspace.js',
                            "is_raw": False
                       }]

MODAL_CREATE_WORKSPACE = [
                            "core_workspace_app/list/create_workspace.html"
                         ]

JS_ASSIGN_WORKSPACE = [{
                            "path": 'core_workspace_app/user/js/list/modals/assign_workspace.js',
                            "is_raw": False
                       }]

MODAL_ASSIGN_WORKSPACE = [
                            "core_workspace_app/list/modals/assign_workspace.html"
                         ]

MODAL_ASSIGN_WORKSPACE_FORM = [
                                 "core_workspace_app/list/modals/assign_workspace_form.html"
                              ]


JS_PUBLIC_WORKSPACE = [{
                            "path": 'core_workspace_app/user/js/list/modals/set_public.js',
                            "is_raw": False
                       }]

MODAL_PUBLIC_WORKSPACE_FORM = [
                                 "core_workspace_app/list/modals/set_public.html"
                              ]

JS_INIT = [{
                "path": 'core_workspace_app/user/js/init.js',
                "is_raw": False
           }]

JS_TABLES = [{
                "path": 'core_workspace_app/user/js/tables.js',
                "is_raw": True
             }]

MODAL_ADD_USER = "core_workspace_app/list/modals/add_user.html"

MODAL_ADD_USER_FORM = [
                         "core_workspace_app/list/modals/add_user_form.html"
                      ]

JS_ADD_USER = [{
                    "path": 'core_workspace_app/user/js/add_user.js',
                    "is_raw": False
               }]

CSS_SWITCH = ['core_workspace_app/user/css/switch.css']
CSS_FORM = ['core_workspace_app/user/css/right-form.css']

JS_SWITCH_RIGHT = [{
                    "path": 'core_workspace_app/user/js/list/modals/switch_right.js',
                    "is_raw": False
                    }]

JS_REMOVE_RIGHT = [{
                    "path": 'core_workspace_app/user/js/list/modals/remove_rights.js',
                    "is_raw": False
                    }]

MODAL_SWITCH_RIGHT = "core_workspace_app/list/modals/switch_right.html"
MODAL_REMOVE_RIGHTS = "core_workspace_app/list/modals/remove_rights.html"

MODAL_ADD_GROUP = "core_workspace_app/list/modals/add_group.html"

MODAL_ADD_GROUP_FORM = [
                         "core_workspace_app/list/modals/add_group_form.html"
                      ]

JS_ADD_GROUP = [{
                    "path": 'core_workspace_app/user/js/add_group.js',
                    "is_raw": False
               }]
