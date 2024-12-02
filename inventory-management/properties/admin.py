from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, AccommodationImage, LocalizeAccommodation

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')

class AccommodationImageInline(admin.TabularInline):
    """
    Inline admin for managing images related to an Accommodation.
    """
    model = AccommodationImage
    extra = 1  # Number of empty slots to display for adding new images
    fields = ('image',)  # Fields to display in the inline
    readonly_fields = ('uploaded_at',)

@admin.register(Accommodation)
class AccommodationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'center', 'location', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'location') 
    search_fields = ('title', 'country_code', 'location__title')
    ordering = ('-created_at',)
    inlines = [AccommodationImageInline]  # Add the inline for managing images
    
    def get_queryset(self, request):
        """
        Limit the queryset to show only the properties owned by the user.
        Superusers see all properties.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        """
        Allow only owners to change their properties.
        """
        if obj is None:
            return True
        return obj.user == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """
        Allow only owners to delete their properties.
        """
        if obj is None:
            return True
        return obj.user == request.user or request.user.is_superuser

@admin.register(AccommodationImage)
class AccommodationImageAdmin(admin.ModelAdmin):
    """
    Admin interface for the AccommodationImage model.
    """
    list_display = ('accommodation', 'image', 'uploaded_at')
    search_fields = ('accommodation__title',)

@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'accommodation', 'language', 'description')
    list_filter = ('language',)
    search_fields = ('description', 'language')