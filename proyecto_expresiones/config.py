"""
Archivo de configuración para el Expansor Algebraico.
Define constantes y configuraciones del sistema.
"""

# Información de la aplicación
APP_NAME = "Expansor Algebraico"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Expande expresiones algebraicas y las convierte a LaTeX"

# Configuración de la GUI
GUI_CONFIG = {
    'window_title': f"{APP_NAME} - LaTeX",
    'window_size': "800x700",
    'min_window_size': (600, 500),
    'font_family': 'Arial',
    'monospace_font': 'Courier',
    'title_font_size': 12,
    'normal_font_size': 10,
    'padding': 10
}

# Configuración de OCR
OCR_CONFIG = {
    'tesseract_config': '--psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/^()[]{}=',
    'max_image_size': (400, 300),
    'supported_formats': ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
}

# Ejemplos de expresiones para la GUI
EXAMPLE_EXPRESSIONS = [
    "(x+1)^2*(x-2)",
    "(a+b)*(c+d)*(e+f)", 
    "x*(x+1)*(x-1)",
    "(2x+3)^2*(x-1)",
    "(x+y)^3",
    "(a+b+c)*(x+y)"
]

# Patrones de conversión LaTeX
LATEX_CONVERSION_PATTERNS = [
    (r'\^{([^}]+)}', r'**(\1)'),  # x^{2} -> x**(2)
    (r'\^([a-zA-Z0-9])', r'**\1'),  # x^2 -> x**2
    (r'\\cdot', '*'),  # \cdot -> *
    (r'\\times', '*'),  # \times -> *
    (r'\\left\(', '('),  # \left( -> (
    (r'\\right\)', ')'),  # \right) -> )
    (r'\\left\[', '['),  # \left[ -> [
    (r'\\right\]', ']'),  # \right] -> ]
    (r'\\left\{', '{'),  # \left{ -> {
    (r'\\right\}', '}'),  # \right} -> }
    (r'\\frac{([^}]+)}{([^}]+)}', r'(\1)/(\2)'),  # \frac{a}{b} -> (a)/(b)
]

# Mensajes de error comunes
ERROR_MESSAGES = {
    'no_expression': "Por favor, ingresa una expresión.",
    'invalid_expression': "La expresión ingresada no es válida.",
    'no_image': "Por favor, carga una imagen primero.",
    'ocr_failed': "No se pudo extraer texto de la imagen.",
    'processing_error': "Error al procesar la expresión.",
    'file_save_error': "Error al guardar el archivo.",
    'file_load_error': "Error al cargar el archivo.",
    'no_results': "No hay resultados para mostrar."
}

# Configuración de archivos
FILE_CONFIG = {
    'supported_image_types': [
        ("Archivos de imagen", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
        ("PNG", "*.png"),
        ("JPEG", "*.jpg *.jpeg"),
        ("Todos los archivos", "*.*")
    ],
    'supported_save_types': [
        ("Archivo de texto", "*.txt"),
        ("Archivo LaTeX", "*.tex"),
        ("Todos los archivos", "*.*")
    ],
    'default_extension': '.txt'
}