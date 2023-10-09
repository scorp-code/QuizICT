from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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
    answer_question = models.JSONField("tugri javob qaysi xarfdaligi", default={})
    user_answer = models.JSONField("user yuborgan javoblar", default={})
    text_question = models.CharField("tugri javob text", max_length=200)
    count = models.IntegerField(default=0)  # testlar soni
    start_time = models.DateTimeField(auto_now_add=True)  # Автоматическое добавление времени начала
    end_time = models.DateTimeField(null=True, blank=True)  # Время окончания теста (поле может быть пустым)

    # id_question = models.IntegerField()

    def is_test_expired(self):
        if self.end_time and timezone.now() > self.end_time:
            return True
        return False

    def str(self):
        return f" {self.user} {self.attempts} {self.end_time}"


class Attempts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    processed_answers = models.ForeignKey(Processed_Answers, on_delete=models.CASCADE, null=True)
    score = models.PositiveIntegerField(default=0)  # shu to'plamdan nechchi ball olgani
    step = models.PositiveIntegerField(default=0)  # Количество попыток по умолчанию 0


# class Processed_Answers(models.Model):
#     processed_id = models.ForeignKey(Processed, on_delete=models.CASCADE, null=True)
#     answer_question = models.CharField("tugri javob qaysi xarfdaligi", max_length=1)
#     id_question = models.IntegerField()
#     text_question = models.CharField("tugri javob text", max_length=200)
#
#
#
#     def __str__(self):
#         return f"{self.id_question},  {self.answer_question}"

# class Processed(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     attempts = models.IntegerField(default=0)  # Количество попыток по умолчанию 0
#     start_time = models.DateTimeField(auto_now_add=True)  # Автоматическое добавление времени начала
#     end_time = models.DateTimeField(null=True, blank=True)  # Время окончания теста (поле может быть пустым)
#
#     def is_test_expired(self):
#         if self.end_time and timezone.now() > self.end_time:
#             return True
#         return False
#
#     def __str__(self):
#         return f"{self.pk}, {self.user}"