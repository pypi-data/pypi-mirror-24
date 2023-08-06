"""

"""
from flask import render_template
from pyedu.student import stud
from pyedu.models import Lesson, Task


@stud.route('/lessons/view', defaults={'lecture_id':None})
@stud.route('/lessons/view/<int:lecture_id>')
def lesson_view_all(lecture_id):
    if lecture_id is None:
        lessons = Lesson.query.all()
    else:
        lessons = Lesson.query.filter_by(lecture_id=lecture_id).all()
    return render_template('student/lessons.html', lessons=lessons)


@stud.route('/lesson/view/<int:lesson_id>')
def lesson_view(lesson_id):
    # load the lesson and all tasks
    lesson = Lesson.query.get_or_404(lesson_id)
    tasks = Task.query.filter_by(lesson_id=lesson.id).order_by(Task.seq.asc()).all()

    return render_template('student/view_lesson.html', lesson=lesson, tasks=tasks)
