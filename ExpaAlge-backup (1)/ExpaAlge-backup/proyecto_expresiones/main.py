# Importaciones de módulos propios y estándar
from input_parser import InputParser # Importa la clase InputParser para analizar expresiones.
from expander import Expander # Importa la clase Expander para realizar la expansión algebraica.
from latex_exporter import LatexExporter # Importa la clase LatexExporter para convertir expresiones a formato LaTeX.
from config import APP_NAME, APP_VERSION # Importa el nombre y la versión de la aplicación desde el archivo de configuración.
from giu_app import ExpanderGUI # Importa la clase ExpanderGUI, que maneja la interfaz gráfica de usuario.
import sys # Importa el módulo sys para acceder a funciones del sistema, como sys.exit().
import argparse # Importa el módulo argparse para manejar argumentos de línea de comandos.

class AlgebraicExpanderCLI:
    """
    Clase para la interfaz de línea de comandos (CLI) del Expansor Algebraico.
    Permite procesar expresiones algebraicas desde la terminal, en modo interactivo, por lotes o con argumentos.
    """
    def __init__(self):
        self.parser = InputParser() # Instancia del parser para analizar expresiones.
        self.expander = Expander() # Instancia del expansor algebraico.
        self.latex_exporter = LatexExporter() # Instancia del exportador a LaTeX.

    def process_expression(self, input_expr, input_format="text", output_format="both"):
        """
        Procesa una expresión individual, la expande y la convierte a LaTeX si se solicita.
        Args:
            input_expr (str): Expresión a procesar.
            input_format (str): 'text' o 'latex'.
            output_format (str): 'text', 'latex' o 'both'.
        Returns:
            dict: Resultados del procesamiento.
        """
        try:
            if input_format == "latex":
                expr = self.parser.parse_latex(input_expr) # Parsea como LaTeX
            else:
                expr = self.parser.parse(input_expr) # Parsea como texto plano

            expanded = self.expander.expand_expression(expr) # Expande la expresión

            result = {
                'original': str(expr), # Expresión original en texto
                'expanded': str(expanded), # Expresión expandida en texto
                'success': True,
                'error': None
            }

            if output_format in ["latex", "both"]:
                result['original_latex'] = self.latex_exporter.to_latex(expr) # LaTeX original
                result['expanded_latex'] = self.latex_exporter.to_latex(expanded) # LaTeX expandida

            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'original': input_expr
            }

    def interactive_mode(self):
        """
        Modo interactivo tipo REPL para ingresar expresiones una a una desde la terminal.
        Permite lanzar la GUI o salir con comandos especiales.
        """
        print(f"=== {APP_NAME} v{APP_VERSION} ===") # Encabezado
        print("Ingresa expresiones algebraicas para expandir.")
        print("Comandos especiales:")
      #  print("  'latex:' + expresión para entrada LaTeX")
        print("  'gui' para abrir interfaz gráfica")
        print("  'salir' para terminar")
        print()

        while True:
            try:
                entrada = input("🔹 Expresión: ").strip() # Solicita la expresión

                if entrada.lower() in ['salir', 'exit', 'quit']:
                    print("¡Hasta luego! 👋")
                    break

                if entrada.lower() == 'gui':
                    self.launch_gui()
                    continue

                if not entrada:
                    continue

                input_format = "text"
                if entrada.lower().startswith("latex:"):
                    entrada = entrada[6:].strip()
                    input_format = "latex"

                result = self.process_expression(entrada, input_format, "both")

                if result['success']:
                    print(f"\n✅ Expresión original: {result['original']}")
                    print(f"🔸 Expresión expandida: {result['expanded']}")
                    if 'original_latex' in result:
                        print(f"📐 LaTeX original: {result['original_latex']}")
                        print(f"📐 LaTeX expandida: {result['expanded_latex']}")
                    print()
                else:
                    print(f"❌ Error: {result['error']}\n")

            except KeyboardInterrupt:
                print("\n¡Hasta luego! 👋")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {str(e)}\n")

    def launch_gui(self):
        """
        Lanza la interfaz gráfica de usuario (GUI) desde la CLI.
        """
        try:
            import tkinter as tk
            print("\n🖥️  Abriendo interfaz gráfica...")
            root = tk.Tk()
            app = ExpanderGUI(root)
            root.mainloop()
            print("📱 Interfaz gráfica cerrada. Regresando al modo texto.\n")
        except ImportError as e:
            print(f"❌ Error al cargar la GUI: {e}")
        except Exception as e:
            print(f"❌ Error inesperado en GUI: {e}")

    def batch_process(self, expressions, input_format="text"):
        """
        Procesa un conjunto de expresiones (por lotes) y retorna los resultados.
        Args:
            expressions (list): Lista de expresiones a procesar.
            input_format (str): 'text' o 'latex'.
        Returns:
            list: Lista de resultados (uno por expresión).
        """
        results = []
        for expr in expressions:
            results.append(self.process_expression(expr, input_format, "both"))
        return results

# Función principal que se ejecuta al correr el script

def main():
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} v{APP_VERSION} - Expande expresiones algebraicas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py
  python main.py -e "(x+1)^2" --latex
  python main.py --gui
  python main.py -e "(a+b)^2" --from-gui
"""
    )

    parser.add_argument('-e', '--expression', help='Expresión algebraica a expandir')
    parser.add_argument('--latex', action='store_true', help='La entrada está en formato LaTeX')
    parser.add_argument('--gui', action='store_true', help='Abrir la interfaz gráfica')
    parser.add_argument('--format', choices=['text', 'latex', 'both'], default='both', help='Formato de salida')
    parser.add_argument('--batch', help='Archivo con expresiones a procesar')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo detallado')
    parser.add_argument('--from-gui', action='store_true', help='Usar el motor de procesamiento de la GUI')

    args = parser.parse_args()

    if args.gui:
        try:
            import tkinter as tk
            print(f"🖥️  Iniciando {APP_NAME} - Interfaz Gráfica")
            root = tk.Tk()
            app = ExpanderGUI(root)
            root.mainloop()
            return
        except ImportError as e:
            print(f"❌ Error al cargar GUI: {e}")
            return
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return

    cli = AlgebraicExpanderCLI()

    if args.batch:
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                expressions = [line.strip() for line in f if line.strip()]

            input_format = "latex" if args.latex else "text"
            results = cli.batch_process(expressions, input_format)

            for i, result in enumerate(results, 1):
                print(f"\n--- Expresión {i} ---")
                if result['success']:
                    print(f"Original: {result['original']}")
                    print(f"Expandida: {result['expanded']}")
                    if args.format in ['latex', 'both']:
                        print(f"LaTeX: {result['expanded_latex']}")
                else:
                    print(f"❌ Error: {result['error']}")

            return

        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {args.batch}")
            return
        except Exception as e:
            print(f"❌ Error procesando archivo: {e}")
            return

    if args.expression:
        input_format = "latex" if args.latex else "text"
        if args.from_gui:
            # Llama al método estático de ExpanderGUI para procesar la expresión.
            result = ExpanderGUI.expand_expression_gui(args.expression, is_latex=args.latex)
        else:
            result = cli.process_expression(args.expression, input_format, args.format)

        if result['success']:
            print("=== RESULTADO ===")
            print(f"Original: {result['original']}")
            print(f"Expandida: {result['expanded']}")
            if 'original_latex' in result:
                print(f"LaTeX Original: {result['original_latex']}")
                print(f"LaTeX Expandida: {result['expanded_latex']}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    else:
        cli.interactive_mode()

if __name__ == '__main__':
    main()