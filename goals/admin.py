from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'title', 'description', 'status', 'priority', 'due_date', "created", "updated")
    search_fields = ('user', 'category', 'title', 'description', 'status', 'priority', 'due_date')


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('goal', 'user', 'text', "created", "updated")
    search_fields = ('goal', 'user', 'text')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)

