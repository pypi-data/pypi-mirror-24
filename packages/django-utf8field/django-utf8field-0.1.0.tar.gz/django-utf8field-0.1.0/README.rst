==================
Django UTF-8 Field
==================

.. image:: https://travis-ci.org/megasnort/django-utf8field.svg
    :target: https://travis-ci.org/megasnort/django-utf8field/
    :alt: Build status

.. image:: https://coveralls.io/repos/github/megasnort/django-utf8field/badge.svg?branch=master
    :target: https://coveralls.io/github/megasnort/django-utf8field?branch=master
    :alt: Coverage

Sometimes you want to only allow the uploading of UTF-8 text files. This library extends the Django FileField by checking if the content of a file is UTF-8. If not, it generates an error.

Requirements
------------
Django >= 1.8


Installation
------------
::

    pip install django-utf8field


Usage
-----

Add the app to your settings:

::

    INSTALLED_APPS = (
        ...
        'utf8field',
        ...


Create a model like you would do normally, but instead of using FileField you use UTF8FileField:

::

    from django.db import models
    from utf8field.fields import UTF8FileField

    class YourModel(models.Model):
        title = models.CharField(max_length=255)
        created_on = models.DateTimeField(auto_add_on=True)
        text = models.UTF8FileField()





You also have the option to provide the option `max_content_length` to limit the number of characters in the file. If the content is longer an error will be displayed.

::

    text = models.UTF8FileField(max_content_length=1000)




