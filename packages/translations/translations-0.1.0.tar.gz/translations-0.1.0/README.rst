Translations
============

A django application to help create translations for database string columns.

Requirements
------------

* Python: 2.7, 3.6
* Django: 1.11, 2.0

Setup
-----

Install from **pip**:

.. code-block:: sh

    pip install django-db-translations

Configuration
-------------

Follow the instruction for activating i18n at https://docs.djangoproject.com/en/1.10/topics/i18n/

and after declaring your LANGUAGES in the settings.py, migrate.

Use in models.py
----------------
For any class you want one of its fields to have a translation, you need to:

1. Inherit from the TranslatableAbstractModel.

2. Overwrite the translations dictionary field of the model inheriting from TranslatableAbstractModel with a keys the name of fields you want to be translated and for their values use the class name from one of the TranslationModel classes (VerySmallTranslationString, SmallTranslationString, MediumTranslationString, LongTranslationString, VeryLongTranslationString or TextTranslationString).

.. code-block:: sh

    # for example
    class Company(TranslatableAbstractModel):
        translations = {
            'title': LongTranslationString,
            'description': TextTranslationString,
        }
        title = models.CharField(max_length=256)
        description = models.TextField()

Use in templates
----------------
To be able to get the translation of a model's field using the template language, call the translate filter and to it the field you want to get its value translated to the active language.

1. {% load i18n %}

2. {% load translate %}

3. {{ company_object|translate:'title' }}
