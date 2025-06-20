"""
Módulo de utilidades para el Expansor Algebraico.
Contiene funciones auxiliares y herramientas.
"""

import re # Importa el módulo 're' (regular expressions) para operaciones con expresiones regulares, útil para buscar y manipular patrones en cadenas de texto.
import logging # Importa el módulo 'logging' para configurar y usar un sistema de registro (logs) de eventos y mensajes de la aplicación.
from datetime import datetime # Importa la clase 'datetime' del módulo 'datetime' para trabajar con fechas y horas, usada para generar marcas de tiempo.
from config import APP_NAME, APP_VERSION # Importa las variables 'APP_NAME' (nombre de la aplicación) y 'APP_VERSION' (versión de la aplicación) desde el archivo de configuración.

def setup_logging(log_level=logging.INFO):
    """
    Configura el sistema de logging de la aplicación.
    Establece dónde se guardarán los logs (archivo y consola) y el formato de los mensajes.
    
    Args:
        log_level: Nivel de logging deseado (ej. logging.INFO, logging.DEBUG, logging.ERROR).
                   Por defecto, se usa logging.INFO, lo que significa que se registrarán mensajes informativos y superiores.
    """
    logging.basicConfig( # Configura los parámetros básicos del sistema de logging.
        level=log_level, # Establece el nivel mínimo de los mensajes que serán procesados por los 'handlers'.
        format='%(asctime)s - %(levelname)s - %(message)s', # Define el formato de cada mensaje de log:
                                                            # %(asctime)s: Tiempo en que se registró el evento.
                                                            # %(levelname)s: Nivel de severidad del mensaje (INFO, DEBUG, ERROR, etc.).
                                                            # %(message)s: El mensaje de log real.
        handlers=[ # Define dónde se enviarán los mensajes de log.
            logging.FileHandler('expander.log'), # Un 'handler' para escribir los logs en un archivo llamado 'expander.log'.
            logging.StreamHandler() # Un 'handler' para enviar los logs a la consola (salida estándar).
        ]
    )

def validate_mathematical_expression(expr_str):
    """
    Valida si una cadena de texto tiene la estructura básica de una expresión matemática válida.
    Realiza varias comprobaciones, como caracteres permitidos, balanceo de paréntesis y uso de operadores.
    No es un validador sintáctico completo (para eso se usa SymPy), pero filtra errores obvios.
    
    Args:
        expr_str (str): La cadena de texto de la expresión a validar.
        
    Returns:
        tuple: Una tupla que contiene:
               - bool: True si la expresión parece válida, False en caso contrario.
               - list: Una lista de cadenas describiendo los problemas encontrados.
    """
    problems = [] # Inicializa una lista vacía para almacenar cualquier problema encontrado en la expresión.
    
    if not expr_str or not expr_str.strip(): # Verifica si la cadena está vacía o solo contiene espacios en blanco.
        problems.append("La expresión está vacía") # Agrega un mensaje de error si está vacía.
        return False, problems # Retorna False y la lista de problemas inmediatamente.
    
    # Verificar caracteres válidos
    # Define un conjunto de caracteres que son considerados válidos en una expresión matemática.
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/^()[]{}= .')
    # Crea un conjunto de caracteres presentes en la expresión y les resta los caracteres válidos para encontrar los inválidos.
    invalid_chars = set(expr_str) - valid_chars 
    
    if invalid_chars: # Si se encontraron caracteres inválidos.
        problems.append(f"Caracteres inválidos encontrados: {', '.join(invalid_chars)}") # Agrega un mensaje de error con los caracteres inválidos.
    
    # Verificar balanceado de paréntesis
    if not are_parentheses_balanced(expr_str): # Llama a la función auxiliar para verificar si los paréntesis están balanceados.
        problems.append("Paréntesis no balanceados") # Agrega un mensaje de error si no están balanceados.
    
    # Verificar que no empiece o termine con operadores
    # `re.match(r'^[+\-*/^]', expr_str.strip())` busca si la cadena (sin espacios al inicio/final) comienza con uno de los operadores.
    if re.match(r'^[+\-*/^]', expr_str.strip()): 
        problems.append("La expresión no puede empezar con un operador") # Mensaje si empieza con operador.
    
    # `re.search(r'[+\-*/^]$', expr_str.strip())` busca si la cadena (sin espacios al inicio/final) termina con uno de los operadores.
    if re.search(r'[+\-*/^]$', expr_str.strip()):
        problems.append("La expresión no puede terminar con un operador") # Mensaje si termina con operador.
    
    # Verificar operadores consecutivos (ej. "x++y")
    # `re.search(r'[+\-*/^]{2,}', expr_str)` busca dos o más (`{2,}`) ocurrencias consecutivas de cualquier operador.
    if re.search(r'[+\-*/^]{2,}', expr_str):
        problems.append("Operadores consecutivos encontrados") # Mensaje si hay operadores consecutivos.
    
    # Si la lista de problemas está vacía, la expresión se considera válida por esta función.
    return len(problems) == 0, problems # Retorna True/False y la lista de problemas.

