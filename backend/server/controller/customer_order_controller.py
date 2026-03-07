from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import uuid
from decimal import Decimal
from ..models import Order, OrderItem, Product, User
from django.shortcuts import get_object_or_404


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    data = request.data

    if not data.get("shipping_address"):
        return Response(
            {"status": "error", "message": "Shipping address is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if we should save the address
    save_address = data.get("save_address", False)
    shipping_address = data.get("shipping_address")

    # Save the shipping address to the user's account if requested
    if save_address and shipping_address:
        try:
            # Update the user's address
            user.address = shipping_address

            # Extract city, state, postal code if possible
            address_parts = shipping_address.split("\n")
            if len(address_parts) >= 4:
                city_state_zip = address_parts[3].split(",")
                if len(city_state_zip) >= 1:
                    user.city = city_state_zip[0].strip()
                if len(city_state_zip) >= 2:
                    state_zip = city_state_zip[1].strip().split(" ", 1)
                    if len(state_zip) >= 1:
                        user.state = state_zip[0].strip()
                    if len(state_zip) >= 2:
                        user.postal_code = state_zip[1].strip()

            # Set country if provided
            if len(address_parts) >= 5:
                user.country = address_parts[4].strip()

            user.save()
        except Exception as e:
            # Log the error but continue with order creation
            print(f"Error saving address: {str(e)}")

    items_data = data.get("items")
    if not items_data:
        return Response(
            {"status": "error", "message": "No cart found and no cart items provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        with transaction.atomic():
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            total_amount = Decimal("0.00")

            # Create order
            order = Order.objects.create(
                user=user,
                order_number=order_number,
                shipping_address=shipping_address,
                total_amount=total_amount,
                payment_status=False,
            )

            # Create order items
            for item_data in items_data:
                product_id = item_data.get("product_id")
                quantity = item_data.get("quantity", 1)
                price = Decimal(str(item_data.get("price")))
                try:
                    product = Product.objects.get(id=product_id)
                    if product.stock < quantity:
                        raise ValueError(
                            f"Not enough stock for {product.name}. Available: {product.stock}"
                        )

                    product.stock -= quantity
                    product.save()

                except Product.DoesNotExist:
                    raise ValueError(f"Product with ID {product_id} not found")

                OrderItem.objects.create(
                    order=order, product=product, quantity=quantity, price=price
                )

                total_amount += price * quantity

            order.total_amount = total_amount
            order.save()

            return Response(
                {
                    "status": "success",
                    "message": "Order created successfully",
                    "data": {
                        "order_id": order.id,
                        "order_number": order.order_number,
                        "total_amount": str(order.total_amount),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

    except ValueError as e:
        return Response(
            {"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": f"Failed to create order: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def process_payment(request, order_id):
    """Process payment for a specific order"""
    user = request.user
    data = request.data

    try:
        # Get the order and verify it belongs to the authenticated user
        order = get_object_or_404(Order, id=order_id, user=user)

        # Update order payment details
        order.payment_status = data.get("payment_status", True)

        # Update payment method
        order.payment_method = data.get("payment_method", "credit_card")

        # Set payment date to current time
        from django.utils import timezone

        order.payment_date = timezone.now()

        # Update order status to processing after payment
        order.status = "processing"

        # Save the order
        order.save()

        return Response(
            {
                "status": "success",
                "message": "Payment processed successfully",
                "data": {
                    "order_id": order.id,
                    "order_number": order.order_number,
                    "payment_status": order.payment_status,
                },
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": f"Payment processing failed: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return Response({"id": user.id, "username": user.username, "email": user.email})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    """Get all orders for the authenticated user"""
    user = request.user
    # Eager load the order items and their associated products to avoid N+1 queries
    orders = Order.objects.filter(user=user).prefetch_related("items__product").order_by("-created_at")

    orders_data = []
    for order in orders:
        order_items = []
        for item in order.items.all():
            order_items.append(
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "price": str(item.price),
                    "subtotal": str(item.price * item.quantity),
                }
            )

        orders_data.append(
            {
                "id": order.id,
                "order_number": order.order_number,
                "status": order.status,
                "total_amount": str(order.total_amount),
                "shipping_address": order.shipping_address,
                "payment_status": order.payment_status,
                "created_at": order.created_at,
                "items": order_items,
            }
        )

    return Response(
        {"status": "success", "data": orders_data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_details(request, order_id):
    """Get details of a specific order"""
    user = request.user

    try:
        # Ensure the order belongs to the authenticated user and eager load items + products
        order = Order.objects.prefetch_related("items__product").get(id=order_id, user=user)

        order_items = []
        for item in order.items.all():
            order_items.append(
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "price": str(item.price),
                    "subtotal": str(item.price * item.quantity),
                }
            )

        order_data = {
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total_amount": str(order.total_amount),
            "shipping_address": order.shipping_address,
            "payment_status": order.payment_status,
            "created_at": order.created_at,
            "items": order_items,
        }

        return Response(
            {"status": "success", "data": order_data},
            status=status.HTTP_200_OK,
        )
    except Order.DoesNotExist:
        return Response(
            {"status": "error", "message": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
