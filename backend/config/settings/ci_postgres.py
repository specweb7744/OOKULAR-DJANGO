"""Run behavior checks against PostgreSQL; excluded from test-file discovery."""

from .test import *

DATABASES = {"default": env.db("TEST_DATABASE_URL")}
