from uuid import uuid4
from datetime import datetime, date
from repositories import repository, sales_repository
from models import Product, SaleItem, Sale
from utils import (show_selling_options_menu, safe_input, safe_input_number, safe_input_date, safe_input_yes_no, Validators)
import csv
import os
from collections import defaultdict

def insert_product():
  barcode = safe_input("Digite o código de barras do produto: ", Validators.validate_barcode)
  if barcode is None:
    return

  product = repository.get_product_by_barcode(barcode)

  if product:
    print("Produto já cadastrado. Atualizando quantidade...")
    quantity = safe_input_number("Digite a quantidade que será inserida: ", int, Validators.validate_positive_integer, "Quantidade")
    if quantity is None:
      return
    new_quantity = product.get_quantity() + quantity
    product.set_quantity(new_quantity)
    product.set_updated_at(datetime.now())
    repository.update_product(product.get_id(), product)
    print(f"Quantidade atualizada para {new_quantity}.")
    return

  name = safe_input("Digite o nome do produto: ", Validators.validate_name)
  if name is None:
    return

  description = safe_input("Digite a descrição do produto: ", Validators.validate_description)
  if description is None:
    return

  price = safe_input_number("Digite o preço do produto: ", float, Validators.validate_price)
  if price is None:
    return

  brand = safe_input("Digite a marca do produto: ", Validators.validate_brand)
  if brand is None:
    return

  quantity = safe_input_number("Digite a quantidade inicial: ", int, Validators.validate_non_negative_integer, "Quantidade")
  if quantity is None:
    return

  is_perishable = safe_input_yes_no("O produto é perecível? (s/n): ")
  if is_perishable is None:
    return

  expiration_date = None
  if is_perishable:
    expiration_date = safe_input_date("Digite a data de validade (AAAA-MM-DD): ", "Data de validade", validate_future=True)
    if expiration_date is None:
      return

  now = datetime.now()
  new_product = Product(
    id=uuid4(),
    name=name,
    description=description,
    price=price,
    brand=brand,
    quantity=quantity,
    barcode=barcode,
    created_at=now,
    updated_at=now,
    is_perishable=is_perishable,
    expiration_date=expiration_date
  )

  repository.insert_product(new_product)
  print("Produto inserido com sucesso!")

def update_product():
  barcode = safe_input("\nDigite o código de barras do produto: ", Validators.validate_barcode)
  if barcode is None:
    return

  product = repository.get_product_by_barcode(barcode)
  if product is None:
    print("Produto não encontrado!")
    return

  name = safe_input("Digite o nome do produto: ", Validators.validate_name)
  if name is None:
    return

  description = safe_input("Digite a descrição do produto: ", Validators.validate_description)
  if description is None:
    return

  price = safe_input_number("Digite o preço do produto: ", float, Validators.validate_price)
  if price is None:
    return

  brand = safe_input("Digite a marca do produto: ", Validators.validate_brand)
  if brand is None:
    return

  quantity = safe_input_number("Digite a quantidade inicial: ", int, Validators.validate_non_negative_integer, "Quantidade")
  if quantity is None:
    return

  is_perishable = safe_input_yes_no("O produto é perecível? (s/n): ")
  if is_perishable is None:
    return

  expiration_date = None
  if is_perishable:
    expiration_date = safe_input_date("Digite a data de validade (AAAA-MM-DD): ", "Data de validade", validate_future=True)
    if expiration_date is None:
      return

  now = datetime.now()

  product.set_name(name)
  product.set_description(description)
  product.set_price(price)
  product.set_brand(brand)
  product.set_quantity(quantity)
  product.set_is_perishable(is_perishable)
  product.set_expiration_date(expiration_date)
  product.set_updated_at(now)
  
  updated_product = repository.update_product(product.get_id(), product)

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
    
    if product.get_is_perishable():
      print(f"Data de validade: {product.get_expiration_date().strftime('%d/%m/%Y')}")
    else:
      print("Produto não perecível")
    
    print(f"Código de barras: {product.get_barcode()}")
    print(f"Criado em: {product.get_created_at().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Atualizado em: {product.get_updated_at().strftime('%d/%m/%Y %H:%M:%S')}")

