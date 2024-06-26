from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
import logging
from django.urls import reverse_lazy
from django.views import View
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, JsonResponse
import json
from django.db.models import Sum, Q, DecimalField, F
from django.db.models.functions import Coalesce, Cast
import jwt
import calendar
from itertools import chain
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.forms.models import ModelMultipleChoiceField
from decimal import Decimal
from django.http import HttpResponseNotFound
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.core.mail.backends.smtp import EmailBackend
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.forms import modelformset_factory
from .constants import NATIONALITIES 
from django.urls import reverse
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .serializers import LoginSerializer
from django.contrib.auth.views import LogoutView, LoginView
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from django.urls import get_resolver
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls.resolvers import RoutePattern
from .serializers import *
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.http import HttpResponseNotFound

####### admin cache clear

def clear_cache_admin(request):
    # Clear all cache keys
    cache.clear()
    return HttpResponse("Cache cleared successfully.")


# class SalesByStaffItemServiceViewSet(viewsets.ModelViewSet):
#     queryset = SalesByStaffItemService.objects.all()
#     serializer_class = SalesByStaffItemServiceSerializer


# class EmployeeViewSet(viewsets.ViewSet):
#     @action(detail=False, methods=['get'])
#     def list_employees(self, request):
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many=True)
#         return Response(serializer.data)

        
#     @action(detail=False, methods=['post'])
#     def logout(self, request):
#         # You can revoke the token here if needed
#         return JsonResponse({'message': 'Logged out successfully'})

#     @action(detail=False, methods=['get'])
#     def profile(self, request):
#         try:
#             # Extract employee_id from the JWT token
#             token = request.headers.get('Authorization').split(' ')[1]  # Assuming token is passed in the Authorization header
#             secretkey = 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTcxMDQ4OTM3NywiaWF0IjoxNzEwNDg5Mzc3fQ.HUVrXY6SIzuVoFmrrssoxunYOxFJVOPRi-vv0Py-6EY'
#             decoded_token = jwt.decode(token, secretkey, algorithms=['HS256'])
#             employee_id = decoded_token['employee_id']
            
#             # Fetch employee profile using employee_id
#             employee = get_object_or_404(Employee, id=employee_id)
#             serializer = EmployeeSerializer(employee)
#             return Response(serializer.data)
#         except jwt.ExpiredSignatureError:
#             return JsonResponse({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
#         except jwt.InvalidTokenError:
#             return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

#     @action(detail=False, methods=['get'])
#     def employee_dashboard(self, request):
#         try:
#             # Extract employee_id from the JWT token
#             token = request.headers.get('Authorization').split(' ')[1]  # Assuming token is passed in the Authorization header
#             secretkey = 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTcxMDQ4OTM3NywiaWF0IjoxNzEwNDg5Mzc3fQ.HUVrXY6SIzuVoFmrrssoxunYOxFJVOPRi-vv0Py-6EY'
#             decoded_token = jwt.decode(token, secretkey, algorithms=['HS256'])
#             employee_id = decoded_token['employee_id']
            
#             # Fetch employee data using employee_id
#             employee = get_object_or_404(Employee, pk=employee_id)

#             # Fetch other related data (business_profile, shop, etc.)
#             business_profile = BusinessProfile.objects.filter(name=employee.business_profile).first()
#             shop = Shop.objects.filter(name=business_profile.name).first()
            
#             # Fetch dashboard metrics
#             total_services = DayClosing.objects.filter(employee_id=employee_id).aggregate(total_services=Sum('total_services'))['total_services']
#             total_sales = DayClosing.objects.filter(employee_id=employee_id).aggregate(total_sales=Sum('total_sales'))['total_sales']
#             total_advance = DayClosing.objects.filter(employee_id=employee_id).aggregate(total_advance=Sum('advance'))['total_advance']

#             # Fetch chart data for the last 10 days
#             ten_days_ago = datetime.now() - timedelta(days=10)
#             day_closings = DayClosing.objects.filter(employee_id=employee_id, date__gte=ten_days_ago)

#             chart_data = [{
#                 'date': closing.date.strftime('%Y-%m-%d'),
#                 'total_services': float(closing.total_services),
#                 'total_sales': float(closing.total_sales),
#                 'advance': float(closing.advance)
#             } for closing in day_closings]

#             # Construct response context
#             context = {
#                 'employee': {
#                     'id': employee.id,
#                     'employee_id': employee.employee_id,
#                     'username': employee.username,
#                     # Add other fields as needed
#                 },
#                 'business_profile': {
#                     'name': business_profile.name,
#                     # Add other fields as needed
#                 },
#                 'shop': {
#                     'name': shop.name,
#                     # Add other fields as needed
#                 },
#                 'total_services': total_services,
#                 'total_sales': total_sales,
#                 'total_advance': total_advance,
#                 'chart_data': chart_data,
#             }
#             return JsonResponse(context)
#         except jwt.ExpiredSignatureError:
#             return JsonResponse({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
#         except jwt.InvalidTokenError:
#             return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class DayClosingViewSet(viewsets.ModelViewSet):
#     queryset = DayClosing.objects.all()
#     serializer_class = DayClosingSerializer


# class DayClosingViewSet(viewsets.ModelViewSet):
#     queryset = DayClosing.objects.all()
#     serializer_class = DayClosingSerializer
    

# class DailySummaryViewSet(viewsets.ModelViewSet):
#     queryset = DailySummary.objects.all()
#     serializer_class = DailySummarySerializer
    

def not_found_view(request, exception):
    return render(request, 'error.html', status=404)

def error_page(request):
    return render(request, 'error.html')

def error_404(request, exception):
    return render(request, 'error.html', status=404)

def error_500(request):
    return render(request, 'error.html', status=500)

class CustomUserAddView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'admin/auth/user/add_form.html'
    success_url = reverse_lazy('admin:index')  # Redirect to admin index after user creation

custom_user_add_view = CustomUserAddView.as_view()


#AdminUserForm = formset_factory(AdminUserForm, extra=1)


class CustomLoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '/home/'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            # Retrieve associated shop object using a related field
            shop = user.shop_admin.shop if hasattr(user, 'shop_admin') else None
            #print(shop)
            if shop:
                # Pass the shop ID to the session
                self.request.session['shop'] = shop.id
                # for key, value in self.request.session.items():
                #     print(f"{key}: {value}")
                #print(self.request.session['shop'])
                # Similarly, retrieve other related objects and pass their IDs to the session if needed
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid login credentials')
            return super().form_invalid(form)
        
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        # Clear all caches and sessions
        # Your cache clearing logic here

        # Clear session
        request.session.flush()

        # Logout user
        auth_logout(request)

        # Redirect to a desired URL after logout
        return redirect('login')

def reset_session_timeout(request):
    request.session.modified = True  # Update the session modification time
    return JsonResponse({'message': 'Session timeout reset successfully'})

# @login_required(login_url='login')
def sidebar(request):

    is_superuser = request.user.is_superuser
    is_admin = request.user.groups.filter(name='Admin').exists()
    is_employee = not is_superuser and not is_admin

    return render(request, 'sidebar.html', {'user': request.user, 'is_superuser': is_superuser, 'is_admin': is_admin, 'is_employee': is_employee})


class ShopListView(ListView):
    model = Shop
    template_name = 'shop_list.html'
    context_object_name = 'shops'

    def get_queryset(self):

        return Shop.objects.all().order_by('-name')

class ShopAdminCreateView(CreateView):
    model = User
    form_class = ShopAdminForm
    template_name = 'create_admin_user.html'
    success_url = '/home'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        shop = Shop.objects.create(name=user.username + "'s Shop", license_number="License-" + user.username)
        ShopAdmin.objects.create(user=user, shop=shop)
        return super().form_valid(form)

class ShopCreateView(CreateView):
    model = Shop
    form_class = ShopForm
    template_name = 'create_shop.html'
    success_url = '/login'

    def form_valid(self, form):
        shop = form.save(commit=False)
        admin_user = self.request.user
        if not ShopAdmin.objects.filter(user=admin_user).exists():
            ShopAdmin.objects.create(user=admin_user, shop=shop)
            return super().form_valid(form)
        else:
            # Only one shop can be created under each user
            return super().form_invalid(form)

