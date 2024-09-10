from django.contrib import admin
from .models import InfoSource

@admin.register(InfoSource)
class InfoSourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'rating', 'url')  # Display rating in list view
    search_fields = ('title', 'tags', 'prompts')  # Include prompts in search
    list_filter = ('category', 'rating')  # Add rating filter
    ordering = ('title',)  # Optional: order by title
    readonly_fields = ('url',)  # Make URL read-only if needed

    def rating_display(self, obj):
        return f'{obj.rating} ★'  # Optional: display rating with star
    rating_display.short_description = 'Rating'

    # Optional: If you want to show the image in the list display
    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 50px; height:50px;" />'
        return "No Image"
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'
