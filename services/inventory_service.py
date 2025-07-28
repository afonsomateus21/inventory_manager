from uuid import uuid4
from datetime import datetime, date
from repositories import repository, sales_repository
from models import Product, SaleItem, Sale
from utils import show_selling_options_menu
import csv
import os

def insert_product():
  barcode = input("Digite o código de barras do produto: ")

  product = repository.get_product_by_barcode(barcode)

  if product:
    print("Produto já cadastrado. Atualizando quantidade...")
    quantity = int(input("Digite a quantidade que será inserida: "))
    new_quantity = product.get_quantity() + quantity
    product.set_quantity(new_quantity)
    product.set_updated_at(datetime.now())
    repository.update_product(product.get_id(), product)
    print(f"Quantidade atualizada para {new_quantity}.")
    return

  name = input("Digite o nome do produto: ")
  description = input("Digite a descrição do produto: ")
  price = float(input("Digite o preço do produto: "))
  brand = input("Digite a marca do produto: ")
  quantity = int(input("Digite a quantidade inicial: "))

  expiration_date_str = input("Digite a data de validade (AAAA-MM-DD): ")
  expiration_date = date.fromisoformat(expiration_date_str)

  now = datetime.now()
  new_product = Product(
    id=uuid4(),
    name=name,
    description=description,
    price=price,
    brand=brand,
    quantity=quantity,
    expiration_date=expiration_date,
    barcode=barcode,
    created_at=now,
    updated_at=now
  )

  repository.insert_product(new_product)

  print("Produto inserido com sucesso!")

def update_product():
  barcode = input("\nDigite o código de barras do produto: ")

  product = repository.get_product_by_barcode(barcode)

  name = input("Digite o nome do produto: ")
  description = input("Digite a descrição do produto: ")
  price = float(input("Digite o preço do produto: "))
  brand = input("Digite a marca do produto: ")
  quantity = int(input("Digite a quantidade inicial: "))

  expiration_date_str = input("Digite a data de validade (AAAA-MM-DD): ")
  expiration_date = date.fromisoformat(expiration_date_str)

  now = datetime.now()

  product.set_name(name)
  product.set_description(description)
  product.set_price(price)
  product.set_brand(brand)
  product.set_quantity(quantity)
  product.set_expiration_date(expiration_date)
  product.set_updated_at(now)
  
  updated_product = repository.update_product(product.get_id, product)

  if updated_product:
    print("Produto atualizado com sucesso!")

def show_inventory():
  inventory = repository.list_products()

  if not inventory:
    print("\nO estoque está vazio.")
    return

  print("\n")
  for product in inventory.values():
    print("=" * 10)
    print(f"Nome: {product.get_name()}")
    print(f"Descrição: {product.get_description()}")
    print(f"Preço: R$ {product.get_price():.2f}")
    print(f"Marca: {product.get_brand()}")
    print(f"Quantidade em estoque: {product.get_quantity()}")
    print(f"Data de validade: {product.get_expiration_date().isoformat()}")
    print(f"Código de barras: {product.get_barcode()}")
    print(f"Criado em: {product.get_created_at().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Atualizado em: {product.get_updated_at().strftime('%d/%m/%Y %H:%M:%S')}")

def get_product():
  barcode = input("Digite o código de barras: ")

  product = repository.get_product_by_barcode(barcode)

  if product is None:
    print("Produto não encontrado!")

  print(f"Nome: {product.get_name()}")
  print(f"Descrição: {product.get_description()}")
  print(f"Preço: R$ {product.get_price():.2f}")
  print(f"Marca: {product.get_brand()}")
  print(f"Quantidade em estoque: {product.get_quantity()}")
  print(f"Data de validade: {product.get_expiration_date().isoformat()}")
  print(f"Código de barras: {product.get_barcode()}")
  print(f"Criado em: {product.get_created_at().strftime('%d/%m/%Y %H:%M:%S')}")
  print(f"Atualizado em: {product.get_updated_at().strftime('%d/%m/%Y %H:%M:%S')}")


