"""
Módulo de utilidades para el Expansor Algebraico.
Contiene funciones auxiliares y herramientas esenciales para el parseo y validación de expresiones.
"""

import re

# --- VALIDACIÓN DE EXPRESIONES ---
def validate_mathematical_expression(expr_str):
    """
    Valida si una cadena de texto tiene la estructura básica de una expresión matemática válida.
    Realiza varias comprobaciones, como caracteres permitidos, balanceo de paréntesis y uso de operadores.
    No es un validador sintáctico completo (para eso se usa SymPy), pero filtra errores obvios.
    """
    problems = []
    if not expr_str or not expr_str.strip():
        problems.append("La expresión está vacía")
        return False, problems
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/^()[]{}= .')
    invalid_chars = set(expr_str) - valid_chars 
    if invalid_chars:
        problems.append(f"Caracteres inválidos encontrados: {', '.join(invalid_chars)}")
    if not are_parentheses_balanced(expr_str):
        problems.append("Paréntesis no balanceados")
    if re.match(r'^[+\-*/^]', expr_str.strip()): 
        problems.append("La expresión no puede empezar con un operador")
    if re.search(r'[+\-*/^]$', expr_str.strip()):
        problems.append("La expresión no puede terminar con un operador")
    if re.search(r'[+\-*/^]{2,}', expr_str):
        problems.append("Operadores consecutivos encontrados")
    return len(problems) == 0, problems

def are_parentheses_balanced(expr_str):
    """
    Verifica si todos los tipos de paréntesis (redondos, cuadrados, llaves) están correctamente balanceados
    en una expresión. Utiliza una pila (stack) para rastrear los paréntesis de apertura.
    """
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    for char in expr_str:
        if char in pairs:
            stack.append(char)
        elif char in pairs.values():
            if not stack:
                return False
            if pairs[stack.pop()] != char:
                return False
    return len(stack) == 0

# --- LIMPIEZA DE EXPRESIONES ---
def clean_expression(expr_str):
    """
    Elimina espacios de una expresión matemática para facilitar el parseo.
    """
    return expr_str.replace(' ', '')

# Alias para compatibilidad
is_valid_expression = validate_mathematical_expression