def are_parentheses_balanced(expr_str):
    """
    Verifica si todos los tipos de paréntesis (redondos, cuadrados, llaves) están correctamente balanceados
    en una expresión. Utiliza una pila (stack) para rastrear los paréntesis de apertura.
    
    Args:
        expr_str (str): La cadena de la expresión a verificar.
        
    Returns:
        bool: True si todos los paréntesis están balanceados y en el orden correcto, False en caso contrario.
    """
    stack = [] # Inicializa una pila (lista) vacía para almacenar los paréntesis de apertura.
    pairs = {'(': ')', '[': ']', '{': '}'} # Diccionario que mapea cada paréntesis de apertura con su correspondiente de cierre.
    
    for char in expr_str: # Itera sobre cada carácter en la cadena de la expresión.
        if char in pairs: # Si el carácter actual es un paréntesis de apertura (es una clave en 'pairs').
            stack.append(char) # Lo añade a la pila.
        elif char in pairs.values(): # Si el carácter actual es un paréntesis de cierre (es un valor en 'pairs').
            if not stack: # Si la pila está vacía y encontramos un paréntesis de cierre, significa que no hay un paréntesis de apertura correspondiente.
                return False # Los paréntesis no están balanceados.
            # `stack.pop()` remueve y devuelve el último elemento añadido a la pila (el último paréntesis de apertura).
            # Comprueba si el paréntesis de cierre actual coincide con el que debería cerrar el último paréntesis de apertura.
            if pairs[stack.pop()] != char: 
                return False # Si no coinciden, los paréntesis no están balanceados (ej. `([)]`).
    
    # Después de revisar todos los caracteres, si la pila está vacía, significa que todos los paréntesis de apertura
    # tuvieron un paréntesis de cierre correspondiente y en el orden correcto.
    return len(stack) == 0 # Retorna True si la pila está vacía, False si aún quedan paréntesis de apertura sin cerrar.

def clean_mathematical_text(text):
    """
    Limpia texto extraído de operaciones de OCR (Reconocimiento Óptico de Caracteres)
    para mejorar su interpretabilidad como expresión matemática.
    Corrige errores comunes de OCR y elimina caracteres no matemáticos.
    
    Args:
        text (str): El texto a limpiar, probablemente obtenido de un OCR.
        
    Returns:
        str: El texto limpio y más apto para el procesamiento matemático.
    """
    if not text: # Si el texto de entrada está vacío o es None.
        return "" # Retorna una cadena vacía.
    
    # Eliminar espacios extra: reemplaza múltiples espacios en blanco por uno solo y elimina espacios al inicio/final.
    text = re.sub(r'\s+', ' ', text.strip()) 
    
    # Reemplazar caracteres comunes mal reconocidos por OCR
    replacements = { # Diccionario de caracteres que suelen ser mal reconocidos por OCR y sus correcciones.
        'х': 'x',    # 'x' cirílica por 'x' latina (a menudo confundida).
        '×': '*',    # Símbolo de multiplicación '×' por el asterisco '*'.
        '÷': '/',    # Símbolo de división '÷' por la barra '/'.
        '—': '-',    # Guión largo por el signo menos '-'.
        '–': '-',    # Guión medio por el signo menos '-'.
        '"': '',     # Comillas dobles (pueden aparecer por ruido en OCR) se eliminan.
        "'": '',     # Apóstrofes (similares a comillas, también se eliminan).
    }
    
    for old, new in replacements.items(): # Itera sobre cada par de carácter_antiguo:carácter_nuevo en el diccionario.
        text = text.replace(old, new) # Realiza el reemplazo en la cadena de texto.
    
    # Eliminar caracteres no matemáticos comunes
    # `r'[^\w+\-*/^()[\]{}= .]'` es un patrón que busca cualquier carácter que NO esté (`^` al inicio del conjunto)
    # en el conjunto de caracteres alfanuméricos (`\w`), operadores (`+-*/^`), paréntesis/corchetes/llaves (`()[]{}`),
    # signo igual (`=`), punto (`.`) o espacio (` `).
    # Todos los caracteres que coincidan con este patrón serán eliminados (reemplazados por una cadena vacía).
    text = re.sub(r'[^\w+\-*/^()[\]{}=. ]', '', text) 
    
    return text.strip() # Retorna el texto final, eliminando cualquier espacio extra que pudiera haber quedado al final.

