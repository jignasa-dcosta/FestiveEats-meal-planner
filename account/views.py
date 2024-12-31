from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Category, Recipe, MealPlan, RatingComment
from .forms import CustomUserCreationForm,SigninForm,RecipeForm,RecipeFilterForm,AddtoMealForm,RatingCommentForm

# Create your views here.

def index(request):
    return render(request,"index.html")

def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('category')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = SigninForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('signin')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = user.email # Ensure username is set to email or another unique value
            user.save() 
            login(request, user)
            return redirect('signin')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def category(request):
    categories = Category.objects.all()
    return render(request,"category.html",{'categories': categories})

def recipe_list(request, category_id=None, category=None):
    query = request.GET.get('q')  # Get the search query from the URL parameter
    if category_id:
        # Handling "Add Category Ideas" button from Meal Plan page
        category = get_object_or_404(Category, id=category_id)
        recipes = Recipe.objects.filter(category=category)
        active_category = category.name
    elif category:
        # Handling filter buttons from Recipe List page
        category = get_object_or_404(Category, name__iexact=category)
        recipes = Recipe.objects.filter(category=category)
        active_category = category.name
    else:
        # Show all recipes
        recipes = Recipe.objects.all()
        active_category = 'all'
    
    # Handle search query
    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) | Q(ingredients__icontains=query)
        )

    categories = Category.objects.all()

     # Add user's meal plan recipe IDs to the context
    user_meal_plan_recipes = []
    if request.user.is_authenticated:
        user_meal_plan_recipes = MealPlan.objects.filter(user=request.user).values_list('recipe_id', flat=True)

    context = {
        'recipes': recipes,
        'categories': categories,
        'active_category': active_category,
        'search_query': query,
        'user_meal_plan_recipes': user_meal_plan_recipes,
    }
    return render(request, 'recipe_list.html', context)


def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    
    if request.method == 'POST':
        form = RatingCommentForm(request.POST)
        
        if form.is_valid():
            rating_comment, created = RatingComment.objects.get_or_create(
                recipe=recipe,
                user=request.user,
                defaults={'rating': form.cleaned_data['rating'], 'comment': form.cleaned_data['comment']}
            )
            if not created:
                rating_comment.rating = form.cleaned_data['rating']
                rating_comment.comment = form.cleaned_data['comment']
                rating_comment.save()
            
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RatingCommentForm()

    # Fetch existing ratings and comments
    rating_comments = RatingComment.objects.filter(recipe=recipe).select_related('user')

    context = {
        'recipe': recipe,
        'form': form,
        'rating_comments': rating_comments,
    }
    return render(request, "recipe_detail.html", context)

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('recipe_list')  # Redirect to the category page or any other page
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})


@login_required
def meal_plan(request):
    """
    Display the user's meal plan with recipes categorized.
    """
    categories = Category.objects.all()
    user_meal_plans = MealPlan.objects.filter(user=request.user).select_related('recipe', 'category')

    # Attach recipes directly to categories
    for category in categories:
        category.user_recipes = user_meal_plans.filter(category=category)

    context = {
        'categories': categories,
    }
    return render(request, 'meal_plan.html', context)

@login_required
def add_to_mealplan(request, recipe_id):
    """
    Add a recipe to the user's meal plan.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    category = recipe.category

    # Prevent duplicate entries
    if not MealPlan.objects.filter(user=request.user, recipe=recipe).exists():
        MealPlan.objects.create(user=request.user, recipe=recipe, category=category)

    return redirect('meal_plan')

@login_required
def remove_from_mealplan(request, recipe_id):
    """
    Remove a recipe from the user's meal plan.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    meal_plan_entry = MealPlan.objects.filter(user=request.user, recipe=recipe).first()
    
    if meal_plan_entry:
        meal_plan_entry.delete()
    
    return redirect('meal_plan')

