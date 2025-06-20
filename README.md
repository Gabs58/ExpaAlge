# ExpaAlge
Expansor algebraico 
 proyecto ExpaAlge:

ExpaAlge es una herramienta para expandir expresiones algebraicas y convertirlas a formato LaTeX de manera sencilla, tanto desde una interfaz gráfica (GUI) como desde la línea de comandos (CLI). El proyecto está pensado para facilitar el manejo de expresiones matemáticas, permitiendo al usuario ingresar expresiones, expandirlas paso a paso, visualizar el resultado en LaTeX y exportar el resultado a PDF.

Flujo de trabajo del proyecto:

Entrada del usuario:
El usuario puede interactuar con el programa de dos maneras:

Interfaz gráfica (GUI): Introducir una expresión algebraica manualmente, seleccionar ejemplos o ingresar expresiones en LaTeX.
Línea de comandos (CLI): Ejecutar el programa, ingresar expresiones una a una o procesar un archivo de expresiones (modo batch).
Parseo de la expresión:
La entrada se pasa al módulo InputParser, que limpia la cadena, convierte la sintaxis LaTeX a algo interpretable por SymPy, y valida la expresión.

Expansión algebraica:
Una vez parseada, la expresión se envía a la clase Expander, que utiliza SymPy para expandirla algebraicamente y opcionalmente agrupar términos.

Conversión a LaTeX:
El resultado expandido se convierte a formato LaTeX usando la clase LatexExporter, que lo puede mostrar en la interfaz o preparar para exportar.

Presentación y exportación:

En la GUI, el usuario puede visualizar los resultados, copiar el LaTeX, o exportar la expresión expandida como PDF.
En la CLI, los resultados se muestran en consola y pueden guardarse o exportarse si se implementa esa opción.
Resumen visual del flujo:

Code
[Usuario (GUI / CLI)]
        ↓
 [InputParser: limpieza y validación]
        ↓
   [Expander: expansión algebraica]
        ↓
 [LatexExporter: conversión a LaTeX]
        ↓
[Presentación: GUI / CLI / Exportar PDF]
Características adicionales:

Configuración centralizada (config.py)
Ejemplos predefinidos para la GUI
Mensajes de error amigables
Soporte para entrada OCR (opcional, si activado en la GUI)
Código modular y fácil de extender



1. config.py
No contiene clases, solo variables y diccionarios de configuración.

Python
"""
Archivo de configuración central para Expansor Algebraico.
Define constantes de aplicación, parámetros de GUI, OCR, ejemplos, patrones LaTeX y mensajes de error.
"""
2. expander.py
Clase:

Python
class Expander:
    """
    Clase que centraliza la lógica de expansión algebraica utilizando SymPy.

    Métodos:
        - expand_expression(expr): Expande una expresión algebraica.
        - expand_and_collect(expr, variables): Expande y agrupa términos por variables.
    """
3. giu app.py
Clase:

Python
class ExpanderGUI:
    """
    Interfaz gráfica de usuario para el Expansor Algebraico.

    Permite ingresar expresiones, expandirlas, visualizar el resultado en LaTeX,
    y exportar el resultado a PDF. Se apoya en el motor de expansión algebraica y exportador LaTeX.

    Atributos principales:
        - root: Instancia principal de Tkinter.
        - expression_var: Variable para la expresión ingresada.
        - current_expression: Diccionario con los resultados de la última expansión.

    Métodos principales:
        - process_manual_expression: Procesa la expresión introducida manualmente.
        - export_to_pdf: Exporta el resultado expandido en LaTeX a un PDF.
        - clear_results: Limpia el área de resultados.
        - copy_latex: Copia el LaTeX al portapapeles.
    """
4. input_parser.py
Clase:

Python
class InputParser:
    """
    Clase para parsear y limpiar cadenas de texto matemático y LaTeX,
    convirtiéndolas en objetos SymPy.

    Métodos:
        - clean_expression(expr_str): Limpia y normaliza expresiones estándar.
        - latex_to_sympy(latex_expr): Convierte LaTeX a sintaxis compatible con SymPy.
        - parse(expr_str): Convierte texto a expresión SymPy.
        - parse_latex(latex_expr): Convierte LaTeX a expresión SymPy.
        - validate_expression(expr_str, format_type): Valida la parseabilidad de la expresión.
    """
5. latex_exporter.py
Clase:

Python
class LatexExporter:
    """
    Clase utilitaria para convertir expresiones SymPy a LaTeX y exportar a PDF usando pdflatex.

    Métodos:
        - to_latex(expr): Devuelve la representación LaTeX de una expresión SymPy.
        - export_latex_to_pdf(latex_code, output_path): Compila código LaTeX y lo exporta a PDF.
    """
6. main.py
Clase:

Python
class AlgebraicExpanderCLI:
    """
    Interfaz de línea de comandos (CLI) para el Expansor Algebraico.

    Permite procesar expresiones en modo interactivo, por lotes, y lanzar la GUI.
    Usa InputParser, Expander y LatexExporter para el procesamiento.

    Métodos:
        - process_expression: Procesa una expresión individual.
        - interactive_mode: Modo interactivo tipo REPL.
        - launch_gui: Lanza la interfaz gráfica.
        - batch_process: Procesa un conjunto de expresiones desde archivo.
    """