def format_expression_for_display(expr_str, max_length=50):
    """
    Formatea una cadena de expresión para su visualización, truncándola si excede una longitud máxima.
    Esto es útil para mostrar expresiones largas en interfaces de usuario donde el espacio es limitado.
    
    Args:
        expr_str (str): La expresión como cadena de texto.
        max_length (int): La longitud máxima deseada para la expresión formateada.
                          Por defecto es 50 caracteres.
        
    Returns:
        str: La expresión formateada. Si es más larga que `max_length`, se trunca y se añaden "..." al final.
    """
    if len(expr_str) <= max_length: # Comprueba si la longitud de la expresión es menor o igual a la longitud máxima.
        return expr_str # Si es así, la devuelve tal cual.
    
    # Si la expresión es más larga, la trunca.
    # `expr_str[:max_length-3]` toma los primeros `max_length-3` caracteres. Se resta 3 para dejar espacio para los puntos suspensivos.
    return expr_str[:max_length-3] + "..." # Retorna la expresión truncada seguida de "...".

def generate_report_header():
    """
    Genera una cadena de texto para usar como encabezado en reportes o archivos de salida.
    Incluye el nombre de la aplicación, versión y la fecha/hora de generación del reporte.
    
    Returns:
        str: El encabezado formateado.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Obtiene la fecha y hora actuales y la formatea como una cadena.
    return f""" # Retorna una f-string multilinea con la información del encabezado.
=== {APP_NAME} v{APP_VERSION} === # Nombre y versión de la aplicación.
Reporte generado: {now} # Fecha y hora de generación.
Descripción: Expansión de expresiones algebraicas # Descripción del reporte.

