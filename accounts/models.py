from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from distutils.command.upload import upload
# Create your models here.

# MODEL RESPONSIBLE FOR CREATING USER AND SUPERUSER
class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None):
        if not email:
            raise ValueError('User must have an e-mail address')
        
        if not username:
            raise ValueError('User must have an Username')

        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
            phone_number = phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, username, email, phone_number, password):
        user = self.create_user(
            email      = self.normalize_email(email),
            username   = username,
            password   = password,
            phone_number = phone_number,
        )
        user.is_admin   = True
        user.is_active  = True
        user.is_superadmin  = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# MODEL RESPONSIBLE FOR STORING RIGHTS 
class Rights(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# MODEL RESPONSIBLE FOR STORING ROLES 
class Role(models.Model):
    name = models.CharField(max_length=100)
    # Additional fields for Role model
    rights = models.ManyToManyField(Rights)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# MODEL RESPONSIBLE FOR STORING USERS
class Account(AbstractBaseUser):
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50,null=True)
    role            = models.ForeignKey(Role, on_delete=models.CASCADE,  null=True, blank=True)
    #Required fields
    date_joined     = models.DateTimeField(auto_now_add=True)  
    last_login      = models.DateTimeField(auto_now_add=True)  
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    objects = MyAccountManager()

    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True



    