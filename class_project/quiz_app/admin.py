from django.contrib import admin
import nested_admin
from .models import *

class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 4

# Inline for Questions
class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 5

# Quiz Admin
@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
    readonly_fields = ('total_score',)
    #search_fields = ('title', 'category')

admin.site.register(UserProfile)
admin.site.register(Result)
