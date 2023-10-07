from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    text = models.TextField()

    option_A = models.CharField(max_length=200)
    option_B = models.CharField(max_length=200)
    option_C = models.CharField(max_length=200)
    option_D = models.CharField(max_length=200)

    correct_answer = models.CharField('To\'g\'ri javob',
                                      max_length=1,
                                      choices=[
                                          ('A', 'A'),
                                          ('B', 'B'),
                                          ('C', 'C'),
                                          ('D', 'D'),
                                      ], default='A'
                                      )

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class Processed_Answers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answer_question = models.CharField("tugri javob qaysi xarfdaligi", max_length=1)
    id_question = models.IntegerField()
    text_question = models.CharField("tugri javob text", max_length=200)

    def __str__(self):
        return f"{self.id_question},  {self.answer_question}"
