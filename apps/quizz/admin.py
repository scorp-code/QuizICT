from django.contrib import admin
from apps.quizz.models import Question, Processed_Answers, Attempts
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


class QuestionResource(resources.ModelResource):
    options = fields.Field(column_name='text', attribute='text')

    class Meta:
        model = Question


class QuestionAdmin(ImportExportModelAdmin):
    list_display = ['text', 'option_A', 'option_B', 'option_C', 'option_D']


class ProcessedAnswersAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer_question', 'user', 'user_answer', 'end_time']


class AttemptsAmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'processed_answers', 'score', 'step']


admin.site.register(Question, QuestionAdmin),
admin.site.register(Processed_Answers, ProcessedAnswersAdmin)
admin.site.register(Attempts, AttemptsAmin)
