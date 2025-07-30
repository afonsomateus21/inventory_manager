from models import Sale, SaleItem
from repositories import repository
from utils import load_json, save_json, custom_encoder
from uuid import UUID
from datetime import datetime, date

class SalesRepository:
  def __init__(self):
    self.__sales: list[Sale] = []

  def make_sale(self, sale: Sale) -> bool:
    if sale:
      self.__sales.append(sale)
      return True
    
    return False
  
  def list_sales(self) -> list[Sale]:
    return self.__sales
  
  def save_to_file(self, filename="sales.json"):
    data = [self.sale_to_dict(sale) for sale in self.__sales]
    save_json(data, filename)

  def load_from_file(self, filename="sales.json"):
    data = load_json(filename)
    if not data:
        return
    for s in data:
        sale = self.dict_to_sale(s)
        self.make_sale(sale)

  def sale_to_dict(self, sale: Sale) -> dict:
    return {
      "id": str(sale.get_id()),
      "seller_name": sale.get_seller_name(),
      "buyer_cpf": sale.get_buyer_cpf(),
      "sale_date": sale.get_sale_date().isoformat(),
      "items": [
        {
          "product_id": str(item.get_product().get_id()),
          "quantity": item.get_quantity()
        }
        for item in sale.get_items()
      ]
    }

  def dict_to_sale(self, data: dict) -> Sale:
    items = []
    for i in data["items"]:
      product = repository.get_product(UUID(i["product_id"]))
      if product:
        items.append(SaleItem(product=product, quantity=int(i["quantity"])))
    return Sale(
      id=UUID(data["id"]),
      seller_name=data["seller_name"],
      buyer_cpf=data["buyer_cpf"],
      sale_date=datetime.fromisoformat(data["sale_date"]),
      items=items
    )

  
sales_repository = SalesRepository()

