"""
ENUMs garantem que o código seja mais claro e menos sujeito a erros, além de facilitar validações. 
Usaremos o módulo enum do Python para criar o PaymentMethod e ajustaremos o código para utilizar-
este Enum nos repositórios, serviços e nas views. O Enum FormaPagamento substitui strings cruas, tornando o código mais seguro e legível.
"""

from enum import Enum

class PaymentMethod(Enum):
    PIX = 'P'
    CREDIT_CARD = 'C'
    DEBIT_CARD = 'D'
