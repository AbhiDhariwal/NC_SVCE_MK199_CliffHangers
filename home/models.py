from django.db import models
from django.template.defaultfilters import slugify

from accounts.models import User

# Create your models here.

class Road(models.Model):
    road_id = models.CharField(max_length=255, unique=True)
    pci = models.IntegerField(verbose_name='Pavement Condition Index', null=True, blank=True)
    block = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    total_images = models.IntegerField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    limit_choices_to={'role': 'con'}, related_name='assigned_roads')
    slug = models.SlugField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.road_id

    def save(self, *args, **kwargs):
        self.slug = slugify(self.road_id)
        super(Road, self).save(*args, **kwargs)

class Image(models.Model):
    QUALITY = (
        (1, 'Severe'),
        (2, 'Poor'),
        (3, 'Fair'),
        (4, 'Satisfactory'),
        (5, 'Good'),
    )

    road = models.ForeignKey(Road, on_delete=models.CASCADE, related_name='images')
    image_id = models.CharField(max_length=50)
    image = models.ImageField(upload_to='road_images', null=True, blank=True)
    quality = models.IntegerField(choices=QUALITY, null=True, blank=True)
    village = models.CharField(max_length=255, blank=True)
    habitation = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (('road', 'image_id'),)

    def __str__(self):
        return f'{self.image_id} ({self.road.road_id})'

class Issue(models.Model):
    issue_id = models.CharField(max_length=50, unique=True)  # For ordering and grouping
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class IssueDetail(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='issues')
    issue = models.ForeignKey(Issue, on_delete=models.PROTECT, related_name='details')
    count = models.IntegerField()
    quality = models.IntegerField(choices=Image.QUALITY, null=True, blank=True)  # On a scale of 1-10?? Currently 1-5

    class Meta:
        unique_together = (('image', 'issue'),)

    def __str__(self):
        return f'{self.image.image_id} - {self.issue.name}'

