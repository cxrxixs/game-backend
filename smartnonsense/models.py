from django.contrib.auth.models import User
from django.db import models
from django.utils.html import strip_tags


class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True)
    color_hex = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        related_name="authored_questions",
        on_delete=models.CASCADE,
    )
    text = models.TextField()  # The question text
    image_url = models.URLField(blank=True, null=True)  # Optional image URL for the question
    tags = models.ManyToManyField(Tag, related_name="questions")  # Many-to-many relationship with Tag

    class Meta:
        ordering = ["created_at"]

    @property
    def correct_answer(self):
        return self.options.filter(is_correct=True).first()

    def __str__(self):
        return strip_tags(self.text)[:50]


class Option(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ("question", "text")  # Ensure options are unique for a specific question


class Solution(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.OneToOneField(Question, related_name="solution", on_delete=models.CASCADE)
    content = models.TextField()  # Solution content
    image_url = models.URLField(blank=True, null=True)  # Optional image URL for the solution

    def __str__(self):
        return f"Solution for: {strip_tags(self.question.text)[:50]}"


class SolutionStep(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    solution = models.ForeignKey(Solution, related_name="steps", on_delete=models.CASCADE)
    title = models.TextField()
    result = models.TextField()
    image_url = models.URLField(blank=True, null=True)  # Optional image URL for the step

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return strip_tags(self.title)[:50]
