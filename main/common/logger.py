import logging
from functools import wraps

# Suppress urllib3 logging due to incorrect qwiki response headers parsing
# Todo this code have to be removed once issue is fixed
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

# set logger for info data which will show with params --logging-level=INFO --no-logcapture
log = logging.getLogger("api_logs")
log.setLevel(logging.INFO)

# set logger for debugging info which will show with params --logging-level=DEBUG --no-logcapture
log_develop = logging.getLogger("api_dev_logs")


def api_logger(func):
    @wraps(func)
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        log.info(f"REQUEST: {response.request.method}: {response.request.url} Status: {response.status_code}")
        if response.request.method in ["POST", "PUT", "PATCH"]:
            log_develop.debug(f"REQUEST_DATA: {response.request.body}")
        log_develop.debug(f'CONTENT: {response.content}')

        return response

    return inner
