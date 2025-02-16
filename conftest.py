import pytest
from django.core.management import call_command

@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker):
    """Ensure the test database is created once and not deleted after each run."""

    with django_db_blocker.unblock():
        from django.db import connection

        test_db_name = "test_dev"
        connection.settings_dict["NAME"] = test_db_name

        # Ensure pgvector extension exists
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        # Apply migrations once
        call_command("migrate", verbosity=0)
