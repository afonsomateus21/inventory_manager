from datetime import date, datetime
from uuid import UUID
from typing import Optional

class Product:
  def __init__(
    self, 
    id: UUID,
    name: str, 
    description: str, 
    price: float, 
    brand: str,
    quantity: int,
    barcode: str,
    created_at: datetime, 
    updated_at: datetime,
    is_perishable: bool = True,
    expiration_date: Optional[date] = None, 
  ):
    self.__id = id
    self.__name = name
    self.__description = description
    self.__price = price
    self.__brand = brand
    self.__quantity = quantity
    self.__barcode = barcode
    self.__created_at = created_at
    self.__updated_at = updated_at
    self.__is_perishable = is_perishable
    self.__expiration_date = expiration_date

  def set_id(self, id: UUID):
    self.__id = id

  def set_name(self, name: str):
    self.__name = name

  def set_description(self, description: str):
    self.__description = description

  def set_price(self, price: float):
    self.__price = price

  def set_brand(self, brand: str):
    self.__brand = brand

  def set_quantity(self, quantity: int):
    self.__quantity = quantity

  def set_barcode(self, barcode: str):
    self.__barcode = barcode

  def set_created_at(self, created_at: datetime):
    self.__created_at = created_at  

  def set_updated_at(self, updated_at: datetime):
    self.__updated_at = updated_at

  def set_is_perishable(self, is_perishable: bool):
    self.__is_perishable = is_perishable

  def set_expiration_date(self, expiration_date: Optional[date]):
    self.__expiration_date = expiration_date

  def get_id(self):
    return self.__id

  def get_name(self):
    return self.__name

  def get_description(self):
    return self.__description

  def get_price(self):
    return self.__price
  
  def get_brand(self):
    return self.__brand
  
  def get_quantity(self):
    return self.__quantity

  def get_barcode(self):
    return self.__barcode

  def get_created_at(self):
    return self.__created_at

  def get_updated_at(self):
    return self.__updated_at

  def get_is_perishable(self):
    return self.__is_perishable

  def get_expiration_date(self):
    return self.__expiration_date

  def is_expired(self):
    """Verifica se o produto está vencido"""
    if not self.__is_perishable:
      return False
    if self.__expiration_date is None:
      return False
    return self.__expiration_date < date.today()

  def days_until_expiration(self):
    """Retorna dias até o vencimento (negativo se vencido)"""
    if not self.__is_perishable or self.__expiration_date is None:
      return None
    return (self.__expiration_date - date.today()).days