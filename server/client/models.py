from django.db import models

# Create your models here.
class InventoryModel(models.Model):
    Medication_Name = models.CharField(max_length=200,null=True,blank=True)
    Description = models.TextField(blank = True,null=True)
    Medication_Size = models.CharField(max_length=200,null=True,blank=True)
    Quantity = models.IntegerField(null=True,blank=True)
    ReStock_Level = models.IntegerField(null=True,blank=True)
    Qr_Code = models.CharField(max_length=200,null=True,blank=True)
    Medication_Image = models.ImageField(null=True, blank=True,upload_to='files/Medication')
    Qr_image = models.ImageField(null=True, blank=True,upload_to='files/Qr_Codes')
    shelf =  models.CharField(max_length=200,null=True,blank=True,default="Yes")
    last_updated = models.DateTimeField(auto_now_add=True, null=True)
    dateField = models.DateField(auto_now_add=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Medication_Name

class MedicationBasket(models.Model):
    Medication_ID = models.ForeignKey(InventoryModel, blank=True, null=True,on_delete=models.CASCADE,related_name="baseket",default=None)
    Quantity = models.IntegerField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Medication_ID.Medication_Name


class CompleteOrder(models.Model):
    Medication_ID = models.ForeignKey(InventoryModel, blank=True, null=True,on_delete=models.CASCADE,related_name="complete",default=None)
    Quantity = models.IntegerField(null=True,blank=True)
    month = models.CharField(max_length=200,null=True,blank=True)
    year = models.IntegerField(null=True,blank=True)
    dateField = models.DateField(auto_now_add=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Medication_ID.Medication_Name

class MedicationLabel(models.Model):
    Medication_ID = models.ForeignKey(InventoryModel, blank=True, null=True,on_delete=models.CASCADE,related_name="label_id",default=None)
    Take = models.CharField(max_length=200,null=True,blank=True)
    Times = models.CharField(max_length=200,null=True,blank=True)
    Hours = models.CharField(max_length=200,null=True,blank=True)
    ExpireDate = models.DateField(auto_now_add=False,null=True)
    before = models.CharField(max_length=200,null=True,blank=True)
    after = models.CharField(max_length=200,null=True,blank=True)
    label = models.CharField(max_length=200,null=True,blank=True,default="No")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
            return self.Medication_ID.Medication_Name

class ClinicLogo(models.Model):
    clinic_logo = models.ImageField(null=True, blank=True,upload_to='files/clinicLogo')
    name = "Tshepang Healthcare"

    def __str__(self):
            return self.name

