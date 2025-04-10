def success(code=0, message="Success", data={}):
    response = {
        "code": code,
        "msg": message,
        "data": data
    }

    return response


def error(code=1, message="Error", status_code=200):
    response = {
        "code": code,
        "msg": message,
        "data": []
    }, status_code

    return response
