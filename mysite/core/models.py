from django.forms import inlineformset_factory
from django import forms
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultipleChooserPanel, InlinePanel, MultiFieldPanel
from django.db import models
from django.contrib.auth.models import User
from wagtail.fields import RichTextField


class Category(Page):
    name = models.CharField(max_length=255, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('name'),

    ]

    def __str__(self):
        return self.name or 'Unnamed Category'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VendorCategory(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name='vendor_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vendor.name} - {self.category.name}"


class CategoryIndexPage(Page):
    subpage_types = ['Category']
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

class VendorIndexPage(Page):

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    def get_categories(self):
        return Category.objects.all()

class Vendor(Page):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255, default='Unknown')
    vendor_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    admin_deactivated = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='vendors')

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('country'),
        FieldPanel('city'),
        FieldPanel('vendor_owner'),
        FieldPanel('is_active'),
        FieldPanel('admin_deactivated'),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Categories"),

    ]

    def save(self, *args, **kwargs):
        # Save the page first to ensure it has an ID
        super().save(*args, **kwargs)

        # Save the selected categories
        categories = self.categories.all()
        for category in categories:
            VendorCategory.objects.get_or_create(vendor=self, category=category)

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

