from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,UserProfile,Category,Recipe,MealPlan,RatingComment

class CustomUserAdmin(UserAdmin):
    list_display = ('username','email', 'first_name', 'last_name')
admin.site.register(CustomUser, CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
admin.site.register(UserProfile, UserProfileAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','tagline')
admin.site.register(Category, CategoryAdmin)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'description', 'category', 'dietary_preference','difficulty_level', 'preparation_time', 'cooking_time', 'serving_options', 'ingredients', 'cooking_instructions', 'image','average_rating', 'total_comments')
admin.site.register(Recipe, RecipeAdmin)

# class RatingAdmin(admin.ModelAdmin):
#     list_display = ('recipe','user','rating','created_at')
# admin.site.register(Rating, RatingAdmin)

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('recipe','user','comment','created_at')
# admin.site.register(Comment, CommentAdmin)

class RatingCommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'rating', 'comment', 'created_at')
admin.site.register(RatingComment, RatingCommentAdmin)

class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('user','recipe','category', 'added_at')
admin.site.register(MealPlan, MealPlanAdmin)
