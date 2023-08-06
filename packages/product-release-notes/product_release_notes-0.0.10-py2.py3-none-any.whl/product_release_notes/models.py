from __future__ import absolute_import, unicode_literals

from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


class ClientIcons(object):
    """
    Maps to FontAwesome icons - http://fontawesome.io/icons/
    """

    DESKTOP = 'desktop'
    APPLE = 'apple'
    ANDROID = 'android'

    CHOICES = (
        (DESKTOP, 'Desktop',),
        (APPLE, 'Apple',),
        (ANDROID, 'Android',),
    )


@python_2_unicode_compatible
class Client(models.Model):
    """
    Android, iOS, Web
    """

    name = models.CharField(max_length=255)
    icon = models.CharField(
        max_length=20, choices=ClientIcons.CHOICES, default=ClientIcons.DESKTOP
    )

    # Used for new version detection
    itunes_url = models.CharField(
        max_length=1000, blank=True,
        help_text='Enter the url to iTunes to automatically pull in new release notes as drafts.'
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ReleaseNotesManager(models.Manager):

    def published(self):
        return self.filter(
            is_published=True
        ).select_related('client')


@python_2_unicode_compatible
class ReleaseNote(models.Model):
    client = models.ForeignKey(
        Client, related_name='release_notes',
        on_delete=models.CASCADE
    )

    notes = models.TextField()
    release_date = models.DateField(default=datetime.today)
    version = models.CharField(max_length=255, blank=True, db_index=True)

    is_published = models.BooleanField(
        default=False, help_text='Check this box when you\'re ready to publish')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = ReleaseNotesManager()

    def save(self, *args, **kwargs):
        self.notes = self.notes.strip()
        return super(ReleaseNote, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return '{}: {}'.format(self.client.name, self.version)


class ReleaseNoteEdit(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='releas',
        on_delete=models.CASCADE
    )

    notes = models.TextField()
    is_published = models.BooleanField(default=False)

    edited_at = models.DateTimeField(auto_now=True)
