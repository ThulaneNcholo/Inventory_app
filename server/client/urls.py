from .import views

# images urls 
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path

urlpatterns = [
    path('',views.IndexView,name='index'),
    path('add_Inventory',views.AddInventory,name='add_Inventory'),
    path('bulk_Inventory',views.BulkEntry,name='bulk_Inventory'),

    path('stock_out',views.StockOut,name='stock_out'),
    path('low_stock',views.LowStock,name='low_stock'),
    path('scan_Qr/<int:qr_code>',views.ScanQrCode,name='scan_Qr'),
    path('transactions',views.Transactions,name='transactions'),
    path('inventory',views.MedicationList,name='inventory'),
    path('inventory_details/<int:item_id>',views.MedicationDetails,name='inventory_details'),
    path('basket',views.Basket,name='basket'),
    path('scanner',views.ScannerJs,name='scanner'),
    path('labels',views.Labels,name='labels'),
    path('label/<int:item_id>',views.ViewLabel,name='label'),
    path('team',views.TeamMembers,name='team'),
    path('create-pdf/<int:item_id>',views.CreatePdf,name='create-pdf'),

    # Notes 
    path('notes',views.AddNotes,name='notes'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
