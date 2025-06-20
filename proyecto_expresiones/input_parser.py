"""
Módulo para parsear expresiones algebraicas desde diferentes formatos.
Soporta tanto sintaxis matemática estándar como LaTeX.
"""

from sympy import sympify # Importa la función 'sympify' de la librería SymPy. Esta función es clave: toma una cadena de texto (como "x + y") y la convierte en un objeto de expresión simbólica que SymPy puede manipular.
from sympy.parsing.latex import parse_latex # Importa la función 'parse_latex' de un submódulo específico de SymPy. Esta función está diseñada para interpretar cadenas de texto en formato LaTeX y convertirlas directamente en expresiones simbólicas de SymPy. Esta fue la línea que causó el error anterior y que se corrigió.
from sympy.core.sympify import SympifyError # Importa 'SympifyError', que es una excepción específica que SymPy lanza cuando la función 'sympify' no puede entender o convertir una cadena dada en una expresión simbólica válida. Esto nos permite manejar errores de parseo de forma específica.
import re # Importa el módulo 're' (regular expressions). Este módulo es fundamental para realizar búsquedas y reemplazos de patrones de texto complejos en las cadenas de entrada, especialmente útil para normalizar la sintaxis.

class InputParser:
    """
    Clase para convertir cadenas de texto en expresiones simbólicas de SymPy.
    Soporta múltiples formatos de entrada incluyendo LaTeX.
    """
    
    def __init__(self):
        """
        Constructor de la clase InputParser.
        Inicializa los patrones de expresiones regulares que se usarán para
        pre-procesar las cadenas LaTeX antes de pasarlas a SymPy.
        """
        # Patrones de conversión de LaTeX a SymPy
        self.latex_patterns = [
            # La lista 'latex_patterns' contiene tuplas, donde cada tupla es (patrón_regex, reemplazo).
            # Estos patrones son usados por el método 'latex_to_sympy' para traducir sintaxis LaTeX común
            # a una forma que SymPy pueda entender mejor, especialmente cuando 'parse_latex' nativo falla o no es suficiente.

            (r'\^{([^}]+)}', r'**(\1)'),  # Patrón 1: Convierte potencias con llaves como `x^{2}` a `x**(2)`.
                                          # `\^` coincide con el símbolo de potencia. `([^}]+)` captura cualquier carácter
                                          # excepto '}' una o más veces (el exponente), y `\1` lo inserta en el reemplazo.
                                          # `**` es el operador de potencia en Python.

            (r'\^([a-zA-Z0-9])', r'**\1'),  # Patrón 2: Convierte potencias simples como `x^2` (donde el exponente es un solo carácter alfanumérico)
                                          # a `x**2`. Similar al anterior, pero para exponentes sin llaves.

            (r'\\cdot', '*'),             # Patrón 3: Reemplaza el comando LaTeX `\cdot` (punto de multiplicación) por el operador `*`.
            (r'\\times', '*'),            # Patrón 4: Reemplaza el comando LaTeX `\times` (símbolo de multiplicación en cruz) por el operador `*`.

            (r'\\left\(', '('),           # Patrón 5: Reemplaza el comando LaTeX `\left(` (paréntesis izquierdo escalable) por un simple `(`.
            (r'\\right\)', ')'),         # Patrón 6: Reemplaza el comando LaTeX `\right)` (paréntesis derecho escalable) por un simple `)`.
            # Los siguientes son similares para otros tipos de corchetes/llaves escalables de LaTeX:
            (r'\\left\[', '['),           # Patrón 7: `\left[` a `[`.
            (r'\\right\]', ']'),          # Patrón 8: `\right]` a `]`.
            (r'\\left\{', '{'),           # Patrón 9: `\left{` a `{`.
            (r'\\right\}', '}'),          # Patrón 10: `\right}` a `}`.

            (r'\\frac{([^}]+)}{([^}]+)}', r'(\1)/(\2)'), # Patrón 11: Convierte fracciones LaTeX `\frac{numerador}{denominador}`
                                                       # a la sintaxis `(numerador)/(denominador)`.
                                                       # `([^}]+)` captura el numerador y el denominador, y `\1`, `\2` los insertan.
        ]
    
    def clean_expression(self, expr_str):
        """
        Limpia y normaliza una expresión matemática de texto plano.
        Esta función se encarga de estandarizar la sintaxis de las expresiones para que SymPy las entienda correctamente,
        especialmente agregando multiplicaciones implícitas y normalizando el operador de potencia.
        
        Args:
            expr_str (str): La cadena de texto de la expresión a limpiar.
            
        Returns:
            str: La expresión limpia y normalizada.
        """
        # Eliminar espacios extra
        expr_str = expr_str.strip() # `.strip()` elimina cualquier espacio en blanco al inicio y al final de la cadena.
        
        # Reemplazar ^ por ** para potencias
        expr_str = expr_str.replace("^", "**") # Reemplaza el operador de potencia `^` (común en matemáticas) por `**`,
                                              # que es la sintaxis de potencia en Python y SymPy.
        
        # Agregar multiplicación implícita entre número y variable (ej. "2x" -> "2*x")
        # `r'(\d)([a-zA-Z])'` busca un dígito `\d` seguido de una letra `[a-zA-Z]`.
        # `\1` y `\2` se refieren a los grupos capturados (el dígito y la letra).
        # `r'\1*\2'` inserta un `*` entre ellos.
        expr_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr_str)
        
        # Agregar multiplicación implícita entre paréntesis (ej. "(x+1)(y-1)" -> "(x+1)*(y-1)")
        # `r'\)(\('` busca un paréntesis de cierre `)` seguido inmediatamente de un paréntesis de apertura `(`.
        # `r')*\1'` inserta un `*` entre ellos.
        expr_str = re.sub(r'\)(\()', r')*\1', expr_str)

        # Agregar multiplicación implícita entre un paréntesis de cierre y una variable (ej. "(x+1)y" -> "(x+1)*y")
        # `r'(\))([a-zA-Z])'` busca un paréntesis de cierre capturado `(\))` seguido de una letra `([a-zA-Z])`.
        expr_str = re.sub(r'(\))([a-zA-Z])', r'\1*\2', expr_str)

        # Agregar multiplicación implícita entre una variable y un paréntesis de apertura (ej. "x(y+1)" -> "x*(y+1)")
        # `r'([a-zA-Z])(\()'` busca una letra capturada `([a-zA-Z])` seguida de un paréntesis de apertura `(\()`.
        expr_str = re.sub(r'([a-zA-Z])(\()', r'\1*\2', expr_str)
        
        return expr_str # Retorna la cadena de expresión después de todas las normalizaciones.
    
    def latex_to_sympy(self, latex_expr):
        """
        Convierte una expresión LaTeX a un formato de cadena compatible con SymPy
        aplicando una serie de reemplazos basados en expresiones regulares.
        Este es un pre-procesador manual, útil para cubrir casos que el parser nativo de SymPy podría no manejar.
        
        Args:
            latex_expr (str): La cadena de la expresión en formato LaTeX.
            
        Returns:
            str: La expresión LaTeX convertida a una sintaxis más cercana a la de SymPy.
        """
        result = latex_expr # Inicia el resultado con la expresión LaTeX original.
        
        # Aplicar patrones de conversión
        for pattern, replacement in self.latex_patterns: # Itera sobre cada tupla (patrón, reemplazo) definida en `self.latex_patterns`.
            result = re.sub(pattern, replacement, result) # Aplica el reemplazo de expresión regular. 're.sub' busca el 'pattern'
                                                         # en 'result' y lo reemplaza con 'replacement'.
        
        # Limpiar la expresión resultante
        # Aunque ya es LaTeX pre-procesado, esta llamada aplica reglas adicionales como
        # la inserción de '*' para multiplicaciones implícitas, lo cual es útil incluso después de la conversión de LaTeX.
        result = self.clean_expression(result) 
        
        return result # Retorna la cadena final pre-procesada.
    
    def parse(self, expr_str):
        """
        Convierte una cadena de texto (en sintaxis matemática estándar) a un objeto de expresión SymPy.
        Esta es la función principal para el parseo de expresiones no LaTeX.
        
        Args:
            expr_str (str): La expresión matemática como una cadena de texto.
            
        Returns:
            Expression: Un objeto de expresión de SymPy.
            
        Raises:
            ValueError: Si la expresión no es sintácticamente válida y no puede ser parseada por SymPy.
        """
        try: # Bloque try-except para manejar posibles errores durante el parseo.
            # Limpiar y normalizar la expresión
            clean_expr = self.clean_expression(expr_str) # Primero, se normaliza la cadena de entrada usando `clean_expression`.
                                                        # Esto es crucial para que `sympify` la entienda.
            
            # Intentar convertir a expresión SymPy
            expr = sympify(clean_expr) # Aquí es donde la cadena limpia se convierte en un objeto SymPy.
                                       # SymPy intentará interpretar la cadena como una expresión matemática.
            
            return expr # Si todo va bien, la expresión SymPy es retornada.
            
        except SympifyError as e: # Si `sympify` no puede parsear la cadena, lanza un `SympifyError`.
            # Captura el error específico de SymPy y lo encapsula en un `ValueError` más informativo.
            raise ValueError(f"Expresión inválida '{expr_str}': {str(e)}")
        except Exception as e: # Captura cualquier otro tipo de excepción inesperada que pueda ocurrir.
            # Esto es un "catch-all" para problemas no relacionados directamente con `SympifyError`.
            raise ValueError(f"Error al procesar la expresión '{expr_str}': {str(e)}")
    
    def parse_latex(self, latex_expr):
        """
        Convierte una cadena de texto en formato LaTeX a un objeto de expresión SymPy.
        Intenta usar el parser nativo de SymPy para LaTeX primero, y si falla, recurre a
        un pre-procesamiento manual seguido de 'sympify'.
        
        Args:
            latex_expr (str): La expresión en formato LaTeX.
            
        Returns:
            Expression: Un objeto de expresión de SymPy.
            
        Raises:
            ValueError: Si la expresión LaTeX no es sintácticamente válida o no puede ser convertida.
        """
        try: # Bloque try-except principal para manejar errores en todo el proceso de parseo de LaTeX.
            # Intentar usar el parser nativo de LaTeX de SymPy primero
            try: # Primer intento: usar la función 'parse_latex' nativa de SymPy, que es robusta para muchas expresiones LaTeX.
                expr = parse_latex(latex_expr) # Intenta parsear la cadena LaTeX directamente.
                return expr # Si es exitoso, retorna la expresión SymPy.
            except: # Si 'parse_latex' falla por alguna razón (ej. sintaxis LaTeX no totalmente soportada por el parser nativo).
                # Si falla, usar conversión manual (nuestro pre-procesamiento)
                # Esta es una estrategia de "fallback" para manejar LaTeX que el parser nativo no puede,
                # pero que nuestros patrones regex sí pueden traducir a una forma parseable por `sympify`.
                converted = self.latex_to_sympy(latex_expr) # Pre-procesa la cadena LaTeX usando nuestro método `latex_to_sympy`.
                expr = sympify(converted) # Intenta convertir la cadena pre-procesada a un objeto SymPy.
                return expr # Retorna la expresión SymPy si esta segunda opción tiene éxito.
                
        except Exception as e: # Captura cualquier excepción que pueda ocurrir en cualquiera de los dos intentos de parseo.
            # Lanza un `ValueError` genérico indicando que la expresión LaTeX es inválida.
            raise ValueError(f"Expresión LaTeX inválida '{latex_expr}': {str(e)}")
    
    def validate_expression(self, expr_str, format_type="text"):
        """
        Valida si una expresión dada es parseable por la clase, sin devolver el objeto SymPy.
        Es útil para verificar la validez de la entrada antes de intentar usarla para cálculos.
        
        Args:
            expr_str (str): La expresión a validar.
            format_type (str): El tipo de formato de la expresión ("text" para estándar, "latex" para LaTeX).
            
        Returns:
            tuple: Una tupla que contiene:
                   - `True` si la expresión es válida y parseable.
                   - `False` si la expresión no es válida.
                   - `None` si es válida, o una cadena de texto con el mensaje de error si no lo es.
        """
        try: # Bloque try-except para intentar parsear la expresión y capturar errores.
            if format_type == "latex": # Si el formato especificado es LaTeX.
                self.parse_latex(expr_str) # Intenta parsear la expresión usando el método `parse_latex`.
            else: # Si el formato es texto estándar.
                self.parse(expr_str) # Intenta parsear la expresión usando el método `parse`.
            return True, None # Si ninguna excepción es lanzada, la expresión es válida. Retorna `True` y `None` (sin error).
        except ValueError as e: # Si `parse` o `parse_latex` lanzan un `ValueError` (indicando una expresión inválida).
            return False, str(e) # Retorna `False` y el mensaje de error de la excepción.
    
    def get_variables(self, expr_str, format_type="text"):
        """
        Obtiene el conjunto de variables simbólicas (símbolos libres) presentes en una expresión.
        
        Args:
            expr_str (str): La expresión matemática como una cadena de texto.
            format_type (str): El tipo de formato de la expresión ("text" o "latex").
            
        Returns:
            set: Un conjunto de objetos de símbolos de SymPy que representan las variables encontradas.
                 Retorna un conjunto vacío si la expresión no es válida o no contiene variables.
        """
        try: # Bloque try-except para manejar errores durante el parseo de la expresión.
            if format_type == "latex": # Si el formato especificado es LaTeX.
                expr = self.parse_latex(expr_str) # Parsea la expresión LaTeX a un objeto SymPy.
            else: # Si el formato es texto estándar.
                expr = self.parse(expr_str) # Parsea la expresión de texto a un objeto SymPy.
            
            # `free_symbols` es una propiedad de los objetos de expresión de SymPy que devuelve
            # un conjunto de todos los símbolos (variables) que no están "ligados" o son constantes.
            return expr.free_symbols 
            
        except ValueError: # Si ocurre un `ValueError` durante el parseo (es decir, la expresión es inválida).
            return set() # Retorna un conjunto vacío, ya que no se pudieron extraer variables de una expresión inválida.