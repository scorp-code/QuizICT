import random
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.quizz.models import Question, Processed_Answers


class QuestionListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, requests, *args, **kwargs):
        # if not "name" requests.data["name"] :
        #     return Response ({'error': 'not user'})

        random_questions = Question.objects.order_by('?')[:10]

        if random_questions:
            questions_data = []
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
                    # 'correct_answer': random_question.correct_answer,
                }

                processed_answers = [
                    Processed_Answers(user=requests.user, id_question=random_question.id, answer_question=i)
                    for i, k in question_data['answer_choices'].items()
                    if k == random_question.option_A
                ]
                Processed_Answers.objects.bulk_create(processed_answers)

                questions_data.append(question_data)

            return Response(questions_data)
        else:
            return Response({'error': 'No questions available'})


