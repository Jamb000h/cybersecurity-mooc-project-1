from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Recipe, Log, Comment


def index_view(request):
    name = request.GET.get("name", None)
    if name is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name FROM Recipe WHERE name LIKE '%%%s%%'" % name)
            rows = cursor.fetchall()
            recipes = []
            for row in rows:
                recipes.append({"id": row[0], "name": row[1]})
            return render(request, 'pages/index.html', {'recipes': recipes, 'filter': name})
    recipes = Recipe.objects.all()
    return render(request, 'pages/index.html', {'recipes': recipes})


def logs_view(request):
    logs = Log.objects.all()
    return render(request, 'pages/logs.html', {'logs': logs})


def users_view(request):
    users = User.objects.all()
    return render(request, 'pages/users.html', {'users': users})


def single_recipe(request):
    recipe_id = request.GET.get("recipeid", None)
    if recipe_id is not None:
        recipe = Recipe.objects.get(pk=recipe_id)
        if recipe is not None:
            recipe_comments = recipe.comments.all()
            print("pissa")
            canedit = recipe.user == request.user
            print("%s" % canedit)
            return render(request, 'pages/recipe.html', {'recipe': recipe, 'comments': recipe_comments, 'canedit': canedit})
        return redirect('/')
    return redirect('/recipes')


def add_recipe(request):
    name = request.POST.get("name", None)
    if name is None:
        return render(request, 'pages/addRecipe.html')
    ingredients = request.POST.get("ingredients", None)
    directions = request.POST.get("directions", None)
    if name is not None and ingredients is not None and directions is not None:
        recipe = Recipe.objects.create(
            user=request.user, name=name, ingredients=ingredients, directions=directions)
        recipe.save()
        return redirect('/recipe?recipeid=%s' % recipe.pk)

    return redirect('/')


def edit_recipe(request):
    if request.method == "GET":
        recipe_id = request.GET.get("recipeid", None)
        if recipe_id is not None:
            recipe = Recipe.objects.get(pk=recipe_id)
            if recipe is not None:
                canedit = recipe.user == request.user
                return render(request, 'pages/editRecipe.html', {'recipe': recipe, 'canedit': canedit})
            return redirect('/')
    recipeid = request.POST.get("recipeid", None)
    if recipeid is None:
        return redirect('/')
    canedit = request.POST.get("canedit", None)
    if canedit is None or canedit != "True":
        return redirect('/recipe?recipeid=%s' % recipeid)
    name = request.POST.get("name", None)
    ingredients = request.POST.get("ingredients", None)
    directions = request.POST.get("directions", None)
    if recipeid is not None and name is not None and ingredients is not None and directions is not None:
        recipe = Recipe.objects.get(pk=recipeid)
        recipe.name = name
        recipe.ingredients = ingredients
        recipe.directions = directions
        recipe.save()
        return redirect('/recipe?recipeid=%s' % recipe.pk)

    return redirect('/')


def add_user(request):
    username = request.POST.get("username")
    if username is None:
        return render(request, 'pages/addUser.html')
    password = request.POST.get("password")
    if username is not None and password is not None:
        User.objects.create_user(username=username, password=password)
    return redirect('/')


def comment(request):
    message = request.GET.get("message", None)
    if message is None:
        return redirect('/')
    recipe_id = request.GET.get("recipeid", None)
    if recipe_id is not None:
        c = Comment.objects.create(
            user=request.user, recipe=Recipe.objects.get(pk=recipe_id), message=message)
        c.save()
        return redirect('/recipe?recipeid=%s' % recipe_id)

    return redirect('/')
