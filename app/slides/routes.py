from flask import (current_app, flash, redirect, render_template, request, url_for, jsonify, session)
from flask_login import current_user, login_required

from app import db
from app.models import User, Course, User_Course, Lessons
from . import slides_blueprint


@slides_blueprint.route('/slide', methods=['GET', 'POST'])
@login_required
def slide():
    course_id = session['course_id']
    lesson_id = session['lesson_id']

    course_info = Course.query.filter_by(id=course_id).first()
    user_course_info = User_Course.query.filter_by(course_id=course_id, user_id=current_user.id).first()
    lesson_info = Lessons.query.filter_by(id=lesson_id).first()

    first_slide = lesson_info.first_slide
    user_slide_number = user_course_info.slideNumber

    if user_slide_number > lesson_info.last_slide:
        rendered_html = "<div style='font-size: 26px; margin-top: 20px; margin-bottom: 20px;'>" + render_template('end.html')+"</div>"
        return jsonify(result=rendered_html, percent=100)
    else:
        file_name = str(int(course_id) - 1) + '/' + str(user_slide_number) + '.html'
        rendered_html = "<div class='card' style='font-size: 26px; margin-top: 20px; margin-bottom: 20px;'><div class='card-body'>" + render_template(file_name)+"</div></div>"
        user_course_info.slideNumber += 1
        db.session.commit()

        # obliczanie percent
        ile_slides = lesson_info.last_slide - lesson_info.first_slide + 2
        ile_zrobione = min(user_course_info.slideNumber, lesson_info.last_slide + 1) - lesson_info.first_slide
        percent = ile_zrobione / ile_slides * 100
        print(percent)

        return jsonify(result=rendered_html, percent=percent)


@slides_blueprint.route('/all_slides', methods=['GET', 'POST'])
@login_required
def all_slides():
    course_id = session['course_id']
    lesson_id = session['lesson_id']

    course_info = Course.query.filter_by(id=course_id).first()
    user_course_info = User_Course.query.filter_by(course_id=course_id, user_id=current_user.id).first()
    lesson_info = Lessons.query.filter_by(id=lesson_id).first()

    actual_slide = user_course_info.slideNumber
    first_slide = lesson_info.first_slide
    last_slide = lesson_info.last_slide

    # obliczanie percent
    ile_slides = lesson_info.last_slide - lesson_info.first_slide + 1
    ile_zrobione = min(user_course_info.slideNumber, lesson_info.last_slide + 1) - lesson_info.first_slide
    percent = ile_zrobione / ile_slides * 100

    html_content = ""
    for i in range(first_slide, min(actual_slide, last_slide+1)):
        file_name = str(int(course_id) - 1) + '/' + str(i) + '.html'
        rendered_html = "<div class='card' style='font-size: 26px; margin-top: 20px; margin-bottom: 20px;'><div class='card-body'>" + render_template(file_name)+"</div></div>"
        html_content += rendered_html
    if int(actual_slide) >= int(lesson_info.last_slide) + 1:
        rendered_html = "<div style='font-size: 26px; margin-top: 20px; margin-bottom: 20px;'>" + render_template('end.html')+"</div>"
        html_content += rendered_html
    return jsonify(result=html_content, percent=percent)
