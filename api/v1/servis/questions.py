import random
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.quizz.models import Question, Processed_Answers, Attempts


class QuestionListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, requests, *args, **kwargs):
        count = requests.data['count']
        test_time = requests.data['test_time']

        if not count or not test_time:
            return Response({'error': 'Please provide count and test_time in the request data'}, status=status.HTTP_400_BAD_REQUEST)

        random_questions = Question.objects.order_by('?')[:count]

        """urinishlar"""
        total_step = sum(attempt.step for attempt in Attempts.objects.filter(user=requests.user))
        if total_step >= 5:
            return Response({"error": "you have run out of attempts"}, status=status.HTTP_400_BAD_REQUEST)

        if random_questions:
            questions_data = [{'test_id': None}]
            javob = {}
            for random_question in random_questions:

                answer_choices = list('ABCD')
                random.shuffle(answer_choices)

                question_data = {
                    'question_id': random_question.id,
                    'question_text': random_question.text,
                    'answer_choices': {
                        'A': random_question.__dict__['option_' + answer_choices[0]],
                        'B': random_question.__dict__['option_' + answer_choices[1]],
                        'C': random_question.__dict__['option_' + answer_choices[2]],
                        'D': random_question.__dict__['option_' + answer_choices[3]],
                    },
                }

                for i, k in question_data['answer_choices'].items():
                    if k == random_question.option_A:
                        javob[random_question.id] = i

                questions_data.append(question_data)

            processed_answer = Processed_Answers.objects.create(
                user=requests.user,
                answer_question=javob,
                count=count,
                end_time=timezone.now() + timezone.timedelta(minutes=test_time)
            )

            questions_data[0]['test_id'] = processed_answer.id

            return Response(questions_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No questions available'}, status=status.HTTP_404_NOT_FOUND)






# num = [{'test_id': 10}]
# num.extend(questions_data)

# class QuestionListAPI(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, requests, *args, **kwargs):
#         count = requests.data['count']
#         test_time = requests.data['test_time']
#
#         random_questions = Question.objects.order_by('?')[:count]
#
#         if random_questions:
#
#             root = Processed(user=requests.user, end_time=timezone.now() + timezone.timedelta(minutes=test_time))
#             root.save()
#             Processed = Processed.objects.filter(user=requests.user).first()
#
#             questions_data = []
#             for random_question in random_questions:
#
#                 answer_choices = list('ABCD')
#                 random.shuffle(answer_choices)
#
#                 question_data = {
#                     'question_id': random_question.id,
#                     'question_text': random_question.text,
#                     'answer_choices': {
#                         'A': random_question.__dict__['option_' + answer_choices[0]],
#                         'B': random_question.__dict__['option_' + answer_choices[1]],
#                         'C': random_question.__dict__['option_' + answer_choices[2]],
#                         'D': random_question.__dict__['option_' + answer_choices[3]],
#                     },
#                     # 'correct_answer': random_question.correct_answer,
#                 }
#
#                 processed_answers = [
#                     Processed_Answers(processed_id=Processed.id, id_question=random_question.id, answer_question=i)
#                     for i, k in question_data['answer_choices'].items()
#                     if k == random_question.option_A
#                 ]
#
#                 Processed_Answers.objects.bulk_create(processed_answers)
#
#                 questions_data.append(question_data)
#
#             return Response(questions_data)
#         else:
#             return Response({'error': 'No questions available'})
#


# def post(self, requests, *args, **kwargs):
#     count = requests.data['count']
#     test_time = requests.data['test_time']
#
#     random_questions = Question.objects.order_by('?')[:count]
#
#     if random_questions:
#         questions_data = [{'test_id': None}]
#         javob = {}
#         for random_question in random_questions:
#
#             answer_choices = list('ABCD')
#             random.shuffle(answer_choices)
#
#             question_data = {
#                 'question_id': random_question.id,
#                 'question_text': random_question.text,
#                 'answer_choices': {
#                     'A': random_question.__dict__['option_' + answer_choices[0]],
#                     'B': random_question.__dict__['option_' + answer_choices[1]],
#                     'C': random_question.__dict__['option_' + answer_choices[2]],
#                     'D': random_question.__dict__['option_' + answer_choices[3]],
#                 },
#             }
#
#             for i, k in question_data['answer_choices'].items():
#                 if k == random_question.option_A:
#                     javob[random_question.id] = i
#
#             questions_data.append(question_data)
#
#         processed_answer = Processed_Answers.objects.create(
#             user=requests.user,
#             answer_question=javob,
#             end_time=timezone.now() + timezone.timedelta(minutes=test_time)
#         )
#
#         # Update the 'test_id' in questions_data
#         questions_data[0]['test_id'] = processed_answer.id
#
#         return Response(questions_data)
#     else:
#         return Response({'error': 'No questions available'})



    # def post(self, request, *args, **kwargs):
    #     count = request.data.get('count')
    #     test_time = request.data.get('test_time')
    #
    #     if not count or not test_time:
    #         return Response({'error': 'Please provide count and test_time in the request data'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     random_questions = Question.objects.order_by('?')[:count]
    #
    #     if not random_questions:
    #         return Response({'error': 'No questions available'}, status=status.HTTP_404_NOT_FOUND)
    #
    #     questions_data = []
    #     javob = {}
    #
    #     for random_question in random_questions:
    #         answer_choices = random.sample(['A', 'B', 'C', 'D'], 4)  # Use random.sample to shuffle choices
    #
    #         question_data = {
    #             'question_id': random_question.id,
    #             'question_text': random_question.text,
    #             'answer_choices': {
    #                 answer_choices[0]: getattr(random_question, f'option_{answer_choices[0]}'),
    #                 answer_choices[1]: getattr(random_question, f'option_{answer_choices[1]}'),
    #                 answer_choices[2]: getattr(random_question, f'option_{answer_choices[2]}'),
    #                 answer_choices[3]: getattr(random_question, f'option_{answer_choices[3]}'),
    #             },
    #         }
    #
    #         correct_choice = next(key for key, value in question_data['answer_choices'].items() if value == random_question.option_A)
    #         javob[random_question.id] = correct_choice
    #
    #         questions_data.append(question_data)
    #
    #     end_time = timezone.now() + timezone.timedelta(minutes=test_time)
    #     processed_answer = Processed_Answers.objects.create(
    #         user=request.user,
    #         answer_question=javob,
    #         end_time=end_time,
    #         count=count
    #     )
    #
    #     data = [{'test_id': processed_answer.id}]
    #     data.extend(questions_data)
    #
    #     return Response(data, status=status.HTTP_200_OK)