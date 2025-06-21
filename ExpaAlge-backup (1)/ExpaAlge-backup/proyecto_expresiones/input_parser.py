"""
Módulo para convertir expresiones algebraicas en texto a expresiones simbólicas de sympy.
Este módulo maneja la conversión de la entrada del usuario a un formato que sympy puede procesar.

Funcionalidades:
- Conversión de notación matemática común (^) a notación Python (**)
- Conversión de expresiones LaTeX a formato SymPy
- Validación de expresiones
- Manejo de errores de sintaxis
"""

import re
from sympy import sympify, Symbol, symbols, latex
from sympy.core.sympify import SympifyError
from utils import clean_expression, is_valid_expression

class InputParser:
    """
    Clase encargada de convertir expresiones algebraicas en texto a expresiones simbólicas.
    Maneja la conversión de la notación matemática común y LaTeX a la notación de Python.
    
    Atributos:
        variables (set): Conjunto de variables válidas en las expresiones
    """
    def __init__(self):
        """Inicializa el parser con las variables permitidas."""
        self.variables = set()  # Se detectarán automáticamente

    def parse_expression(self, expr_str: str, is_latex: bool = False):
        """
        Convierte una cadena de texto a una expresión simbólica de sympy.
        
        Args:
            expr_str (str): Expresión algebraica en texto
            is_latex (bool): Si la entrada está en formato LaTeX
            
        Returns:
            dict: Diccionario con el resultado del procesamiento
        """
        try:
            print(f"DEBUG: InputParser - Procesando: '{expr_str}'")
            print(f"DEBUG: InputParser - Es LaTeX: {is_latex}")
            
            # Limpiar la expresión
            expr_str = clean_expression(expr_str)
            print(f"DEBUG: InputParser - Expresión limpia: '{expr_str}'")
            
            if not expr_str:
                return {
                    "success": False,
                    "error": "No se proporcionó una expresión"
                }
            
            # Validar la expresión
            if not is_valid_expression(expr_str):
                return {
                    "success": False,
                    "error": "La expresión no es válida"
                }
            
            # Convertir LaTeX a formato sympy si es necesario
            if is_latex:
                print("DEBUG: InputParser - Convirtiendo LaTeX a SymPy...")
                expr_str = self._latex_to_sympy(expr_str)
                print(f"DEBUG: InputParser - Expresión convertida: '{expr_str}'")
            
            # Detectar variables en la expresión
            self.variables = set(re.findall(r'[a-zA-Z]', expr_str))
            print(f"DEBUG: InputParser - Variables detectadas: {self.variables}")
            
            # Crear símbolos para las variables
            sympy_vars = {}
            for var in self.variables:
                sympy_vars[var] = symbols(var)
            
            # Convertir la expresión a formato sympy
            print("DEBUG: InputParser - Convirtiendo a expresión SymPy...")
            sympy_expr = self._string_to_sympy(expr_str, sympy_vars)
            print(f"DEBUG: InputParser - Expresión SymPy: {sympy_expr}")
            
            return {
                "success": True,
                "expression": sympy_expr,
                "variables": self.variables,
                "original": expr_str
            }
            
        except Exception as e:
            print(f"DEBUG: InputParser - Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Error al procesar la expresión: {str(e)}"
            }
    def _latex_to_sympy(self, latex_expr: str) -> str:
        import re
        result = latex_expr
    
        # Elimina comandos \left y \right
        result = result.replace('\\left', '').replace('\\right', '')
    
        # Reemplazos básicos de LaTeX a sympy
        replacements = {
            r'\cdot': '*',
            r'\times': '*',
            r'\div': '/',
            r'\pi': 'pi',
            r'\infty': 'oo'
        }
        for latex_sym, sympy_sym in replacements.items():
            result = result.replace(latex_sym, sympy_sym)
    
        # Fracciones
        result = re.sub(r'\\frac{([^}]+)}{([^}]+)}', r'(\1)/(\2)', result)
    
        # Exponentes: ^{...} y ^x
        result = re.sub(r'\^\{([^}]+)\}', r'**(\1)', result)
        result = re.sub(r'\^([a-zA-Z0-9])', r'**\1', result)
    
        # Multiplicación implícita: exponente seguido de paréntesis
        result = re.sub(r'(\)\*\*\d+)(\()', r'\1*\2', result)
        result = re.sub(r'(\)\*\*\([^\)]+\))(\()', r'\1*\2', result)
        result = re.sub(r'(\))(\()', r'\1*\2', result)
        result = re.sub(r'(\d|\w)(\()', r'\1*\2', result)
        result = re.sub(r'(\))(\w|\d)', r'\1*\2', result)
    
        # Elimina cualquier backslash restante
        result = result.replace('\\', '')
    
        # Elimina espacios extra
        result = result.replace(' ', '')

        # --- INSERCIÓN DE MULTIPLICACIÓN IMPLÍCITA ---
        # Insertar multiplicación entre número y paréntesis o variable
        result = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', result)
        # Insertar multiplicación entre paréntesis y paréntesis
        result = re.sub(r'(\))(\()', r'\1*\2', result)
        # Insertar multiplicación entre paréntesis y variable
        result = re.sub(r'(\))([a-zA-Z])', r'\1*\2', result)

        print(f"DEBUG: InputParser - Resultado de conversión: '{result}'")
        return result
    
    def _string_to_sympy(self, expr_str: str, variables: dict):
        """
        Convierte una cadena de texto a expresión sympy.
        
        Args:
            expr_str (str): Expresión como cadena
            variables (dict): Diccionario de variables sympy
            
        Returns:
            sympy.Expr: Expresión sympy
        """
        # Crear un entorno local con las variables
        local_dict = variables.copy()
        
        # Agregar funciones matemáticas básicas
        from sympy import sqrt, sin, cos, tan, log, exp, pi, oo
        local_dict.update({
            'sqrt': sqrt,
            'sin': sin,
            'cos': cos,
            'tan': tan,
            'log': log,
            'exp': exp,
            'pi': pi,
            'oo': oo
        })
        
        # Agregar constantes matemáticas
        local_dict.update({
            'e': exp(1),
            'i': 1j
        })
        
        # Crear un entorno seguro para eval
        safe_dict = {"__builtins__": {}}
        safe_dict.update(local_dict)
        
        try:
            # Evaluar la expresión
            return eval(expr_str, safe_dict)
        except Exception as e:
            # Si falla, intentar con una evaluación más simple
            raise ValueError(f"No se pudo evaluar la expresión '{expr_str}': {str(e)}")

    def parse(self, expr_str):
        """
        Método legacy para compatibilidad.
        
        Args:
            expr_str (str): Expresión algebraica en texto
            
        Returns:
            sympy.Expr: Expresión simbólica de sympy
        """
        result = self.parse_expression(expr_str, is_latex=False)
        if result["success"]:
            return result["expression"]
        else:
            raise ValueError(result["error"])

    def parse_latex(self, latex_expr):
        """
        Convierte una cadena de texto en formato LaTeX a un objeto de expresión SymPy.
        
        Args:
            latex_expr (str): La expresión en formato LaTeX.
            
        Returns:
            Expression: Un objeto de expresión de SymPy.
            
        Raises:
            ValueError: Si la expresión LaTeX no es sintácticamente válida o no puede ser convertida.
        """
        try:
            # Usar nuestro método de conversión manual
            converted = self._latex_to_sympy(latex_expr)
            expr = sympify(converted)
            return expr
                
        except Exception as e:
            raise ValueError(f"Expresión LaTeX inválida '{latex_expr}': {str(e)}")
    
    def validate_expression(self, expr_str, format_type="text"):
        """
        Valida si una expresión dada es parseable por la clase.
        
        Args:
            expr_str (str): La expresión a validar.
            format_type (str): El tipo de formato de la expresión ("text" para estándar, "latex" para LaTeX).
            
        Returns:
            tuple: Una tupla que contiene:
                   - `True` si la expresión es válida y parseable.
                   - `False` si la expresión no es válida.
                   - `None` si es válida, o una cadena de texto con el mensaje de error si no lo es.
        """
        try:
            if format_type == "latex":
                self.parse_latex(expr_str)
            else:
                self.parse(expr_str)
            return True, None
        except ValueError as e:
            return False, str(e)
    
    def get_variables(self, expr_str, format_type="text"):
        """
        Obtiene el conjunto de variables simbólicas presentes en una expresión.
        
        Args:
            expr_str (str): La expresión matemática como una cadena de texto.
            format_type (str): El tipo de formato de la expresión ("text" o "latex").
            
        Returns:
            set: Un conjunto de objetos de símbolos de SymPy que representan las variables encontradas.
        """
        try:
            if format_type == "latex":
                expr = self.parse_latex(expr_str)
            else:
                expr = self.parse(expr_str)
            
            return expr.free_symbols
            
        except ValueError:
            return set() 