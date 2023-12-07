from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from .comparison import compare_uploaded_file_with_database
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import os
from pdf2image import convert_from_path

import concurrent.futures
from .comparison import compare_file_similarity

from .helper import roboflowHelperFunc, ocrHelperFunc, makeDir

import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


COVER_PAGE_DIRECTORY = 'coverdirectory/'
# PDF_DIRECTORY = 'pdfdirectory/'
COVER_PAGE_FORMAT = 'jpg'

class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, email, password, is_active=True, is_staff=False, is_superuser=False, full_name=None):

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

        User.full_name = full_name

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

    # @staticmethod
    # def preprocess_ocr_data(ocr_data):
    #     # This removes the commas from the txt files to not cause bloated percentage
    #     return [word.strip() for word in ocr_data.split(',') if word.strip()]

    # def read_file_content(self):
    #     # Implement this method to read and return the content of the file
    #     try:
    #         with open(self.file.path, 'r') as file:
    #             content = file.read()
    #             preprocessed_content = FileModel.preprocess_ocr_data(content)
    #             return preprocessed_content
    #     except Exception as exc:
    #         print(f"Error reading file '{self.filename}': {exc}")
    #         return ""

    def save(self, *args, **kwargs):
        # Assign a default user if 'uploaded_by' is not set
        if not self.uploaded_by:
            # Replace with the actual default user
            self.uploaded_by = User.objects.get(Email='a@a.com')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.filename

class FileComparisonModel(models.Model):
    uploaded_file = models.ForeignKey(
        FileModel, on_delete=models.CASCADE, related_name='uploaded_file')
    other_file = models.ForeignKey(
        FileModel, on_delete=models.CASCADE, related_name='other_file')
    similarity_result = models.FloatField()

    def __str__(self):
        return f"Comparison between {self.uploaded_file.filename} and {self.other_file.filename}"

class FileImage(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pdfFile = models.ForeignKey(FileModel, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='fileImages/')

    def __str__(self):
        return self.filename

class AIDetection(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    detection_results_Human = models.FloatField(null=True)
    detection_results_AI = models.FloatField(null=True)

    def __str__(self):
        return f"Result of {self.uploaded_file.filename} is {self.detection_results_Human}"


# def compare_uploaded_file_with_database(uploaded_file_content, uploaded_file_data, file_model_list):
#     comparisons = []  # To store comparison results before saving

#     # Some parallel processing magic which I have no clue of
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future_to_filename = {
#             executor.submit(compare_file_similarity, uploaded_file_content, file_model): file_model.filename
#             for file_model in file_model_list
#         }
#         for future in concurrent.futures.as_completed(future_to_filename):
#             filename = future_to_filename[future]
#             try:
#                 result = future.result()
#                 if result[1] is not None:
#                     print(
#                         f"Similarity between uploaded file and '{filename}': {result[1] * 100:.2f}")
#                     # Create a dictionary to store comparison data
#                     comparison_data = {
#                         'uploaded_file': uploaded_file_data,
#                         'other_file': file_model_list.get(filename=filename),
#                         'similarity_result': result[1],
#                     }
#                     comparisons.append(comparison_data)
#                 else:
#                     print(
#                         f"Error processing '{filename}': Unable to calculate similarity.")
#             except Exception as exc:
#                 print(f"Error processing '{filename}': {exc}")

#     FileComparisonModel.objects.bulk_create(
#         [FileComparisonModel(**data) for data in comparisons])


# @receiver(post_save, sender=FileModel)
# def calculate_similarity_on_upload(sender, instance, created, **kwargs):
#     if created:
#         # Get the content of the uploaded file using the newly defined method
#         uploaded_file_content = instance.read_file_content()

#         # Get all other files from the database
#         other_files = FileModel.objects.exclude(pk=instance.pk)

#         uploaded_file_data = instance

#         # Trigger similarity calculation for the uploaded file with all other files
#         compare_uploaded_file_with_database(
#             uploaded_file_content, uploaded_file_data, other_files)



@receiver(post_save, sender=FileModel)
def convert_pdf_to_image(sender, instance, created, **kwargs):
    if created:
        # check if COVER_PAGE_DIRECTORY exists, create it if it doesn't
        # have to do this because of setting coverpage attribute of instance programmatically
        cover_page_dir = os.path.join(settings.MEDIA_ROOT, COVER_PAGE_DIRECTORY)

        if not os.path.exists(cover_page_dir):
            os.mkdir(cover_page_dir)

        # convert page cover (in this case) to jpg and save
        cover_page_image = convert_from_path(
            pdf_path=instance.file.path,
            dpi=200, 
            first_page=1, 
            last_page=1, 
            fmt=COVER_PAGE_FORMAT, 
            output_folder=cover_page_dir,
            poppler_path = r"C:\Users\Nandini\Downloads\Release-23.11.0-0\poppler-23.11.0\Library\bin"
            )[0]
        
        cover_page_image.close()

        # get name of pdf_file 
        pdf_filename, extension = os.path.splitext(os.path.basename(instance.file.name))
        new_cover_page_path = '{}.{}'.format(os.path.join(cover_page_dir, pdf_filename), COVER_PAGE_FORMAT)
        # rename the file that was saved to be the same as the pdf file
        os.rename(cover_page_image.filename, new_cover_page_path)
        # get the relative path to the cover page to store in model
        new_cover_page_path_relative = '{}.{}'.format(os.path.join(COVER_PAGE_DIRECTORY, pdf_filename), COVER_PAGE_FORMAT)
        instance.coverpage = new_cover_page_path_relative

        file_image = FileImage(
            uploaded_by=instance.uploaded_by,
            pdfFile=instance,
            filename=instance.filename,
            description=instance.description,
            file=new_cover_page_path_relative,  # Set the file field to the cover page path
        )

        # Save the new FileImage instance
        file_image.save()

        # call save on the model instance to update database record
        instance.save()


@receiver(post_save, sender =FileImage)
def create_ai_detection(sender, instance, created, **kwargs):
    if created:
        model_path = 'model'
        tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        num_labels = 2
        Bert_Model = DistilBertForSequenceClassification.from_pretrained(
            model_path, num_labels=num_labels)
        Bert_Model.eval()

        makeDir()

        lines = roboflowHelperFunc(instance)

        print("Type of 'detections':", type(lines))

        text = ocrHelperFunc(lines)
    
        inputs = tokenizer(text, return_tensors="pt")

        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        with torch.no_grad():
            outputs = Bert_Model(input_ids, attention_mask)
            logits = outputs.logits

        probabilities = torch.softmax(logits, dim=1)

        percentage_probs = (probabilities * 100).tolist()[0]

        class_labels = [str(i) for i in range(num_labels)]

        class_percentage_dict = {label: percentage for label,
                                percentage in zip(class_labels, percentage_probs)}

        for label, percentage in class_percentage_dict.items():
            print(f"Class {label}: {percentage:.2f}%")
        
        detection_results_Human = percentage_probs[0]
        detection_results_AI = percentage_probs[1]

        print(detection_results_Human)

        # Create an AIDetection instance associated with the uploaded FileModel
        ai_detection = AIDetection(
            uploaded_by=instance.uploaded_by,
            detection_results_Human=detection_results_Human,
            detection_results_AI=detection_results_AI,
            # You can set initial values for detection_results_Human and detection_results_AI here if needed
        )
        ai_detection.save()