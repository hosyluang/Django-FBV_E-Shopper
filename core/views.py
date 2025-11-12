from django.shortcuts import render
from product.models import Product
from django.core.paginator import Paginator
# Create your views here.


def home(request):
    products = Product.objects.all().order_by("-id")
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "core/home.html", {"page_obj": page_obj, "paginator": paginator}
    )
