from time import mktime
import functools
import datetime
from torpedo import Request, send_response, BaseApiRequest
from .error import UnauthorisedError,  ValidationError, ObjectNotFoundError
import hashlib
import inspect
from constants import constants

service_name = None
_super_user_role = constants.UserRoles.ROLE_ADMIN
user_client = None

def authenticate(roles: list, super_user_role: str=None, is_pharma_panel=False):
    def decor(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            auth_token = args[0].headers.get('Authorization', None)
            if auth_token is None:
                raise UnauthorisedError('Invalid authorization')
            try:
                user = yield from user_client.authenticate(auth_token)
            except ObjectNotFoundError:
                raise UnauthorisedError('Invalid authorization token')

            if is_pharma_panel:
                pass
            else:
                if service_name not in user['roles']:
                    raise UnauthorisedError("Not valid role for app '{}'".format(service_name))

            _authenticated = False
            super_user = False
            if super_user_role and super_user_role in user['roles'][service_name]:
                _authenticated = True
                super_user = True
            else:
                if roles is None:
                    _authenticated = True
                else:
                    for user_role in user['roles'][service_name]:
                        if user_role in roles:
                            _authenticated = True

            if not _authenticated:
                raise UnauthorisedError('Invalid authorization')

            custom_request = Request(args[0], user, super_user)
            if inspect.isgeneratorfunction(func):
                return (yield from func(self, custom_request))
            else:
                return func(self, custom_request)

        return wrapper

    return decor

async def sha1(text: str) -> str:
    """
    generate SHA-1 hex
    :param str text:

    :return: SHA-A hex
    :rtype: str
    """
    hash_object = hashlib.sha1(text.encode())
    return hash_object.hexdigest()

@BaseApiRequest.get('/cloudinary/signature')
# @silence_coroutine(_exceptions, http_exception_handler)
@authenticate(None, _super_user_role)
async def cloudinary_data_form_data(self, custom_request: Request):
    time_stamp = int(mktime(datetime.datetime.now().timetuple()))
    if custom_request.request.GET:
        folder = custom_request.request.GET.get('folder', None)
        if folder and folder != '':
            signature = await sha1('folder={}&timestamp={}{}'.format(folder, time_stamp, config['CLOUDINARY_API_SECRET']))
        else:
            raise ValidationError('Invalid payload')
    else:
        signature = await sha1('timestamp={}{}'.format(time_stamp, config['CLOUDINARY_API_SECRET']))
    data = {
        'data_form_data': {
            'timestamp': time_stamp,
            'signature': signature,
            'api_key': config['CLOUDINARY_API_KEY'],
            's3_config': {
                'bucket': config['GUMLET']['S3_BUCKET'],
                'region': config['GUMLET']['S3_REGION'],
                'identity_pool': config['GUMLET']['IDENTITY_POOL']
            }
        },
        'cloud_name': config['CLOUDINARY_CLOUD_NAME'],
        'api_key': config['CLOUDINARY_API_KEY']
    }
    return send_response(data)