def get_product():
  barcode = safe_input("Digite o código de barras: ", Validators.validate_barcode)
  if barcode is None:
    return

  product = repository.get_product_by_barcode(barcode)

  if product is None:
    print("Produto não encontrado!")
    return

  print(f"Nome: {product.get_name()}")
  print(f"Descrição: {product.get_description()}")
  print(f"Preço: R$ {product.get_price():.2f}")
  print(f"Marca: {product.get_brand()}")
  print(f"Quantidade em estoque: {product.get_quantity()}")
  
  if product.get_is_perishable():
    print(f"Data de validade: {product.get_expiration_date().strftime('%d/%m/%Y')}")
  else:
    print("Produto não perecível")
  
  print(f"Código de barras: {product.get_barcode()}")
  print(f"Criado em: {product.get_created_at().strftime('%d/%m/%Y %H:%M:%S')}")
  print(f"Atualizado em: {product.get_updated_at().strftime('%d/%m/%Y %H:%M:%S')}")


def make_sale():
  keep_selling = True
  sale_items: list[SaleItem] = []

  while keep_selling:
    barcode = safe_input("Digite o código de barras do produto: ", Validators.validate_barcode)
    if barcode is None:
      return

    product = repository.get_product_by_barcode(barcode)

    if product is None:
      print("Produto não encontrado!")
      return
    
    quantity = safe_input_number("Digite a quantidade: ", int, Validators.validate_quantity_for_sale, product.get_quantity())
    if quantity is None:
      return
    
    quantity_remaining = product.get_quantity() - quantity
    product.set_quantity(quantity_remaining)
    repository.update_product(product.get_id(), product)

    sale_item = SaleItem(product=product, quantity=quantity)
    sale_items.append(sale_item)

    show_selling_options_menu()
    sale_option = safe_input_number("Digite a opção desejada: ", int)
    if sale_option is None:
      return

    if sale_option == 2:
      keep_selling = False

  seller_name = safe_input("Digite o nome do vendedor(a): ", Validators.validate_seller_name)
  if seller_name is None:
    return

  buyer_cpf = safe_input("Digite o CPF do comprador(a): ", Validators.validate_cpf)
  if buyer_cpf is None:
    return

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
  
  print(f"Relatório gerado com sucesso em 'sales_report_{timestamp}.txt'")

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

def show_expiration_report():
  """Mostra relatório de validade no terminal"""
  inventory = repository.list_products()
  
  if not inventory:
      print("\nO estoque está vazio.")
      return

  perishable_products = [p for p in inventory.values() if p.get_is_perishable()]
  non_perishable_products = [p for p in inventory.values() if not p.get_is_perishable()]
  
  today = date.today()
  expired_products = []
  expiring_soon = []
  expiring_month = []
  valid_products = []
  
  for product in perishable_products:
      days_until_expiration = product.days_until_expiration()
      
      if days_until_expiration < 0:
          expired_products.append((product, abs(days_until_expiration)))
      elif days_until_expiration <= 7:
          expiring_soon.append((product, days_until_expiration))
      elif days_until_expiration <= 30:
          expiring_month.append((product, days_until_expiration))
      else:
          valid_products.append((product, days_until_expiration))
  
  print("\n" + "=" * 60)
  print("RELATÓRIO DE CONTROLE DE VALIDADE")
  print("=" * 60)
  
  print(f"RESUMO:")
  print(f"- Produtos vencidos: {len(expired_products)}")
  print(f"- Vencendo em até 7 dias: {len(expiring_soon)}")
  print(f"- Vencendo em até 30 dias: {len(expiring_month)}")
  print(f"- Produtos com validade adequada: {len(valid_products)}")
  print(f"- Produtos não perecíveis: {len(non_perishable_products)}")
  
  if expired_products:
      print("\nPRODUTOS VENCIDOS:")
      for product, days_expired in expired_products:
          print(f"{product.get_name()} (Código: {product.get_barcode()})")
          print(f"   Vencido há {days_expired} dia(s) - Validade: {product.get_expiration_date()}")
          print(f"   Quantidade em estoque: {product.get_quantity()}")
          print()
  
  if expiring_soon:
      print("\nPRODUTOS VENCENDO EM ATÉ 7 DIAS:")
      for product, days_left in expiring_soon:
          print(f"{product.get_name()} (Código: {product.get_barcode()})")
          print(f"   Vence em {days_left} dia(s) - Validade: {product.get_expiration_date()}")
          print(f"   Quantidade em estoque: {product.get_quantity()}")
          print()
  
  if expiring_month:
      print("\nPRODUTOS VENCENDO EM ATÉ 30 DIAS:")
      for product, days_left in expiring_month:
          print(f"{product.get_name()} (Código: {product.get_barcode()})")
          print(f"   Vence em {days_left} dia(s) - Validade: {product.get_expiration_date()}")
          print(f"   Quantidade em estoque: {product.get_quantity()}")
          print()
  
  if not expired_products and not expiring_soon and not expiring_month:
      print("\nTodos os produtos perecíveis estão com validade adequada!")
  
  print("=" * 60)

