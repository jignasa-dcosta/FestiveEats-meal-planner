from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Make email unique
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Add profile picture field
    user_permissions=models.ManyToManyField('auth.Permission',related_name='account_user_permission_set',blank=True)
    groups = models.ManyToManyField('auth.Group',related_name='account_user_set',blank=True)

    USERNAME_FIELD = 'email' # Use email as the username field
    REQUIRED_FIELDS = ['username']  

    def __str__(self): 
        return self.email

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    favorite_recipes = models.ManyToManyField('Recipe', blank=True, related_name='liked_by')

    def __str__(self):
        return f"{self.user.first_name}{self.user.last_name}"



# Recipe Categories and Dietary Preferences
CATEGORY_CHOICES = [
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Party Snacks', 'Party Snacks'),
    ('Starters', 'Starters'),
    ('Sides', 'Sides'),
    ('Dessert', 'Dessert'),
    ('Beverages', 'Beverages'),
]

DIETARY_PREFERENCES = [
    ('Vegetarian', 'Vegetarian'),
    ('Non-Vegetarian', 'Non-Vegetarian'),
    ('Vegan', 'Vegan'),
    ('Gluten-Free', 'Gluten-Free'),
    ('Keto', 'Keto'),
]

DIFFICULTY_LEVELS = [
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
]

SERVING_OPTIONS = [
    ('1-2', '1-2'),
    ('3-4', '3-4'),
    ('5-6', '5-6'),
    ('7-8', '7-8'),
    ('more_than_8', 'More than 8'),
]


class Category(models.Model):
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    tagline = models.CharField(max_length=255, blank=True, null=True, default="Fun Tagline")

    def __str__(self):
        return self.name

class Recipe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        'Category',  # Reference the model name
        on_delete=models.CASCADE,  # Ensure cascading delete
       related_name='cat_recipes',  # Optional: Reverse lookup name
        null=True,  # Allow null if needed
        blank=True  # Allow empty value in forms
    )
    dietary_preference = models.CharField(max_length=50, choices=DIETARY_PREFERENCES)
    ingredients = models.TextField(help_text="Enter each ingredient on a new line.")
    cooking_instructions = models.TextField()
    serving_options = models.CharField(max_length=255, choices=SERVING_OPTIONS)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    additional_notes = models.TextField(blank=True, null=True)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='meal_plans')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='meal_plans')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s plan: {self.recipe.name}"