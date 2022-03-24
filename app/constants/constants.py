from enum import Enum

X_SHARED_CONTEXT = "X-SHARED-CONTEXT"


class ListenerEventTypes(Enum):
    AFTER_SERVER_START = "after_server_start"
    BEFORE_SERVER_START = "before_server_start"
    BEFORE_SERVER_STOP = "before_server_stop"
    AFTER_SERVER_STOP = "after_server_stop"


class CorporateType(Enum):
    API = 'API'
    B2B2E = 'B2B2E'
    insurance = 'insurance'

class UserRoles(Enum):
    ROLE_ADMIN = 'ROLE_ADMIN'
    user = "user is defined"

