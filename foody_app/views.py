from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Count
from .filters import RestaurantFilter
from django.views.generic import DetailView
from django.core.paginator import Paginator
import bcrypt


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash
            )
            request.session['user_id'] = user.id
            request.session['greeting'] = user.first_name
            return redirect('/dashboard')
    return redirect('/')

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
                request.session['user_id'] = user.id
                request.session['greeting'] = user.first_name
                return redirect('/dashboard')
        messages.error(request, "Email for password are not right")
    return redirect('/')

def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        contact_list = Restaurant.objects.all()
        paginator = Paginator(contact_list, 5) 
        page_num = request.GET.get('page')
        page = paginator.get_page(page_num)
        
        context = {
            'fav_restaurant': Restaurant.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id']),
            'page': page,
            'count': paginator.count
        }
        
        return render(request, 'dashboard.html', context)

def new(request):
    context = {
            'this_user': User.objects.get(id=request.session['user_id'])
        }
    return render(request, 'new.html', context)

def create_restaurant(request):
    errors = Restaurant.objects.restaurant_validator(request.POST)

    if len(errors):
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        user = User.objects.get(id=request.session["user_id"])
        restaurant = Restaurant.objects.create(
            restaurant_name = request.POST['restaurant_name'],
            date = request.POST['date'],
            time = request.POST['time'],
            address = request.POST['address'],
            creator = user
        )
        restaurant.joined_by.add(User.objects.get(id=request.session['user_id']))
        return redirect(f'/dashboard')

def one_restaurant(request, id):
    context = {
        'one_restaurant': Restaurant.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "one_restaurant.html", context)


def search(request):
    restaurant_list = Restaurant.objects.all()
    myFilter = RestaurantFilter(request.GET,queryset=restaurant_list)
    restaurant_list=myFilter.qs
    paginator = Paginator(restaurant_list, 5) 
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    context = {
        'all_restaurant': Restaurant.objects.all,
        'this_user': User.objects.get(id=request.session['user_id']),
        'page': page,
        'count': paginator.count,
        'myFilter':myFilter
        }
    return render(request, "search.html", context)

def my_profile(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        another_user= User.objects.get(id=id) 
        print(another_user)
        context = {
            'another_user': User.objects.get(id=id),
            'current_user': User.objects.get(id=request.session['user_id']),
            'all_images':User.objects.all()
        }
        return render(request, 'profile.html', context)

def user_profile(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        buddy_user= User.objects.get(id=id) 
        print(buddy_user)
        context = {
            'buddy_user': User.objects.get(id=id),
            'current_user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'user.html', context)

def delete(request, id):
    one_restaurant= Restaurant.objects.get(id=id)
    one_restaurant.delete()
    return redirect('/dashboard')

def follow(request, id):
    users = User.objects.get(id=request.session['user_id'])
    follow = User.objects.get(id=id)
    follow.followers.add(users)
    return redirect(f'/dashboard/user/{id}')

def unfollow(request, id):
    users = User.objects.get(id=request.session['user_id'])
    follow = User.objects.get(id=id)
    follow.followers.remove(users)
    print (users.followers.all())
    return redirect(f'/dashboard/user/{id}')

def join(request, id):
    user = User.objects.get(id=request.session['user_id'])
    join= Restaurant.objects.get(id=id)
    join.joined_by.add(user)
    return redirect(f'/dashboard/{id}')

def leave(request, id):
    user = User.objects.get(id=request.session['user_id'])
    join= Restaurant.objects.get(id=id)
    join.joined_by.remove(user)
    return redirect(f'/dashboard/{id}')


def logout(request):
    request.session.flush()

    return redirect('/')


def image_upload_view(request, id):
    pic=request.FILES['picture']
    user = User.objects.get(id=request.session['user_id']) # Get logged in user's object
    user.profile_pic = pic # Link the image
    user.save() # Save the updated profile
    # User.objects.create(profile_pic=pic) # You're creating a new user, not linking the user to the profile picture
    return redirect(f'/dashboard/profile/{id}')

