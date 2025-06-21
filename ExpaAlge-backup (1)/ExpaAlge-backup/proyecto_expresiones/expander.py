# Importaciones de SymPy para manipulación simbólica
from sympy import expand, simplify, factor, collect  # Funciones principales de álgebra simbólica
from sympy.core.expr import Expr  # Tipo base de expresiones SymPy
from input_parser import InputParser  # Importa el parser para convertir cadenas a expresiones SymPy
from latex_exporter import LatexExporter  # Importa el exportador para convertir expresiones a LaTeX

class Expander:
    """
    Clase para expandir expresiones algebraicas usando SymPy.
    Convierte productos de factores en sumas de términos y centraliza el flujo de procesamiento para la GUI y CLI.
    """
    def __init__(self):
        """Inicializa el expandidor. (No requiere atributos de instancia actualmente)"""
        pass

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
        parser = InputParser()  # Instancia del parser para convertir texto/LaTeX a SymPy
        latex_exporter = LatexExporter()  # Instancia del exportador para convertir a LaTeX
        try:
            # Parsea la expresión según el formato
            expr = parser.parse_latex(expression) if is_latex else parser.parse(expression)
            # Expande la expresión simbólica
            expanded = Expander.expand_expression(expr)
            return {
                "success": True,
                "original": str(expr),  # Expresión original en texto
                "expanded": str(expanded),  # Expresión expandida en texto
                "original_latex": latex_exporter.to_latex(expr),  # LaTeX de la original
                "expanded_latex": latex_exporter.to_latex(expanded),  # LaTeX de la expandida
                "error": None
            }
        except Exception as e:
            # Siempre retorna todas las claves, aunque estén vacías
            return {
                "success": False,
                "error": str(e),
                "original": expression,
                "expanded": "",
                "original_latex": "",
                "expanded_latex": ""
            }

    @staticmethod
    def expand_expression(expr):
        """
        Expande una expresión algebraica usando sympy.expand.
        Args:
            expr: Expresión SymPy a expandir
        Returns:
            Expression: Expresión expandida
        """
        return expand(expr)  # Llama a la función expand de SymPy

    @staticmethod
    def expand_and_simplify(expr):
        """
        Expande y simplifica una expresión algebraica.
        Args:
            expr: Expresión SymPy a expandir y simplificar
        Returns:
            Expression: Expresión expandida y simplificada
        """
        expanded = Expander.expand_expression(expr)  # Expande primero
        simplified = simplify(expanded)  # Luego simplifica
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
        expanded = Expander.expand_expression(expr)  # Expande la expresión
        if variables is None:
            # Si no se especifican variables, usar todas las variables libres
            variables = list(expanded.free_symbols)
        if variables:
            collected = collect(expanded, variables)  # Agrupa por variables
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
        except Exception:
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
                'original': original,  # Expresión original
                'expanded': expanded,  # Expresión expandida
                'is_factored': Expander.is_factored_form(original),  # ¿Estaba factorizada?
                'variables': list(original.free_symbols),  # Variables presentes
                'degree': expanded.as_poly().total_degree() if expanded.free_symbols else 0,  # Grado total
                'terms_count': len(expanded.as_ordered_terms()) if hasattr(expanded, 'as_ordered_terms') else 1,  # Número de términos
                'changed': original != expanded  # ¿Cambió tras expandir?
            }
            return info
        except Exception as e:
            return {
                'original': expr,
                'expanded': expr,
                'error': str(e),
                'changed': False
            }