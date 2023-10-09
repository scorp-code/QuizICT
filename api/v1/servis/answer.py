from django.db.models import Max
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.quizz.models import Question, Answer, Processed_Answers , Attempts


class AnswerListAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, requests, *args, **kwargs):

        user_attempts = Attempts.objects.filter(user=requests.user)
        if user_attempts:
            max_score = user_attempts.aggregate(max_score=Max('score'))['max_score']
            max_score_attempt = user_attempts.filter(score=max_score).first()

            response_data = {
                'max_score_test_id': max_score_attempt.id if max_score_attempt else None,
                'max_score': max_score,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "siz hali test to'plamini ishlamagansiz"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, requests, *args, **kwargs):
        data = requests.data
        answers = Processed_Answers.objects.filter(id=data['test_id']).first()
        attemp = Attempts.objects.filter(processed_answers=data['test_id']).first()

        if attemp:
            return Response({'error': f"bu to'plam '{attemp.user}' tomonidan ishlangan"}, status=status.HTTP_400_BAD_REQUEST)

        if answers.is_test_expired():
            root = Attempts()
            root.user = requests.user
            root.processed_answers = answers
            root.step += 1
            root.save()

            return Response({'error': "bu test uchun ajratilgan vaqt tugadi"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not answers:
            return Response({"error": "no test suite found at this id"}, status=status.HTTP_400_BAD_REQUEST)

        if len(data['answers']) > answers.count:
            return Response({"error": "There are more answers than questions"}, status=status.HTTP_400_BAD_REQUEST)

        user_answer = {str(answer['question_id']): answer['user_answer'] for answer in data['answers']}
        answers.user_answer = user_answer
        answers.save()

        correct_answers = answers.answer_question
        total_score = sum(5 for i, k in user_answer.items() if i in correct_answers and k == correct_answers[i])

        root = Attempts()
        root.user = requests.user
        root.processed_answers = answers
        root.score = total_score
        root.step += 1
        root.save()

        return Response({"score": total_score}, status=status.HTTP_200_OK)








        # user_answer={}
        # data =requests.data
        # if len(data['javoblar']) > 10:
        #     return Response({"error": "yuborayotgan javoblar savollardan ko'p"})
        # answers = Processed_Answers.objects.filter(id=data['test_id']).first()
        # for i in range(len(data['javoblar'])):
        #     user_answer[str(data['javoblar'][i]['question_id'])]=data['javoblar'][i]['user_answer']
        # answers.user_answer = user_answer
        # answers.save()
        # total_score = 0
        # for i,k in user_answer.items():
        #     for j,l in answers.answer_question.items():
        #         # print(i.id_question, type(i.id_question))
        #         if i == j and k == l:
        #             print(i,'==',j, "and", k,'==',l )
        #             total_score += 5
        # return Response({"score": total_score})



        #
        #
        # user_answers = {(item['question_id'], item['user_answer']) for item in requests.data}
        # quiz_answers = {(item.id_question, item.answer_question) for item in
        #                 Processed_Answers.objects.filter(user_id=requests.user.id)}
        # common_answers = user_answers.intersection(quiz_answers)
        # total_score = sum(1 for _ in common_answers) * 5

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
