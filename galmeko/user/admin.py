
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from hospital.forms import CustomHospitalCreationForm
from vendor.forms import CustomVendorCreationForm
from setting.forms import CustomVehicleCreationForm
from django.contrib.auth.models import Group
from .models import User, EmailTemplate
from django.core.mail import send_mail
from django.template import Context, Template
from hospital.models import Hospital
from vendor.models import Vendor
from setting.models import Vehicle
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy
from django.shortcuts import redirect, render
from .admin_view import get_vehicle_list, delete_vehicle, get_driver_list,GetUserDataByType,GetLatLongByAddress,add_booking
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django import forms


class MyAdminSite(admin.AdminSite):
    index_title = ugettext_lazy('Admin')

    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.

        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        self.site_title = ugettext_lazy('User')
        self.index_title = ugettext_lazy('Dashboard')
        self.site_header = ugettext_lazy('GLEMKO')

        script_name = request.META['SCRIPT_NAME']
        site_url = script_name if self.site_url == '/' and script_name else self.site_url
        return {
            'site_title': self.site_title,
            'site_header': self.site_header,
            'site_url': site_url,
            'has_permission': self.has_permission(request),
            'available_apps': self.get_app_list(request),
            'is_popup': False,
        }

    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()
        my_urls = [
            url('^get-vehicle/', self.admin_view(get_vehicle_list)),
            url('^delete_vehicle/', self.admin_view(delete_vehicle)),
            url('^get-driver/', self.admin_view(get_driver_list)),
            url('^get_user_data/', self.admin_view(GetUserDataByType)),
            url('^get_lat_long/', self.admin_view(GetLatLongByAddress)),
            path('add_booking/', self.admin_view(add_booking))
        ]
        return my_urls + urls


admin_site = MyAdminSite()


class HospitalInline(admin.TabularInline):
    model = Hospital
    form = CustomHospitalCreationForm


class VendorInline(admin.TabularInline):
    model = Vendor
    form = CustomVendorCreationForm


class VehicleInline(admin.TabularInline):
    extra = 1
    model = Vehicle
    form = CustomVehicleCreationForm


class UserAdmin(UserAdmin):
    inlines = [
        HospitalInline, VendorInline, VehicleInline
    ]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ('first_name', 'last_name', 'user_type',
                    'email', 'is_staff', 'is_active',)
    list_filter = ('status',)
    list_per_page = 5  # No of records per page
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone','password', 'type')}),
        # ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'is_staff', 'is_active', 'type')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
 
    def user_type(self, obj):
        get_type = User.objects.get(id=obj.id)
        user_type = get_type.type
        if user_type == 1:
            type = 'Hospital'
        elif user_type == 2:
            type = 'Vendor'
        elif user_type == 4:
            type = 'Admin'
        else:
            type = 'User'

        return type
        user_type.short_description = "Type"

    def save_model(self, request, obj, form, change):
        user_type = obj.type   # Type 4 = Admin ,1=Hospital ,2=Vendor ,3=User
        if user_type == 4:
            obj.is_active = 1
            obj.is_staff  = 1
        else:
            obj.is_active = 0
            obj.is_staff  = 0

        super().save_model(request, obj, form, change)
        if not change:
            sendTo = form.cleaned_data['email']
            name = form.cleaned_data['first_name'] + \
                ' ' + form.cleaned_data['last_name']
            password = form.cleaned_data['password1']
            msg_plain = 'Login Details ' + name + ' / ' + password
            getTemplate = EmailTemplate.objects.get(pk=1)
            templates = Template(getTemplate.template)
            context = Context(
                {
                    'name': sendTo,
                    'password': password,
                    'site_url': settings.SITE_BASE_URL,
                    'site_name': settings.SITE_NAME
                }
            )
            msg_html = templates.render(context)
            send_mail(
                'Registration Successfully.',
                msg_plain,
                settings.FROM_EMAIL,
                [sendTo],
                fail_silently=True,
                html_message=msg_html,
            )
        
admin_site.register(User, UserAdmin)
