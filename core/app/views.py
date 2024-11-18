from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect ,reverse
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from . forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q


class LoginView(View):
    def get(self, request):
        # Render the login form on GET request
        form = AuthenticationForm()
        return render(request, 'html/login.html', {'form': form})

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Authenticate using the email and password
        user = authenticate(request, username=email, password=password)
        print("1")

        user = User.objects.get(email=email)
        if user:
            return redirect("form")  # Redirect to the index page after login success
        else:
            messages.error(request, "Invalid email or password")
            return render(request, 'html/login.html')
        

class SignupView(View):
    def get(self, request):
        """Render the signup form."""
        form = SignupForm()
        return render(request, 'html/signup.html', {'form': form})

    def post(self, request):
        """Handle form submission."""
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            return redirect('form')
        else:
            # If the form is invalid, re-render with errors
            return render(request, 'html/signup.html', {'form': form})
        

class IndexView(View):
    def get(self, request):
        return render(request,'html/index.html')
    

class FormPage(View):
    def get(self, request):
        form = NewsForm()  # Instantiate a blank form
        categories = Category.objects.all()  # Fetch all categories
        return render(request, 'html/forms-basic-inputs.html', {'form': form, 'categories': categories})
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            category_id = request.GET.get('category_id')
            if category_id:
                subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
                return JsonResponse({'subcategories': list(subcategories)})
        return JsonResponse({'error': 'Invalid request'}, status=400)

def fetch_subcategories(request):
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse({'subcategories': list(subcategories)}, status=200)
    return JsonResponse({'error': 'No category ID provided'}, status=400)

