from sanic import Blueprint
from .corporate import corporate
from .basic import basic
from .basic_with_background_task import basic_with_background_task
from .basic_with_db_cache import basic_with_db_cache
from .basic_with_service_client import with_service_client

blueprint_group = Blueprint.group(
    basic, basic_with_db_cache, with_service_client, basic_with_background_task, corporate
)
