from flask import (current_app, flash, redirect, render_template, request, url_for, jsonify, session)
from flask_login import current_user, login_required

from app import db
from app.models import User, Course, User_Course, Lessons
from . import sheets_blueprint


@sheets_blueprint.route('/sheet', methods=['GET', 'POST'])
@login_required
def sheet():
    return render_template('sheets.html')