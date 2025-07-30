from datetime import datetime, date
from uuid import uuid4, UUID
from models import Product 
from repositories import repository, sales_repository
from services import (
    insert_product, update_product, show_inventory, make_sale, 
    generate_sales_report, generate_sales_text_report, 
    generate_sales_csv_report, get_product, search_products,
    show_expiration_report, generate_expiration_text_report,
    generate_expiration_csv_report, remove_expired_products
)
from utils import show_options_menu

repository.load_from_file()
sales_repository.load_from_file()
keep_application_working = True

while keep_application_working:
  show_options_menu()
  option = int(input("\nDigite o número da opção escolhida: "))
  match option:
    case 1:
      insert_product()
    case 2:
      update_product()
    case 3:
      make_sale()
    case 4:
      get_product()
    case 5:
      search_products()
    case 6:
      show_inventory()
    case 7:
      generate_sales_report()
    case 8:
      generate_sales_text_report()
    case 9:
      generate_sales_csv_report()
    case 10:
      show_expiration_report()
    case 11:
      generate_expiration_text_report()
    case 12:
      generate_expiration_csv_report()
    case 13:
      remove_expired_products()
    case 14:
      keep_application_working = False
      repository.save_to_file()
      sales_repository.save_to_file()