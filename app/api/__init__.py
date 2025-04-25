from flask import Blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

from .upload import *
from .resume import *
from .auth import *
from .user import *
