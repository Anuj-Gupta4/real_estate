
from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Listing
from .forms import ListingForm
import pandas as pd
import joblib

reloadModel = joblib.load('./models/pipeline1.pkl')

# Create your views here.

class CustomLoginView(LoginView):
    template_name='login.html'
    fields = '__all___'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('listing_list')

class RegisterPage(FormView):
    template_name='register.html'
    form_class = UserCreationForm
    redirect_authenticated_user=True
    success_url = reverse_lazy('listing_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('listing_list')
        return super(RegisterPage, self).get(*args, **kwargs)

def index(request):
    temp={}
    context= {'temp':temp}
    return render(request, 'base.html',context)

def predict(request):
    print(request)
    if request.method == 'POST':
            
        temp=dict()
        # temp.columns =['Name', 'Code', 'Age', 'Weight']
        temp['City'] = [request.POST.get('City')]
        temp['Bedroom'] = [request.POST.get('Bedroom')]
        temp['Bathroom'] = [request.POST.get('Bathroom')]
        temp['Floors'] = [request.POST.get('Floors')]
        temp['Parking'] = [request.POST.get('Parking')]
        temp['Face'] = [request.POST.get('Face')]
        temp['Area'] = [request.POST.get('Area')]
        temp['Road_Width'] = [request.POST.get('Road_Width')]
        temp['Road_Type'] = [request.POST.get('Road_Type')]
        temp['Build_Area'] = [request.POST.get('Build_Area')]
        temp['Amenities'] = [request.POST.get('Amenities')]
    print(temp)

    data_df = pd.DataFrame(temp)
    ans= reloadModel.predict(data_df)
    # probs= reloadModel.predict_proba(data_df)

    context={'scoreval':ans,'temp':temp}
    return render(request,'base.html',context)

# @login_required
def listing_list(request):
    listings = Listing.objects.all()
    context = {
        "listings" : listings
    }
    return render(request, "listings.html", context)

@login_required
def listing_retrieve(request,pk):
    listing= Listing.objects.get(id=pk)
    context={
        "listing":listing
    }
    return render(request,"listing.html",context)

# @login_required
# def listing_create(request):
#     form = ListingForm()
#     if request.method == "POST":
#         form = ListingForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("listings/")

#     context = {
#         "form":form
#     }
#     return render(request, "listing_create.html", context)

#CRUD -Create, Retrieve, Update, Delete
class listing_create(LoginRequiredMixin, CreateView):
    model = Listing
    fields= ['Title', 'Location', 'City', 'Price', 'Bedroom', 'Bathroom', 'Floors', 'Parking', 'Face', 'Area', 'Road_Width', 
    'Road_Type', 'Build_Area', 'Amenities', 'Contact_number', 'Contact_mail', 'Image']
    template_name='listing_create.html'
    success_url=reverse_lazy('listing_list')
    def form_valid(self,form):
        form.instance.user=self.request.user
        print(form.instance.user)
        return super(listing_create,self).form_valid(form)

@login_required
def listing_update(request, pk):
    listing= Listing.objects.get(id=pk)

    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing, files = request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/user_specific_listings")
    else:
        form = ListingForm(instance=listing)

    context = {
        "form":form
    }
    return render(request, "listing_update.html", context)

@login_required
def listing_delete(request, pk):
    listing = Listing.objects.get(id = pk)
    listing.delete()
    return redirect("/user_specific_listings")

@login_required
def user_specific_listings(request):
    queryset_list=Listing.objects.all()
    username = request.user.username
    queryset_list=Listing.objects.filter(user__username=username)

    context={
        'listings':queryset_list,
    }

    return render(request, "user_specific_listings.html", context)

# @login_required
def listing_search(request):
    queryset_list=Listing.objects.all()

    # Title
    if 'Title' in request.GET:
        Title = request.GET['Title']
        if Title:
            queryset_list = queryset_list.filter(Title__icontains = Title)
    else:
        Title = ''
        
    #City
    if 'City' in request.GET:
        city = request.GET['City']
        print(city)
        if city:
            queryset_list=queryset_list.filter(City__iexact = city)
    else:
        city = ''

    #Face
    if 'Face' in request.GET:
        Face = request.GET['Face']
        if Face:
            queryset_list=queryset_list.filter(Face__iexact = Face)
    else:
        Face = ''
    
     # Bedroom
    if 'Bedroom' in request.GET:
        Bedroom = request.GET['Bedroom']
        if Bedroom:
            queryset_list=queryset_list.filter(Bedroom__gte=Bedroom)
    else:
        Bedroom = ''

    # Bathroom
    if 'Bathroom' in request.GET:
        Bathroom = request.GET['Bathroom']
        if Bathroom:
            queryset_list=queryset_list.filter(Bathroom__gte=Bathroom)
    else:
        Bathroom = ''

    # Floors
    if 'Floors' in request.GET:
        Floors = request.GET['Floors']
        if Floors:
            queryset_list=queryset_list.filter(Floors__gte=Floors)
    else:
        Floors = ''

    # Area
    if 'Area' in request.GET:
        Area = request.GET['Area']
        if Area:
            queryset_list=queryset_list.filter(Area__lte=Area)
    else:
        Area = ''

    # Price
    if 'Price' in request.GET:
        Price = request.GET['Price']
        if Price:
            queryset_list=queryset_list.filter(Price__lte=Price)
    else:
        Price = ''
                
    context={
        'listings':queryset_list, 'Price':Price, 'Area':Area, 'Floors':Floors, 'Bathroom':Bathroom, 'Bedroom':Bedroom,
        'Face':Face, 'City': city, 'Title': Title
    }

    return render(request, "listing_search.html", context)