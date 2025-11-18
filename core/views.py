from django.http import JsonResponse
from django.shortcuts import render
from product.models import Product
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    products = Product.objects.all().order_by("-id")
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "core/home.html", {"page_obj": page_obj, "paginator": paginator}
    )


def four_zero_four(request):
    return render(request, "core/404.html")


def contact(request):
    return render(request, "core/contact.html")


@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)
        cart = request.session.get("cart", [])

        for item in cart:
            if item["id"] == product.id:
                item["qty"] += 1
                item["total"] = item["qty"] * float(item["price"])
                break
        else:
            total = float(item["price"]) * item["qty"]
            cart.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "image": product.images[0],
                    "price": float(product.price),
                    "qty": 1,
                    "total": total,
                }
            )
        request.session["cart"] = cart
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)
