from django.db import models

class InfoSource(models.Model):
    CATEGORY_CHOICES = [
        ('blog', 'Blog'),
        ('website', 'Website'),
        ('news_channels', 'News Channels'),
        ('youtube', 'YouTube'),
        ('redits', 'Redits'),
        ('facebook', 'Facebook'),
        ('other', 'Other'),
    ]

    RATING_CHOICES = [
        (1.0, '1 Star'),
        (1.5, '1.5 Stars'),
        (2.0, '2 Stars'),
        (2.5, '2.5 Stars'),
        (3.0, '3 Stars'),
        (3.5, '3.5 Stars'),
        (4.0, '4 Stars'),
        (4.5, '4.5 Stars'),
        (5.0, '5 Stars'),
    ]

    title = models.CharField(max_length=255)
    url = models.URLField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.CharField(max_length=255, help_text="Comma-separated tags")
    prompts = models.TextField(null=True, blank=True, help_text="Textual prompts or descriptions")
    rating = models.DecimalField(max_digits=3, decimal_places=1, choices=RATING_CHOICES, default=1.0, help_text="Rating from 1 to 5 stars")
    
    # Subscriber count field
    subscribers_count = models.CharField(max_length=10, help_text="Number of subscribers")

    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the record was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the record was last updated")

    def __str__(self):
        return self.title
