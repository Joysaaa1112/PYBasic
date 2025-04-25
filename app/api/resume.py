from flask import request, g

from common.service.api.resume_service import make_resume, get_resume_info, get_resume_list
from common.utils.output import success, error
from . import api_blueprint


@api_blueprint.route('/resume', methods=['POST', 'PUT', 'GET'])
def resume():
    """
    创建或修改简历
    """
    if not request.is_json and request.method not in ['GET']:
        return error(message='Invalid request')
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
    else:
        data = request.args
    if request.method == 'POST':
        status, result = make_resume(uid=data.get('uid'), template=data.get('template'),
                                     data=data.get('data'))
    elif request.method == 'PUT':
        status, result = make_resume(uid=data.get('uid'), code=data.get('code', None), template=data.get('template'),
                                     data=data.get('data'))
    elif request.method == 'GET':
        uid = data.get('uid', '')
        code = data.get('code', '')
        status, result = get_resume_info(uid=uid, code=code)
    else:
        status, result = False, 'Invalid request'
    if not status:
        return error(message=result)

    return success(message='successfully', data=result)


@api_blueprint.route('/resume/list', methods=['GET'])
def resume_list():
    """
    获取简历列表
    """
    if request.method == 'GET':
        page = request.args.get('page', 1)
        page_size = request.args.get('page_size', 10)

        status, result = get_resume_list(uid=g.uid, page=page, page_size=page_size)
        if not status:
            return error(message=result)

        return success(data=result)
