from models import Product
from uuid import UUID

inventory: dict[UUID, Product] = {}

def insert_product(product: Product):
  inventory[product.get_id()] = product

def update_product(id: UUID, product: Product) -> Product | None:
  inventory[id] = product
  return product

def list_products() -> dict[UUID, Product]:
  return inventory

def list_products_by_brand(brand: str) -> list[Product]:
  return [
    product for product in inventory.values() if product.get_brand().lower() == brand.lower()
  ]

def get_product(id: UUID) -> Product | None:
  return inventory.get(id)

def get_product_by_name(name: str) -> Product | None:
  for product in inventory.values():
    if product.get_name() == name.lower():
      return product

  return None

def get_product_by_barcode(barcode: str) -> Product | None:
  for product in inventory.values():
    if product.get_barcode() == barcode:
      return product

  return None

def remove_product(id: UUID) -> bool:
  if id in inventory:
    del inventory[id]
    return True
  return False

