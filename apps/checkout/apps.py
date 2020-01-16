from django.apps import AppConfig
import logging
import threading

logger = logging.getLogger(__name__)


class CheckoutConfig(AppConfig):
    name = 'apps.checkout'
    verbose_name = 'Checkout'

'''    def ready(self):
        super().ready()

        logger.info("Iniciando %s", __name__)
        #CartItem = self.get_model('CartItem')
        OrderItem = self.get_model('OrderItem')
        thread = threading.Thread(target=back_tasks.run_order_item(OrderItem), daemon=True)
        thread.start()
        logger.info("Finalizando %s", __name__)
'''