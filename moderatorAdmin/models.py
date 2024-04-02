from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.postgres.fields import ArrayField


class Role(models.Model):
    name                 = models.CharField(max_length=100)
    #privilege_properties = models.JSONField()

    class Meta:
        db_table = 'role'


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name          = models.CharField(max_length=255, null=False, blank=False)
    last_name           = models.CharField(max_length=255, null=False, blank=False)
    email               = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    #profile_photo       = models.ImageField(upload_to="images/", null=False)

    # all the fields below are nullable fields
    date_of_birth       = models.DateField(null=False, blank=False)
    date_created        = models.DateField(null=False, blank=False)
    date_updated        = models.DateField(null=True, blank=True)
    last_login_date     = models.DateField(null=False, blank=False)
    email_notification  = models.BooleanField(null=False, blank=False)
    nationality         = models.CharField(max_length=255, null=True, blank=True)
    type                = models.CharField(max_length=255)
    gender              = models.CharField(max_length=255)
    banned              = models.BooleanField(default=False)

    role                = models.ForeignKey(Role, on_delete=models.CASCADE)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.email

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
    
    class Meta:
        db_table = 'user'


class Magazine(models.Model): 
    title         = models.CharField(max_length=255)
    flag          = models.CharField(max_length=255) 
    date_created  = models.DateTimeField()
    date_released = models.DateTimeField()

    class Meta:
        db_table = 'magazine'


class ScheduledJobs(models.Model):
    job_id = models.CharField(primary_key=True)
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    magazine_title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    updated_time = models.DateTimeField()
    release_date = models.DateTimeField()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'category'


class Blog(models.Model): 
    title        = models.CharField(max_length=255)
    content      = models.TextField(max_length=5000) 
    is_approved  = models.BooleanField(default=False)
    is_draft     = models.BooleanField(default=False)
    # is_rejected  = models.BooleanField(default=False) # might need it to get post rejected and their feedback
    is_ready= models.BooleanField() 
    is_rejected = models.BooleanField(default=False)
    rejection_number=models.IntegerField(default=0) 

    date_created = models.DateTimeField(null=False, blank=False)
    date_updated = models.DateTimeField(null=True, blank=True)
    reader_ids   = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    keywords     = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    likes        = models.PositiveIntegerField(default=0, null=False, blank=False) 
    comments     = models.PositiveIntegerField(default=0, null=False, blank=False) 
    readers      = models.PositiveIntegerField(default=0, null=False, blank=False) 

    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    magazine     = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    categories   = models.ManyToManyField(Category, related_name='blogs')

    class Meta:
        db_table = 'blog'
        ordering = ['-date_created']


class File(models.Model):
    uid  = models.UUIDField(editable=False)
    url  = models.FileField(upload_to='files/')

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='files') 

    class Meta:
        db_table = 'file'


class Like(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    blog      = models.ForeignKey(Blog, on_delete=models.CASCADE)

    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'like'


class Comment(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    blog      = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text      = models.TextField(max_length=500)

    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'comment'


class Feedback(models.Model):
    blog    = models.ForeignKey(Blog, related_name='blogs', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)

    class Meta:
        db_table = 'feedback'


class EmailNotification(models.Model):
    email = models.EmailField(primary_key=True)
    id = models.BigIntegerField(unique=True)
    type = models.CharField(max_length=255)
    text = models.TextField(max_length=500)
    success = models.BooleanField()

    class Meta:
        db_table = 'email_notification'


class AppNotification(models.Model):
    type      = models.CharField(max_length=255)
    text      = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    blog      = models.ForeignKey(Blog, on_delete=models.CASCADE)
    sender    = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver  = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)

    class Meta:
        db_table = 'app_notification'