from django.contrib import admin
from .forms import BookingCreationForm
from booking.forms import CustomStopCreationForm, CustomBookingFeatureCreationForm, CustomBookingFeatureChangeForm, BookingChangeForm
from django.utils.html import format_html
from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy
from user.admin import admin_site
from booking.models import Booking, BookingStop, BookingFeature
from django.template.defaultfilters import truncatechars  # or truncatewords
from setting.models import Vehicle, VehicleCategory,Features


class StopInline(admin.TabularInline):
    template = 'admin/edit_inline/tabular_stop.html'
    extra = 1
    max_num = 7
    model = BookingStop
    fieldsets = [
        ('None', {'fields': (('name', 'phone','address','stop_geocode'),)}),
    ]
    form = CustomStopCreationForm

class BookingFeatureInline(admin.TabularInline):
    template = 'admin/edit_inline/tabular_booking_feature.html'
    extra = 1
    max_num = 1
    model = BookingFeature
    form = CustomBookingFeatureChangeForm
    add_form = CustomBookingFeatureCreationForm


class BookingAdmin(admin.ModelAdmin):
    change_list_template = 'admin/booking/change_list.html'
    inlines = [
        StopInline, BookingFeatureInline
    ]
    js = ("booking/js/booking.js",)
    form = BookingCreationForm
    form = BookingChangeForm
    add_form = BookingCreationForm
    model = Booking
    list_display = ('booking_type', 'source',
                    'destination', 'fare', 'round_trip','status','Action')
    fieldsets = [
        ('Booking For', {'fields': (('booking_type', 'user'),)}),
        ('Vehicle', {'fields': ('category', 'fare', 'round_trip','booking_msg')}),
        ("Trip Details", {'fields': (
            ('origin_name', 'origin_phone', 'origin_address', 'origin_geocode',"destination_name", "destination_phone",
                                    "destination_address", "destination_geocode"),), }),
    ]
    list_filter = ('round_trip',)
    list_per_page = 5
    search_fields = ('booking_type',)
    ordering = ('-id',)

    def Action(self, obj):
        edit = '<a class="button edit-icon" title="Edit" data-id="%s" href="edit/%s/"><i class="fa fa-edit" aria-hidden="true"></i></a>&nbsp;' % (
            obj.id, obj.id)
        return format_html(edit)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url('^add_booking/', self.add_booking),
            url('^edit/(?P<bookingId>\d+)/$', self.edit_view),
        ]
        return my_urls + urls
    
    def edit_view(self, request,bookingId):
        context_data = admin_site.each_context(request)
        context_data['site_title'] = ugettext_lazy('Booking')
        booking = Booking.objects.filter(status=1).get(id=bookingId)
        bookingStop = list(BookingStop.objects.filter(booking_id = bookingId))
        is_stop = 0
        if len(bookingStop) > 0:
            is_stop = len(bookingStop)
        bookingFeature = list(BookingFeature.objects.filter(booking_id = bookingId))
        context_data['data'] = {
            'category' : VehicleCategory.objects.filter(status=1),
            'feature_list' : Features.objects.filter(status=1),
            'stop' : bookingStop,
            'is_stop' : is_stop,
            'booking_feature' : bookingFeature,
            'data' : booking
        }
        return TemplateResponse(request, 'admin/booking/edit_booking.html', context=context_data)
    
    def add_booking(self, request):
        context_data = admin_site.each_context(request)
        context_data['site_title'] = ugettext_lazy('Booking')
        context_data['features'] = Features.objects.filter(status=1)
        context_data['category'] = VehicleCategory.objects.filter(status=1)
        return TemplateResponse(request, 'admin/booking/add_booking.html', context=context_data)

    def source(self, obj):
        return truncatechars(obj.origin_address, 30)
    source.short_description = "Source"

    def destination(self, obj):
        return truncatechars(obj.destination_address, 30)
    source.short_description = "Destination"

    def vehicle_id(self, obj):
        vehicleDetail = Vehicle.objects.get(id=obj.vehicle_id)
        return vehicleDetail.vehicle_no
    vehicle_id.short_description = "Vehicle_Number"


admin_site.register(Booking, BookingAdmin)
