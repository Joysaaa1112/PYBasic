from app import create_app
from common.models.UserResume import UserResume

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        user = UserResume.query.filter_by(id=1).first()
        print(user.to_dict())
