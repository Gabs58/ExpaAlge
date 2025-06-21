"""
Archivo de configuración para el Expansor Algebraico.
Define constantes y configuraciones del sistema.
"""

# Información de la aplicación
APP_NAME = "Expansor Algebraico"  # Usado en main.py y para el título de la ventana GUI
APP_VERSION = "1.0.0"             # Usado en main.py y para mostrar la versión

# Configuración de la GUI (usada en ExpanderGUI)
GUI_CONFIG = {
    'window_title': f"{APP_NAME} - LaTeX",  # Título de la ventana principal
    'window_size': "1100x840",               # Tamaño inicial de la ventana (más ancho)
    'min_window_size': (900, 600),           # Tamaño mínimo de la ventana (más ancho)
    'font_family': 'Arial',                  # Fuente principal
    'monospace_font': 'Courier',             # Fuente monoespaciada para resultados
    'title_font_size': 12,                   # Tamaño de fuente para títulos
    'normal_font_size': 10,                  # Tamaño de fuente normal
    'padding': 10                            # Espaciado entre elementos
}

# Ejemplos de expresiones para la GUI (usados en ExpanderGUI)
EXAMPLE_EXPRESSIONS = [
    r"\left(x+1\right)^2 \left(x-2\right)",
    r"\left(a+b\right)\left(c+d\right)\left(e+f\right)",
    r"x\left(x+1\right)\left(x-1\right)",
    r"\left(2x+3\right)^2 \left(x-1\right)",
    r"\left(x+y\right)^3",
    r"\left(a+b+c\right)\left(x+y\right)"
]

# Mensajes de error comunes (usados en ExpanderGUI)
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

# Configuración de archivos (usada en ExpanderGUI para diálogos de abrir/guardar)
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