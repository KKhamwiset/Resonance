from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import Cart, CartItem, Product


def get_cart_data(user):
    """Helper function to fetch cart data for a user."""
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=user)

    # Get cart items with product details (optimized using select_related)
    items = []
    # Eager load the product and its category to avoid N+1 queries
    for item in cart.items.select_related("product", "product__category").all():
        items.append(
            {
                "id": item.product.id,
                "name": item.product.name,
                "price": float(item.product.price),
                "sale_price": float(item.product.sale_price)
                if item.product.sale_price
                else None,
                "category": item.product.category.name if item.product.category else "",
                "image": item.product.image_url,
                "quantity": item.quantity,
                "stock": item.product.stock,
            }
        )

    return {"status": "success", "data": items}


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    """
    Get the current user's cart items
    """
    user = request.user
    return Response(get_cart_data(user))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """
    Add an item to the cart
    """
    user = request.user
    data = request.data
    print(f"Raw data: {request.user.id} - {data}")

    if not data.get("product_id"):
        return Response(
            {"status": "error", "message": "Product ID is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    if quantity <= 0:
        return Response(
            {"status": "error", "message": "Quantity must be greater than 0"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Get the product
        product = get_object_or_404(Product, id=product_id)
        print(f"Product found: {product.id}, Stock: {product.stock}")

        # Check stock
        if product.stock < quantity:
            return Response(
                {
                    "status": "error",
                    "message": f"Not enough stock. Only {product.stock} available.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=user)
        print(f"Cart {'created' if created else 'retrieved'}: {cart.id}")

        # Check if item already exists in cart
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            print(
                f"CartItem found: {cart_item.id}, Current quantity: {cart_item.quantity}"
            )
            # Update quantity
            cart_item.quantity += quantity
            cart_item.save()
            print(f"Updated CartItem quantity: {cart_item.quantity}")
        except CartItem.DoesNotExist:
            # Create new cart item
            cart_item = CartItem.objects.create(
                cart=cart, product=product, quantity=quantity
            )
            print(f"Created new CartItem: {cart_item.id}")

        # Return updated cart
        return Response(get_cart_data(user))

    except Exception as e:
        import traceback

        print(f"Error in add_to_cart: {str(e)}")
        print(traceback.format_exc())
        return Response(
            {"status": "error", "message": f"Server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """
    Update cart item quantity
    """
    user = request.user
    data = request.data

    if "quantity" not in data:
        return Response(
            {"status": "error", "message": "Quantity is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    quantity = int(data.get("quantity"))

    try:
        # Get cart
        cart = get_object_or_404(Cart, user=user)

        # Get product
        product = get_object_or_404(Product, id=item_id)

        # Get cart item
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)

            if quantity <= 0:
                # Remove item if quantity is 0 or negative
                cart_item.delete()
            else:
                # Check stock
                if product.stock < quantity:
                    return Response(
                        {
                            "status": "error",
                            "message": f"Not enough stock. Only {product.stock} available.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Update quantity
                cart_item.quantity = quantity
                cart_item.save()

        except CartItem.DoesNotExist:
            if quantity > 0:
                # Create new cart item if it doesn’t exist and quantity is positive
                cart_item = CartItem.objects.create(
                    cart=cart, product=product, quantity=quantity
                )

        # Return updated cart
        return Response(get_cart_data(user))

    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    """
    Remove an item from the cart
    """
    user = request.user

    try:
        # Get cart
        cart = get_object_or_404(Cart, user=user)

        # Get product
        product = get_object_or_404(Product, id=item_id)

        # Delete cart item if it exists
        CartItem.objects.filter(cart=cart, product=product).delete()

        # Return updated cart
        return Response(get_cart_data(user))

    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """
    Clear the entire cart
    """
    user = request.user

    try:
        # Get cart
        cart = get_object_or_404(Cart, user=user)

        # Delete all cart items
        cart.items.all().delete()

        return Response(
            {"status": "success", "message": "Cart cleared successfully", "data": []}
        )

    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def sync_cart(request):
    """Sync the local cart with the server"""
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"User: {request.user}")

    data = request.data
    print(f"Raw data: {data}")

    items_data = data.get("items", [])
    print(f"Items data: {items_data}")

    try:
        cart, created = Cart.objects.get_or_create(user=request.user)

        if data.get("replace_all", False):
            cart.items.all().delete()

        for item in items_data:
            try:
                print(f"Item: {item}")
                product_id = int(item.get("id"))
                quantity = int(item.get("quantity", 1))
            except (TypeError, ValueError):
                print(f"Error converting values for item: {item}")
                continue

            try:
                # Get the product and create/update cart item
                product = Product.objects.get(id=product_id)

                # Update quantity based on available stock
                quantity = min(quantity, product.stock)
                if quantity <= 0:
                    continue

                # Create or update the cart item
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart, product=product, defaults={"quantity": quantity}
                )

                if not created and not data.get("replace_all", False):
                    cart_item.quantity += quantity
                    cart_item.save()
            except Product.DoesNotExist:
                print(f"Product with id {product_id} not found")

        # Return the updated cart
        return Response(get_cart_data(request.user))

    except Exception as e:
        import traceback

        print(f"Exception occurred: {e}")
        print(traceback.format_exc())
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
