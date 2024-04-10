from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/media/photos')

class CustomUserManager(BaseUserManager):
    def create_user(self, id, password=None, **extra_fields):
        if not id:
            raise ValueError('The User ID must be set')
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(id=id, password=password, **extra_fields)

class CustomUser(AbstractBaseUser):
    id=models.CharField(max_length=15,unique=True,primary_key=True)     #중복이 있으면 안되므로 primary_key를 true로 설정
    name=models.CharField(max_length=30)
    email=models.EmailField()
    major=models.CharField(max_length=20)
    nickname=models.CharField(max_length=10)
    password=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=13)
    age = models.IntegerField(null=True, blank=True)  
    hobbies = models.TextField(null=True, blank=True)  
    photo = models.ImageField(upload_to='media/', null=True, blank=True) 



    USERNAME_FIELD = 'id'
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    def __str__(self):
        return self.id
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser