import os
import platform
from contextlib import contextmanager

import pika
import pytest

from dramatiq import Worker
from dramatiq.middleware.threading import is_gevent_active


@contextmanager
def worker(*args, **kwargs):
    try:
        worker = Worker(*args, **kwargs)
        worker.start()
        yield worker
    finally:
        worker.stop()


skip_in_ci = pytest.mark.skipif(
    os.getenv("APPVEYOR") is not None or
    os.getenv("GITHUB_ACTION") is not None,
    reason="test skipped in CI"
)

skip_on_windows = pytest.mark.skipif(platform.system() == "Windows", reason="test skipped on Windows")
skip_on_pypy = pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="Time limits are not supported under PyPy.")
skip_with_gevent = pytest.mark.skipif(is_gevent_active(), reason="Behaviour with gevent is different.")
skip_without_gevent = pytest.mark.skipif(not is_gevent_active(), reason="Behaviour without gevent is different.")

RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_CREDENTIALS = pika.credentials.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
