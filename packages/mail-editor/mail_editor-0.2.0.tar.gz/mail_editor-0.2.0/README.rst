MailEditor
==========

.. image:: https://travis-ci.org/maykinmedia/mail-editor.svg?branch=master
    :target: https://travis-ci.org/maykinmedia/mail-editor
.. image:: https://codecov.io/gh/maykinmedia/mail-editor/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/maykinmedia/mail-editor
.. image:: https://lintly.com/gh/maykinmedia/mail-editor/badge.svg
    :target: https://lintly.com/gh/maykinmedia/mail-editor/
    :alt: Lintly

Django e-mail templates!

Many projects have a well defined set of events that trigger an outgoing e-mail,
and the sensible thing is to template these out.

However, doing code updates and deployments for small template tweaks are a bit
cumbersome and annoying.

This project aims to solve that - define the types of templates in the code,
and edit the actual templates in the front-end. Templates are validated on
syntax *and* required/optional content.

This project also aims to solve the HTML email template problems that you can have when
supporting all email clients. For this we will inject the css as inline styles.
We do this using a node project calles inline-css. This was also used by
`foundation for email`_. Foundation for email is a good way to build your initial email
template on development mode. It will generate a separete html file and css file.

For e-mail sending and logging, we recommend using a solution such as `Django Yubin`_.

This is only tested on a postgres database.

Supported (read: Travis tested) are:

- python 2.7, 3.4, 3.5
- Django 1.8, 1.9, 1.10, 1.11
- PostgreSQL

Warning
-------

This project is currently in development and not stable.


Using the template
------------------

There are 2 templates that you can use.

The *_base.html*, this template can not be edited by the user. This will only be
rendered when the email is send.

The *_outer_table.html*, this template can be edited by the user and will be loaded
in the editor in the admin. This template will be saved in the database with the
modifications.

You can use the templates in some different ways. The shortest way is:

.. code:: python

    from mail_editor.helpers import find_template

    def email_stuff():
        template = find_template('activation')

        context = {
            'name': 'Test Person',
            'site_name': 'This site',
            'activation_link': 'https://github.com/maykinmedia/mail-editor',
        }

        template.send_mail(to='test@example.com', context=context)

Settings
--------

The following settings are mandatory:

.. code:: python

    # Email templates with available variables
    MAIL_EDITOR_TEMPLATES = {
        # Email template unique key.
        'activation': {
            # Template name in the Django admin (optional).
            'name': ugettext_noop('Activation Email'),
            # Describe what this template is about and when it is sent (optional).
            'description': ugettext_noop('This email is used when people need to activate their account.'),
            # The default subject (optional).
            'subject_default': 'Activate your account for {{ site_name }}',
            # The default body (optional).
            'body_default': """
                <h1>Hi {{ name }},</h1>

                <p>Welcome! You activated your account on {{ site_name }}.</p>

                <p>{{ activation_link }}</p>
            """,
            # The variables available in the subject (optional).
            'subject': [{
                'name': 'site_name',
                'description': ugettext_noop('This is the name of the site.'),
            }],
            # The variables available in the body (optional).
            'body': [{
                'name': 'name',
                'description': ugettext_noop('This is the name of the user'),
            }, {
                'name': 'site_name',
                'description': ugettext_noop('This is the name of the site.'),
            }, {
                'name': 'activation_link',
                'description': ugettext_noop('This is the link to activate their account.'),
            }]
        },
        ...
    }

    # The full base URL for any relative URLs in your template.
    MAIL_EDITOR_BASE_URL = 'https://example.com'

These settings are usefull to add:

.. code:: python

    # These settings are for inlining the css.
    MAIL_EDITOR_PACKAGE_JSON_DIR = '/path/to/the/package.json'
    MAIL_EDITOR_ADD_BIN_PATH = True or False
    MAIL_EDITOR_BIN_PATH = 'path/to/virtualenv/bin'

    # These settings make sure that CKEDITOR does not strip any html tags. like <center></center>
    CKEDITOR_CONFIGS = {
        'mail_editor': {
            'allowedContent': True,
            'contentsCss': ['/static/css/email.css'], # Enter the css file used to style the email.
            'height': 600,  # This is optional
            'entities': False, # This is added because CKEDITOR escapes the ' when you do an if statement
        }
    }


Installation
------------

Install with pip:

.. code:: shell

    pip install mail_editor


Add *'mail_editor'* to the installed apps:

.. code:: python

    # settings.py

    INSTALLED_APPS = [
        ...
        'mail_editor',
        ...
    ]

.. _Django Yubin: https://github.com/APSL/django-yubin
.. _Sergei Maertens: https://github.com/sergei-maertens
.. _langerak-gkv: https://github.com/sergei-maertens/langerak-gkv/blob/master/src/langerak_gkv/mailing/mail_template.py
.. _foundation for email: http://foundation.zurb.com/emails.html
.. role:: python(code)
    :language: python
