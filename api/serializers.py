import re

from rest_framework import serializers

from contentmanagement.models import Question, Solution, SolutionStep, Tag


def convert_html_to_tmp(html_text):
    # Replace <b><i> with TMP equivalent
    html_text = re.sub(r"<b><i>(.*?)</i></b>", r"<b><i>\1</i></b>", html_text)

    # Replace <font color="#XXXXXX"> with TMP <color=#XXXXXX>
    html_text = re.sub(r'<font color="(#[0-9A-Fa-f]{6})">', r"<color=\1>", html_text)

    # Replace inline background styling with <mark=#XXXXXX>
    html_text = re.sub(
        r'style="background-color: rgb\((\d+), (\d+), (\d+)\);"',
        lambda match: f"<mark=#{int(match.group(1)):02X}{int(match.group(2)):02X}{int(match.group(3)):02X}>",
        html_text,
    )

    # Replace </font> with </color> and </mark> closing tags
    html_text = html_text.replace("</font>", "</color>").replace("</mark>", "</mark>")

    return html_text


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class SolutionStepSerializer(serializers.ModelSerializer):
    Title = serializers.SerializerMethodField()
    Result = serializers.SerializerMethodField()
    ImageUrl = serializers.URLField(source="image_url", allow_null=True)

    class Meta:
        model = SolutionStep
        fields = ["Title", "Result", "ImageUrl"]

    def get_Title(self, obj):
        return convert_html_to_tmp(obj.title)

    def get_Result(self, obj):
        return convert_html_to_tmp(obj.result)


class SolutionSerializer(serializers.ModelSerializer):
    Steps = SolutionStepSerializer(source="steps", many=True, read_only=True)
    Solution = serializers.CharField(source="content")
    ImageUrl = serializers.URLField(source="image_url", allow_null=True)

    class Meta:
        model = Solution
        fields = ["Solution", "ImageUrl", "Steps"]


class QuestionSerializer(serializers.ModelSerializer):
    Question = serializers.SerializerMethodField()
    Solution = serializers.SerializerMethodField()
    CorrectAnswer = serializers.SerializerMethodField()
    Options = serializers.SerializerMethodField()
    Tags = serializers.SerializerMethodField()
    Steps = serializers.SerializerMethodField()
    ImageUrl = serializers.URLField(source="image_url", allow_null=True)

    class Meta:
        model = Question
        fields = ["Question", "Tags", "Solution", "CorrectAnswer", "Options", "Steps", "ImageUrl"]

    def get_Question(self, obj):
        question_text = obj.text
        if question_text:
            return convert_html_to_tmp(question_text)
        return None

    def get_Solution(self, obj):
        if hasattr(obj, "solution"):
            solution = obj.solution.content
            if solution:
                return convert_html_to_tmp(solution)
        return None

    def get_CorrectAnswer(self, obj):
        return obj.correct_answer.text if obj.correct_answer else None

    def get_Options(self, obj):
        return [option.text for option in obj.options.all()]

    def get_Steps(self, obj):
        if hasattr(obj, "solution"):
            steps = SolutionStepSerializer(obj.solution.steps.all(), many=True).data
            return steps
        return []

    def get_Tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
