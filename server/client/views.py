from django.shortcuts import render,redirect
from .models import InventoryModel,MedicationBasket,CompleteOrder,MedicationLabel,ClinicLogo
from django.contrib import messages

# Qr Code Imports 
import random
import cv2
from pyzbar.pyzbar import decode
import time
import qrcode
from PIL import Image

from datetime import datetime
from django.db.models import Sum , F
from django.db.models import Q

# pdf imports 
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.
def IndexView(request):
    today = datetime.today()
    hero_date = today.strftime("%B %d, %Y")
    stockOut_Count = CompleteOrder.objects.filter(dateField = today).count()
    stockIn_count = InventoryModel.objects.filter(dateField = today).count()
    lowInventory_count = InventoryModel.objects.filter(Quantity__lte=F('ReStock_Level')).count()
    basket_count = MedicationBasket.objects.all().count()
    lowInventory = InventoryModel.objects.filter(Quantity__lte=F('ReStock_Level'))
    
    context = {
        "stockOut_Count" : stockOut_Count ,
        "stockIn_count" : stockIn_count,
        "lowInventory_count" : lowInventory_count,
        "hero_date" : hero_date,
        "basket_count" : basket_count,
        "lowInventory" : lowInventory
    }
    return render(request,'client/index.html',context)

def AddInventory(request):
    if request.method == 'POST' and 'add_Inventory' in request.POST:
        save_Data = InventoryModel()
        save_Data.Medication_Name = request.POST.get('medicationName')
        save_Data.Description = request.POST.get('description')
        save_Data.Medication_Size = request.POST.get('Size')
        save_Data.Quantity = request.POST.get('Quantity')
        save_Data.ReStock_Level = request.POST.get('Restock')
        save_Data.Medication_Image  = request.FILES['med_Image']
        
        # create Qr Code 
        QrCode_Reference = random.randrange(0, 1000000000000)
        GeneratedQrCode = qrcode.make(QrCode_Reference)
        GeneratedQrCode.save(f"{save_Data.Medication_Name}.png",scale = 7)
        
        # save to datbase 
        save_Data.Qr_image = (f"{save_Data.Medication_Name}.png")
        save_Data.Qr_Code = QrCode_Reference
        save_Data.save()
        messages.success(request,save_Data.Medication_Name + ' successfully added.')
        return redirect('inventory_details' ,save_Data.id)
        
    return render(request,'client/add_Iventory.html')

def BulkEntry(request):
    if request.method == 'POST' and 'bulk_Inventory' in request.POST:
        save_Data = InventoryModel()
        save_Data.Medication_Name = request.POST.get('medicationName')
        save_Data.Description = request.POST.get('description')
        save_Data.Medication_Size = request.POST.get('Size')
        save_Data.ReStock_Level = request.POST.get('Restock')
        save_Data.Medication_Image  = request.FILES['med_Image']

        Quantity_in_box = request.POST.get('Quantity')
        boxes = request.POST.get('Boxes')
        save_Data.Quantity = int(Quantity_in_box) * int(boxes)
        
        # create Qr Code 
        QrCode_Reference = random.randrange(0, 1000000000000)
        GeneratedQrCode = qrcode.make(QrCode_Reference)
        GeneratedQrCode.save(f"{save_Data.Medication_Name}.png",scale = 7)
        
        # save to database 
        save_Data.Qr_image = (f"{save_Data.Medication_Name}.png")
        save_Data.Qr_Code = QrCode_Reference
        save_Data.save()
        messages.success(request,save_Data.Medication_Name + ' successfully added.')
        return redirect('inventory_details' ,save_Data.id)
    return render(request,'client/bulk_entry.html')

