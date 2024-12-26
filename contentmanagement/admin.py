from django import forms
from django.contrib import admin
from django.utils.html import strip_tags
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget

from .models import Option, Question, Solution, SolutionStep, Tag


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "text": SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1


class SolutionStepForm(forms.ModelForm):
    class Meta:
        model = SolutionStep
        fields = "__all__"
        widgets = {
            "result": SummernoteWidget(),
            "title": SummernoteWidget(),
        }


class SolutionStepsInline(admin.StackedInline):
    model = SolutionStep
    form = SolutionStepForm
    extra = 1


@admin.register(Solution)
class SolutionAdmin(SummernoteModelAdmin):
    inlines = [SolutionStepsInline]
    list_display = ("stripped_text", "question")
    search_fields = ("question__text",)
    summernote_fields = ("content",)

    def stripped_text(self, obj):
        stripped = strip_tags(obj.text)
        return stripped[:52] + "..." if len(stripped) > 55 else stripped

    stripped_text.short_description = "Solution Content"


@admin.register(Question)
class QuestionAdmin(SummernoteModelAdmin):
    form = QuestionAdminForm
    inlines = [OptionInline]
    list_display = (
        "stripped_text",
        "correct_answer",
        "display_tags",
        "image_url",
    )
    search_fields = ("text",)
    list_filter = (
        "tags",
        "options__text",
    )
    summernote_fields = ("text",)
    filter_horizontal = ("tags",)

    def stripped_text(self, obj):
        stripped = strip_tags(obj.text)
        return stripped[:52] + "..." if len(stripped) > 55 else stripped

    stripped_text.short_description = "Question Text"

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = "Tags"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_field = ("name",)
