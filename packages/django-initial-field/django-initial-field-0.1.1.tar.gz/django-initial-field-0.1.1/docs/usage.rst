=====
Usage
=====

To use Django initial form field in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'initial_field.apps.InitialFieldConfig',
        ...
    )

Add Django initial form field's URL patterns:

.. code-block:: python

    from initial_field import urls as initial_field_urls


    urlpatterns = [
        ...
        url(r'^', include(initial_field_urls)),
        ...
    ]
