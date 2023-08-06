# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numconv
import numpy

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

def generate_code():
    """
    Generates a random seven character string using [0-9A-Za-z]
    for the pk/id field of the Code model.
    The pk/id capacity of 64**12 and uint64 of 10**19.266
    and collision resolution built in,
    though normally it should be reduntant and return in the first iteration.
    """
    max_uint64 = numpy.iinfo(numpy.uint64).max
    while True:  # equivelent to do-while
        candidate_key = numconv.int2str(
            int(numpy.random.randint(0, max_uint64, dtype=numpy.uint64)),
            radix=64,
            alphabet=numconv.BASE64URL
        )
        if not Code.objects.filter(pk=candidate_key):
            return candidate_key

@python_2_unicode_compatible
class Code(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_code,
        max_length=12, verbose_name=_('id'),
    )
    class Meta:
        verbose_name = _('code')
        verbose_name_plural = _('codes')
    def __str__(self, ):
        return self.id

def create_code():
    return Code.objects.create()

@python_2_unicode_compatible
class VeryShortTranslationString(models.Model):
    code = models.ForeignKey(
        'Code', on_delete=models.CASCADE,
        related_name='very_short_translation_strings', verbose_name=_('code'),
    )
    language = models.CharField(
        max_length=8, choices=settings.LANGUAGES, verbose_name=_('language'),
    )
    string = models.CharField(
        max_length=16, verbose_name=_('string'),
    )
    class Meta:
        unique_together = (
            ('code', 'language'),
        )
        verbose_name = _('very short translation string')
        verbose_name_plural = _('very short translation strings')
    def __str__(self, ):
        return self.string

@python_2_unicode_compatible
class ShortTranslationString(models.Model):
    code = models.ForeignKey(
        'Code', on_delete=models.CASCADE,
        related_name='short_translation_strings', verbose_name=_('code'),
    )
    language = models.CharField(
        max_length=8, choices=settings.LANGUAGES, verbose_name=_('language'),
    )
    string = models.CharField(
        max_length=16, verbose_name=_('string'),
    )
    class Meta:
        unique_together = (
            ('code', 'language'),
        )
        verbose_name = _('short translation string')
        verbose_name_plural = _('short translation strings')
    def __str__(self, ):
        return self.string

@python_2_unicode_compatible
class MediumTranslationString(models.Model):
    code = models.ForeignKey(
        'Code', on_delete=models.CASCADE,
        related_name='medium_translation_strings', verbose_name=_('code'),
    )
    language = models.CharField(
        max_length=8, choices=settings.LANGUAGES, verbose_name=_('language'),
    )
    string = models.CharField(
        max_length=64, verbose_name=_('string'),
    )
    class Meta:
        unique_together = (
            ('code', 'language'),
        )
        verbose_name = _('medium translation string')
        verbose_name_plural = _('medium translation strings')
    def __str__(self, ):
        return self.string

@python_2_unicode_compatible
class LongTranslationString(models.Model):
    code = models.ForeignKey(
        'Code', on_delete=models.CASCADE,
        related_name='long_translation_strings', verbose_name=_('code'),
    )
    language = models.CharField(
        max_length=8, choices=settings.LANGUAGES, verbose_name=_('language'),
    )
    string = models.CharField(
        max_length=256, verbose_name=_('string'),
    )
    class Meta:
        unique_together = (
            ('code', 'language'),
        )
        verbose_name = _('long translation string')
        verbose_name_plural = _('long translation strings')
    def __str__(self, ):
        return self.string

@python_2_unicode_compatible
class VeryLongTranslationString(models.Model):
    code = models.ForeignKey(
        'Code', on_delete=models.CASCADE,
        related_name='very_long_translation_strings', verbose_name=_('code'),
    )
    language = models.CharField(
        max_length=8, choices=settings.LANGUAGES, verbose_name=_('language'),
    )
    string = models.CharField(
        max_length=1024, verbose_name=_('string'),
    )
    class Meta:
        unique_together = (
            ('code', 'language'),
        )
        verbose_name = _('very long translation string')
        verbose_name_plural = _('very long translation strings')
    def __str__(self, ):
        return self.string

@python_2_unicode_compatible
class TextTranslationString(models.Model):
    code = models.ForeignKey(
        'Code', on_delete=models.CASCADE,
        related_name='text_translation_strings', verbose_name=_('code'),
    )
    language = models.CharField(
        max_length=8, choices=settings.LANGUAGES, verbose_name=_('language'),
    )
    string = models.TextField(verbose_name=_('string'),)
    class Meta:
        unique_together = (
            ('code', 'language'),
        )
        verbose_name = _('text translation string')
        verbose_name_plural = _('text translation strings')
    def __str__(self, ):
        return self.string

class TranslatableAbstractModel(models.Model):
    translations = {}
    code = models.OneToOneField(
        'translations.Code', primary_key=True, default=create_code,
        related_name='%(class)ss_code', verbose_name=_('code'),
    )
    class Meta:
        abstract = True
    def translate(self, field_name, language_code=settings.LANGUAGES[0][0]):
        if ( # default language
            language_code == settings.LANGUAGES[0][0]
        ) or ( # no translations exist for this field
            field_name not in self.translations
        ): # return the default value as would {{ object.field }}
            return getattr(self, field_name)
        # else look if there is a translation for it
        try:
            return self.translations[field_name].objects.get(
                code=self.code, language=language_code,
            ).string
        except ObjectDoesNotExist:
            return '' # if there isn't, return an empty string
