from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    CustomLoginView, CustomLogoutView, HomeView, create_business_profile, fetch_shop_details,
    profile_created, business_profile_list, get_shop_details, ShopListView, ShopCreateView,
    ShopUpdateView, ShopDeleteView, SaleListCreateView, submit_sale, get_employee_data,
    DayClosingView, day_closing_report, edit_day_closing, approve_day_closing, create_sale,
    success_view, sales_by_staff_item_service, sale_by_admin_service, sales_report,
    RoleListView, RoleCreateView, RoleDeleteView, employee_list, create_receipt_type,
    EmployeeCreateView, employee_edit, employee_delete, ExpenseTypeListView,
    create_expense_type, ExpenseTypeUpdateView, ExpenseTypeDeleteView,
    ReceiptTransactionListView, ReceiptTransactionUpdateView,
    ReceiptTransactionDeleteView, PaymentTransactionListView, PaymentTransactionCreateView,
    PaymentTransactionUpdateView, PaymentTransactionDeleteView, BankDepositListView,
    BankDepositCreateView, BankDepositUpdateView, BankDepositDeleteView, ServiceListView,
    ServiceCreateView, ServiceUpdateView, ServiceDeleteView, ProductListView, create_product,
    ProductUpdateView, ProductDeleteView, EmployeeTransactionListView, employee_transaction_create,
    EmployeeTransactionUpdateView, EmployeeTransactionDeleteView, DailySummaryListView,
    DailySummaryCreateView, DailySummaryUpdateView, DailySummaryDeleteView, RoleUpdateView, create_receipt_transaction, day_closing_admin
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('create-business-profile/', create_business_profile, name='create_business_profile'),
    path('fetch_shop_details/', fetch_shop_details, name='fetch_shop_details'),
    path('profile-created/', profile_created, name='profile_created'),
    path('business/', business_profile_list, name='business_profile_list'),
    path('get_shop_details/<str:name>/', get_shop_details, name='get_shop_details'),
    path('shop/', ShopListView.as_view(), name='shop_list'),
    path('shop/create/', ShopCreateView.as_view(), name='create_shop'),
    path('shop/update/<int:pk>/', ShopUpdateView.as_view(), name='update_shop'),
    path('shop/delete/<int:pk>/', ShopDeleteView.as_view(), name='delete_shop'),
   # path('sales/', SaleListCreateView.as_view(), name='sale-list-create'),
    path('sale/salesbystaff/', submit_sale, name='submit_sale'),
    path('get_employee_data/<int:employee_id>/', get_employee_data, name='get_employee_data'),
    path('dayclosing/admin/', day_closing_admin, name='dayclosing_admin'),
    path('sale/dayclosing/', DayClosingView, name='dayclosing'),
    path('sale/day-closing-report/', day_closing_report, name='day_closing_report'),
    path('sale/dayclosing/<int:pk>/edit/', edit_day_closing, name='edit_day_closing'),
    path('sale/day-closing-report/<int:dayclosing_id>/approve/', approve_day_closing, name='approve_day_closing'),
    path('sale/', create_sale, name='sales_by_admin_item_form'),
    path('sale/success/', success_view, name='success'),
    path('sale/sales-by-staff-item-service/', sales_by_staff_item_service, name='sales_by_staff_item_service'),
    path('sale/sales-by-admin-service', sale_by_admin_service, name='sales_by_admin_service'),
    path('sale/sales-report/', sales_report, name='sales_report'),
    path('role/', RoleListView.as_view(), name='role_list'),
    path('role/create/', RoleCreateView.as_view(), name='create_role'),
    path('role/update/<int:pk>/', RoleUpdateView.as_view(), name='update_role'),
    path('role/delete/<int:pk>/', RoleDeleteView.as_view(), name='delete_role'),
    path('employee/', employee_list, name='employee_list'),
    path('employee/create/', EmployeeCreateView.as_view(), name='create_employee'),
    path('employees/<int:pk>/edit/', employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', employee_delete, name='employee_delete'),
    path('expense-type/', ExpenseTypeListView.as_view(), name='expense_type_list'),
    path('expense-type/create/', create_expense_type, name='create_expense_type'),
    path('expense-type/<int:pk>/edit/', ExpenseTypeUpdateView.as_view(), name='edit_expense_type'),
    path('expense-type/<int:pk>/delete/', ExpenseTypeDeleteView.as_view(), name='delete_expense_type'),
    path('receipt-type/create/', create_receipt_type, name='create_receipt_type'),
    path('receipt-transaction/', ReceiptTransactionListView.as_view(), name='receipt_transaction_list'),
    path('receipt-transaction/create/', create_receipt_transaction, name='create_receipt_transaction'),
    path('receipt-transaction/update/<int:pk>/', ReceiptTransactionUpdateView.as_view(), name='update_receipt_transaction'),
    path('receipt-transaction/delete/<int:pk>/', ReceiptTransactionDeleteView.as_view(), name='delete_receipt_transaction'),
    path('payment-transaction/', PaymentTransactionListView.as_view(), name='payment_transaction_list'),
    path('payment-transaction/create/', PaymentTransactionCreateView.as_view(), name='create_payment_transaction'),
    path('payment-transaction/update/<int:pk>/', PaymentTransactionUpdateView.as_view(), name='update_payment_transaction'),
    path('payment-transaction/delete/<int:pk>/', PaymentTransactionDeleteView.as_view(), name='delete_payment_transaction'),
    path('bank-deposit/', BankDepositListView.as_view(), name='bank_deposit_list'),
    path('bank-deposit/create/', BankDepositCreateView.as_view(), name='create_bank_deposit'),
    path('bank-deposit/update/<int:pk>/', BankDepositUpdateView.as_view(), name='update_bank_deposit'),
    path('bank-deposit/delete/<int:pk>/', BankDepositDeleteView.as_view(), name='delete_bank_deposit'),
    path('service/', ServiceListView.as_view(), name='service_list'),
    path('service/create/', ServiceCreateView.as_view(), name='create_service'),
    path('service/update/<int:pk>/', ServiceUpdateView.as_view(), name='update_service'),
    path('service/delete/<int:pk>/', ServiceDeleteView.as_view(), name='delete_service'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/create/', create_product, name='create_product'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('employee-transaction/', EmployeeTransactionListView.as_view(), name='employee_transaction_list'),
    path('employee-transaction/create/', employee_transaction_create, name='create_employee_transaction'),
    path('employee-transaction/update/<int:pk>/', EmployeeTransactionUpdateView.as_view(), name='update_employee_transaction'),
    path('employee-transaction/delete/<int:pk>/', EmployeeTransactionDeleteView.as_view(), name='delete_employee_transaction'),
    path('daily-summary/', DailySummaryListView.as_view(), name='daily_summary_list'),
    path('daily-summary/create/', DailySummaryCreateView.as_view(), name='create_daily_summary'),
    path('daily-summary/update/<int:pk>/', DailySummaryUpdateView.as_view(), name='update_daily_summary'),
    path('daily-summary/delete/<int:pk>/', DailySummaryDeleteView.as_view(), name='delete_daily_summary'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)