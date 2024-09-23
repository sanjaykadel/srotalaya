from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InfoSource
from .forms import InfoSourceForm  # Assuming you have a form to create/edit InfoSource
import re


def about(request):
    return render(request, 'server/about.html')

from django.shortcuts import render
from .models import InfoSource
from django.db.models import Q

def merge_duplicate_info_sources(request):
    # Fetch all InfoSource objects
    all_sources = InfoSource.objects.all()

    # Create a dictionary to track unique URLs and their latest entries
    url_dict = {}

    for source in all_sources:
        # If the URL already exists in the dictionary
        if source.url in url_dict:
            existing_source = url_dict[source.url]

            # Choose the most recent entry based on 'updated_at'
            if source.created_at > existing_source.created_at:
                # Merge tags by combining both sets of tags, split by comma
                existing_tags = set(existing_source.tags.split(','))
                new_tags = set(source.tags.split(','))
                merged_tags = ','.join(existing_tags.union(new_tags))
                
                # Update the latest entry with new data
                existing_source.tags = merged_tags
                existing_source.category = source.category  # or keep the existing category
                existing_source.prompts = source.prompts  # Update prompts if needed
                existing_source.rating = source.rating  # Update rating if needed
                
                # Save the updated latest entry
                existing_source.save()

                # Delete the redundant entry
                source.delete()
        else:
            # Add the URL and source to the dictionary
            url_dict[source.url] = source

    # Render a success message or redirect
    return render(request, 'server/index.html', {'message': 'Duplicates merged successfully'})



# Helper function to parse subscribers count for sorting
def parse_subscribers_count(count_str):
    """ Convert subscriber count string to a numeric value for sorting. """
    cleaned_str = re.sub(r'[^\d.,KM]', '', count_str).upper()
    
    if 'M' in cleaned_str:
        return float(cleaned_str.replace('M', '').replace(',', '')) * 1e6
    elif 'K' in cleaned_str:
        return float(cleaned_str.replace('K', '').replace(',', '')) * 1e3
    else:
        return float(cleaned_str.replace(',', ''))

# Index view to display all InfoSource records
def index(request):
    info_sources = InfoSource.objects.all()
    category_choices = InfoSource.CATEGORY_CHOICES

    # Sort by subscriber count
    info_sources = sorted(
        info_sources,
        key=lambda source: parse_subscribers_count(source.subscribers_count),
        reverse=True  # Ensure higher subscriber counts come first
    )

    return render(request, 'server/index.html', {
        'news_sources': info_sources,
        'category_choices': category_choices
    })

def Test(request):
    info_sources = InfoSource.objects.all()
    category_choices = InfoSource.CATEGORY_CHOICES

    # Sort by subscriber count
    info_sources = sorted(
        info_sources,
        key=lambda source: parse_subscribers_count(source.subscribers_count),
        reverse=True  # Ensure higher subscriber counts come first
    )

    return render(request, 'server/index copy.html', {
        'news_sources': info_sources,
        'category_choices': category_choices
    })


# Create new InfoSource (only for logged-in users)
@login_required
def create_info_source(request):
    if request.method == 'POST':
        form = InfoSourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('test')  # Redirect to index page after successful creation
    else:
        form = InfoSourceForm()
    
    return render(request, 'server/create_info_source.html', {'form': form})

# Delete an InfoSource (only for staff members)
@login_required
def delete_info_source(request, pk):
    source = get_object_or_404(InfoSource, pk=pk)
    if request.method == 'POST':
        source.delete()
        return redirect('test')  # Redirect to the index page after deletion
    return render(request, 'server/confirm_delete.html', {'source': source})
