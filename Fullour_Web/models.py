from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
    
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=70, unique=True)
    first_name = models.CharField(max_length=35, null=True, blank=True)
    last_name = models.CharField(max_length=35, null=True, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null = True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    view_all = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class API(models.Model):
    api_name = models.CharField(max_length=64, primary_key=True)
    api_call_address = models.CharField(max_length=32)
    api_owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    api_release_type = models.CharField(
        max_length=7,
        choices=(('public', 'public'), ('private', 'private')),
        null=True, blank=True,
    )
    api_type = models.CharField(
        max_length=1,
        choices=(('i', 'interface API'), ('o', 'open API')),
        null=True, blank=True,
    )
    description = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    # registered in eureka or not
    api_status = models.BooleanField(default=False)
    def __str__(self):
        return self.api_name
    def get_api_name(self):
        return self.api_name

class InstanceAPI(models.Model):
    appID = models.CharField(max_length=32, primary_key=True)
    instanceID = models.CharField(max_length=32)
    api_name = models.ForeignKey(API, on_delete=models.CASCADE)
    url_address = models.CharField(max_length=32)
    instance_status = models.CharField(
        max_length=1,
        choices=(('a', 'active'), ('d', 'deactive')),
    )
    
    using_user = models.ForeignKey(MyUser, on_delete=models.CASCADE,
        null=True, blank=True)
    usage_apply = models.CharField(
        max_length=1,
        choices=(('r', 'register use'), ('i', 'in use')),
        null=True, blank=True,
    )
    call_time = models.DateField(blank=True, null=True)

    #log_file
    def __str__(self):
        return self.appID
    