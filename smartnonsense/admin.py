from django import forms
from django.contrib import admin
from django.utils.html import strip_tags
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget

from .models import Option, Question, Solution, SolutionStep


# Custom form for Question to limit correct_answer options
class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "text": SummernoteWidget(),  # Add Summernote to the 'text' field
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        if self.instance and self.instance.pk:
            # Limit correct_answer choices to options related to this question
            self.fields["correct_answer"].queryset = Option.objects.filter(question=self.instance)
        """


# Inline admin for Options (allows adding/editing options directly within the Question admin page)
class OptionInline(admin.TabularInline):
    model = Option
    extra = 1  # Number of empty forms displayed to add new options


# Custom form for SolutionStep to use Summernote for `result` and `title` fields
class SolutionStepForm(forms.ModelForm):
    class Meta:
        model = SolutionStep
        fields = "__all__"
        widgets = {
            "result": SummernoteWidget(),  # Apply Summernote to the `result` field
            "title": SummernoteWidget(),  # Apply Summernote to the `title` field
        }


# Inline admin for SolutionSteps (to edit SolutionSteps directly on the Solution page)
class SolutionStepsInline(admin.StackedInline):
    model = SolutionStep
    form = SolutionStepForm  # Use the custom form with Summernote
    extra = 1  # Number of empty forms displayed to add new steps


# Admin for Solution with inline SolutionSteps
@admin.register(Solution)
class SolutionAdmin(SummernoteModelAdmin):
    inlines = [SolutionStepsInline]
    # list_display = ("content", "question")
    list_display = ("stripped_text",)
    search_fields = ("question__text",)  # Enables searching by question text
    # summernote_fields = ("steps",)  # Apply Summernote to the 'steps' field
    summernote_fields = ("content",)  # Apply Summernote to the 'text' field

    # Custom method to display stripped text
    def stripped_text(self, obj):
        return strip_tags(obj.content)

    stripped_text.short_description = "Solution Content"  # Column name in admin


# Admin for Question with inline Options and custom form
@admin.register(Question)
class QuestionAdmin(SummernoteModelAdmin):
    form = QuestionAdminForm
    inlines = [OptionInline]
    list_display = ("stripped_text", "correct_answer", "image_url")
    search_fields = ("text",)
    list_filter = ("options__text",)  # Optional: Add filters if necessary
    summernote_fields = ("text",)  # Apply Summernote to the 'text' field

    # Custom method to display stripped text
    def stripped_text(self, obj):
        return strip_tags(obj.text)

    stripped_text.short_description = "Question Text"  # Column name in admin


# Admin for Option (if needed for standalone management)
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("text", "question")
    search_fields = ("text", "question__text")  # Enables searching by option text and question text
    list_filter = ("question",)  # Filter options by related question


# Admin for SolutionSteps (if needed for standalone management)
"""
@admin.register(SolutionStep)
class SolutionStepsAdmin(SummernoteModelAdmin):
    list_display = ("title", "solution", "result", "image_url")
    search_fields = ("title", "solution__question__text")  # Enables searching by step title and question text
    summernote_fields = ("result", "title")  # Apply Summernote to the 'result' field
"""
