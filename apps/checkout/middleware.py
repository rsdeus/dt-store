# coding=utf-8

from .models import CartItem, OrderItem

def cart_item_middleware(get_response):
    def middleware(request):
        session_key = request.session.session_key

        #TODO: implemetar de outra forma a limpeza do carrinho e do pedido não finalizados
        OrderItem.return_stock_from_order()
        CartItem.return_stock_from_cart_item()

        response = get_response(request)

        if session_key and request.session.session_key:
            if session_key != request.session.session_key:
                CartItem.objects.filter(cart_key=session_key).update(
                    cart_key=request.session.session_key
                )

        return response

    return middleware
