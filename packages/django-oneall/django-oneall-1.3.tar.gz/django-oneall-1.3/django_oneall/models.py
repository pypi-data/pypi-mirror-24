# -*- coding: utf-8 -*-
from logging import getLogger
from random import Random
from re import match, sub
from uuid import uuid4

from django.conf import settings as django_settings
from django.db import models
from django.db.transaction import atomic
from django.utils.timezone import now
from pyoneall.base import OADict

from .app import get_user_model, settings

log = getLogger(__name__)


class SocialUserCache(models.Model):
    """
    OneAll User Identity Model
    Caches raw JSON corresponding with user's social identity allow instant retrieval of user details.
    """
    user_token = models.UUIDField(primary_key=True)
    raw = models.TextField(default='{}')
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL, null=True)

    def __init__(self, *args, **kwargs):
        """
        Upon creation, creates attributes to correspond with the cached data in `raw`
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        self.__dict__.update(OADict(**eval(self.raw)))

    def refresh(self, raw=None):
        """
        Refresh identity cache from OneAll
        :param raw: JSON data as given by OneAll.
        """
        if not raw:
            from .auth import oneall

            raw = oneall.user(self.user.username).identities.identity[0]
        raw.pop('id', None)
        raw.pop('user', None)
        self.raw = str(raw)
        self.__dict__.update(OADict(**eval(self.raw)))
        self.save()

    def update_user_cache(self):
        """
        Update selected fields in the User model from social identity
        """
        user_model = get_user_model()
        user = self.user
        if 'emails' in self.__dict__ and self.emails:
            email = self.emails[0].value
            if not user:
                user = user_model.objects.filter(email=email).first() or user_model(email=email)
            else:
                user.email = email
        if not user:
            user = user_model()
        if hasattr(user, 'first_name') and 'name' in self.__dict__ and 'givenName' in self.name:
            user.first_name = self.name.givenName
        if hasattr(user, 'last_name') and 'name' in self.__dict__ and 'familyName' in self.name:
            user.last_name = self.name.familyName
        if not user.username:
            username = getattr(self, 'preferredUsername', None)
            username = username or sub(r'@.*$', '', str(self.emails[0].value))
            username = _find_unique_username(username)
            user.username = username
        user.save()
        self.user = user
        self.save()


class EmailLoginToken(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now=True)

    @classmethod
    @atomic
    def issue(cls, email):
        cls._expire()
        cls.objects.filter(email=email).delete()
        login = cls(email=email)
        login.save()
        return login

    @classmethod
    @atomic
    def consume(cls, token):
        cls._expire()
        login = cls.objects.get(token=token)
        login.delete()
        return login  # Despite being removed from the db, we're still going to use this object for a bit longer.

    def produce_user(self):
        user_model = get_user_model()
        user = user_model.objects.filter(email=self.email).first()
        if not user:
            preferred_username = sub(r'@.*$', '', str(self.email))
            user = user_model(email=self.email, username=_find_unique_username(preferred_username))
            user.save()
        return user

    @classmethod
    @atomic
    def _expire(cls):
        cls.objects.filter(created__lt=now() - settings.token_expiration).delete()


def _find_unique_username(current):
    """
    Checks whether given username is unique.
    If not unique or not given, tries to derive a new username that is.
    """
    user_model = get_user_model()
    max_length = settings.max_username_length

    def exists(n):
        return user_model.objects.filter(username=n).exists()

    def cat_maxlen(a, b, l):
        return a[:l - len(b) - 1] + b

    current = str(current)[:max_length]
    if current and not exists(current):
        return current
    prefix, suffix = match(r'^(.+?)(\d*)$', current or 'user').groups()
    suffix = int(suffix or 0) + 1
    current = cat_maxlen(prefix, str(suffix), max_length)
    while exists(current):
        suffix += 1
        current = cat_maxlen(prefix, str(suffix), max_length)
    return current


def get_pseudo_random_user(seed):
    """ Creates or finds a user with a pseudo-random username and no further information.
    :param seed: A hashable object used to find the user. Will not be stored. """
    user_model = get_user_model()
    max_length = settings.max_username_length

    alphabet = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'  # [chr(i+65)+chr(i+97) for i in range(26)]
    not_so_random = Random(seed)
    username = ''.join(map(lambda x: not_so_random.choice(alphabet), range(max_length)))
    try:
        return user_model.objects.get(username=username)
    except user_model.DoesNotExist:
        user = user_model(username=username)
        user.save()
        return user
