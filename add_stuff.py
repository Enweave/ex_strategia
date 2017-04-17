# -*- coding: utf-8 -*-

import os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from main.models import Post, Comment
from mixer.backend.django import mixer


mixer.cycle(6).blend(Comment)
