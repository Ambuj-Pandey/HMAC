from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import os
from pdf2image import convert_from_path
from .models import FileModel, FileImage, AIDetection
from .helper import roboflowHelperFunc, ocrHelperFunc, makeDir

import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


COVER_PAGE_DIRECTORY = 'coverdirectory/'
# PDF_DIRECTORY = 'pdfdirectory/'
COVER_PAGE_FORMAT = 'jpg'

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