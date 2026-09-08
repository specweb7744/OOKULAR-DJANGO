from django.core.management import call_command
from django.db import migrations


def create_cache(apps, schema_editor):
    call_command(
        "createcachetable", "ookular_auth_cache",
        database=schema_editor.connection.alias, verbosity=0,
    )


def drop_cache(apps, schema_editor):
    schema_editor.execute("DROP TABLE ookular_auth_cache")


class Migration(migrations.Migration):
    dependencies = [("accounts", "0001_initial")]
    operations = [migrations.RunPython(create_cache, drop_cache)]
