from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser,Recipe,MealPlan,Category

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Confirm your password'})
    )
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name','autofocus': 'autofocus'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class SigninForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        required=True,
        label='Email Address',
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        required=True,
        label='Password',
    )
    
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['user']
        fields = [
            'name', 'description', 'category', 'dietary_preference', 'difficulty_level',
            'ingredients', 'cooking_instructions', 'preparation_time', 'cooking_time', 'serving_options',
            'additional_notes', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a short introduction about your recipe'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'dietary_preference': forms.Select(attrs={'class': 'form-select'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-select'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'List ingredients, one per line'}),
            'cooking_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Step-by-step instructions'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 15'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 30'}),
            'serving_options': forms.Select(attrs={'class': 'form-select'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any extra tips or notes'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if commit:
            recipe.save()
        return recipe
    
class RecipeFilterForm(forms.Form):
    PREP_TIME_CHOICES = [
        ('under_15', 'Under 15 mins'),
        ('15_to_30', '15-30 mins'),
        ('30_to_60', '30-60 mins'),
        ('over_1_hour', 'Over 1 hour'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    DIETARY_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('non_veg', 'Non-Veg'),
        ('egg', 'Egg'),
    ]
    SERVING_SIZE_CHOICES = [
        ('1_to_2', '1-2'),
        ('3_to_4', '3-4'),
        ('5_to_6', '5-6'),
        ('7_to_8', '7-8'),
        ('more_than_8', 'More than 8'),
    ]

    prep_time = forms.ChoiceField(choices=PREP_TIME_CHOICES, widget=forms.RadioSelect, required=False)
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, widget=forms.RadioSelect, required=False)
    dietary_preference = forms.MultipleChoiceField(choices=DIETARY_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    serving_size = forms.ChoiceField(choices=SERVING_SIZE_CHOICES, widget=forms.RadioSelect, required=False)


class AddtoMealForm(forms.Form):
    meal_id = forms.ModelChoiceField(queryset=MealPlan.objects.all(), widget=forms.HiddenInput())
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.HiddenInput())



