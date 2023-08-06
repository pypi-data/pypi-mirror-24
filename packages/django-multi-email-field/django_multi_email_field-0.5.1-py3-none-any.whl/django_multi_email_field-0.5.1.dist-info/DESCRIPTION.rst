Field and widget to store a list of e-mail addresses in a `Django <https://www.djangoproject.com>`_ project.

It provides:

* A form field and a form widget to edit a list of e-mails in a Django form;
* A model field to store the captured list of e-mails;

==================
COMPATIBILITY
==================

* Python 2.7/3.3/3.4/3.5
* Django 1.8/1.9/1.10

==================
INSTALL
==================

For now:

::

    pip install django-multi-email-field

==================
USAGE
==================

* Add ``multi_email_field`` to your ``INSTALLED_APPS``:

::

    # settings.py
    INSTALLED_APPS = (
    ...
    'multi_email_field',
    )

* Use the provided form field and widget:

::

    # forms.py
    from django import forms
    from multi_email_field.forms import MultiEmailField

    class SendMessageForm(forms.Form):
        emails = MultiEmailField()

==================
IN YOUR MODELS
==================

If you want to store a list of e-mails, you can use this:

::

    from django.db import models
    from multi_email_field.fields import MultiEmailField

    class ContactModel(models.Model):
        emails = MultiEmailField()


==================
AUTHORS
==================

    * Florent Lebreton <florent.lebreton@makina-corpus.com>

|makinacom|_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com



=========
CHANGELOG
=========

0.5.1 (2017-08-11)
==================

** New **

- Czech translation (thanks @petrmifek)

** Bugfixes **

- Fix pypi release (thanks @costela)


0.5 (2016-10-28)
==================

- Django 1.10 compatibility (thanks @AGASS007)

** Drop support **

- Django < 1.8 is no longer supported


0.4 (2016-04-10)
==================

- Better Django (1.8/1.9) and Python (3.5) compatibility


0.3.1 (2014-12-18)
==================

** New **

- South is not required anymore


0.3 (2014-12-05)
==================

** New **

- Add support for Python 3 (thanks @Hanan-Natan)
- Add support for Django 1.7


0.2 (2014-04-08)
==================

** Bugfixes **

- Stupid blocking bad call


0.1 (2014-04-07)
==================

- Initial release


