from datetime import datetime

from common.models.User import User, db
from common.models.UserResume import UserResume
from common.utils.password import generate_random_string


def make_resume(uid='', template='', code=None, data=None):
    if not uid or not data:
        return False, "Missing required parameters"
    try:
        user = User.query.filter_by(id=uid).first()
        if code:
            resume = UserResume.query.filter_by(code=code, uid=uid).first()
            resume.template = template
            resume.configuration = data
            resume.update_time = datetime.utcnow()
        else:
            code = f"RES-{datetime.now().strftime('%Y%m%d')}-{generate_random_string(6)}"
            resume = UserResume(
                code=code,
                template=template,
                configuration=data,
                uid=user.id if user else 0,
            )
            db.session.add(resume)
        db.session.commit()
        return True, resume.to_dict()
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def get_resume_info(uid='', code=''):
    if not uid or not code:
        return False, "Missing required parameters"
    try:
        resume = UserResume.query.filter_by(code=code, uid=uid).first()
        if not resume:
            return False, "Resume notfound"
        return True, resume.to_dict()
    except Exception as e:
        return False, str(e)


def get_resume_list(uid=None, page=1, page_size=10):
    if not uid:
        return False, "Missing required parameters"

    try:
        query = UserResume.query.filter_by(uid=uid)
        total = query.count()
        resume_list = query.order_by(UserResume.create_time.desc()).paginate(page=int(page), per_page=int(page_size),
                                                                             error_out=False)
        return True, {
            'total': total,
            'page': page,
            'page_size': page_size,
            'resume_list': [resume.to_dict() for resume in resume_list.items]
        }
    except Exception as e:
        return False, str(e)
