from ..models import CorporateService
from torpedo.wrappers import ORMWrapper

async def uuid_tostring(payload):
    for object in payload:
        object['id'] = str(object['id'])
    return payload

async def date_to_str(payload):
    for object in payload:
        object['created_at'] = str(object['created_at'])
    return payload

class CorporateManager:

    @classmethod
    async def create_corporate(cls, payload):
        payload['created_at'] = str(datetime.date.today())
        _response = await ORMWrapper.create(CorporateService, payload)
        new_user = await _response.to_dict()
        new_user['created_at'] = str(new_user['created_at'])
        return new_user

    @classmethod
    async def get_all_cprporate(cls):
        _result = await ORMWrapper.raw_sql("SELECT * FROM corporates")
        _result = await uuid_tostring(_result)
        _result = await date_to_str(_result)
        return _result
