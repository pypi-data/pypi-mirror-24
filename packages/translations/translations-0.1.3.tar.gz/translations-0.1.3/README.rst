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

    pip install translations

Configuration
-------------

Follow the instruction for activating i18n at https://docs.djangoproject.com/en/1.10/topics/i18n/

and after declaring your LANGUAGES in the settings.py, migrate.

Use in models.py
----------------

For any class you want one of its fields to have a translation, you need to:

1. Add 'translations' to your installed apps.

2. Import TranslatableAbstractModel and any of the String models you will use (VerySmallTranslationString (4 chars), SmallTranslationString (16 chars), MediumTranslationString (64 chars), LongTranslationString (128 chars), VeryLongTranslationString (1024 chars) or TextTranslationString).

3. Inherit from the TranslatableAbstractModel.

4. Overwrite the model's translations dictionary field of the model inheriting from TranslatableAbstractModel with a keys the name of fields you want to be translated and for their values use the class name from one of the TranslationModel classes.

.. code-block:: sh

    # for example
    from translations.models import (
        TranslatableAbstractModel,
        LongTranslationString, TextTranslationString,
    )

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

Use in templates
----------------

1. Translations for DRF ModelSerializer
