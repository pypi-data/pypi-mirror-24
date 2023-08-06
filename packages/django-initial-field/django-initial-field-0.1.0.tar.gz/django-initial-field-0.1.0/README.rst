=============================
Django initial form field
=============================

.. image:: https://badge.fury.io/py/django-initial-field.svg
    :target: https://badge.fury.io/py/django-initial-field

.. image:: https://travis-ci.org/PetrDlouhy/django-initial-field.svg?branch=master
    :target: https://travis-ci.org/PetrDlouhy/django-initial-field

.. image:: https://codecov.io/gh/PetrDlouhy/django-initial-field/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PetrDlouhy/django-initial-field

Sometimes it is needed to pass some default values to the objects created by ModelForm. This simple mixin enables that by creating HiddenInput fields and passing initial parameters to the created Model

Documentation
-------------

The full documentation is at https://django-initial-field.readthedocs.io.

Quickstart
----------

Install Django initial form field::

    pip install django-initial-field

Use InitialFieldMixin in your `ModelForm` and set `initial_field` parameter:

.. code-block:: python

    class MyForm(InitialFieldsMixin, forms.ModelForm):
        initial_fields = ('my_field')

Then set initial value in your FormView:

.. code-block:: python

	class MyView(FormView):
		 def get_initial(self):
			  return {'my_field': "some value"}


Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