class ShopUpdateView(UpdateView):
    model = Shop
    form_class = ShopForm
    template_name = 'update_shop.html'
    success_url = reverse_lazy('shop_list')

class ShopDeleteView(DeleteView):
    model = Shop
    template_name = 'delete_shop.html'
    success_url = reverse_lazy('shop_list')



# @method_decorator(login_required, name='dispatch')
class RoleListView(ListView):
    model = Role
    template_name = 'role_list.html'
    context_object_name = 'roles'  # Rename object_list to roles in the template

    def get_queryset(self):
        business_profile = self.get_business_profile()
        return Role.objects.filter(business_profile=business_profile)

    def get_business_profile(self):
        try:
            # Get the current shop admin
            try:
                shop_admin = ShopAdmin.objects.get(user=self.request.user)
            except ShopAdmin.DoesNotExist:
        # Redirect to the login page
                return redirect('login')
            # Get the associated shop
            shop = shop_admin.shop
            # Get the business profile associated with the shop
            business_profile = BusinessProfile.objects.get(name=shop.name)
            return business_profile
        except (ShopAdmin.DoesNotExist, BusinessProfile.DoesNotExist):
            return None
        

def create_role(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile
    
    if request.method == 'POST':
        role_name = request.POST.get('name')
        module_names = request.POST.getlist('modules')
        is_employee = request.POST.get('is_employee') == 'on'

        new_role = Role.objects.create(name=role_name, is_employee=is_employee, business_profile=business_profile)

        for module_name in module_names:
            module = Module.objects.get(name=module_name)
            new_role.modules.add(module)

        new_role.save()

        return redirect('role_list')
    else:
        modules = Module.objects.all()
        return render(request, 'create_role.html', {'modules': modules, 'business_profile': business_profile})




def analytics_view(request):

    total_employees = Employee.objects.all().count()

    total_revenue = DailySummary.objects.aggregate(total_revenue=Sum('amount'))['total_revenue']

    return render(request, 'home.html', {
        'total_employees': total_employees,
        'total_revenue': total_revenue,

    })



class RoleUpdateView(UpdateView):
    model = Role
    fields = "__all__"
    template_name = 'update_role.html'

    def form_valid(self, form):
        role = form.save(commit=False)
        role.business_profile = self.get_business_profile()
        role.save()  # Save the role after setting the business profile
        messages.success(self.request, 'Role updated successfully.')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        role_id = self.kwargs.get('pk')
        return get_object_or_404(Role, pk=role_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role_id = self.kwargs.get('pk')
        role = get_object_or_404(Role, pk=role_id)
        context['role'] = role
        context['modules'] = Module.objects.all()  # Pass all modules queryset
        context['business_profile'] = self.get_business_profile()
        return context

    def get_success_url(self):
        return reverse_lazy('role_list')  # Redirect to the role_list page
    
    def get_business_profile(self):
        # Get the current shop admin
        try:
            shop_admin = ShopAdmin.objects.get(user=self.request.user)
        except ShopAdmin.DoesNotExist:
        # Redirect to the login page
            return redirect('login')
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        return BusinessProfile.objects.get(name=shop.name)
    
class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'delete_role.html'
    success_url = reverse_lazy('role_list')

# @login_required(login_url='login')
def create_expense_type(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile

    if request.method == 'POST':
        form = ExpenseTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_type_list')
    else:
        form = ExpenseTypeForm()
    return render(request, 'create_expense_type.html', {'form': form})

# @login_required
def employee_list(request):
    # Get the shop admin user
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Get the shop associated with the shop admin
    shop = shop_admin.shop

    # Get the business profile associated with the shop
    business_profile = shop

    query = request.GET.get('q')
    if query:
        employees = Employee.objects.filter(
            Q(employee_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(second_name__icontains=query),
            business_profile=business_profile,
            # shop=shop
        )
    else:
        employees = Employee.objects.filter(business_profile=business_profile)

    paginator = Paginator(employees, 10)
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    return render(request, 'employee_list.html', {'employees': employees})
# @login_required
def create_employee(request):
    error_occurred = False  
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile

    # Fetch the shop details associated with the logged-in user
    try:
        shop_admin = ShopAdmin.objects.get(user=request.user)
        shop = shop_admin.shop
    except ShopAdmin.DoesNotExist:
        shop = None

    if shop:
        num_users = shop.num_users
        # Check the number of users created under this shop
        num_users_created = Employee.objects.filter(business_profile=shop).count()
        
        # Pass the maximum allowed users count to the template
        max_users_allowed = num_users
        # context = {
        #     'num_users_created': num_users_created,
        #     'max_users_allowed': max_users_allowed,
        #     'business_profile_id': shop.id  # Pass the business_profile_id to the template context
        # }
    business_profiles = BusinessProfile.objects.filter(name=shop)
    business_profile = get_object_or_404(BusinessProfile, name=shop)
        
        # Filter roles based on the business profile
    roles = Role.objects.filter(business_profile=business_profile)
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            if num_users_created >= max_users_allowed:
                # If the maximum limit is reached, display an error message
                error_occurred = True
                messages.error(request, "Max User Registration limit is reached.")
            else:
                try:
                    employee = form.save(commit=False)
                    employee.business_profile_id = request.POST.get('business_profile_id')  # Set business_profile_id from POST data
                    employee.save()
                    return redirect('employee_list') 
                except Exception as e:
                    # print("An error occurred while saving the form:", e)
                    error_occurred = True  
                    messages.error(request, "An error occurred while saving the form.")
    else:
        form = EmployeeForm()

    # Filter Business Profiles based on the shop associated with the logged-in user
    

    context = {
    'form': form,
    'roles':roles,
    'business_profiles': business_profiles,
    'error_occurred': error_occurred,
    'num_users_created': num_users_created,
    'max_users_allowed': max_users_allowed,
    'business_profile_id': shop.id,
    'nationalities': NATIONALITIES,  # Pass NATIONALITIES to the template context
    }

    return render(request, 'create_employee.html', context)


def check_username_availability(request):
    username = request.GET.get('username')
    if Employee.objects.filter(username=username).exists():
        available = False
    else:
        available = True
    return JsonResponse({'available': available})

def get_employee_data(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    data = {
        'total_services': employee.total_services,
        'total_sales': employee.total_sales,
    }
    return JsonResponse(data)

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_edit.html', {'form': form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_delete.html', {'employee': employee})


@csrf_protect
def employee_login(request):
    error_message = None  # Initialize error_message variable
    
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                employee = Employee.objects.get(username=username)
            except Employee.DoesNotExist:
                employee = None
            
            if employee is not None and employee.password == password:
                request.session['employee_id'] = employee.pk
                return redirect('employee_dashboard')
            else:
                error_message = "Invalid username or password."  # Set error message
    else:
        form = EmployeeLoginForm()
    
    return render(request, 'employee_login.html', {'form': form, 'error_message': error_message})

def employee_logout(request):
    # Remove employee_id from the session if it exists
    if 'employee_id' in request.session:
        del request.session['employee_id']
    
    # Redirect to the login page after logout
    response = redirect('employee_login')
    
    # Clear localStorage session using JavaScript
    response.content = """
    <script>
        localStorage.clear();
    </script>
    """
    
    return response

def employee_dashboard(request):
    # Get the employee_id from the session
    employee_id = request.session.get('employee_id')
    
    # Fetch the employee object using the employee_id
    employee = get_object_or_404(Employee, pk=employee_id)

    # Fetch the associated BusinessProfile for the employee
    business_profile = BusinessProfile.objects.filter(name=employee.business_profile).first()
    
    # Fetch the associated Shop for the employee
    shop = Shop.objects.filter(name=business_profile.name).first()
    
    # Get the current month and year
    current_month = timezone.now().month
    current_year = timezone.now().year

    # Get the first and last day of the current month
    first_day_of_month = timezone.datetime(current_year, current_month, 1)
    last_day_of_month = timezone.datetime(current_year, current_month, calendar.monthrange(current_year, current_month)[1])

    # Aggregate total services, total sales, and total advance for the current month
    day_closings = DayClosing.objects.filter(employee_id=employee_id, date__gte=first_day_of_month, date__lte=last_day_of_month)

    # If job_role exists, filter roles based on it
    role = Role.objects.filter(name=employee.job_role).first()
      
    # Get active modules based on the filtered role
    active_modules = role.modules.all()
  
    # Check if day_closings is not empty
    if day_closings.exists():
        total_services = day_closings.aggregate(total_services=Sum('total_services'))['total_services'] or 0
        total_sales = day_closings.aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0
    # Ensure that advance is converted to a float only if it's not None
        total_advance = sum(float(closing.advance) for closing in day_closings if closing.advance is not None)
        print(total_advance)
    else:
    # If day_closings is empty, set totals to 0
        total_services = 0
        total_sales = 0
        total_advance = 0
    # Commission calculation
    if employee and employee.commission_percentage:
        com_cal = employee.commission_percentage / 100
    else:
        com_cal = 0

    # Check if total_services and total_sales are not None
    if total_services is not None and total_sales is not None:
        commission = (total_services + total_sales) * com_cal
    else:
        commission = 0  # Set commission to 0 if total_services or total_sales is None

    # Prepare data for the chart
    chart_data = [{
        'date': closing.date.strftime('%Y-%m-%d'),
        'total_services': float(closing.total_services),
        'total_sales': float(closing.total_sales),
        'total_advance': float(closing.advance) if closing.advance is not None else 0,
        
    } for closing in day_closings]

    # Convert data to JSON format
    chart_data_json = json.dumps(chart_data)
    
    context = {
        'employee': employee,
        'business_profile': business_profile,
        'shop': shop,
        'total_services': total_services,
        'total_sales': total_sales,
        'total_advance': total_advance,
        'commission': commission,
        'chart_data_json': chart_data_json,
        'active_modules': active_modules,
    }
    return render(request, 'employee_dashboard.html', context)


def employee_profile(request):
    # Retrieve employee ID from session
    employee_id = request.session.get('employee_id')
    
    # Fetch employee details
    employee = get_object_or_404(Employee, id=employee_id)
     # If job_role exists, filter roles based on it
    role = Role.objects.filter(name=employee.job_role).first()
      
    # Get active modules based on the filtered role
    active_modules = role.modules.all()
  
    context = {
        'employee': employee,
        'active_modules': active_modules,
    }
    return render(request, 'employee_profile.html', context)

class ExpenseTypeListView(ListView):
    model = ExpenseType
    template_name = 'expense_type_list.html'
    def get_queryset(self):
        # Return the queryset of DailySummary objects sorted by date in ascending order
        return ExpenseType.objects.order_by('-created_on')
class ExpenseTypeUpdateView(UpdateView):
    model = ExpenseType
    form_class = ExpenseTypeForm
    template_name = 'update_expense_type.html'
    success_url = reverse_lazy('expense_type_list')

class ExpenseTypeDeleteView(DeleteView):
    model = ExpenseType
    template_name = 'delete_expense_type.html'
    success_url = reverse_lazy('expense_type_list')

class ReceiptTransactionListView(ListView):
    model = ReceiptTransaction
    template_name = 'receipt_transaction_list.html'
    def get_queryset(self):
        # Return the queryset of DailySummary objects sorted by date in ascending order
        return ReceiptTransaction.objects.order_by('-created_on')

class ReceiptTypeListView(ListView):
    model = ReceiptType
    template_name = 'receipt_type_list.html'
    context_object_name = 'object_list'  # Define the name used in the template for the queryset
    success_url = reverse_lazy('receipt_type_list')

class ReceiptTransactionUpdateView(UpdateView):
    model = ReceiptTransaction
    form_class = ReceiptTransactionForm
    template_name = 'update_receipt_transaction.html'
    success_url = reverse_lazy('receipt_transaction_list')

class ReceiptTransactionDeleteView(DeleteView):
    model = ReceiptTransaction
    template_name = 'delete_receipt_transaction.html'
    success_url = reverse_lazy('receipt_transaction_list')

class PaymentTransactionListView(ListView):
    model = PaymentTransaction
    template_name = 'payment_transaction_list.html'
    def get_queryset(self):
        # Return the queryset of DailySummary objects sorted by date in ascending order
        return PaymentTransaction.objects.order_by('-created_on')
    
class PaymentTransactionCreateView(CreateView):
    model = PaymentTransaction
    form_class = PaymentTransactionForm
    template_name = 'create_payment_transaction.html'
    success_url = reverse_lazy('payment_transaction_list')

    def dispatch(self, request, *args, **kwargs):
        try:
            # Get the current shop admin
            shop_admin = ShopAdmin.objects.get(user=request.user)
            # Get the associated shop
            shop = shop_admin.shop
            # Get the business profile associated with the shop
            self.business_profile = BusinessProfile.objects.get(name=shop.name)
        except BusinessProfile.DoesNotExist:
            messages.error(request, "Business profile is not created. Please create a business profile first.")
            return redirect('create_business_profile')  # Redirect to the view where you create a business profile
        return super().dispatch(request, *args, **kwargs)


class PaymentTransactionUpdateView(UpdateView):
    model = PaymentTransaction
    form_class = PaymentTransactionForm
    template_name = 'update_payment_transaction.html'
    success_url = reverse_lazy('payment_transaction_list')

class PaymentTransactionDeleteView(DeleteView):
    model = PaymentTransaction
    template_name = 'delete_payment_transaction.html'
    success_url = reverse_lazy('payment_transaction_list')

class BankDepositListView(ListView):
    model = BankDeposit
    template_name = 'bank_deposit_list.html'
    def get_queryset(self):
        # Return the queryset of DailySummary objects sorted by date in ascending order
        return BankDeposit.objects.order_by('-created_on')

def create_bank_deposit(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile
    
    if request.method == 'POST':
        form = BankDepositForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_deposit_list')  
    else:
        form = BankDepositForm()

    # Fetch all banks
    banks = Bank.objects.all()

    context = {
        'form': form,
        'banks': banks,  # Pass the banks to the context
    }
    return render(request, 'create_bank_deposit.html', context)
class BankListView(ListView):
    model = Bank
    template_name = 'bank_list.html'
    def get_queryset(self):
        # Return the queryset of DailySummary objects sorted by date in ascending order
        return Bank.objects.order_by('-created_on')
    
def create_bank(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile
    
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_list')  
    else:
        form = BankForm()

    context = {
        'form': form,
    }
    return render(request, 'create_bank.html', context)

class BankDepositUpdateView(UpdateView):
    model = BankDeposit
    form_class = BankDepositForm
    template_name = 'update_bank_deposit.html'
    success_url = reverse_lazy('bank_deposit_list')

class BankDepositDeleteView(DeleteView):
    model = BankDeposit
    template_name = 'delete_bank_deposit.html'
    success_url = reverse_lazy('bank_deposit_list')

# @login_required
class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        # Retrieve the shop associated with the logged-in user
        try:
            try:
                shop_admin = ShopAdmin.objects.get(user=self.request.user)
            except ShopAdmin.DoesNotExist:
        # Redirect to the login page
                return redirect('login')
            shop = shop_admin.shop
            business = BusinessProfile.objects.get(license_number=shop.license_number)
        
        except AttributeError:
        #     # Handle cases where the user is not associated with a shop
            business = None
        
        # Filter services based on the retrieved shop
        queryset = Service.objects.filter(business_profile=business.id)
        return queryset
    
def create_service(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Get the shop associated with the shop admin
    shop = shop_admin.shop
    
    # Get the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            # Set the business profile for the service before saving
            service = form.save(commit=False)
            service.business_profile = business_profile.id
            service.save()
            return redirect('service_list')  
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form, 'business_profile': business_profile.id})


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'update_service.html'
    success_url = reverse_lazy('service_list')

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'delete_service.html'
    success_url = reverse_lazy('service_list')

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    
    context_object_name = 'product'

    def get_queryset(self):
        # Retrieve the shop associated with the logged-in user
        try:
            try:
                shop_admin = ShopAdmin.objects.get(user=self.request.user)
            except ShopAdmin.DoesNotExist:
        # Redirect to the login page
                return redirect('login')
            shop = shop_admin.shop
            business = BusinessProfile.objects.get(license_number=shop.license_number)
            #print("shop license:", shop.license_number)
            #print("business id:", business.id)
            #print("business license:", business.license_number)
        # try:
        #     # Assuming there's an intermediary model linking User and Shop
        #     shop_admin = user.shop_admin
        #     print("shop_admin =", shop_admin)
        #     shop = shop_admin.shop
        except AttributeError:
        #     # Handle cases where the user is not associated with a shop
            business = None
        
        # Filter services based on the retrieved shop
        queryset = Product.objects.filter(business_profile=business.id)
        return queryset
    
def create_product(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Get the shop associated with the shop admin
    shop = shop_admin.shop
    
    # Get the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
  
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Set the business profile for the product before saving
            product = form.save(commit=False)
            product.business_profile = business_profile.id
            product.save()
            return redirect('product_list')  
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form, 'business_profile': business_profile.id})

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('product_list')

def employee_transaction_create(request):
    if request.method == 'POST':
        form = EmployeeTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  
    else:
        form = EmployeeTransactionForm()
    return render(request, 'create_employee_transaction.html', {'form': form})

class EmployeeTransactionListView(ListView):
    model = EmployeeTransaction
    template_name = 'employee_transaction_list.html'
    def get_queryset(self):
        # Return the queryset of DailySummary objects sorted by date in ascending order
        return EmployeeTransaction.objects.order_by('-created_on')
    
class EmployeeTransactionCreateView(CreateView):
    model = EmployeeTransaction
    form_class = EmployeeTransactionForm
    template_name = 'create_employee_transaction.html'
    success_url = reverse_lazy('employee_transaction_list')

class EmployeeTransactionUpdateView(UpdateView):
    model = EmployeeTransaction
    form_class = EmployeeTransactionForm
    template_name = 'update_employee_transaction.html'
    success_url = reverse_lazy('employee_transaction_list')

class EmployeeTransactionDeleteView(DeleteView):
    model = EmployeeTransaction
    template_name = 'delete_employee_transaction.html'
    success_url = reverse_lazy('employee_transaction_list')

class DailySummaryListView(ListView):
    model = DailySummary
    template_name = 'daily_summary_list.html'

    def get_queryset(self):
        # Return the queryset of DailySummary objects sorted by date in ascending order
        return DailySummary.objects.order_by('-created_on')
    
logger = logging.getLogger(__name__)


# @login_required
def DailySummaryCreate(request):
    if request.method == 'POST':
        form = DailySummaryForm(request.POST)
        if form.is_valid():
            daily_summary = form.save()
            # Pass the created daily_summary object to send_daily_summary_email function
            send_daily_summary_email(request, daily_summary)
            return redirect('daily_summary_list')
    else:
        last_daily_summary = DailySummary.objects.order_by('-date').first()
        if last_daily_summary:
            last_daily_summary_date = last_daily_summary.date
        else:
            # If no daily summaries exist, set last_daily_summary_date to a default value
            last_daily_summary_date = datetime.now().date() - timedelta(days=1)

        # Calculate the minimum date as last_daily_summary_date + 1 day
        min_date = last_daily_summary_date + timedelta(days=1)
        # Pass the minimum date to the form
        form = DailySummaryForm(initial={'min_date': min_date})

    return render(request, 'create_daily_summary.html', {'form': form})

def fetch_summary_data(request, date):
    # Initialize default values
    opening_balance = 0
    total_received_amount = 0
    total_expense_amount = 0
    total_bank_deposit = 0
    net_collection = 0
    balance = 0

    # Fetch the latest DailySummary for the selected date
    try:
        daily_summary = DailySummary.objects.filter(date=date).latest('created_on')
        opening_balance = daily_summary.opening_balance
    except DailySummary.DoesNotExist:
        pass

    # Fetch the DayClosingAdmin objects for the given date
    day_closing_admins = DayClosingAdmin.objects.filter(date=date)
    if day_closing_admins.exists():
        # If there are multiple DayClosingAdmin objects, take the latest one
        day_closing_admin = day_closing_admins.latest('created_on')
        net_collection = day_closing_admin.net_collection

    # Calculate total_received_amount from ReceiptTransactions
    receipt_transactions_total = ReceiptTransaction.objects.filter(date=date).aggregate(total_amount=Sum('received_amount'))['total_amount'] or 0
    total_received_amount = receipt_transactions_total + net_collection

    # Calculate total_bank_deposit from BankDeposit
    total_bank_deposit = BankDeposit.objects.filter(date=date).aggregate(amount=Sum('amount'))['amount'] or 0

    # Calculate total_expense_amount from PaymentTransactions
    payment_transactions_total = PaymentTransaction.objects.filter(date=date).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    total_expense_amount = payment_transactions_total

    # Calculate the balance
    balance = opening_balance + total_received_amount - total_expense_amount - total_bank_deposit

    # Construct data dictionary
    data = {
        'opening_balance': opening_balance,
        'net_collection': net_collection,
        'total_received_amount': total_received_amount,
        'total_expense_amount': total_expense_amount,
        'total_bank_deposit': total_bank_deposit,
        'balance': balance
    }

    return JsonResponse(data)

def send_daily_summary_email(request, daily_summary):
    try:
        # Construct HTML email content using the passed daily_summary object
        email_subject = 'Latest Daily Summary Data'
        email_html = render_to_string('daily_summary_email.html', {'daily_summary': daily_summary})
        email_text = strip_tags(email_html)

        # Send email to admin
        send_mail(
            email_subject,
            email_text,
            'nazbeer.ahammed@gmail.com',  # Use sender email from settings
           # [settings.EMAIL_HOST_USER],  # Change this to your admin email address
           ['6598040e-ceb7-44ae-a975-e1630c4856e4@mailslurp.com'],
            html_message=email_html,
        )

        logger.info('Email sent successfully')  # Log success message
        messages.success(request, 'Email sent successfully')  # Add success message
    except Exception as e:
        logger.error(f'Failed to send email: {e}')  # Log error message
        messages.error(request, f'Failed to send email: {e}')  # Add error message
class DailySummaryUpdateView(UpdateView):
    model = DailySummary
    form_class = DailySummaryForm
    template_name = 'update_daily_summary.html'
    success_url = reverse_lazy('daily_summary_list')

class DailySummaryDeleteView(DeleteView):
    model = DailySummary
    template_name = 'delete_daily_summary.html'
    success_url = reverse_lazy('daily_summary_list')

def get_shop_details(request, name):
    try:
        shop = Shop.objects.get(name=name)

        return JsonResponse({
            'shop_name': shop.name,
            'license_number': shop.license_number,

        })
    except Shop.DoesNotExist:
        return JsonResponse({'error': 'Shop not found'}, status=404)
# @login_required
def create_business_profile(request):
    error_occurred = False  

    if request.method == 'POST':
        business_profile_form = BusinessProfileForm(request.POST, request.FILES)
        if business_profile_form.is_valid():
            business_profile = business_profile_form.save(commit=False)
            business_profile.save()
            return redirect('success')
        else:
            # Form is not valid, display form with errors
            messages.error(request, "Please correct the errors below.")
    else:
        business_profile_form = BusinessProfileForm()

    context = {'business_profile_form': business_profile_form}
    if request.user.is_authenticated:
        # Fetch the shop details associated with the logged-in user
        try:
            shop_admin = ShopAdmin.objects.get(user=request.user)
            shop_name = shop_admin.shop.name
            context['shop_details'] = shop_admin.shop
            context['license_number'] = shop_admin.shop.license_number

            # Check if a business profile already exists with the same name as shop name
            if BusinessProfile.objects.filter(name=shop_name).exists():
                context['disable_submit'] = True  # Disable submit button
                # messages.info(request, "Only one business profile can be created under a shop.")
        except ShopAdmin.DoesNotExist:
            context['shop_details'] = None
            context['license_number'] = None

    return render(request, 'create_business_profile.html', context)



def edit_business_profile(request, pk):
    business_profile = get_object_or_404(BusinessProfile, pk=pk)
    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, request.FILES, instance=business_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business profile updated successfully.')
            return redirect('business_profile_list')
    else:
        form = BusinessProfileForm(instance=business_profile)
    return render(request, 'edit_business_profile.html', {'form': form, 'business_profile': business_profile})

def delete_business_profile(request, pk):
    business_profile = get_object_or_404(BusinessProfile, pk=pk)
    if request.method == 'POST':
        business_profile.delete()
        messages.success(request, 'Business profile deleted successfully.')
        return redirect('business_profile_list')
    return render(request, 'delete_business_profile.html', {'business_profile': business_profile})

def fetch_shop_details(request):
    shop_id = request.GET.get('shop_id')
    if shop_id:
        try:
            shop = Shop.objects.get(pk=shop_id)
            #print(shop)

            data = {
                'license_number': '2455',

            }

            return JsonResponse(data)
        except Shop.DoesNotExist:
            return JsonResponse({'error': 'Shop not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

def business_profile_list(request):
    context = {}
    if request.user.is_authenticated:
        try:
            # Fetch the shop details associated with the logged-in user
            shop_admin = ShopAdmin.objects.get(user=request.user)
            shop_name = shop_admin.shop.name
            
            # Filter Business Profiles based on the logged-in user's shop name
            profiles = BusinessProfile.objects.filter(name=shop_name)
            context['profiles'] = profiles
            context['shop_details'] = shop_admin.shop
            context['license_number'] = shop_admin.shop.license_number
        except ShopAdmin.DoesNotExist:
            context['profiles'] = None
            context['shop_details'] = None
            context['license_number'] = None
    else:
        # If user is not authenticated, set profiles to None
        context['profiles'] = None

    return render(request, 'business_profile_list.html', context)


def profile_created(request):
    return render(request, 'profile_created.html')

def success_view(request):
    return render(request, 'success.html')

@cache_control(max_age=18000)  # 5 hours in seconds
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.POST)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Invalid login credentials, display error message
                messages.error(request, 'Invalid username or password. Please try again.')
                return redirect('login')
    else:
        serializer = LoginSerializer()

    return render(request, 'login.html', {'serializer': serializer})

def sales_by_admin_item(request):
    # Get the business profile associated with the logged-in user
    
    try:
        shop_admin = ShopAdmin.objects.get(user=request.user)
        business_profile = BusinessProfile.objects.get(name=shop_admin.shop.name)
        # print(business_profile)
        employees = Employee.objects.filter(business_profile=shop_admin.shop)
        
        products = Product.objects.filter(business_profile=business_profile.id)
        # print(products)
    except (ShopAdmin.DoesNotExist, BusinessProfile.DoesNotExist):
        employees = Employee.objects.none()
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile
    

    if request.method == 'POST':
        form = SalesByAdminItemForm(request.POST)
        if form.is_valid():
            form = form.save()
            # return HttpResponse(f'Sale created successfully')  
            return redirect('sales_report_admin')
    else:
        form = SalesByAdminItemForm()

    return render(request, 'sales_by_admin_item.html', {'form': form, 'employees': employees, 'products': products})


def sale_by_admin_service(request):
    try:
        shop_admin = ShopAdmin.objects.get(user=request.user)
        business_profile = BusinessProfile.objects.get(name=shop_admin.shop.name)
        # print(business_profile)
        employees = Employee.objects.filter(business_profile=shop_admin.shop)

        services = Service.objects.filter(business_profile=business_profile.id)
    except (ShopAdmin.DoesNotExist, BusinessProfile.DoesNotExist):
        employees = Employee.objects.none()
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile
    
    if request.method == 'POST':
        sales_form = SaleByAdminServiceForm(request.POST)
        if sales_form.is_valid():
            sales_form = sales_form.save(commit=False)
            # sales_form.itemtotal = request.POST['itemTotal']
            # sales_form.servicetotal = request.POST['serviceTotal']
            sales_form.save()
            return redirect('sales_report_admin')
    else:
        sales_form = SaleByAdminServiceForm()

    return render(request, 'sales_by_admin_service.html', {'sales_form': sales_form, 'services': services, 'employees':employees})

# class SaleListCreateView(generics.ListCreateAPIView):
#     queryset = Sale.objects.all()
#     serializer_class = SaleSerializer

def submit_sale(request):
    employee_id = request.session.get('employee_id')
    employees = Employee.objects.get(id=employee_id)
    # print(employees.id)
      
    role = Role.objects.filter(name=employees.job_role).first()
            
    # Get active modules based on the filtered role
    active_modules = role.modules.all()
    
    
        # business_profile = employee.business_profile_id.businessprofile_set.first()
    # business_profile = BusinessProfile.objects.get(id=employees.id)
    # print("BP: ", business_profile)
    # except Employee.DoesNotExist:
    #     # Handle the case where the employee does not exist
    #     # You might want to redirect the user or show an error message
    #     return render(request, 'error.html')

    # Retrieve products based on the employee's business profile
    if employees:
        services = Service.objects.filter(business_profile=employees.business_profile_id)
    else:
        # Handle the case where there's no business profile associated with the employee
        # You might want to redirect the user or show an error message
        return render(request, 'error.html')
    

    if request.method == 'POST':
        sales_form = SalesByStaffServiceForm(request.POST)
        if sales_form.is_valid():
            sales_form = sales_form.save(commit=False)
            # sales_form.itemtotal = request.POST['itemTotal']
            # sales_form.servicetotal = request.POST['serviceTotal']
            sales_form.save()
            return redirect('sales_report')
    else:
        sales_form = SalesByStaffServiceForm()

    return render(request, 'sales-by-staff-service.html', {'sales_form': sales_form, 'services': services,'employees':employees, 'active_modules':active_modules})

# @login_required

def DayClosingCreate(request):
    # Retrieve the logged-in employee's ID from the session
    employee_id = request.session.get('employee_id')
    
    # Fetch the employee object using the employee_id
    employees = get_object_or_404(Employee, pk=employee_id)

    # Fetch the associated BusinessProfile for the employee
    business_profile = BusinessProfile.objects.filter(name=employees.business_profile).first()
    
    # Fetch the associated Shop for the employee
    shop = Shop.objects.filter(name=business_profile.name).first()
    role = Role.objects.filter(name=employees.job_role).first()
            
    # Get active modules based on the filtered role
    active_modules = role.modules.all()
    # context = {
    #     'employees': employees,
    #     'business_profile': business_profile,
    #     'shop': shop
    # }

    current_date = timezone.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        form = DayClosingForm(request.POST)
        if form.is_valid():
            day_closing = form.save(commit=False)
            
            # Assign the logged-in employee to the day closing object
            #day_closing.employee = logged_in_employee
            
            day_closing.save()  # Save the day closing object
            return redirect('day_closing_report')
    else:
        form = DayClosingForm()

    # Pass the logged-in employee to the template as a list
    #employees = logged_in_employee

    return render(request, 'dayclosing.html', {'current_date': current_date, 'form': form, 'employees':employees, 'active_modules':active_modules})


def fetch_data(request, employee_id):
    # Fetch data for the selected employee
    # Example: calculate total_services, total_sales, total_collection
    current_date = timezone.now().strftime('%Y-%m-%d')
    
    total_services = (SalesByStaffItemService.objects
                      .filter(employee_id=employee_id, date=current_date)
                      .aggregate(total_services=Sum('servicetotal'))['total_services'] or 0) + \
                     (SaleByStaffService.objects
                      .filter(employee_id=employee_id, date=current_date)
                      .aggregate(total_services=Sum('total_amount'))['total_services'] or 0)

    total_sales = (SalesByStaffItemService.objects
                   .filter(employee_id=employee_id, date=current_date)
                   .aggregate(total_sales=Sum('itemtotal'))['total_sales'] or 0) + \
                  (SaleByStaffItem.objects
                   .filter(employee_id=employee_id, date=current_date)
                   .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0) 
                   
    total_collection = total_sales + total_services 

    data = {
        'total_services': total_services,
        'total_sales': total_sales,
        'total_collection': total_collection
    }
    return JsonResponse(data)
    

def day_closing_admin(request):
    current_date = timezone.now().date()

    # Get the shop admin associated with the current user
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Get the shop associated with the shop admin
    shop = shop_admin.shop
    
    # Get the business profile associated with the shop
    business_profile = shop
    all_employees = Employee.objects.filter(business_profile=business_profile)

    # Get the list of employees who have completed day closing for the selected date
    employees_with_day_closing = all_employees.filter(dayclosing__date=current_date)

    # Exclude employees who have completed day closing for the selected date
    remaining_employees = all_employees.exclude(id__in=employees_with_day_closing.values_list('id', flat=True))

    if request.method == 'POST':
        form = DayClosingAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('day_closing_admin_report')
    else:
        form = DayClosingAdminForm(initial={'date': current_date.strftime('%Y-%m-%d')})  # Initialize with current date
    #print(current_date.strftime('%Y-%m-%d'))
    return render(request, 'dayclosing_admin.html', {'current_date': current_date, 'remaining_employees':remaining_employees,'form': form})
def fetch_data_admin(request, selected_date, employee_id):
    # Convert the employee_id to an integer
    employee_id = int(employee_id)
    #print("emp id", employee_id)
    # Fetch total services for the selected date and employee
    total_services = (
        SaleByAdminService.objects.filter(date=selected_date, employee_id=employee_id)
        .aggregate(total_services=Sum('total_amount'))['total_services'] or 0
    )
    total_services += (
        SalesByStaffItemService.objects.filter(date=selected_date, employee_id=employee_id)
        .aggregate(total_services=Sum('servicetotal'))['total_services'] or 0
    )
    total_services += (
        SaleByStaffService.objects.filter(date=selected_date, employee_id=employee_id)
        .aggregate(total_services=Sum('total_amount'))['total_services'] or 0
    )
    #print(total_services)
    # Fetch total sales for the selected date and employee
    total_sales = (
        SalesByAdminItem.objects.filter(date=selected_date, employee_id=employee_id)
        .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    )
    total_sales += (
        SalesByStaffItemService.objects.filter(date=selected_date, employee_id=employee_id)
        .aggregate(total_sales=Sum('itemtotal'))['total_sales'] or 0
    )
    total_sales += (
        SaleByStaffItem.objects.filter(date=selected_date, employee_id=employee_id)
        .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    )

    # Calculate total collection
    total_collection = total_sales + total_services

    # Fetch advance for the selected date
    advance = (
        DayClosing.objects.filter(date=selected_date)
        .aggregate(total_advance=Sum('advance'))['total_advance'] or 0
    )

    # Create a dictionary containing the fetched data
    data = {
        'total_services': total_services,
        'total_sales': total_sales,
        'total_collection': total_collection,
        'advance': advance
    }

    # Return the data as a JSON response
    return JsonResponse(data)

def fetch_remaining_employees(request, selected_date):
    # Get the shop admin associated with the current user
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Get the shop associated with the shop admin
    shop = shop_admin.shop
    
    # Get the business profile associated with the shop
    business_profile = shop

    # Get all employees associated with the business profile
    all_employees = Employee.objects.filter(business_profile=business_profile)

    # Get the list of employees who have completed day closing for the selected date
    employees_with_day_closing = DayClosingAdmin.objects.filter(date=selected_date).values_list('employee', flat=True)

    # Filter employees who haven't done day closing on the selected date
    remaining_employees = all_employees.exclude(id__in=employees_with_day_closing)
    
    # #print('remaing:', remaining_employees)
    # Serialize remaining employees data
    
    if not remaining_employees:
        # If there are no remaining employees, return a custom message
        return JsonResponse({'message': 'Day Closing for all employees is completed'})

    # Serialize remaining employees data
    serialized_data = [{'id': emp.id, 'first_name': emp.first_name, 'second_name': emp.second_name} for emp in remaining_employees]

    # Return the serialized data as a JSON response
    return JsonResponse({'remaining_employees': serialized_data})


def edit_day_closing(request, pk):
    day_closing = get_object_or_404(DayClosing, pk=pk)
    employees = Employee.objects.all()
    status_choices = STATUS_CHOICES 
    if request.method == 'POST':
        form = DayClosingForm(request.POST, instance=day_closing)
        if form.is_valid():
            form.save()
            return redirect('day_closing_report')  
    else:
        form = DayClosingForm(instance=day_closing)
    
    return render(request, 'dayclosing_edit.html', {'form': form, 'employees': employees, 'status_choices': status_choices })

def day_closing_report(request):
    # Retrieve the logged-in employee's ID from the session or local storage
    logged_in_employee_id = request.session.get('employee_id')  # If using session
    # logged_in_employee_id = localStorage.getItem('employee_id')  # If using local storage in JavaScript

    # Filter the DayClosing queryset to get only the day closings associated with the logged-in employee
    day_closings_list = DayClosing.objects.filter(employee__id=logged_in_employee_id).order_by('-created_on')
    employees = Employee.objects.get(id=logged_in_employee_id)
    # #print(employees.id)
      
    role = Role.objects.filter(name=employees.job_role).first()
            
    # Get active modules based on the filtered role
    active_modules = role.modules.all()

    # Paginate the day closings list
    paginator = Paginator(day_closings_list, 10)
    page = request.GET.get('page')

    try:
        day_closings = paginator.page(page)
    except PageNotAnInteger:
        day_closings = paginator.page(1)
    except EmptyPage:
        day_closings = paginator.page(paginator.num_pages)

    return render(request, 'day_closing_report.html', {'day_closings': day_closings, 'active_modules':active_modules})


def day_closing_admin_report(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Get the shop associated with the shop admin
    shop = shop_admin.shop
    
    # Get the business profile associated with the shop
    business_profile = shop

    # Get all employees associated with the business profile
    all_employees = Employee.objects.filter(business_profile=business_profile)
    
    # Get all day closings from DayClosing and DayClosingAdmin
    day_closings_list = DayClosing.objects.filter(employee__in=all_employees)
    day_closings_admin_list = DayClosingAdmin.objects.filter(employee__in=all_employees)

    # Combine the querysets
    day_closings = list(chain(day_closings_list, day_closings_admin_list))

    return render(request, 'day_closing_admin_report.html', {'day_closings': day_closings})



def approve_day_closing(request, dayclosing_id):
    dayclosing = DayClosing.objects.get(pk=dayclosing_id)
    dayclosingadmin = DayClosingAdmin.objects.get(pk=dayclosing_id)
    dayclosing.status = 'approved'
    dayclosingadmin.status = 'approved'
    dayclosing.save()
    dayclosingadmin.save()
    return redirect('day_closing_report')

def error_view(request):
    # Your condition to choose between base.html and emp_base.html
    use_emp_base = True  # Example condition, replace it with your actual condition

    # Render the error.html template with the chosen base template
    return render(request, 'error.html', {'use_emp_base': use_emp_base})

def handler404(request, exception):
    # Call error_view with 404 condition
    return error_view(request)
def sales_by_staff_item(request):
    employee_id = request.session.get('employee_id')
    
    # Retrieve the employee
    # try:
    employee = Employee.objects.get(id=employee_id)
    role = Role.objects.filter(name=employee.job_role).first()
    # #print("Role:", role)
            
    # Get active modules based on the filtered role
    active_modules = role.modules.all()
    # #print("Active Modules:", active_modules)
    
    # Retrieve products based on the employee's business profile
    if employee:
        products = Product.objects.filter(business_profile=employee.business_profile_id)
    else:
        # Handle the case where there's no business profile associated with the employee
        # You might want to redirect the user or show an error message
        return render(request, 'error.html')
    # print(products)
    if request.method == 'POST':
        sales_form = SaleByStaffItemForm(request.POST)
        if sales_form.is_valid():
            sales_form = sales_form.save(commit=False)
            # sales_form.itemtotal = request.POST['itemTotal']
            # sales_form.servicetotal = request.POST['serviceTotal']
            sales_form.save()
            return redirect('sales_report')
    else:
        sales_form = SaleByStaffItemForm()

    return render(request, 'sales_by_staff_item.html', {'sales_form': sales_form, 'products': products, 'employee': employee, 'active_modules':active_modules})



def sales_by_staff_item_service(request):
    employee_id = request.session.get('employee_id')

    # Filter employees based on the retrieved employee ID
    employees = Employee.objects.get(id=employee_id)
    # print(employees.id)
    

    
    if employees:
        products = Product.objects.filter(business_profile=employees.business_profile_id)
        services = Service.objects.filter(business_profile=employees.business_profile_id)
    else:
       return render(request, 'error.html')
    role = Role.objects.filter(name=employees.job_role).first()
    # print("Role:", role)
            
    # Get active modules based on the filtered role
    active_modules = role.modules.all()
    # print("Active Modules:", active_modules)
    
    if request.method == 'POST':
        sales_form = SalesByStaffItemServiceForm(request.POST)
        if sales_form.is_valid():
            sales_form = sales_form.save(commit=False)
            # sales_form.itemtotal = request.POST['itemTotal']
            # sales_form.servicetotal = request.POST['serviceTotal']
            sales_form.save()
            return redirect('sales_report')
    else:
        sales_form = SalesByStaffItemServiceForm()

    return render(request, 'sales_by_staff_item_service.html', {'sales_form': sales_form, 'products': products, 'services': services, 'employees': employees,'active_modules':active_modules})


def sales_report(request):
    # Retrieve the logged-in employee's ID from the session
    logged_in_employee_id = request.session.get('employee_id') 

    # Query the sales data filtered by the logged-in employee's ID
    sales = SalesByStaffItemService.objects.filter(employee__id=logged_in_employee_id)
    sales_staff_service = SaleByStaffService.objects.filter(employee__id=logged_in_employee_id)
    sales_staff_item = SaleByStaffItem.objects.filter(employee__id=logged_in_employee_id)
    employees = Employee.objects.get(id=logged_in_employee_id)
    role = Role.objects.filter(name=employees.job_role).first()
    # print("Role:", role)
            
    # Get active modules based on the filtered role
    active_modules = role.modules.all()
    # print("Active Modules:", active_modules)
    
    # Pass the filtered sales data to the template
    context = {'sales': sales, 'sales_staff_service': sales_staff_service, 'sales_staff_item': sales_staff_item,'active_modules':active_modules}
    return render(request, 'sales_report.html', context)

def sales_report_admin(request):
    try:
        shop_admin = ShopAdmin.objects.get(user=request.user)
        shop = shop_admin.shop
        business = BusinessProfile.objects.get(license_number=shop.license_number)
        employees = Employee.objects.filter(business_profile=business)

        # Get all types of sales data
        sales_by_staff_item = SaleByStaffItem.objects.filter(employee__in=employees).select_related('employee', 'item')
        sales_by_staff_item_service = SalesByStaffItemService.objects.filter(employee__in=employees).select_related('employee')
        sales_by_staff_service = SaleByStaffService.objects.filter(employee__in=employees).select_related('employee', 'service')
        sales_by_admin_item = SalesByAdminItem.objects.filter(employee__in=employees).select_related('employee', 'item')
        sales_by_admin_service = SaleByAdminService.objects.filter(employee__in=employees).select_related('employee', 'service')

        # Combine sales data
        service_sales = [(sale, 'Staff') for sale in sales_by_staff_service] + [(sale, 'Admin') for sale in sales_by_admin_service]
        sales = [(sale, 'Admin') for sale in sales_by_admin_item] + [(sale, 'Staff') for sale in sales_by_staff_item]
        salesa = sales_by_staff_item_service
        
    except AttributeError:
        business = None
        employees = None
        service_sales = []
        sales = []
        salesa = []

    context = {
        'sales': sales,
        'salesa': salesa,
        'service_sales': service_sales,
    }
    return render(request, 'sales_report_admin.html', context)

def update_item_sales_data(request):
    try:
        shop_admin = ShopAdmin.objects.get(user=request.user)
        shop = shop_admin.shop
        business = BusinessProfile.objects.get(license_number=shop.license_number)
        employees = Employee.objects.filter(business_profile=business)
        sales = SalesByAdminItem.objects.filter(employee__in=employees).select_related('employee')
        #service_sales = SaleByAdminService.objects.filter(employee__in=employees).select_related('employee')
        # print("shop license:", shop.license_number)
        # print("business id:", business.id)
        # print("business license:", business.license_number)
        # print("sales", sales)
        # print("service_sales", service_sales)
    except AttributeError:
        business = None
        employees = None
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # print("start date: ", start_date)
    # Retrieve filtered item sales data based on the selected date range
    sales = SalesByAdminItem.objects.filter(date__range=[start_date, end_date]).values('date',
        'employee__id',
        'employee__employee_id',
        'employee__first_name',
        'employee__second_name',
        'item__name',
        'quantity',
        'price',
        'discount',
        'total_amount',
        'payment_method')
    # print(sales)
    return JsonResponse(list(sales), safe=False)

def update_service_sales_data(request):
    try:
        shop_admin = ShopAdmin.objects.get(user=request.user)
        shop = shop_admin.shop
        business = BusinessProfile.objects.get(license_number=shop.license_number)
        employees = Employee.objects.filter(business_profile=business)
        #sales = SalesByAdminItem.objects.filter(employee__in=employees).select_related('employee')
        service_sales = SaleByAdminService.objects.filter(employee__in=employees).select_related('employee')
    except AttributeError:
        business = None
        employees = None
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    #  print("start date service: ", start_date)
    # Retrieve filtered service sales data based on the selected date range
    service_sales = SaleByAdminService.objects.filter(date__range=[start_date, end_date]).values('date',
        'employee__id',
        'employee__employee_id',
        'employee__first_name',
        'employee__second_name',
        'service__name',
        'quantity',
        'price',
        'discount',
        'total_amount',
        'payment_method')
    # print(service_sales)
    return JsonResponse(list(service_sales), safe=False)

class ExportSalesReportAdminPDF(View):
    def get(self, request, *args, **kwargs):
        report_type = request.GET.get('report_type')

        if report_type == 'item':
            sales = SalesByAdminItem.objects.all()
            filename = 'sales_report_item.pdf'
        elif report_type == 'service':
            services = SaleByAdminService.objects.all()
            filename = 'sales_report_service.pdf'
        else:
            return HttpResponse('Invalid report type.')

        template_path = 'sales_report_pdf_template.html'
        context = {'sales': sales, 'services': services}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        template = get_template(template_path)
        html = template.render(context)

        # Create PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF creation error.')
        return response
    
def create_receipt_transaction(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile
    
    if request.method == 'POST':
        form = ReceiptTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receipt_transaction_list')  
    else:
        form = ReceiptTransactionForm()
    return render(request, 'create_receipt_transaction.html', {'form': form})

def create_receipt_type(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile
    
    if request.method == "POST":
        form = ReceiptTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_receipt_transaction')  
    else:
        form = ReceiptTypeForm()
    return render(request, 'create_receipt_type.html', {'form': form})

def license_expiration_reminder_due(license_expiration, reminder_days):
    return (license_expiration - timezone.now().date()).days <= reminder_days

def vat_submission_date_reminder_due(submission_dates, reminder_days):
    today = timezone.now().date()
    return any((date and (date - today).days <= reminder_days) for date in submission_dates)
# Notification view
def notification_view(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile

    notifications = []

    # Fetch the shop associated with the current user
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop

    # Get the associated BusinessProfile
    business_profile = BusinessProfile.objects.get(license_number=shop.license_number)
    business_profileID=business_profile.id
    # Check if all reminder flags are True for the shop
    if shop.vat_remainder and shop.employee_transaction_window \
            and shop.license_expiration_reminder \
            and shop.employee_visa_expiration_reminder :
            # and shop.employee_passport_expiration_reminder:

        # Get employees associated with the business profile
        employees = Employee.objects.filter(business_profile_id=business_profileID)

        # Check which reminder has the earliest due date
        earliest_due_date = None
        earliest_due_reminder = None

        if business_profile.vat_submission_date_reminder_due():
            earliest_due_date = business_profile.vat_submission_date_1
            earliest_due_reminder = 'VAT submission date'
        if business_profile.license_expiration_reminder_due():
            if earliest_due_date is None or earliest_due_date > business_profile.license_expiration:
                earliest_due_date = business_profile.license_expiration
                earliest_due_reminder = 'License expiration'
        if any(employee.id_expiration_due() for employee in employees):
            earliest_id_due_date = min([employee.id_expiration_date for employee in employees if employee.id_expiration_due()])
            if earliest_due_date is None or earliest_due_date > earliest_id_due_date:
                earliest_due_date = earliest_id_due_date
                earliest_due_reminder = 'Employee ID expiration'
        # if any(employee.passport_expiration_due() for employee in employees):
        #     earliest_passport_due_date = min([employee.passport_expiration_date for employee in employees if employee.passport_expiration_due()])
        #     if earliest_due_date is None or earliest_due_date > earliest_passport_due_date:
        #         earliest_due_date = earliest_passport_due_date
        #         earliest_due_reminder = 'Employee passport expiration'

        # If there's a due reminder, add it to the notifications
        if earliest_due_reminder:
            days_until_reminder = (earliest_due_date - timezone.now().date()).days
            notifications.append({
                'reminder_type': earliest_due_reminder,
                'expiration_date': earliest_due_date,
                'reminder_days': days_until_reminder,
                'employee_visa_reminder_days': business_profile.employee_visa_expiration_reminder_days
            })

    # Render the template with the notifications
    return render(request, 'notification_list.html', {'notifications': notifications})

def sidebar_emp(request):
    # Fetch employee ID from session
    employee_id = request.session.get('employee_id')
    #print("Employee ID from session:", employee_id)
    
    # Fetch employee details
    employee = get_object_or_404(Employee, pk=employee_id)
    #print("Employee Details:", employee)
    
    # Check if the employee has a job_role
    if employee.job_role:
        # If job_role exists, filter roles based on it
        role = Role.objects.filter(name=employee.job_role).first()
        #print("Role:", role)
        
        if role:
            # Get active modules based on the filtered role
            active_modules = role.modules.all()
            #print("Active Modules:", active_modules)
            
            context = {
                'active_modules': active_modules,
            }

            return render(request, 'emp_base.html', context)
        else:
            # Handle case where no role is found for the job_role
            return render(request, 'error.html', {'message': 'No role assigned for this job role.'})
    else:
        # Handle case where employee has no job_role assigned
        return render(request, 'error.html', {'message': 'No job role assigned to this employee.'})
    


def module_detail(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    return redirect(module.url)
 
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Fetch the shop details associated with the logged-in user
            try:
                try:
                    shop_admin = ShopAdmin.objects.get(user=self.request.user)
                except ShopAdmin.DoesNotExist:
    
                    return redirect('login')
                context['shop'] = shop_admin.shop
                
                # Get employees associated with the shop
                employees = Employee.objects.filter(business_profile=context['shop'])
                
                today = timezone.now()
                start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                next_month = start_of_month.replace(month=start_of_month.month + 1, day=1)
                end_of_month = next_month - timezone.timedelta(days=1)
                current_month_year = timezone.now().strftime("%B %Y") 
                total_services_all = 0
                total_sales_all = 0
                # Fetch day closings from both models using a Union query
                day_closings1 = DayClosing.objects.filter(
                    Q(date__range=[start_of_month, end_of_month]) & Q(employee__in=employees)
                ).annotate(
                    total_services_annotated=Cast('total_services', output_field=DecimalField()),
                    total_sales_annotated=Cast('total_sales', output_field=DecimalField()),
                    total_advance_annotated=Cast('advance', output_field=DecimalField())  # Assuming advance is a DecimalField
                ).values('date', 'employee', 'total_services_annotated', 'total_sales_annotated', 'total_advance_annotated')

                day_closings_admin = DayClosingAdmin.objects.filter(
                    Q(date__range=[start_of_month, end_of_month]) & Q(employee__in=employees)
                ).annotate(
                    total_services_annotated=Cast('total_services', output_field=DecimalField()),
                    total_sales_annotated=Cast('total_sales', output_field=DecimalField()),
                    total_advance_annotated=Cast('advance', output_field=DecimalField())  # Assuming advance is a DecimalField
                ).values('date', 'employee', 'total_services_annotated', 'total_sales_annotated', 'total_advance_annotated')
                # print(day_closings_admin)
                # Combine the two querysets using Union
                combined_day_closings = day_closings1.union(day_closings_admin)

                for closing in combined_day_closings:
                    # Extract relevant information from the closing
                    date = closing['date']
                    employee = closing['employee']
                    total_services = closing['total_services_annotated']
                    total_sales = closing['total_sales_annotated']
                    total_advance = closing['total_advance_annotated']

                    # Perform processing or actions with the extracted data
                    # For example, you can print the information
                    # print(f"Date: {date}, Employee: {employee}, Total Services: {total_services}, Total Sales: {total_sales}, Total Advance: {total_advance}")

                    # Or you can perform other operations, such as calculations or saving to another data structure
                    # For instance, you might aggregate the total services and total sales for all employees
                    total_services_all += total_services
                    total_sales_all += total_sales
                    
                # Optionally, you can pass the combined_day_closings queryset to the template context
                    context = {
                        'combined_day_closings': combined_day_closings,
                        'total_services_all': total_services_all,
                        'total_sales_all': total_sales_all,
                        # Other context data as needed
                    }
                # Fetch day closings for the current month
                day_closings = DayClosingAdmin.objects.filter(date__range=[start_of_month, end_of_month], employee__in=employees)
                
                # Calculate totals for services, sales, and advances for the current month
                total_services_this_month = day_closings.aggregate(total_services=Sum('total_services'))['total_services'] or 0
                total_sales_this_month = day_closings.aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0
                total_advance_given_this_month = day_closings.aggregate(total_advance=Sum('advance'))['total_advance'] or 0
                employee_totals = []
                for employee in employees:
                    employee_day_closings = DayClosingAdmin.objects.filter(date__range=[start_of_month, end_of_month], employee=employee)
                    employee_total_services = employee_day_closings.aggregate(total_services=Sum('total_services'))['total_services'] or Decimal(0)
                    employee_total_sales = employee_day_closings.aggregate(total_sales=Sum('total_sales'))['total_sales'] or Decimal(0)
                    employee_total_advance = employee_day_closings.aggregate(total_advance=Sum('advance'))['total_advance'] or Decimal(0)

                    # Fetching the first closing date of the employee
                    first_closing_date = employee_day_closings.order_by('date').first().date.strftime('%Y-%m-%d') if employee_day_closings.exists() else None

                    employee_totals.append({
                        'date': first_closing_date,
                        'employee': employee.id,
                        'employee_total_services': float(employee_total_services),
                        'employee_total_sales': float(employee_total_sales),
                        'employee_total_advance': float(employee_total_advance)
                    })

                # Prepare chart data
                chart_data_json = [{
                    'date': closing.date.strftime('%Y-%m-%d'),
                    'total_services': float(closing.total_services),
                    'total_sales': float(closing.total_sales),
                    'advance': float(closing.advance),
                } for closing in day_closings]

                # Add totals to the context
                context['total_services_this_month'] = total_services_this_month
                context['total_sales_this_month'] = total_sales_this_month
                context['total_advance_given_this_month'] = total_advance_given_this_month
                context['chart_data_json'] = json.dumps(chart_data_json)
                context['employee_json'] = json.dumps(employee_totals)
                context['employees'] = employees
                context['current_month_year'] = current_month_year
                # print(json.dumps(employee_totals))
            except ShopAdmin.DoesNotExist:
                context['shop'] = None
                context['total_services_this_month'] = 0
                context['total_sales_this_month'] = 0
                context['total_advance_given_this_month'] = 0
                context['chart_data_json'] = '[]'
                context['employee_json'] = '[]'
                context['current_month_year'] = current_month_year
                
        categories = [
            {
                'name': 'Shop Management',
                'links': [
                    {'label': 'Create Business', 'url_name': 'create_business_profile'},
                    {'label': 'Business Profiles', 'url_name': 'business_profile_list'},
                ]
            },
            {
                'name': 'Role Management',
                'links': [
                    {'label': 'Create Role', 'url_name': 'create_role'},
                    {'label': 'Role List', 'url_name': 'role_list'},
                   
                ]
            },
            {
                'name': 'Employee Management',
                'links': [
                        {'label': 'Create Employee', 'url_name': 'create_employee'},
                    {'label': 'Employee List', 'url_name': 'employee_list'},
                  
                ]
            },
        ]

        context['categories'] = categories
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login page if user is not logged in
            return redirect(reverse('login'))  # Adjust 'login' to your login URL name
        return super().dispatch(request, *args, **kwargs)