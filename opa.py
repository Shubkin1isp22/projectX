class Product:
    """Класс для хранения информации о товаре"""
    def __init__(self, product_id, name, price, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category  # Ссылка на объект Category

    def __str__(self):
        return f"{self.name} - {self.price}$ (Категория: {self.category.name})"


class Category:
    """Класс для категорий товаров"""
    def __init__(self, name):
        self.name = name
        self.products = []  # Список товаров в категории

    def add_product(self, product):
        """Добавляет товар в категорию"""
        self.products.append(product)

    def list_products(self):
        """Выводит список товаров в категории"""
        return [str(product) for product in self.products]

    def __str__(self):
        return f"Категория: {self.name}, товаров: {len(self.products)}"


class Customer:
    """Класс для хранения данных о клиенте"""
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"Клиент: {self.name}, Email: {self.email}"


class Order:
    """Класс для хранения заказа"""
    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer  # Связь с объектом Customer
        self.items = []  # Список товаров в заказе
        self.total_price = 0

    def add_product(self, product, quantity=1):
        """Добавляет товар в заказ"""
        self.items.append((product, quantity))
        self.total_price += product.price * quantity

    def __str__(self):
        item_list = "\n".join([f"{p.name} x{q} = {p.price * q}$" for p, q in self.items])
        return f"Заказ {self.order_id} для {self.customer.name}:\n{item_list}\nИтого: {self.total_price}$"


class Store:
    """Основной класс управления магазином"""
    def __init__(self):
        self.products = []
        self.categories = []
        self.customers = []
        self.orders = []

    def add_category(self, category):
        """Добавляет категорию в магазин"""
        self.categories.append(category)

    def add_product(self, product):
        """Добавляет товар в магазин"""
        self.products.append(product)
        product.category.add_product(product)  # Добавляем товар в категорию

    def add_customer(self, customer):
        """Добавляет клиента в магазин"""
        self.customers.append(customer)

    def create_order(self, customer):
        """Создаёт новый заказ"""
        order = Order(len(self.orders) + 1, customer)
        self.orders.append(order)
        return order

    def list_products(self):
        """Выводит список всех товаров"""
        return [str(p) for p in self.products]

    def list_orders(self):
        """Выводит список всех заказов"""
        return [str(order) for order in self.orders]


# Основная функция демонстрации работы
def main():
    store = Store()

    # Создание категорий
    electronics = Category("Электроника")
    clothing = Category("Одежда")
    store.add_category(electronics)
    store.add_category(clothing)

    # Создание товаров
    phone = Product(1, "Смартфон", 700, electronics)
    laptop = Product(2, "Ноутбук", 1200, electronics)
    tshirt = Product(3, "Футболка", 25, clothing)
    jeans = Product(4, "Джинсы", 50, clothing)

    store.add_product(phone)
    store.add_product(laptop)
    store.add_product(tshirt)
    store.add_product(jeans)

    # Создание клиентов
    alice = Customer(1, "Алиса", "alice@example.com")
    bob = Customer(2, "Боб", "bob@example.com")
    store.add_customer(alice)
    store.add_customer(bob)

    # Создание заказа
    order1 = store.create_order(alice)
    order1.add_product(phone, 1)
    order1.add_product(tshirt, 2)

    order2 = store.create_order(bob)
    order2.add_product(laptop, 1)
    order2.add_product(jeans, 1)

    # Вывод информации
    print("\n--- Список товаров в магазине ---")
    print("\n".join(store.list_products()))

    print("\n--- Список заказов ---")
    print("\n".join(store.list_orders()))

    print("\n--- Товары по категориям ---")
    for category in store.categories:
        print(f"\n{category}")
        print("\n".join(category.list_products()))


# Запуск программы
if __name__ == "__main__":
    main()