""".strip() # `.strip()` elimina los espacios en blanco iniciales/finales (incluyendo saltos de línea) de la cadena multilínea.

def is_likely_mathematical_expression(text):
    """
    Heurística para determinar si una cadena de texto es "probablemente" una expresión matemática.
    Se basa en la proporción de caracteres que son típicamente usados en expresiones matemáticas
    frente al total de caracteres (ignorando espacios).
    
    Args:
        text (str): La cadena de texto a evaluar.
        
    Returns:
        bool: True si la cadena parece ser una expresión matemática, False en caso contrario.
    """
    if not text: # Si el texto de entrada está vacío o es None.
        return False # No puede ser una expresión matemática.
    
    # Contar caracteres matemáticos vs texto normal
    # `re.findall(r'[a-zA-Z0-9+\-*/^()[\]{}=]', text)` busca todos los caracteres que son letras, números, operadores,
    # paréntesis, corchetes, llaves o el signo igual.
    math_chars = len(re.findall(r'[a-zA-Z0-9+\-*/^()[\]{}=]', text))
    # `total_chars` es la longitud del texto después de quitar todos los espacios, para obtener una base de cálculo más precisa.
    total_chars = len(text.replace(' ', '')) 
    
    if total_chars == 0: # Evita la división por cero si el texto solo tiene espacios.
        return False # Si no hay caracteres útiles, no es una expresión.
    
    # Si más del 70% son caracteres matemáticos, probablemente es matemático
    ratio = math_chars / total_chars # Calcula la proporción de caracteres matemáticos.
    return ratio > 0.7 # Retorna True si la proporción es mayor que 0.7 (70%). Este es un umbral heurístico.

def extract_variables_from_text(text):
    """
    Extrae cadenas de texto que podrían ser variables matemáticas de una expresión.
    Busca secuencias de letras y números que no sean palabras comunes.
    
    Args:
        text (str): La cadena de texto de la cual extraer variables.
        
    Returns:
        set: Un conjunto de cadenas de texto que se identificaron como variables.
    """
    # Buscar letras solas o seguidas de números (como x, y, x1, y2).
    # `\b` es un límite de palabra. `[a-zA-Z]` busca una letra inicial. `[a-zA-Z0-9]*` busca cero o más letras/números siguientes.
    variables = re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', text) 
    
    # Filtrar palabras comunes que no son variables (ej. "sin", "cos", "and", etc.).
    common_words = {'and', 'or', 'the', 'is', 'in', 'to', 'of', 'for', 'with', 'sin', 'cos', 'tan', 'log', 'exp'}
    # Crea una nueva lista de variables, excluyendo aquellas que están en la lista de palabras comunes (ignorando mayúsculas/minúsculas).
    variables = [var for var in variables if var.lower() not in common_words] 
    
    return set(variables) # Convierte la lista de variables a un conjunto para eliminar duplicados y retorna.

def safe_eval_expression(expr_str, allowed_names=None):
    """
    Realiza una "evaluación segura" de una expresión. No evalúa el valor numérico,
    sino que verifica si la expresión contiene solo caracteres y nombres (variables) permitidos.
    Esto es una medida de seguridad básica para prevenir la ejecución de código arbitrario
    si `eval()` fuera a usarse directamente con entradas de usuario (aunque en este proyecto se usa SymPy).
    
    Args:
        expr_str (str): La cadena de la expresión a verificar.
        allowed_names (set): Un conjunto de nombres (variables) que están explícitamente permitidos en la expresión.
                             Si es None, se usa un conjunto por defecto de todas las letras.
        
    Returns:
        bool: True si la expresión solo contiene elementos permitidos, False si se encuentra algo sospechoso.
    """
    if allowed_names is None: # Si no se proporciona un conjunto de nombres permitidos.
        allowed_names = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') # Se define un conjunto por defecto con todas las letras.
    
    # Verificar que solo contenga caracteres y nombres permitidos
    for char in expr_str: # Itera sobre cada carácter en la expresión.
        if char.isalpha() and char not in allowed_names: # Si el carácter es una letra Y NO está en los nombres permitidos.
            return False # La expresión no es segura.
        # Si el carácter NO es alfanumérico (`isalnum()`) Y NO es uno de los operadores/símbolos matemáticos permitidos.
        elif not (char.isalnum() or char in '+-*/^()[]{}= .'): 
            return False # La expresión contiene un carácter no permitido y no es segura.
    
    return True # Si se recorren todos los caracteres sin encontrar problemas, la expresión se considera segura.

def get_expression_complexity(expr_str):
    """
    Calcula una medida heurística simple de la complejidad de una expresión.
    Esta métrica combina la longitud, el número de variables, operadores y paréntesis.
    No es una medida matemática rigurosa de complejidad, sino un indicador básico.
    
    Args:
        expr_str (str): La expresión como cadena de texto.
        
    Returns:
        dict: Un diccionario que contiene varias métricas de complejidad (longitud, variables, operadores, paréntesis)
              y una puntuación de complejidad calculada.
    """
    metrics = { # Inicializa un diccionario para almacenar las métricas.
        'length': len(expr_str), # Longitud total de la cadena de la expresión.
        'variables': len(extract_variables_from_text(expr_str)), # Número de variables extraídas usando `extract_variables_from_text`.
        'operators': len(re.findall(r'[+\-*/^]', expr_str)), # Número de operadores (+, -, *, /, ^) encontrados.
        'parentheses': expr_str.count('(') + expr_str.count('[') + expr_str.count('{'), # Cuenta la cantidad de paréntesis, corchetes y llaves de apertura.
        'complexity_score': 0 # Puntuación inicial de complejidad.
    }
    
    # Calcular puntuación de complejidad ,se puede implementar mensajes cuando la complegidad sea muy alta
    # Se calcula una puntuación ponderada sumando las diferentes métricas.
    # Los coeficientes (0.1, 2, 1.5, 3) son pesos arbitrarios para dar más importancia a ciertos factores.
    metrics['complexity_score'] = (
        metrics['length'] * 0.1 +        # Cada carácter contribuye un poco a la complejidad.
        metrics['variables'] * 2 +       # Más variables, más compleja.
        metrics['operators'] * 1.5 +     # Más operadores, más compleja.
        metrics['parentheses'] * 3       # Más paréntesis (estructura anidada), más compleja.
    )
    
    return metrics # Retorna el diccionario con todas las métricas y la puntuación de complejidad.