def StockOut(request):
    medication_data = InventoryModel.objects.all().order_by("-date_created")
    basket_count = MedicationBasket.objects.all().count()

    if request.method == 'POST' and 'stock_out' in request.POST:
        medication_ID = request.POST.get('med_ID')
        add_basket = MedicationBasket()
        add_basket.Medication_ID = InventoryModel.objects.get(id = medication_ID)
        add_basket.Quantity = request.POST.get('quantity')
        add_basket.save()
       
        # update inventory Model 
        inventory_update = InventoryModel.objects.get(id = medication_ID)
        inventory_update.Quantity = int(inventory_update.Quantity) - int(add_basket.Quantity)
        inventory_update.save()
       
        messages.success(request,add_basket.Medication_ID.Medication_Name + ' added to basket.')
        return redirect('stock_out')

    # search Stock Out medication 
    if request.method == 'POST' and 'search' in request.POST:
        searchInput = request.POST.get('search_input')
        medication_data = InventoryModel.objects.filter(Q(Medication_Name__icontains = searchInput) | Q(Qr_Code__icontains = searchInput))


    context = {
        "medication_data" : medication_data,
        "basket_count" : basket_count
    }
    return render(request,'client/stock_out.html',context)

def LowStock(request):
    lowInventory = InventoryModel.objects.filter(Quantity__lte=F('ReStock_Level'))

    if request.method == 'POST' and 'filter_lowInventory' in request.POST:
        low_High = request.POST.get('low-high')
        high_low = request.POST.get('high-low')

        if low_High:
            lowInventory = InventoryModel.objects.filter(Quantity__lte=F('ReStock_Level')).order_by("Quantity")

        if high_low:
            lowInventory = InventoryModel.objects.filter(Quantity__lte=F('ReStock_Level')).order_by("-Quantity")

    if request.method == 'POST' and 'search' in request.POST:
        searchInput = request.POST.get('search_input')
        lowInventory = InventoryModel.objects.filter( Q(Quantity__lte=F('ReStock_Level')) & Q(Medication_Name__icontains = searchInput))

        # return redirect('low_stock')


    context = {
        "lowInventory": lowInventory
    }
    return render(request,'client/low_inventory.html',context)

def ScanQrCode(request, qr_code):
    inventory_data = InventoryModel.objects.filter(Qr_Code__icontains = qr_code)
    basket_count = MedicationBasket.objects.all().count()

    if request.method == 'POST' and 'stock_out' in request.POST:
        medication_ID = request.POST.get('med_ID')
        add_basket = MedicationBasket()
        add_basket.Medication_ID = InventoryModel.objects.get(id = medication_ID)
        add_basket.Quantity = request.POST.get('quantity')
        add_basket.save()
        print('ADDED')
        # update inventory Model 
        inventory_update = InventoryModel.objects.get(id = medication_ID)
        inventory_update.Quantity = int(inventory_update.Quantity) - int(add_basket.Quantity)
        inventory_update.save()
        messages.success(request,'successfully added to bakset.')
        return redirect('scan_Qr',qr_code)

    if request.method == 'POST' and 'addSingles' in request.POST:
        singleQuantity = request.POST.get('Quantity')
        updateInventory = InventoryModel.objects.get(Qr_Code = qr_code)
        updateInventory.Quantity = int(updateInventory.Quantity) + int(singleQuantity)
        updateInventory.save()
        messages.success(request,'Inventory Updated.')
        return redirect('scan_Qr',qr_code)

    if request.method == 'POST' and 'addBulk' in request.POST:
        bulkQuantity = request.POST.get('bulkQuantity')
        boxesCheck = request.POST.get('numberBoxes')
        grandTotal = int(bulkQuantity) * int(boxesCheck)
        bulkInventory = InventoryModel.objects.get(Qr_Code = qr_code)
        bulkInventory.Quantity = int(bulkInventory.Quantity) + int(grandTotal)
        bulkInventory.save()
        messages.success(request,'Inventory Updated.')
        return redirect('scan_Qr',qr_code)



    context = {
        "inventory_data" : inventory_data,
        "basket_count" : basket_count
    }

    return render(request,'client/scanQr_code.html',context)

def Transactions(request):
    history_data = CompleteOrder.objects.all().order_by('-date_created')

    # Search Medication history Inventory 
    if request.method == 'POST' and 'search' in request.POST:
        searchInput = request.POST.get('search_input')
        history_data = history_data.filter(Medication_ID__Medication_Name__icontains = searchInput)

        # medication_data = InventoryModel.objects.filter(Medication_Name__icontains = searchInput)

    # Filter medication history Inventory 
    if request.method == 'POST' and 'filter_lowInventory' in request.POST:
        low_High = request.POST.get('low-high')
        high_low = request.POST.get('high-low') 
        dateFilter = request.POST.get('dateInput')

        if low_High:
            history_data = history_data.order_by("Quantity")

        if high_low:
            history_data = history_data.order_by("-Quantity")

        if dateFilter:
            history_data = history_data.filter(dateField = dateFilter)


    context = {
        "history_data" : history_data
    }

    return render(request,'client/transactions.html',context)

