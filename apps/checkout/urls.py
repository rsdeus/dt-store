# coding=utf-8

from django.urls import path

from . import views

app_name = 'checkout'

urlpatterns = [
    path('carrinho/adicionar/<slug>/', views.CreateCartItemView.as_view(), name='create-cartitem'),
    path('carrinho/', views.CartItemView.as_view(), name='cart-item'),
    path('finalizando/', views.CreateOrderView.as_view(), name='create-order'),
    path('pagamento/<int:pk>/', views.PaymentView.as_view(), name='payment'),
    path('pagamento/<int:pk>/pagseguro/', views.PagSeguroView.as_view(), name='pagseguro'),
    path('pagamento/<int:pk>/pagamento-entrega/', views.PaymentOnDeliveryView.as_view(), name='payment-on-delivery'),
    path('meus-pedidos/', views.OrderListView.as_view(), name='order-list'),
    path('pedido/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    #path('pedido-confirmado/<int:pk>/', views.ThanksView.as_view(), name='thanks'),
    path('notificacoes/pagseguro', views.pagseguro_notification, name='pagseguro_notification'),
]