class FetchSubcategoriesView(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        if category_id:
            subcategories = SubCategory.objects.filter(category_id=category_id)
            return JsonResponse({"subcategories": list(subcategories.values("id", "name"))})
        else:
            return JsonResponse({"error": "Category ID is required"}, status=400)
        
class SubmitNewsView(View):
    def get(self, request, *args, **kwargs):
        form = NewsForm()
        return render(request, 'admin_template/submit_news.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check for AJAX request
            form = NewsForm(request.POST)
            if form.is_valid():
                news = form.save()  # Save the news
                # Handling news images
                image_form = NewsImagesForm(request.FILES)
                if image_form.is_valid():
                    for img in request.FILES.getlist('images'):
                        NewsImages.objects.create(news_id=news, images=img)
                return JsonResponse({"success": "News submitted successfully!"})
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": "Invalid request"}, status=400)


class SubCategoryView(View):
    def get(self, request, id=None):
        if id:
            subcategory = get_object_or_404(SubCategory, pk=id)
            subcategory.delete()
            messages.success(request, 'A Sub-Category is deleted successfully.')
            return redirect(reverse('subcategory'))
        else:
            if "q" in request.GET:
                searchobj = request.GET.get("q")
                data = SubCategory.objects.filter(subCategoryName__icontains=searchobj)
            else:
                data = SubCategory.objects.all()

            # Pagination
          
            return render(request, 'html/category.html', {'data': data})
class news_list(View):

    def get(self,request):
        categories = Category.objects.all()  # Assuming Category is the model for categories
        subcategories = SubCategory.objects.all()  # Assuming Subcategory is the model for subcategories
        
        query = request.GET.get('search', '')
        category_id = request.GET.get('category', None)
        subcategory_id = request.GET.get('subcategory', None)

        news_posts = News.objects.all()

        if query:
            news_posts = news_posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

        if category_id:
            news_posts = news_posts.filter(category__id=category_id)

        if subcategory_id:
            news_posts = news_posts.filter(subcategory__id=subcategory_id)

        return render(request, 'html/news_list.html', {
            'news_posts': news_posts,
            'categories': categories,
            'subcategories': subcategories,
        })

class news_detail(View):
    def get(self,request, id):
        # Fetch the news post based on the given ID
        news_post = get_object_or_404(News, id=id)
        news_images = news_post.newsimages.all()
        # Pass the news post to the template
        keywords_list = news_post.keywords.split(",") if news_post.keywords else []

        # Pass the news post and keywords to the template
        context = {
            'news_post': news_post,
            'keywords': keywords_list,
            'news_images': news_images,
        }
        return render(request, 'html/news_detail.html', context)
    

class CategoryView(View):

    def get(self, request, id=None):
        if id:
            # Deleting a specific category if ID is provided
            category = get_object_or_404(Category, pk=id)
            category.delete()
            messages.success(request, 'Category deleted successfully.')
            return redirect(reverse('master:category'))  # Adjust the reverse URL name

        else:
            # Listing categories with optional search and pagination
            if "q" in request.GET:
                search_query = request.GET.get("q")
                categories = Category.objects.filter(name__icontains=search_query)
            else:
                categories = Category.objects.all()

            return render(request, 'html/category.html', {
                'categories': categories
            })

    def post(self, request, id=None):
        if id:
            # Updating an existing category
            category = get_object_or_404(Category, pk=id)

            category_name = request.POST.get('name')
            if not category_name:
                messages.error(request, 'Category name is required.')
                return redirect(reverse('master:category'))

            category.name = category_name
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect(reverse('master:category'))

        else:
            # Creating a new category
            category_name = request.POST.get('name')

            if Category.objects.filter(name=category_name).exists():
                messages.error(request, 'A category with the same name already exists.')
                return redirect(reverse('master:category'))

            try:
                category_instance = Category(name=category_name)
                category_instance.save()
                messages.success(request, 'Category created successfully.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

            return redirect(reverse('master:category'))


class SubCategoryView(View):

    def get(self, request, id=None):
        if id:
            # Deleting a specific subcategory if ID is provided
            subcategory = get_object_or_404(SubCategory, pk=id)
            subcategory.delete()
            messages.success(request, 'SubCategory deleted successfully.')
            return redirect(reverse('master:subcategory'))  # Adjust the reverse URL name

        else:
            # Listing subcategories with optional search and pagination
            if "q" in request.GET:
                search_query = request.GET.get("q")
                subcategories = SubCategory.objects.filter(name__icontains=search_query)
            else:
                subcategories = SubCategory.objects.all()

            # Fetch categories for the dropdown
            categories = Category.objects.all()

            return render(request, 'html/subcategory.html', {
                'subcategories': subcategories,
                'categories': categories  # Sending categories to the template
            })


    def post(self, request, id=None):
        if id:
            # Updating an existing subcategory
            subcategory = get_object_or_404(SubCategory, pk=id)

            subcategory_name = request.POST.get('name')
            category_id = request.POST.get('category')

            if not subcategory_name or not category_id:
                messages.error(request, 'SubCategory name and category are required.')
                return redirect(reverse('master:subcategory'))

            category = get_object_or_404(Category, pk=category_id)
            subcategory.name = subcategory_name
            subcategory.category = category
            subcategory.save()
            messages.success(request, 'SubCategory updated successfully.')
            return redirect(reverse('master:subcategory'))

        else:
            # Creating a new subcategory
            subcategory_name = request.POST.get('name')
            category_id = request.POST.get('category')

            if not subcategory_name or not category_id:
                messages.error(request, 'SubCategory name and category are required.')
                return redirect(reverse('master:subcategory'))

            if SubCategory.objects.filter(name=subcategory_name, category_id=category_id).exists():
                messages.error(request, 'A subcategory with the same name already exists in this category.')
                return redirect(reverse('master:subcategory'))

            try:
                category = get_object_or_404(Category, pk=category_id)
                subcategory_instance = SubCategory(name=subcategory_name, category=category)
                subcategory_instance.save()
                messages.success(request, 'SubCategory created successfully.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

            return redirect(reverse('master:subcategory'))
        

class LogoutView(View):
    def get(self, request):
        # Log the user out
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('login') 