def make_sale():
  keep_selling = True
  sale_items: list[SaleItem] = []

  while keep_selling:
    barcode = input("Digite o código de barras do produto: ")
    quantity = int(input("Digite a quantidade: "))

    product = repository.get_product_by_barcode(barcode)

    if product is None:
      print("Produto não encontrado!")
      return
    
    quantity_remaining = product.get_quantity() - quantity

    if quantity_remaining < 0:
      print("Não há quantidade suficiente desse produto no estoque.")
      return
    
    product.set_quantity(quantity_remaining)
    repository.update_product(product.get_id(), product)

    sale_item = SaleItem(product=product, quantity=quantity)
    sale_items.append(sale_item)

    show_selling_options_menu()
    sale_option = int(input("Digite a opção desejada: "))

    if sale_option == 2:
      keep_selling = False

  seller_name = input("Digite o nome do vendedor(a): ")
  buyer_cpf = input("Digite o CPF do comprador(a): ")

  now = datetime.now()

  sale = Sale(
    seller_name = seller_name,
    buyer_cpf = buyer_cpf,
    sale_date = now,
    items = sale_items
  )

  is_sale_made = sales_repository.make_sale(sale)

  if is_sale_made:
    print("Venda realizada com sucesso!")
  else:
    print("Erro ao realizar a venda")

from collections import defaultdict

def generate_sales_report():
  sales = sales_repository.list_sales()

  if not sales:
    print("Nenhuma venda registrada.")
    return

  total_sales = len(sales)
  total_items_sold = 0
  item_sales_summary = defaultdict(int)

  print("\n")
  print("=" * 50)
  print(f"RELATÓRIO DE VENDAS")
  print(f"Total de vendas realizadas: {total_sales}")

  for sale in sales:
    for item in sale.get_items():
      quantity = item.get_quantity()
      product = item.get_product()
      barcode = product.get_barcode()
      name = product.get_name()

      total_items_sold += quantity
      item_sales_summary[(barcode, name)] += quantity

  print(f"Total de itens vendidos: {total_items_sold}")
  print("\nQuantidade vendida por produto:")
  for (barcode, name), quantity in item_sales_summary.items():
    print(f"- {name} (código: {barcode}): {quantity} unidade(s)")

  print("\nVendas detalhadas:")
  for sale in sales:
    print("-" * 50)
    print(f"ID da venda: {sale.get_id()}")
    print(f"Vendedor: {sale.get_seller_name()}")
    print(f"Comprador (CPF): {sale.get_buyer_cpf()}")
    print(f"Data: {sale.get_sale_date().strftime('%d/%m/%Y %H:%M:%S')}")
    print("Itens vendidos:")

    for item in sale.get_items():
      product = item.get_product()
      print(f"  - {product.get_name()} (x{item.get_quantity()})")

    print(f"Total da venda: R$ {sale.get_total():.2f}")
  print("=" * 50)

def generate_sales_text_report():
  sales = sales_repository.list_sales()
  
  total_sales = len(sales)
  total_items_sold = 0
  items_summary = {} 

  lines = []
  lines.append("RELATÓRIO DE VENDAS\n")
  lines.append(f"Total de vendas: {total_sales}\n")

  for sale in sales:
    lines.append("-" * 40)
    lines.append(f"Data: {sale.get_sale_date().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append(f"Vendedor: {sale.get_seller_name()}")
    lines.append(f"CPF do comprador: {sale.get_buyer_cpf()}")
    lines.append("Itens:")

    for item in sale.get_items():
      name = item.get_product().get_name()
      qty = item.get_quantity()
      lines.append(f"- {name}: {qty}")
      total_items_sold += qty

      if name in items_summary:
        items_summary[name] += qty
      else:
        items_summary[name] = qty

    lines.append("")

  lines.append("=" * 40)
  lines.append(f"\nTotal de itens vendidos: {total_items_sold}")
  lines.append("\nQuantidade vendida por item:")

  for name, qty in items_summary.items():
    lines.append(f"- {name}: {qty}")

  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  with open(f"sales_report_{timestamp}.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
  
  print("Relatório gerado com sucesso em 'sales_report.txt'")

def generate_sales_csv_report():
  sales = sales_repository.list_sales()
  
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  filename = f"sales_report_{timestamp}.csv"
  filepath = os.path.join(os.getcwd(), filename)

  headers = ["Data", "Vendedor", "CPF do Comprador", "Produto", "Quantidade"]

  with open(filepath, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for sale in sales:
      sale_date = sale.get_sale_date().strftime("%d/%m/%Y %H:%M:%S")
      seller = sale.get_seller_name()
      buyer_cpf = sale.get_buyer_cpf()

      for item in sale.get_items():
        product_name = item.get_product().get_name()
        quantity = item.get_quantity()
        writer.writerow([sale_date, seller, buyer_cpf, product_name, quantity])

  print(f"Relatório gerado com sucesso: {filename}")
