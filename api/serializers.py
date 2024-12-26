from rest_framework import serializers

from contentmanagement.models import Option, Question, Solution, SolutionStep, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


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
    Tags = serializers.SerializerMethodField()
    Steps = serializers.SerializerMethodField()
    ImageUrl = serializers.URLField(source="image_url", allow_null=True)

    class Meta:
        model = Question
        fields = ["Question", "Tags", "Solution", "CorrectAnswer", "Options", "Steps", "ImageUrl"]

    def get_Solution(self, obj):
        if hasattr(obj, "solution"):
            return obj.solution.content
        return None

    def get_CorrectAnswer(self, obj):
        return obj.correct_answer.text if obj.correct_answer else None

    def get_Options(self, obj):
        return [option.text for option in obj.options.all()]

    def get_Steps(self, obj):
        if hasattr(obj, "solution"):
            return SolutionStepSerializer(obj.solution.steps.all(), many=True).data
        return []

    def get_Tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
