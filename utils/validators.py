import re
from datetime import date, datetime
from typing import Optional, Union

class ValidationError(Exception):
    """Exceção customizada para erros de validação"""
    pass

class Validators:
    """Classe com métodos estáticos para validação de dados"""
    
    @staticmethod
    def validate_non_empty_string(value: str, field_name: str) -> str:
        """Valida se uma string não está vazia"""
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} deve ser uma string")
        
        value = value.strip()
        if not value:
            raise ValidationError(f"{field_name} não pode estar vazio")
        
        return value
    
    @staticmethod
    def validate_positive_number(value: Union[int, float], field_name: str) -> Union[int, float]:
        """Valida se um número é positivo"""
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{field_name} deve ser um número")
        
        if value <= 0:
            raise ValidationError(f"{field_name} deve ser maior que zero")
        
        return value
    
    @staticmethod
    def validate_non_negative_integer(value: int, field_name: str) -> int:
        """Valida se um inteiro é não-negativo"""
        if not isinstance(value, int):
            raise ValidationError(f"{field_name} deve ser um número inteiro")
        
        if value < 0:
            raise ValidationError(f"{field_name} não pode ser negativo")
        
        return value
    
    @staticmethod
    def validate_positive_integer(value: int, field_name: str) -> int:
        """Valida se um inteiro é positivo"""
        if not isinstance(value, int):
            raise ValidationError(f"{field_name} deve ser um número inteiro")
        
        if value <= 0:
            raise ValidationError(f"{field_name} deve ser maior que zero")
        
        return value
    
    @staticmethod
    def validate_barcode(barcode: str) -> str:
        """Valida formato do código de barras"""
        barcode = Validators.validate_non_empty_string(barcode, "Código de barras")

        barcode = barcode.replace(" ", "")
        if not barcode.isdigit():
            raise ValidationError("Código de barras deve conter apenas números")
        
        return barcode
    
    @staticmethod
    def validate_cpf(cpf: str) -> str:
        """Valida formato e dígitos verificadores do CPF"""
        cpf = Validators.validate_non_empty_string(cpf, "CPF")

        cpf = re.sub(r'[^0-9]', '', cpf)

        if len(cpf) != 11:
            raise ValidationError("CPF deve ter 11 dígitos")

        if cpf == cpf[0] * 11:
            raise ValidationError("CPF inválido")

        def calculate_digit(cpf_digits, position):
            sum_result = sum(int(digit) * weight for digit, weight in zip(cpf_digits, range(position, 1, -1)))
            remainder = sum_result % 11
            return 0 if remainder < 2 else 11 - remainder

        first_digit = calculate_digit(cpf[:9], 10)
        if int(cpf[9]) != first_digit:
            raise ValidationError("CPF inválido - primeiro dígito verificador")

        second_digit = calculate_digit(cpf[:10], 11)
        if int(cpf[10]) != second_digit:
            raise ValidationError("CPF inválido - segundo dígito verificador")
        
        return cpf
    
    @staticmethod
    def validate_date(date_str: str, field_name: str) -> date:
        """Valida e converte string de data"""
        date_str = Validators.validate_non_empty_string(date_str, field_name)
        
        try:
            parsed_date = date.fromisoformat(date_str)
        except ValueError:
            raise ValidationError(f"{field_name} deve estar no formato AAAA-MM-DD")
        
        return parsed_date
    
    @staticmethod
    def validate_expiration_date(expiration_date: date) -> date:
        """Valida se a data de validade não está no passado"""
        if expiration_date < date.today():
            raise ValidationError("Data de validade não pode ser anterior à data atual")
        
        return expiration_date
    
    @staticmethod
    def validate_price(price: float) -> float:
        """Valida preço com formatação específica"""
        price = Validators.validate_positive_number(price, "Preço")

        if round(price, 2) != price:
            raise ValidationError("Preço deve ter no máximo 2 casas decimais")

        if price > 999999.99:
            raise ValidationError("Preço não pode ser maior que R$ 999.999,99")
        
        return price
    
    @staticmethod
    def validate_name(name: str) -> str:
        """Valida nome do produto com regras específicas"""
        name = Validators.validate_non_empty_string(name, "Nome")

        if len(name) < 2:
            raise ValidationError("Nome deve ter pelo menos 2 caracteres")
        
        if len(name) > 100:
            raise ValidationError("Nome deve ter no máximo 100 caracteres")

        if not re.match(r'^[a-zA-Z0-9\sÀ-ÿ\-\.\,\(\)]+$', name):
            raise ValidationError("Nome contém caracteres inválidos")
        
        return name.title()  # Capitaliza o nome
    
    @staticmethod
    def validate_description(description: str) -> str:
        """Valida descrição com regras específicas"""
        description = Validators.validate_non_empty_string(description, "Descrição")
        
        if len(description) > 500:
            raise ValidationError("Descrição deve ter no máximo 500 caracteres")
        
        return description
    
    @staticmethod
    def validate_brand(brand: str) -> str:
        """Valida marca com regras específicas"""
        brand = Validators.validate_non_empty_string(brand, "Marca")
        
        if len(brand) < 2:
            raise ValidationError("Marca deve ter pelo menos 2 caracteres")
        
        if len(brand) > 50:
            raise ValidationError("Marca deve ter no máximo 50 caracteres")

        if not re.match(r'^[a-zA-Z0-9\sÀ-ÿ\-\.\&]+$', brand):
            raise ValidationError("Marca contém caracteres inválidos")
        
        return brand.title() 
    
    @staticmethod
    def validate_seller_name(name: str) -> str:
        """Valida nome do vendedor"""
        name = Validators.validate_non_empty_string(name, "Nome do vendedor")
        
        if len(name) < 2:
            raise ValidationError("Nome do vendedor deve ter pelo menos 2 caracteres")
        
        if len(name) > 100:
            raise ValidationError("Nome do vendedor deve ter no máximo 100 caracteres")

        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', name):
            raise ValidationError("Nome do vendedor deve conter apenas letras e espaços")
        
        return name.title()
    
    @staticmethod
    def validate_quantity_for_sale(requested_quantity: int, available_quantity: int) -> int:
        """Valida se há quantidade suficiente para venda"""
        requested_quantity = Validators.validate_positive_integer(requested_quantity, "Quantidade")
        
        if requested_quantity > available_quantity:
            raise ValidationError(f"Quantidade solicitada ({requested_quantity}) é maior que o disponível em estoque ({available_quantity})")
        
        return requested_quantity

