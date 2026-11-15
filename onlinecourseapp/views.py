
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Course, Choice, Submission


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = course.questions.all()

    for question in questions:
        selected_choice_id = request.POST.get(str(question.id))

        if selected_choice_id:
            choice = get_object_or_404(
                Choice,
                id=selected_choice_id,
                question=question
            )

            Submission.objects.update_or_create(
                question=question,
                user=request.user.username,
                defaults={'selected_choice': choice}
            )

    return redirect('show_exam_result', course_id=course.id)


@login_required
def show_exam_result(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = course.questions.all()

    submissions = Submission.objects.filter(
        question__course=course,
        user=request.user.username
    ).select_related('question', 'selected_choice')

    score = sum(
        s.question.grade
        for s in submissions
        if s.selected_choice.is_correct
    )

    total_marks = sum(q.grade for q in questions)

    return render(
        request,
        'onlinecourseapp/show_exam_result.html',
        {
            'course': course,
            'questions': questions,
            'submissions': submissions,
            'score': score,
            'total_marks': total_marks,
        }
    )
