from django.contrib import admin
from apps.quizz.models import Question, Processed_Answers
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
    list_display = ['id_question', 'answer_question', 'user']


admin.site.register(Question, QuestionAdmin),
admin.site.register(Processed_Answers, ProcessedAnswersAdmin)
