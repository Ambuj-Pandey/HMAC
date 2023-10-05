from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


from .comparison import compare_uploaded_file_with_database
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, email , password, is_active=True, is_staff=False, is_superuser=False, full_name=None):

        if not email:
            raise ValueError('Invalid Email')

        if not password:
            raise ValueError('Password cannot be empty')


        User = self.model(
            email=self.normalize_email(email)
        )
        User.user_id = user_id
        User.is_active = is_active
        User.is_staff = is_staff
        User.is_superuser = is_superuser

        User.set_password(password)
       
        User.full_name=full_name

        User.save(using=self.db)
        return User

    def create_staffuser(self, user_id, email, password):
        User = self.create_user(
            user_id,
            email=email,
            password=password, 
            is_staff=True,
            is_superuser=False
            )
        return User


    def create_superuser(self, user_id, email, password):
        User = self.create_user(
            user_id,
            email=email,
            password=password,
            is_staff=True, 
            is_superuser=True
            )
        return User
    

class User(AbstractUser):
    user_id = models.CharField(max_length=50, unique=True)
    # username = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=255, unique=True)
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    full_name = models.CharField(max_length=50, null=True)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id',]

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

class FileModel(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    filename = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='files/')

    def save(self, *args, **kwargs):
        # Assign a default user if 'uploaded_by' is not set
        if not self.uploaded_by:
            self.uploaded_by = User.objects.get(Email='a@a.com')  # Replace with the actual default user
        super().save(*args, **kwargs)

    @staticmethod
    def preprocess_ocr_data(ocr_data):
        # This removes the commas from the txt files to not cause bloated percentage
        return [word.strip() for word in ocr_data.split(',') if word.strip()]

    
    def read_file_content(self):
        # Implement this method to read and return the content of the file
        try:
            with open(self.file.path, 'r') as file:
                content = file.read()
                preprocessed_content = FileModel.preprocess_ocr_data(content)
                return preprocessed_content
        except Exception as exc:
            print(f"Error reading file '{self.file.name}': {exc}")
            return ""
    
    def __str__(self):
        return self.filename

@receiver(post_save, sender=FileModel)
def calculate_similarity_on_upload(sender, instance, created, **kwargs):
    if created:
        # Get the content of the uploaded file using the newly defined method
        uploaded_file_content = instance.read_file_content()

        # Get all other files from the database
        other_files = FileModel.objects.exclude(pk=instance.pk)

        # Trigger similarity calculation for the uploaded file with all other files
        compare_uploaded_file_with_database(uploaded_file_content, other_files)