# myapp/views.py
from django.shortcuts import render
from .models import InfoSource

def index(request):
    info_sources = InfoSource.objects.all()
    category_choices = InfoSource.CATEGORY_CHOICES
    return render(request, 'server/index.html', {
        'news_sources': info_sources,
        'category_choices': category_choices
    })


def about(request):
    return render(request, 'server/about.html')


from django.shortcuts import render, get_object_or_404
from .models import InfoSource
from django.db.models import Q

def merge_duplicate_info_sources(request):
    # Fetch all InfoSource objects
    all_sources = InfoSource.objects.all()

    # Create a dictionary to track unique URLs and their corresponding entries
    url_dict = {}

    for source in all_sources:
        # If the URL already exists in the dictionary
        if source.url in url_dict:
            existing_source = url_dict[source.url]

            # Merge tags by combining both sets of tags, split by comma
            existing_tags = set(existing_source.tags.split(','))
            new_tags = set(source.tags.split(','))
            merged_tags = ','.join(existing_tags.union(new_tags))
            
            # Update the tags and category of the first entry
            existing_source.tags = merged_tags
            existing_source.category = source.category  # or keep the existing category

            # Save the updated first entry
            existing_source.save()

            # Delete the redundant entry
            source.delete()
        else:
            # Add the URL and source to the dictionary
            url_dict[source.url] = source

    # Render a success message or redirect
    return render(request, 'server/index.html')