def safe_input(prompt: str, validator_func, *args):
    """Função helper para entrada segura de dados com validação"""
    while True:
        try:
            user_input = input(prompt).strip()
            if validator_func:
                return validator_func(user_input, *args)
            return user_input
        except ValidationError as e:
            print(f"Erro: {e}")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")

def safe_input_number(prompt: str, number_type=float, validator_func=None, *args):
    """Função helper para entrada segura de números"""
    while True:
        try:
            user_input = input(prompt).strip()
            number_value = number_type(user_input)
            if validator_func:
                return validator_func(number_value, *args)
            return number_value
        except ValueError:
            type_name = "número inteiro" if number_type == int else "número"
            print(f"Erro: Digite um {type_name} válido")
        except ValidationError as e:
            print(f"Erro: {e}")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")

def safe_input_date(prompt: str, field_name: str, validate_future=False):
    """Função helper para entrada segura de datas"""
    while True:
        try:
            date_input = input(prompt).strip()
            parsed_date = Validators.validate_date(date_input, field_name)
            if validate_future:
                parsed_date = Validators.validate_expiration_date(parsed_date)
            return parsed_date
        except ValidationError as e:
            print(f"Erro: {e}")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")

def safe_input_yes_no(prompt: str):
    """Função helper para entrada segura de sim/não"""
    while True:
        try:
            user_input = input(prompt).strip().lower()
            if user_input in ['s', 'sim', 'y', 'yes']:
                return True
            elif user_input in ['n', 'não', 'nao', 'no']:
                return False
            else:
                print("Erro: Digite 's' para sim ou 'n' para não")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")

def safe_input_date_optional(prompt: str, field_name: str, validate_future=False):
    """Função helper para entrada segura de datas opcionais"""
    while True:
        try:
            date_input = input(prompt).strip()
            if not date_input:
                return None
            parsed_date = Validators.validate_date(date_input, field_name)
            if validate_future:
                parsed_date = Validators.validate_expiration_date(parsed_date)
            return parsed_date
        except ValidationError as e:
            print(f"Erro: {e}")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")