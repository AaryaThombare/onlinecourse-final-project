
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Course, Choice, Submission, Learner, Enrollment


@login_required
def take_exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = course.questions.prefetch_related('choices').all()

    return render(
        request,
        'onlinecourseapp/take_exam.html',
        {'course': course, 'questions': questions}
    )


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    learner, created = Learner.objects.get_or_create(
        user=request.user
    )

    enrollment, created = Enrollment.objects.get_or_create(
        learner=learner,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    for question in course.questions.all():
        selected_choice_id = request.POST.get(str(question.id))

        if selected_choice_id:
            choice = get_object_or_404(
                Choice,
                id=selected_choice_id,
                question=question
            )
            submission.choices.add(choice)

    return redirect(
        'show_exam_result_by_submission',
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, course_id, submission_id=None):
    course = get_object_or_404(Course, id=course_id)

    learner = get_object_or_404(
        Learner,
        user=request.user
    )

    enrollment = get_object_or_404(
        Enrollment,
        learner=learner,
        course=course
    )

    if submission_id is not None:
        submission = get_object_or_404(
            Submission,
            id=submission_id,
            enrollment=enrollment
        )
    else:
        submission = Submission.objects.filter(
            enrollment=enrollment
        ).order_by('-submitted_at', '-id').first()

    selected_ids = (
        list(submission.choices.values_list('id', flat=True))
        if submission else []
    )

    grade = 0

    for question in course.questions.all():
        if question.is_get_score(selected_ids):
            grade += question.grade

    return render(
        request,
        'onlinecourseapp/exam_result_bootstrap.html',
        {
            'course': course,
            'selected_ids': selected_ids,
            'grade': grade,
        }
    )
