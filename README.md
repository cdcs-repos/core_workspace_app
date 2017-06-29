# core_workspace_app

core_workspace_app is a Django app providing a way to manage your resources through a dashboard.

## Quickstart

  1. Add "core_workspace_app" to your INSTALLED_APPS setting like this::

  ```python
  INSTALLED_APPS = [
      ...
      'core_workspace_app',
  ]
  ```

  2. Include the core_workspace_app URLconf in your project urls.py like this::

  ```python
  url(r'^workspace/', include('core_workspace_app.urls')),
  ```
