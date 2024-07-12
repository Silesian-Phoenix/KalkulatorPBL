from flask import Blueprint

sheets_blueprint = Blueprint('sheets',
                            __name__,
                            template_folder='templates')

from . import routes
