from uuid import UUID, uuid4
from datetime import datetime
from typing import List
from models import SaleItem

class Sale:
  def __init__(
    self,
    items: List[SaleItem],
    seller_name: str,
    buyer_cpf: str,
    sale_date: datetime,
    id: UUID = None
  ):
    self.__id = id or uuid4()
    self.__items = items
    self.__seller_name = seller_name
    self.__buyer_cpf = buyer_cpf
    self.__sale_date = sale_date

  def get_id(self):
    return self.__id

  def get_items(self):
    return self.__items

  def get_seller_name(self):
    return self.__seller_name

  def get_buyer_cpf(self):
    return self.__buyer_cpf

  def get_sale_date(self):
    return self.__sale_date

  def get_total(self):
    return sum(item.get_subtotal() for item in self.__items)