def MedicationList(request):
    medication_data = InventoryModel.objects.all().order_by("-date_created") 

    # hero component counts 
    inventoryCount = InventoryModel.objects.count()
    lowInventory_count = InventoryModel.objects.filter(Quantity__lte=F('ReStock_Level')).count()
    shelf_inventory = InventoryModel.objects.filter(shelf = "Yes").count()

    # Search Medication Inventory 
    if request.method == 'POST' and 'search' in request.POST:
        searchInput = request.POST.get('search_input')
        medication_data = InventoryModel.objects.filter(Q(Medication_Name__icontains = searchInput) | Q(Qr_Code__icontains = searchInput))

    # Filter medication Inventory 
    if request.method == 'POST' and 'filter_lowInventory' in request.POST:
        low_High = request.POST.get('low-high')
        high_low = request.POST.get('high-low')
        shelf_filter = request.POST.get('shelf')

        if low_High:
            medication_data = medication_data.order_by("Quantity")

        if high_low:
            medication_data = medication_data.order_by("-Quantity")

        if shelf_filter:
            medication_data =  medication_data.filter(shelf = "Yes")


    context = {
        "medication_data" : medication_data,
        "inventoryCount" : inventoryCount,
        "lowInventory_count" : lowInventory_count,
        "shelf_inventory" : shelf_inventory,
    }

    return render(request,'client/medication_list.html',context)

def MedicationDetails(request, item_id ):
    medication = InventoryModel.objects.get(id = item_id)
    basket_count = MedicationBasket.objects.all().count()

    if request.method == 'POST' and 'update_Inventory' in request.POST:
        update_data = InventoryModel.objects.get(id = item_id)
        update_data.Medication_Name = request.POST.get('medicationName')
        update_data.Description = request.POST.get('description')
        update_data.Medication_Size = request.POST.get('size')
        update_data.ReStock_Level = request.POST.get('restock_level')
        messages.success(request,'Inventory Updated')
        return redirect('inventory_details',item_id )

    if request.method == 'POST' and 'update-quantity' in request.POST:
        update_quantity = InventoryModel.objects.get(id = item_id)
        inStock = update_quantity.Quantity
        quantityUpdate = request.POST.get('quantityUPdate')
        # save Update 
        update_quantity.Quantity = int(inStock) + int(quantityUpdate)
        update_quantity.save()
        messages.success(request,'Inventory Updated')
        return redirect('inventory_details',item_id )

    if request.method == 'POST' and 'addBasket' in request.POST:
        basketQuantity = request.POST.get('Quantity')
        # update item quantity 
        update_quantity = InventoryModel.objects.get(id = item_id)
        update_quantity.Quantity = int(update_quantity.Quantity) - int(basketQuantity)
        update_quantity.save()

        # add to basket 
        item_ID = InventoryModel.objects.get(id = item_id)
        add_basket = MedicationBasket()
        add_basket.Medication_ID = item_ID
        add_basket.Quantity = int(basketQuantity)
        add_basket.save()
        messages.success(request,'Inventory added to basket')
        return redirect('inventory_details',item_id )

    if request.method == 'POST' and 'deleteStock' in request.POST:
        Iventory_Item = InventoryModel.objects.get(id = item_id)
        Iventory_Item.delete()
        messages.success(request,'Inventory item deleted')
        return redirect('inventory' )

    context = {
        "medication" : medication,
        "basket_count" : basket_count
    } 
    return render(request,'client/medication_details.html',context)

