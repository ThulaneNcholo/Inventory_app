from django.contrib import admin
from .models import InventoryModel,MedicationBasket,CompleteOrder,MedicationLabel,ClinicLogo

# Register your models here.
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'Qr_Code', 'Medication_Name', 'Quantity','ReStock_Level'
    )

class MedicationBasketAdmin(admin.ModelAdmin):
    list_display = (
        'Medication_ID','Quantity', 'date_created',
    )

class CompleteOrderAdmin(admin.ModelAdmin):
    list_display = (
        'Medication_ID','Quantity', 'date_created','dateField'
    )

class LabelsAdmin(admin.ModelAdmin):
    list_display = (
        'Medication_ID','Take','Hours', 'Times','before','after','ExpireDate'
    )

admin.site.register(InventoryModel,InventoryAdmin)
admin.site.register(MedicationBasket,MedicationBasketAdmin)
admin.site.register(CompleteOrder,CompleteOrderAdmin)
admin.site.register(MedicationLabel,LabelsAdmin)
admin.site.register(ClinicLogo)
