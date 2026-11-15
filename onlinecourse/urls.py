
from django.contrib import admin
from django.urls import path
from onlinecourseapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'course/<int:course_id>/exam/',
        views.take_exam,
        name='take_exam'
    ),

    path(
        'course/<int:course_id>/submit/',
        views.submit,
        name='submit'
    ),

    path(
        'course/<int:course_id>/result/',
        views.show_exam_result,
        name='show_exam_result'
    ),

    path(
        'course/<int:course_id>/submission/<int:submission_id>/result/',
        views.show_exam_result,
        name='show_exam_result_by_submission'
    ),
]