def Basket(request):
    basket_data = MedicationBasket.objects.all()
    basket_count = MedicationBasket.objects.count()

    if request.method == 'POST' and 'remove_basket' in request.POST:
        item_ID = request.POST.get('item_ID')
        # update Inventory item 
        updateInventory = InventoryModel.objects.get(id = item_ID)
        basket_ID = request.POST.get('basket_ID')
        remove_Item = MedicationBasket.objects.get(id = basket_ID)

        updateInventory.Quantity = int(updateInventory.Quantity) + int(remove_Item.Quantity)
        updateInventory.save()
        # Remove Item from basket 
        remove_Item.delete()
        messages.success(request,updateInventory.Medication_Name + ' removed from basket.')

        return redirect('basket' )

    if request.method == 'POST' and 'confirm_order' in request.POST:
        basket_data = MedicationBasket.objects.all()
        today = datetime.today()
        for i in basket_data:
            complete_data = CompleteOrder()
            complete_data.Medication_ID = InventoryModel.objects.get(id = i.Medication_ID.id)
            complete_data.Quantity = i.Quantity
            complete_data.month = today.strftime("%B")
            complete_data.year = today.strftime("%Y")
            complete_data.save()
            print('Complete Order')

            # update Shelf
            update_shelf = InventoryModel.objects.get(id = i.Medication_ID.id)
            update_shelf.shelf = "No"
            update_shelf.save()
            print('updated shelf')

            # delete from Basket 
            deleteItem = MedicationBasket.objects.get(id = i.id)
            deleteItem.delete()
        messages.success(request,'ORDER COMPLETE')
        return redirect('basket' )

    context = {
        "basket_data" : basket_data,
        "basket_count" : basket_count
    }
    return render(request,'client/basket.html',context)

def AddNotes(request):

    if request.method == 'POST' and 'add-note' in request.POST:
        title = request.POST.get('title')
        note = request.POST.get('notes')
        print(title)
        print(note)
    return render(request,'client/add_note.html')

def ScannerJs(request):
    inventory_data = InventoryModel.objects.all()

    context = {
        "inventory_data" : inventory_data
    }
    return render(request,'client/scanner.html',context)

def Labels(request):
    medication_data = InventoryModel.objects.all().order_by("-date_created") 

    # Search Medication Inventory 
    if request.method == 'POST' and 'search' in request.POST:
        searchInput = request.POST.get('search_input')
        medication_data = InventoryModel.objects.filter(Q(Medication_Name__icontains = searchInput) | Q(Qr_Code__icontains = searchInput))

    context = {
        "medication_data": medication_data
    }
    return render(request,'client/sticker_list.html',context)

def ViewLabel(request,item_id):
    label = InventoryModel.objects.get(id = item_id)

    if request.method == 'POST' and 'createLabel' in request.POST:

        Inventory_ID = InventoryModel.objects.get(id = item_id)

        if MedicationLabel.objects.filter(Medication_ID = Inventory_ID).exists():
            saveLabel = MedicationLabel.objects.get(Medication_ID = Inventory_ID)
            saveLabel.Medication_ID = InventoryModel.objects.get(id = item_id) 
            saveLabel.Take = request.POST.get('Take')
            saveLabel.Times = request.POST.get('Times')
            saveLabel.Hours = request.POST.get('Hours')
            saveLabel.ExpireDate = request.POST.get('ExpireDate')
            saveLabel.before = request.POST.get('before')
            saveLabel.after = request.POST.get('after')
            saveLabel.label = "Yes"
            saveLabel.save()
            label_ID = MedicationLabel.objects.get(id = saveLabel.id)
            print("updated")
            return redirect('create-pdf',label_ID.id )
        else: 
            saveLabel = MedicationLabel()
            saveLabel.Medication_ID = InventoryModel.objects.get(id = item_id) 
            saveLabel.Take = request.POST.get('Take')
            saveLabel.Times = request.POST.get('Times')
            saveLabel.Hours = request.POST.get('Hours')
            saveLabel.ExpireDate = request.POST.get('ExpireDate')
            saveLabel.before = request.POST.get('before')
            saveLabel.after = request.POST.get('after')
            saveLabel.label = "Yes"
            saveLabel.save()
            label_ID = MedicationLabel.objects.get(id = saveLabel.id)
            print("created")
            return redirect('create-pdf',label_ID.id )
        
        
    
    context = {
        "label" : label,
    }
    return render(request,'client/label_view.html',context)

def TeamMembers(request):
    return render(request,'client/team.html')

def CreatePdf(request,item_id):
    label = MedicationLabel.objects.get(id = item_id)
    logoImage = ClinicLogo.objects.all()[:1].get()

    context = {
        "label" : label,
        "logoImage" : logoImage
    }

    return render(request,'client/create_pdf.html',context)

    
    

    