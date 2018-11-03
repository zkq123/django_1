
# Register your models here.
from django.contrib import admin
from .models import Question, Choice
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):

    search_fields = ['question_text']
    list_filter = ['pub_date']
    fieldsets = [
        (None,  {'fields':['question_text']}),
              ('日期部分', {'fields':['pub_date'], 'classes':['collapse']}),
              ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_per_page = 3

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)