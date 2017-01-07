from rest_framework.response import Response

def enum(**enums):
    return type('Enum', (), enums)

global ERROR_CODE
ERROR_CODE = enum(FAILED=-1, AUTH_ERROR=-8, SERIALIZER_ERROR=-9)

def success_response(data):
    return Response({'status': '1', 'content': data})

def failure_response(errorCode, data):
    return Response({'status': str(errorCode), 'content':data})