from rest_framework.response import Response
from rest_framework.decorators import api_view
from users_cart.models import UserCart
from base.utilities import Utilities
from orders.models import Orders
from order_items.models import OrderItems
from users.models import Address
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

@api_view(['POST'])
def place_order(request):
    """
    Place an order using the items in the user's cart.
    """
    user = Utilities.get_user(request)
    try:
        # Fetch cart items for the user
        cart_items = UserCart.objects.filter(user=user)
        if not cart_items.exists():
            return Response({'message': 'Cart is empty'}, status=400)
        
        total_price_sum = sum(item.price * item.quantity for item in cart_items)
        print(f"total_price_sum is {total_price_sum}")

        # Create order
        order = Orders.objects.create(
            price=total_price_sum, 
            buyer=user,
            status=Orders.COMPLETED,
            created_by=user.id,
        )
        shipping_address = user.addresses.filter(address_type=Address.SHIPPING).first()
        billing_address = user.addresses.filter(address_type=Address.BILLING).first()
        
        order.shipping_address = shipping_address
        order.billing_address = billing_address
        order.save()

        for cart_item in cart_items:
            print(f"cart_item is {cart_item}")
            order_item = OrderItems.objects.create(
                quantity=cart_item.quantity,
                product=cart_item.product,
                price=cart_item.quantity * cart_item.price,
                created_by=user.id,
                orders=order 
            )
            # Reduce quantity of the ordered product
            product = cart_item.product
            product.quantity -= cart_item.quantity
            product.save()

        cart_items.delete()
        logger.info(f"'Order placed successfully'")
        # Return success response
        return Response({'message': 'Order placed successfully', 'order_id': order.id}, status=200)
    except Exception as e:
        logger.error(f"Error while placing order {e}")
        return Response({"error": "Error in placing order "+str(e)}, status=400)

