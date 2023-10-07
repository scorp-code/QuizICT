from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.quizz.models import Question, Answer, Processed_Answers


class AnswerListAPI(generics.ListAPIView):

    def get(self, requests, *args, **kwargs):
        pass

    def post(self, requests, *args, **kwargs):

        user_answers = {(item['question_id'], item['user_answer']) for item in requests.data}
        quiz_answers = {(item.id_question, item.answer_question) for item in
                        Processed_Answers.objects.filter(user_id=3)}
        common_answers = user_answers.intersection(quiz_answers)
        total_score = sum(1 for _ in common_answers) * 5

        return Response({"score": total_score})
























# data = requests.data
        # quizz_answer = Processed_Answers.objects.filter(user_id="1")
        # total_score = 0
        # for j in data:
        #     for i in quizz_answer:
        #         print(i.id_question,type(i.id_question))
        #         if j['question_id'] == i.id_question and j['user_answer'] == i.answer_question:
        #             print(j['question_id'] ,"==",i.id_question)
        #             total_score += 5


# return Response({"score": total_score})




       # data = requests.data
        # user_answers = {(item['question_id'], item['user_answer']) for item in data}
        #
        # quiz_answers = {(item.id_question, item.answer_question) for item in
        #                 Processed_Answers.objects.filter(user_id="1")}
        #
        # common_answers = user_answers.intersection(quiz_answers)
        #
        # total_score = len(common_answers) * 5
        #
