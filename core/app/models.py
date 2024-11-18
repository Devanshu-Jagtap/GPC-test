from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=255, blank=True, null=True)  # Optional for Google users
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_google_user = models.BooleanField(default=False)
    google_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add unique related_name attributes to resolve clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    DisplayList = ['id','email','password','is_active','is_staff','is_google_user','google_id']

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    DisplayList = ['id','name']

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    DisplayList = ['id','category','name']

class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True,blank=True)
    publish_date = models.DateField()
    keywords = models.CharField(max_length=255)
    country_of_origin = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    DisplayList = ['id','category','subcategory','title','content','publish_date','keywords','country_of_origin','created_at']


class NewsImages(models.Model):
    news_id = models.ForeignKey(News,on_delete=models.CASCADE, related_name="newsimages")
    images = models.ImageField(upload_to='news_images/', blank=True)

    DisplayList = ['id','news_id','images']