from input_parser import InputParser # Importa la clase InputParser para analizar expresiones.
from expander import Expander # Importa la clase Expander para realizar la expansión algebraica.
from latex_exporter import LatexExporter # Importa la clase LatexExporter para convertir expresiones a formato LaTeX.
from config import APP_NAME, APP_VERSION # Importa el nombre y la versión de la aplicación desde el archivo de configuración.
from giu_app import ExpanderGUI # Importa la clase ExpanderGUI, que presumiblemente maneja la interfaz gráfica de usuario.
import sys # Importa el módulo sys para acceder a funciones del sistema, como sys.exit().
import argparse # Importa el módulo argparse para manejar argumentos de línea de comandos.

class AlgebraicExpanderCLI: # Define la clase para la interfaz de línea de comandos (CLI).
    def __init__(self): # Constructor de la clase CLI.
        self.parser = InputParser() # Inicializa una instancia del analizador de entrada.
        self.expander = Expander() # Inicializa una instancia del expansor de expresiones.
        self.latex_exporter = LatexExporter() # Inicializa una instancia del exportador a LaTeX.

    def process_expression(self, input_expr, input_format="text", output_format="both"): # Define un método para procesar una única expresión.
        try: # Bloque try para manejar posibles errores durante el procesamiento.
            if input_format == "latex": # Comprueba si el formato de entrada es LaTeX.
                expr = self.parser.parse_latex(input_expr) # Parsea la expresión como LaTeX.
            else: # Si el formato de entrada no es LaTeX (es texto plano).
                expr = self.parser.parse(input_expr) # Parsea la expresión como texto plano.

            expanded = self.expander.expand_expression(expr) # Expande la expresión parseada.

            result = { # Crea un diccionario para almacenar los resultados del procesamiento.
                'original': str(expr), # La expresión original como cadena.
                'expanded': str(expanded), # La expresión expandida como cadena.
                'success': True, # Indica que la operación fue exitosa.
                'error': None # No hay error.
            }

            if output_format in ["latex", "both"]: # Si el formato de salida deseado incluye LaTeX.
                result['original_latex'] = self.latex_exporter.to_latex(expr) # Convierte la expresión original a LaTeX.
                result['expanded_latex'] = self.latex_exporter.to_latex(expanded) # Convierte la expresión expandida a LaTeX.

            return result # Retorna el diccionario de resultados.

        except Exception as e: # Captura cualquier excepción que ocurra durante el procesamiento.
            return { # Retorna un diccionario indicando el fallo y el error.
                'success': False, # Indica que la operación falló.
                'error': str(e), # El mensaje de error.
                'original': input_expr # La expresión original que causó el error.
            }

    def interactive_mode(self): # Define el método para ejecutar la aplicación en modo interactivo.
        print(f"=== {APP_NAME} v{APP_VERSION} ===") # Imprime el nombre y la versión de la aplicación.
        print("Ingresa expresiones algebraicas para expandir.") # Instrucciones para el usuario.
        print("Comandos especiales:") # Muestra los comandos especiales disponibles.
      #  print("  'latex:' + expresión para entrada LaTeX") # Comando para entrada LaTeX.
        print("  'gui' para abrir interfaz gráfica") # Comando para abrir la GUI.
        print("  'salir' para terminar") # Comando para salir.
        print() # Imprime una línea en blanco para formato.

        while True: # Bucle infinito para mantener el modo interactivo.
            try: # Bloque try para manejar la interrupción del teclado y otros errores.
                entrada = input("🔹 Expresión: ").strip() # Solicita al usuario una expresión y elimina espacios en blanco.

                if entrada.lower() in ['salir', 'exit', 'quit']: # Si el usuario ingresa un comando para salir.
                    print("¡Hasta luego! 👋") # Mensaje de despedida.
                    break # Sale del bucle.

                if entrada.lower() == 'gui': # Si el usuario ingresa 'gui'.
                    self.launch_gui() # Llama al método para lanzar la GUI.
                    continue # Continúa con la siguiente iteración del bu bucle.

                if not entrada: # Si la entrada está vacía.
                    continue # Continúa con la siguiente iteración del bucle.

                input_format = "text" # Establece el formato de entrada por defecto a "text".
                if entrada.lower().startswith("latex:"): # Si la entrada comienza con "latex:".
                    entrada = entrada[6:].strip() # Elimina "latex:" del inicio de la cadena.
                    input_format = "latex" # Establece el formato de entrada a "latex".

                result = self.process_expression(entrada, input_format, "both") # Procesa la expresión, solicitando ambos formatos de salida.

                if result['success']: # Si el procesamiento fue exitoso.
                    print(f"\n✅ Expresión original: {result['original']}") # Imprime la expresión original.
                    print(f"🔸 Expresión expandida: {result['expanded']}") # Imprime la expresión expandida.
                    if 'original_latex' in result: # Si los resultados incluyen LaTeX.
                        print(f"📐 LaTeX original: {result['original_latex']}") # Imprime la expresión original en LaTeX.
                        print(f"📐 LaTeX expandida: {result['expanded_latex']}") # Imprime la expresión expandida en LaTeX.
                    print() # Imprime una línea en blanco para formato.
                else: # Si hubo un error.
                    print(f"❌ Error: {result['error']}\n") # Imprime el mensaje de error.

            except KeyboardInterrupt: # Captura la excepción cuando el usuario presiona Ctrl+C.
                print("\n¡Hasta luego! 👋") # Mensaje de despedida.
                break # Sale del bucle.
            except Exception as e: # Captura cualquier otra excepción inesperada.
                print(f"❌ Error inesperado: {str(e)}\n") # Imprime un mensaje de error inesperado.

    def launch_gui(self): # Define el método para lanzar la interfaz gráfica.
        try: # Bloque try para manejar errores al importar o lanzar la GUI.
            import tkinter as tk # Intenta importar tkinter. Si falla, significa que tkinter no está disponible.
            print("\n🖥️  Abriendo interfaz gráfica...") # Mensaje indicando que la GUI se está abriendo.
            root = tk.Tk() # Crea la ventana principal de Tkinter.
            app = ExpanderGUI(root) # Crea una instancia de ExpanderGUI.
            root.mainloop() # Inicia el bucle principal de la GUI.
            print("📱 Interfaz gráfica cerrada. Regresando al modo texto.\n") # Mensaje cuando la GUI se cierra.
        except ImportError as e: # Captura un error si tkinter no puede ser importado.
            print(f"❌ Error al cargar la GUI: {e}") # Informa que la GUI no se pudo cargar.
        except Exception as e: # Captura cualquier otro error inesperado en la GUI.
            print(f"❌ Error inesperado en GUI: {e}") # Informa sobre el error inesperado.

    def batch_process(self, expressions, input_format="text"): # Define un método para procesar expresiones en lote.
        results = [] # Lista para almacenar los resultados de cada expresión.
        for expr in expressions: # Itera sobre cada expresión en la lista.
            results.append(self.process_expression(expr, input_format, "both")) # Procesa cada expresión y añade el resultado a la lista.
        return results # Retorna la lista de resultados.