def generate_expiration_text_report():
  """Gera relatório de validade em arquivo TXT"""
  inventory = repository.list_products()
  
  if not inventory:
      print("\nO estoque está vazio.")
      return

  perishable_products = [p for p in inventory.values() if p.get_is_perishable()]
  non_perishable_products = [p for p in inventory.values() if not p.get_is_perishable()]
  
  today = date.today()
  products_by_status = {
      'expired': [],
      'expiring_soon': [],
      'expiring_month': [],
      'valid': []
  }
  
  for product in perishable_products:
      days_until_expiration = product.days_until_expiration()
      
      if days_until_expiration < 0:
          products_by_status['expired'].append((product, abs(days_until_expiration)))
      elif days_until_expiration <= 7:
          products_by_status['expiring_soon'].append((product, days_until_expiration))
      elif days_until_expiration <= 30:
          products_by_status['expiring_month'].append((product, days_until_expiration))
      else:
          products_by_status['valid'].append((product, days_until_expiration))
  
  lines = []
  lines.append("RELATÓRIO DE CONTROLE DE VALIDADE")
  lines.append(f"Gerado em: {today.strftime('%d/%m/%Y')}")
  lines.append("=" * 60)
  lines.append("")

  lines.append(f"RESUMO DO STATUS DOS PRODUTOS (EM LOTES):")
  lines.append(f"- Produtos vencidos: {len(products_by_status['expired'])}")
  lines.append(f"- Vencendo em até 7 dias: {len(products_by_status['expiring_soon'])}")
  lines.append(f"- Vencendo em até 30 dias: {len(products_by_status['expiring_month'])}")
  lines.append(f"- Produtos com validade adequada: {len(products_by_status['valid'])}")
  lines.append(f"- Produtos não perecíveis: {len(non_perishable_products)}")
  lines.append("")
  
  if products_by_status['expired']:
      lines.append("PRODUTOS VENCIDOS:")
      lines.append("-" * 40)
      for product, days_expired in products_by_status['expired']:
          lines.append(f"Nome: {product.get_name()}")
          lines.append(f"Código: {product.get_barcode()}")
          lines.append(f"Vencido há: {days_expired} dia(s)")
          lines.append(f"Data de validade: {product.get_expiration_date()}")
          lines.append(f"Quantidade: {product.get_quantity()}")
          lines.append("")
  
  if products_by_status['expiring_soon']:
      lines.append("PRODUTOS VENCENDO EM ATÉ 7 DIAS:")
      lines.append("-" * 40)
      for product, days_left in products_by_status['expiring_soon']:
          lines.append(f"Nome: {product.get_name()}")
          lines.append(f"Código: {product.get_barcode()}")
          lines.append(f"Vence em: {days_left} dia(s)")
          lines.append(f"Data de validade: {product.get_expiration_date()}")
          lines.append(f"Quantidade: {product.get_quantity()}")
          lines.append("")
  
  if products_by_status['expiring_month']:
      lines.append("PRODUTOS VENCENDO EM ATÉ 30 DIAS:")
      lines.append("-" * 40)
      for product, days_left in products_by_status['expiring_month']:
          lines.append(f"Nome: {product.get_name()}")
          lines.append(f"Código: {product.get_barcode()}")
          lines.append(f"Vence em: {days_left} dia(s)")
          lines.append(f"Data de validade: {product.get_expiration_date()}")
          lines.append(f"Quantidade: {product.get_quantity()}")
          lines.append("")
  
  if non_perishable_products:
      lines.append("PRODUTOS NÃO PERECÍVEIS:")
      lines.append("-" * 40)
      for product in non_perishable_products:
          lines.append(f"Nome: {product.get_name()}")
          lines.append(f"Código: {product.get_barcode()}")
          lines.append(f"Quantidade: {product.get_quantity()}")
          lines.append("")
  
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  filename = f"expiration_report_{timestamp}.txt"
  
  with open(filename, "w", encoding="utf-8") as f:
      f.write("\n".join(lines))
  
  print(f"Relatório de validade gerado: {filename}")

