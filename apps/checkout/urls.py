# coding=utf-8

from django.urls import path

from . import views

app_name = 'checkout'

urlpatterns = [
    path('carrinho/adicionar/<slug>/', views.CreateCartItemView.as_view(), name='create-cartitem'),
    path('carrinho/', views.CartItemView.as_view(), name='cart-item'),
    path('finalizando/', views.CheckoutView.as_view(), name='checkout'),
    path('finalizando/<int:pk>/pagseguro', views.PagSeguroView.as_view(), name='pagseguro-view'),
    path('meus-pedidos/', views.OrderListView.as_view(), name='order-list'),
    path('pedido/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('notificacoes/pagseguro', views.pagseguro_notification, name='pagseguro_notification'),
    path('finalizando/<int:pk>/pagamento-na-entrega', views.PaymentOnDeliveryView.as_view(), name='payment-on-delivery'),
]