def main(): # Define la función principal que se ejecuta cuando el script es llamado.
    parser = argparse.ArgumentParser( # Crea un objeto ArgumentParser para definir los argumentos de línea de comandos.
        description=f"{APP_NAME} v{APP_VERSION} - Expande expresiones algebraicas", # Descripción del programa.
        formatter_class=argparse.RawDescriptionHelpFormatter, # Formateador para mostrar ejemplos de uso.
        epilog="""
Ejemplos de uso:
  python main.py
  python main.py -e "(x+1)^2" --latex
  python main.py --gui
  python main.py -e "(a+b)^2" --from-gui
""" # Ejemplos de uso que se muestran en la ayuda.
)

    parser.add_argument('-e', '--expression', help='Expresión algebraica a expandir') # Argumento para una expresión única.
    parser.add_argument('--latex', action='store_true', help='La entrada está en formato LaTeX') # Flag para indicar que la entrada es LaTeX.
    parser.add_argument('--gui', action='store_true', help='Abrir la interfaz gráfica') # Flag para abrir la GUI.
    parser.add_argument('--format', choices=['text', 'latex', 'both'], default='both', help='Formato de salida') # Argumento para el formato de salida.
    parser.add_argument('--batch', help='Archivo con expresiones a procesar') # Argumento para procesar un archivo en lote.
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo detallado') # Flag para modo detallado (no implementado en este fragmento).
    parser.add_argument('--from-gui', action='store_true', help='Usar el motor de procesamiento de la GUI') # Flag para usar el método de procesamiento de la GUI.

    args = parser.parse_args() # Parsea los argumentos de la línea de comandos.

    if args.gui: # Si se especificó el argumento --gui.
        try: # Intenta iniciar la GUI.
            import tkinter as tk # Importa tkinter.
            print(f"🖥️  Iniciando {APP_NAME} - Interfaz Gráfica") # Mensaje de inicio de GUI.
            root = tk.Tk() # Crea la ventana principal.
            app = ExpanderGUI(root) # Crea la instancia de la GUI.
            root.mainloop() # Inicia el bucle principal de la GUI.
            return # Termina la ejecución del script.
        except ImportError as e: # Si tkinter no está disponible.
            print(f"❌ Error al cargar GUI: {e}") # Mensaje de error.
            return # Termina la ejecución.
        except Exception as e: # Captura otros errores inesperados en la GUI.
            print(f"❌ Error inesperado: {e}") # Mensaje de error.
            return # Termina la ejecución.

    cli = AlgebraicExpanderCLI() # Crea una instancia de la clase CLI.

    if args.batch: # Si se especificó el argumento --batch.
        try: # Intenta procesar el archivo.
            with open(args.batch, 'r', encoding='utf-8') as f: # Abre el archivo en modo lectura.
                expressions = [line.strip() for line in f if line.strip()] # Lee las expresiones del archivo, una por línea.

            input_format = "latex" if args.latex else "text" # Determina el formato de entrada.
            results = cli.batch_process(expressions, input_format) # Procesa las expresiones en lote.

            for i, result in enumerate(results, 1): # Itera sobre los resultados para imprimirlos.
                print(f"\n--- Expresión {i} ---") # Imprime el número de expresión.
                if result['success']: # Si el procesamiento fue exitoso.
                    print(f"Original: {result['original']}") # Imprime la expresión original.
                    print(f"Expandida: {result['expanded']}") # Imprime la expresión expandida.
                    if args.format in ['latex', 'both']: # Si se solicitó salida LaTeX.
                        print(f"LaTeX: {result['expanded_latex']}") # Imprime la expresión expandida en LaTeX.
                else: # Si hubo un error.
                    print(f"❌ Error: {result['error']}") # Imprime el mensaje de error.

            return # Termina la ejecución del script.

        except FileNotFoundError: # Si el archivo no se encuentra.
            print(f"❌ Archivo no encontrado: {args.batch}") # Mensaje de error.
            return # Termina la ejecución.
        except Exception as e: # Captura cualquier otro error al procesar el archivo.
            print(f"❌ Error procesando archivo: {e}") # Mensaje de error.
            return # Termina la ejecución.

    if args.expression: # Si se especificó el argumento --expression.
        input_format = "latex" if args.latex else "text" # Determina el formato de entrada.
        if args.from_gui: # Si se especificó --from-gui.
            # Llama al método estático de ExpanderGUI para procesar la expresión.
            result = ExpanderGUI.expand_expression_gui(args.expression, is_latex=args.latex)
        else: # Si no se especificó --from-gui.
            result = cli.process_expression(args.expression, input_format, args.format) # Procesa la expresión usando la CLI.

        if result['success']: # Si el procesamiento fue exitoso.
            print("=== RESULTADO ===") # Encabezado del resultado.
            print(f"Original: {result['original']}") # Imprime la expresión original.
            print(f"Expandida: {result['expanded']}") # Imprime la expresión expandida.
            if 'original_latex' in result: # Si los resultados incluyen LaTeX.
                print(f"LaTeX Original: {result['original_latex']}") # Imprime la expresión original en LaTeX.
                print(f"LaTeX Expandida: {result['expanded_latex']}") # Imprime la expresión expandida en LaTeX.
        else: # Si hubo un error.
            print(f"❌ Error: {result['error']}") # Imprime el mensaje de error.
            sys.exit(1) # Sale del programa con un código de error.
    else: # Si no se especificó ningún argumento de expresión, lote o GUI.
        cli.interactive_mode() # Inicia el modo interactivo de la CLI.

if __name__ == '__main__': # Verifica si el script se está ejecutando directamente.
    main() # Llama a la función principal para iniciar la aplicación.