def generate_expiration_csv_report():
  """Gera relatório de validade em arquivo CSV"""
  inventory = repository.list_products()
  
  if not inventory:
      print("\nO estoque está vazio.")
      return
  
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  filename = f"expiration_report_{timestamp}.csv"
  filepath = os.path.join(os.getcwd(), filename)

  headers = ["Nome", "Codigo_Barras", "Marca", "Quantidade", "Tipo", "Data_Validade", "Status", "Dias_Para_Vencer"]

  with open(filepath, mode="w", newline="", encoding="utf-8") as file:
      writer = csv.writer(file)
      writer.writerow(headers)

      for product in inventory.values():
          if product.get_is_perishable():
              days_until_expiration = product.days_until_expiration()
              
              if days_until_expiration < 0:
                  status = "VENCIDO"
                  days_display = f"Vencido há {abs(days_until_expiration)} dia(s)"
              elif days_until_expiration <= 7:
                  status = "VENCE_EM_7_DIAS"
                  days_display = f"{days_until_expiration} dia(s)"
              elif days_until_expiration <= 30:
                  status = "VENCE_EM_30_DIAS"
                  days_display = f"{days_until_expiration} dia(s)"
              else:
                  status = "VALIDO"
                  days_display = f"{days_until_expiration} dia(s)"
              
              writer.writerow([
                  product.get_name(),
                  product.get_barcode(),
                  product.get_brand(),
                  product.get_quantity(),
                  "PERECIVEL",
                  product.get_expiration_date().strftime("%d/%m/%Y"),
                  status,
                  days_display
              ])
          else:
              writer.writerow([
                  product.get_name(),
                  product.get_barcode(),
                  product.get_brand(),
                  product.get_quantity(),
                  "NAO_PERECIVEL",
                  "N/A",
                  "NAO_APLICAVEL",
                  "N/A"
              ])

  print(f"Relatório de validade gerado: {filename}")

def remove_expired_products():
  """Remove produtos vencidos do estoque"""
  inventory = repository.list_products()
  
  if not inventory:
      print("\nO estoque está vazio.")
      return

  expired_products = [p for p in inventory.values() if p.get_is_perishable() and p.is_expired()]
  
  if not expired_products:
      print("\nNão há produtos vencidos no estoque.")
      return
  
  print("\nPRODUTOS VENCIDOS ENCONTRADOS:")
  for i, product in enumerate(expired_products, 1):
      days_expired = abs(product.days_until_expiration())
      print(f"{i}. {product.get_name()} (Código: {product.get_barcode()})")
      print(f"   Vencido há {days_expired} dia(s)")
      print(f"   Quantidade: {product.get_quantity()}")
      print()
  
  confirm = input("Deseja remover TODOS os produtos vencidos? (s/N): ").strip().lower()
  
  if confirm == 's' or confirm == 'sim':
      removed_count = 0
      for product in expired_products:
          if repository.remove_product(product.get_id()):
              removed_count += 1
      
      print(f"\n{removed_count} produto(s) vencido(s) removido(s) do estoque.")
  else:
      print("\nOperação cancelada.")

