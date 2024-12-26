from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from rest_framework import generics
from contentmanagement.models import Question

from .serializers import QuestionSerializer


@api_view(["GET"])
def question_list(request):
    try:
        questions = Question.objects.prefetch_related("options", "tags", "solution__steps").select_related("solution")
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
