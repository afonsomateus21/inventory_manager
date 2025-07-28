from models import Product
from uuid import UUID
from utils import save_json, load_json
from datetime import datetime, date
class ProductRepository:
  def __init__(self):
    self.inventory: dict[UUID, Product] = {}

  def insert_product(self, product: Product):
    self.inventory[product.get_id()] = product

  def update_product(self, id: UUID, product: Product) -> Product | None:
    self.inventory[id] = product
    return product

  def list_products(self) -> dict[UUID, Product]:
    return self.inventory

  def list_products_by_brand(self, brand: str) -> list[Product]:
    return [
      product for product in self.inventory.values() if product.get_brand().lower() == brand.lower()
    ]

  def get_product(self, id: UUID) -> Product | None:
    return self.inventory.get(id)

  def get_product_by_name(self, name: str) -> Product | None:
    for product in self.inventory.values():
      if product.get_name() == name.lower():
        return product

    return None

  def get_product_by_barcode(self, barcode: str) -> Product | None:
    for product in self.inventory.values():
      if product.get_barcode() == barcode:
        return product

    return None

  def remove_product(self, id: UUID) -> bool:
    if id in self.inventory:
      del self.inventory[id]
      return True
    return False
  
  def save_to_file(self, filename="inventory.json"):
    data = [self.product_to_dict(p) for p in self.inventory.values()]
    save_json(data, filename)

  def load_from_file(self, filename="inventory.json"):
    data = load_json(filename)
    if not data:
      return
    for item in data:
      product = self.dict_to_product(item)
      self.insert_product(product)

  def product_to_dict(self, product: Product) -> dict:
    return {
      "id": str(product.get_id()),
      "name": product.get_name(),
      "description": product.get_description(),
      "price": product.get_price(),
      "brand": product.get_brand(),
      "quantity": product.get_quantity(),
      "expiration_date": product.get_expiration_date().isoformat(),
      "barcode": product.get_barcode(),
      "created_at": product.get_created_at().isoformat(),
      "updated_at": product.get_updated_at().isoformat(),
    }

  def dict_to_product(self, data: dict) -> Product:
    return Product(
      id=UUID(data["id"]),
      name=data["name"],
      description=data["description"],
      price=float(data["price"]),
      brand=data["brand"],
      quantity=int(data["quantity"]),
      expiration_date=date.fromisoformat(data["expiration_date"]),
      barcode=data["barcode"],
      created_at=datetime.fromisoformat(data["created_at"]),
      updated_at=datetime.fromisoformat(data["updated_at"]),
    )

repository = ProductRepository()