"""
Módulo para expandir expresiones algebraicas usando sympy.
Este módulo proporciona funcionalidad para expandir expresiones matemáticas,
distribuyendo factores y simplificando términos.

Funcionalidades:
- Expansión de expresiones algebraicas
- Simplificación de términos
- Distribución de factores
"""

from sympy import expand, simplify, factor, collect
from sympy.core.expr import Expr
from input_parser import InputParser  # Importa el parser para convertir cadenas a expresiones SymPy
from latex_exporter import LatexExporter  # Importa el exportador para convertir expresiones a LaTeX

class Expander:
    """
    Clase para expandir expresiones algebraicas usando SymPy.
    Convierte productos de factores en sumas de términos y centraliza el flujo de procesamiento para la GUI y CLI.
    """
    def __init__(self):
        """Inicializa el expandidor."""
        pass

    @staticmethod
    def expand_expression(expr):
        """
        Expande una expresión algebraica (distribuye factores).
        Args:
            expr: Expresión SymPy a expandir
        Returns:
            Expression: Expresión expandida
        Raises:
            TypeError: Si la expresión no es válida
            Exception: Si ocurre un error durante la expansión
        """
        if not isinstance(expr, Expr):
            raise TypeError(f"Se esperaba una expresión SymPy, se recibió: {type(expr)}")
        try:
            # Expandir la expresión
            expanded = expand(expr)
            return expanded
        except Exception as e:
            raise Exception(f"Error al expandir la expresión: {str(e)}")

    @staticmethod
    def expand_and_simplify(expr):
        """
        Expande y simplifica una expresión algebraica.
        Args:
            expr: Expresión SymPy a expandir y simplificar
        Returns:
            Expression: Expresión expandida y simplificada
        """
        expanded = Expander.expand_expression(expr)
        simplified = simplify(expanded)
        return simplified

    @staticmethod
    def expand_and_collect(expr, variables=None):
        """
        Expande una expresión y agrupa términos por variables especificadas.
        Args:
            expr: Expresión SymPy a expandir
            variables: Variables por las cuales agrupar (opcional)
        Returns:
            Expression: Expresión expandida y agrupada
        """
        expanded = Expander.expand_expression(expr)
        if variables is None:
            # Si no se especifican variables, usar todas las variables libres
            variables = list(expanded.free_symbols)
        if variables:
            collected = collect(expanded, variables)
            return collected
        else:
            return expanded

    @staticmethod
    def is_factored_form(expr):
        """
        Verifica si una expresión está en forma factorizada.
        Args:
            expr: Expresión SymPy a verificar
        Returns:
            bool: True si está factorizada, False si no
        """
        try:
            # Una expresión está factorizada si expandirla la cambia
            expanded = expand(expr)
            return expr != expanded
        except:
            return False

    @staticmethod
    def get_expansion_info(expr):
        """
        Obtiene información detallada sobre la expansión de una expresión.
        Args:
            expr: Expresión SymPy a analizar
        Returns:
            dict: Diccionario con información sobre la expansión
        """
        try:
            original = expr
            expanded = Expander.expand_expression(expr)
            info = {
                'original': original,
                'expanded': expanded,
                'is_factored': Expander.is_factored_form(original),
                'variables': list(original.free_symbols),
                'degree': expanded.as_poly().total_degree() if expanded.free_symbols else 0,
                'terms_count': len(expanded.as_ordered_terms()) if hasattr(expanded, 'as_ordered_terms') else 1,
                'changed': original != expanded
            }
            return info
        except Exception as e:
            return {
                'original': expr,
                'expanded': expr,
                'error': str(e),
                'changed': False
            }

    @staticmethod
    def process_expression(expression: str, is_latex: bool = False) -> dict:
        """
        Procesa una expresión algebraica: la parsea, expande y convierte a LaTeX.
        Args:
            expression (str): La expresión a procesar.
            is_latex (bool): Si la entrada es LaTeX.
        Returns:
            dict: Resultados del procesamiento (original, expandida, LaTeX, error, etc).
        """
        parser = InputParser()  # Crea una instancia del parser para analizar la expresión
        latex_exporter = LatexExporter()  # Crea una instancia del exportador a LaTeX
        try:
            expr = parser.parse_latex(expression) if is_latex else parser.parse(expression)
            expanded = Expander.expand_expression(expr)
            return {
                "success": True,
                "original": str(expr),
                "expanded": str(expanded),
                "original_latex": latex_exporter.to_latex(expr),
                "expanded_latex": latex_exporter.to_latex(expanded),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original": expression
            } 