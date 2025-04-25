def success(code=0, message="Success", data={}):
    response = {
        "code": code,
        "msg": message,
        "data": data
    }

    return response


def error(code=1, message="Error", status_code=200, data=[]):
    response = {
        "code": code,
        "msg": message,
        "data": data
    }, status_code

    return response
