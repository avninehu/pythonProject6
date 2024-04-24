from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Vendor, VendorIndexPage, VendorCategory, CategoryIndexPage
from django.contrib.auth.decorators import login_required
from wagtail.admin.forms import WagtailAdminPageForm
from django.urls import reverse


def category_index(request):
    category_index_page = CategoryIndexPage.objects.first()
    categories = Category.objects.child_of(category_index)

    if request.method == 'POST':
        # Handle form submission to create a new category
        name = request.POST.get('name')
        category_index_page.add_child(instance=Category(title=name))

    return render(request, 'core/category_index_page.html', {'category_index': category_index, 'categories': categories})

@login_required
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    context = {
        'category': category,
    }

    return render(request, 'core/category_detail.html', context)

def vendor_index(request):
    vendor_index_page = VendorIndexPage.objects.first()
    vendors = Vendor.objects.filter(is_active=True, admin_deactivated=False)

    context = {
        'vendor_index_page': vendor_index_page,
        'vendors': vendors,
    }
    print(context)

    return render(request, 'core/vendor_index_page.html', context)

def vendor_category(request, vendor_category_id):
    vendor_category = VendorCategory.objects.get(id=vendor_category_id)
    return render(request, 'core/vendor_category.html', {
        'vendor_category': vendor_category
    })

@login_required
def vendor_detail(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)

    context = {
        'vendor': vendor,
    }

    return render(request, 'core/vendor.html', context)

def create_category(request):
    if request.method == 'POST':
        # Manually create a WagtailAdminPageForm instance from the request POST data
        form = WagtailAdminPageForm(request.POST)
        if form.is_valid():
            # Create a new Category instance
            category = Category(
                title=form.cleaned_data['title'],
                slug=form.cleaned_data['slug'],
                name=form.cleaned_data['name']
            )
            # Save the new Category instance
            category.save()
            return redirect('category_index')  # Redirect to the category list page
    else:
        # If not a POST request, create an empty form
        form = WagtailAdminPageForm()
    return render(request, 'core/category.html', {'form': form})
