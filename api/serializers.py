from rest_framework import serializers

from smartnonsense.models import Option, Question, Solution, SolutionStep, Tag

"""
class SolutionStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionStep
        fields = [
            "id",
            "title",
            "result",
            "image_url",
            "created_at",
            "updated_at",
        ]


class SolutionSerializer(serializers.ModelSerializer):
    steps = SolutionStepSerializer(many=True, read_only=True)

    class Meta:
        model = Solution
        fields = [
            "id",
            "content",
            "image_url",
            "steps",
            "created_at",
            "updated_at",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    solution = SolutionSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    correct_answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id",
            "created_at",
            "updated_at",
            "author",
            "text",
            "image_url",
            "tags",
            "correct_answer",
            "solution",
        ]

    def get_correct_answer(self, obj):
        return obj.correct_answer.text if obj.correct_answer else None
"""


class SolutionStepSerializer(serializers.ModelSerializer):
    Title = serializers.CharField(source="title")
    Result = serializers.CharField(source="result")
    ImageUrl = serializers.URLField(source="image_url", allow_null=True)

    class Meta:
        model = SolutionStep
        fields = ["Title", "Result", "ImageUrl"]


class SolutionSerializer(serializers.ModelSerializer):
    Steps = SolutionStepSerializer(source="steps", many=True, read_only=True)
    Solution = serializers.CharField(source="content")
    ImageUrl = serializers.URLField(source="image_url", allow_null=True)

    class Meta:
        model = Solution
        fields = ["Solution", "ImageUrl", "Steps"]


class QuestionSerializer(serializers.ModelSerializer):
    Question = serializers.CharField(source="text")
    Solution = serializers.SerializerMethodField()
    CorrectAnswer = serializers.SerializerMethodField()
    Options = serializers.SerializerMethodField()
    Steps = serializers.SerializerMethodField()
    ImageUrl = serializers.URLField(source="image_url", allow_null=True)

    class Meta:
        model = Question
        fields = ["Question", "Solution", "CorrectAnswer", "Options", "Steps", "ImageUrl"]

    def get_Solution(self, obj):
        # Get the solution content if it exists
        if hasattr(obj, "solution"):
            return obj.solution.content
        return None

    def get_CorrectAnswer(self, obj):
        # Use the correct_answer property to fetch the correct option
        return obj.correct_answer.text if obj.correct_answer else None

    def get_Options(self, obj):
        # Return a list of option texts for the question
        return [option.text for option in obj.options.all()]

    def get_Steps(self, obj):
        # Get the steps from the solution if it exists
        if hasattr(obj, "solution"):
            return SolutionStepSerializer(obj.solution.steps.all(), many=True).data
        return []
