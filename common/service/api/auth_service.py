import hashlib

from common.models.User import User, db


def make_register(data):
    if not data:
        return False, "Missing required parameters"

    try:
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return False, "Email already exists"

        user = User(
            email=data['email'],
            password=data['password'],
            password_hash=generate_password_hash(data['password']),
            avatar=data['avatar'],
            role=0,
            status=1
        )

        db.session.add(user)
        db.session.commit()

        return True, user.to_dict()
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def generate_password_hash(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))

    return m.hexdigest()


def get_user_info(uid=None, email=None):
    user = None
    if uid:
        user = User.query.filter_by(id=uid).first()
        if not user:
            return False, "User not found"
    if email:
        user = User.query.filter_by(email=email).first()

    if not user:
        return False, "User not found"

    return True, user