def search_products():
  """Busca produtos por diferentes critérios"""
  print("\n========== Buscar Produtos ==========")
  print("1 - Buscar por código de barras")
  print("2 - Buscar por nome")
  print("3 - Buscar por marca")
  print("4 - Listar produtos com estoque baixo (menos de 5 itens)")
  print("5 - Listar produtos por faixa de preço")
  print("6 - Listar apenas produtos perecíveis")
  print("7 - Listar apenas produtos não perecíveis")
  
  option = safe_input_number("Escolha uma opção: ", int)
  if option is None:
    return
  
  inventory = repository.list_products()
  if not inventory:
    print("\nO estoque está vazio.")
    return
  
  found_products = []
  
  if option == 1:
    barcode = safe_input("Digite o código de barras: ", Validators.validate_barcode)
    if barcode is None:
      return
    product = repository.get_product_by_barcode(barcode)
    if product:
      found_products = [product]
  
  elif option == 2:
    name = safe_input("Digite parte do nome do produto: ", Validators.validate_non_empty_string, "Nome")
    if name is None:
      return
    found_products = [p for p in inventory.values() 
                     if name.lower() in p.get_name().lower()]
  
  elif option == 3:
    brand = safe_input("Digite a marca: ", Validators.validate_non_empty_string, "Marca")
    if brand is None:
      return
    found_products = [p for p in inventory.values() 
                     if brand.lower() in p.get_brand().lower()]
  
  elif option == 4:
    threshold = safe_input_number("Digite a quantidade mínima (padrão 5): ", int, Validators.validate_positive_integer, "Quantidade")
    if threshold is None:
      threshold = 5
    found_products = [p for p in inventory.values() if p.get_quantity() < threshold]
    print(f"\nProdutos com menos de {threshold} itens em estoque:")
  
  elif option == 5:
    min_price = safe_input_number("Digite o preço mínimo: ", float, Validators.validate_positive_number, "Preço mínimo")
    if min_price is None:
      return
    max_price = safe_input_number("Digite o preço máximo: ", float, Validators.validate_positive_number, "Preço máximo")
    if max_price is None:
      return
    
    if min_price > max_price:
      print("Erro: Preço mínimo não pode ser maior que o máximo!")
      return
    
    found_products = [p for p in inventory.values() 
                     if min_price <= p.get_price() <= max_price]
    print(f"\nProdutos na faixa de R$ {min_price:.2f} - R$ {max_price:.2f}:")
  
  elif option == 6:
    found_products = [p for p in inventory.values() if p.get_is_perishable()]
    print("\nProdutos perecíveis:")
  
  elif option == 7:
    found_products = [p for p in inventory.values() if not p.get_is_perishable()]
    print("\nProdutos não perecíveis:")
  
  else:
    print("Opção inválida!")
    return
  
  if not found_products:
    print("\nNenhum produto encontrado com os critérios especificados.")
    return
  
  print(f"\n{len(found_products)} produto(s) encontrado(s):")
  print("=" * 60)
  
  for i, product in enumerate(found_products, 1):
    print(f"\n{i}. {product.get_name()}")
    print(f"   Código: {product.get_barcode()}")
    print(f"   Marca: {product.get_brand()}")
    print(f"   Preço: R$ {product.get_price():.2f}")
    print(f"   Quantidade: {product.get_quantity()}")
    
    if product.get_is_perishable():
      print(f"   Validade: {product.get_expiration_date().strftime('%d/%m/%Y')}")
      
      days_until_expiration = product.days_until_expiration()
      
      if days_until_expiration < 0:
        print(f"   Status: ❌ VENCIDO há {abs(days_until_expiration)} dia(s)")
      elif days_until_expiration <= 7:
        print(f"   Status: ⚠️  Vence em {days_until_expiration} dia(s)")
      elif days_until_expiration <= 30:
        print(f"   Status: 🟡 Vence em {days_until_expiration} dia(s)")
      else:
        print(f"   Status: ✅ Válido por {days_until_expiration} dia(s)")
    else:
      print(f"   Tipo: 📦 Produto não perecível")
  
  print("=" * 60)