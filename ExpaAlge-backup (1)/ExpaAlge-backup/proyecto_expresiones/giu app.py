# Importaciones de librerías estándar y de terceros para la GUI y procesamiento de imágenes/expresiones
import tkinter as tk  # Tkinter para la interfaz gráfica
from tkinter import ttk, filedialog, messagebox, scrolledtext  # Widgets y utilidades de Tkinter
from PIL import Image, ImageTk  # Para manejar imágenes en la GUI
import pytesseract  # Para OCR (no usado actualmente, pero importado)
import io  # Para manejar buffers de imágenes
import matplotlib.pyplot as plt  # Para renderizar LaTeX como imagen
from matplotlib.backends.backend_agg import FigureCanvasAgg  # Backend de Matplotlib para imágenes
from config import GUI_CONFIG, EXAMPLE_EXPRESSIONS, ERROR_MESSAGES, FILE_CONFIG  # Configuración y recursos
import threading  # Para operaciones en segundo plano (no usado actualmente)
from expander import Expander  # Lógica de expansión algebraica
from latex_exporter import LatexExporter  # Exportación a PDF

class ExpanderGUI:
    """
    Clase principal de la interfaz gráfica para el Expansor Algebraico.
    Se encarga de la interacción con el usuario y delega el procesamiento algebraico a Expander.
    """
    def __init__(self, root: tk.Tk):
        self.root = root  # Ventana principal de Tkinter
        self.root.title(GUI_CONFIG['window_title'])  # Título de la ventana
        self.root.geometry(GUI_CONFIG['window_size'])  # Tamaño inicial de la ventana
        self.root.minsize(*GUI_CONFIG['min_window_size'])  # Tamaño mínimo de la ventana
        self.root.resizable(True, True)  # Permitir redimensionar

        self.image_path = None  # Ruta de imagen cargada (no usado actualmente)
        self.current_expression = None  # Diccionario con los resultados de la última expansión

        self.setup_gui()  # Configura los widgets de la interfaz
        self.setup_styles()  # Configura los estilos visuales

    def setup_styles(self):
        style = ttk.Style()  # Crea un objeto de estilos
        style.theme_use('clam')  # Usa el tema 'clam' para mejor apariencia
        # Configura estilos personalizados para títulos y resultados
        style.configure('Title.TLabel', font=(GUI_CONFIG['font_family'], GUI_CONFIG['title_font_size'], 'bold'))
        style.configure('Result.TLabel', font=(GUI_CONFIG['monospace_font'], GUI_CONFIG['normal_font_size']))

    def setup_gui(self):
        # Frame principal que contiene toda la interfaz
        main_frame = ttk.Frame(self.root, padding=str(GUI_CONFIG['padding']))
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Frame para la entrada manual de expresiones
        input_frame = ttk.LabelFrame(main_frame, text="Entrada Manual", padding=str(GUI_CONFIG['padding']))
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Expresión:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))  # Etiqueta de entrada

        self.expression_var = tk.StringVar()  # Variable para almacenar la expresión ingresada
        self.expression_entry = ttk.Entry(input_frame, textvariable=self.expression_var, width=50)  # Campo de entrada
        self.expression_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.expression_entry.bind('<Return>', lambda e: self.process_manual_expression())  # Procesar al presionar Enter

        self.latex_input_var = tk.BooleanVar(value=True)  # Opción LaTeX seleccionada por defecto
        # Checkbox para indicar si la entrada es LaTeX (puede deseleccionarse)
        ttk.Checkbutton(input_frame, text="Entrada LaTeX", variable=self.latex_input_var).grid(row=0, column=2, padx=(5, 0))
        # Botón para expandir la expresión
        ttk.Button(input_frame, text="Expandir", command=self.process_manual_expression).grid(row=0, column=3, padx=(5, 0))

        # Frame para los ejemplos de expresiones
        examples_frame = ttk.Frame(input_frame)
        examples_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        # Etiqueta de ejemplos
        ttk.Label(examples_frame, text="Ejemplos:", font=(GUI_CONFIG['font_family'], 9, 'italic')).pack(anchor=tk.W)
        # Botones de ejemplo en una sola fila
        for example in EXAMPLE_EXPRESSIONS:
            btn = ttk.Button(examples_frame, text=example, command=lambda ex=example: self.load_example(ex))
            btn.pack(side=tk.LEFT, padx=(0, 5), pady=2)

        # Etiqueta para mostrar imágenes renderizadas de LaTeX
        self.latex_canvas_label = ttk.Label(main_frame)
        self.latex_canvas_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # Frame para mostrar los resultados de la expansión
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=str(GUI_CONFIG['padding']))
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Área de texto con scroll para mostrar resultados
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80, font=(GUI_CONFIG['monospace_font'], GUI_CONFIG['normal_font_size']))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.rowconfigure(0, weight=1)

        # Frame para los controles inferiores (limpiar, copiar, exportar)
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Button(controls_frame, text="Limpiar Resultados", command=self.clear_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="Copiar LaTeX", command=self.copy_latex).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="Exportar a PDF", command=self.export_to_pdf).pack(side=tk.LEFT, padx=(0, 5))

        # Barra de estado en la parte inferior
        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def load_example(self, example: str):
        """Carga un ejemplo en el campo de entrada."""
        self.expression_var.set(example)
        self.latex_input_var.set(True)  # Siempre selecciona LaTeX al cargar ejemplo

    def update_status(self, message: str):
        """Actualiza el mensaje de la barra de estado."""
        self.status_var.set(message)
        self.root.update()

    def add_result(self, title: str, content: str):
        """Agrega un bloque de resultado al área de resultados."""
        self.results_text.insert(tk.END, f"\n=== {title} ===\n")
        self.results_text.insert(tk.END, f"{content}\n")
        self.results_text.see(tk.END)

    def render_latex_image(self, latex_code: str):
        """
        Renderiza una cadena LaTeX como imagen y la muestra en la interfaz.
        Utiliza matplotlib para generar la imagen y PIL para mostrarla en Tkinter.
        """
        fig = plt.figure(figsize=(5, 1))  # Crea una figura de matplotlib
        fig.text(0.1, 0.5, f"${latex_code}$", fontsize=20)  # Inserta el código LaTeX
        buf = io.BytesIO()  # Buffer temporal para la imagen
        fig.savefig(buf, format='png')  # Guarda la figura en el buffer
        plt.close(fig)  # Cierra la figura para liberar memoria
        buf.seek(0)  # Vuelve al inicio del buffer
        image = Image.open(buf)  # Abre la imagen desde el buffer
        photo = ImageTk.PhotoImage(image)  # Convierte la imagen a formato Tkinter
        self.latex_canvas_label.config(image=photo)  # Muestra la imagen en la etiqueta
        self.latex_canvas_label.image = photo  # Guarda la referencia para evitar que se borre

    def process_manual_expression(self):
        """
        Procesa la expresión ingresada por el usuario, la expande y muestra los resultados.
        Muestra tanto la expresión original como la expandida, en texto y en LaTeX.
        """
        expression = self.expression_var.get().strip()  # Obtiene la expresión ingresada
        if not expression:
            messagebox.showwarning("Advertencia", ERROR_MESSAGES['no_expression'])  # Advierte si está vacía
            return
        is_latex = self.latex_input_var.get()  # Determina si la entrada es LaTeX
        self.update_status("Procesando expresión...")

        try:
            result = Expander.process_expression(expression, is_latex)  # Procesa la expresión
        except Exception as e:
            self.update_status(f"Error inesperado: {str(e)}")
            messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")
            return

        # Validación robusta del resultado
        if not isinstance(result, dict):
            self.update_status("Error: El resultado no es un diccionario")
            messagebox.showerror("Error", "El resultado del procesamiento no es válido.")
            return

        if result.get("success"):
            self.current_expression = result  # Guarda el resultado actual
            self.add_result("EXPRESIÓN ORIGINAL", result.get('original', ''))  # Muestra la original
            self.add_result("EXPRESIÓN EXPANDIDA", result.get('expanded', ''))  # Muestra la expandida
            self.add_result("LATEX ORIGINAL", result.get('original_latex', ''))  # Muestra LaTeX original
            self.add_result("LATEX EXPANDIDA", result.get('expanded_latex', ''))  # Muestra LaTeX expandida
            # Renderiza ambas imágenes LaTeX (original y expandida)
            if result.get('original_latex'):
                try:
                    self.render_latex_image(result['original_latex'])
                except Exception as e:
                    self.update_status(f"Error al renderizar LaTeX original: {str(e)}")
            if result.get('expanded_latex'):
                try:
                    self.render_latex_image(result['expanded_latex'])
                except Exception as e:
                    self.update_status(f"Error al renderizar LaTeX expandida: {str(e)}")
            self.update_status("Procesamiento completado")
        else:
            self.update_status(f"Error: {result.get('error', 'Error desconocido')}")
            messagebox.showerror("Error", f"Error al procesar la expresión:\n{result.get('error', 'Error desconocido')}")

    def clear_results(self):
        """
        Limpia el área de resultados y actualiza el estado.
        """
        self.results_text.delete(1.0, tk.END)
        self.update_status("Resultados limpiados")

    def copy_latex(self):
        """
        Copia el resultado LaTeX expandido al portapapeles, si existe.
        """
        if self.current_expression and 'expanded_latex' in self.current_expression:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_expression['expanded_latex'])
            self.update_status("LaTeX copiado al portapapeles")
        else:
            messagebox.showwarning("Advertencia", ERROR_MESSAGES['no_results'])

    def export_to_pdf(self):
        """
        Exporta el resultado expandido en LaTeX a un archivo PDF usando LatexExporter y pdflatex.
        """
        if not self.current_expression or 'expanded_latex' not in self.current_expression:
            messagebox.showwarning("Advertencia", ERROR_MESSAGES['no_results'])
            return
        from tkinter import filedialog
        # Pedir al usuario la ubicación para guardar el archivo PDF
        pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivo PDF", "*.pdf"), ("Todos los archivos", "*.")]
        )
        if not pdf_path:
            return  # El usuario canceló
        latex_code = self.current_expression['expanded_latex']
        # Llama al método de LatexExporter para exportar a PDF
        result = LatexExporter.export_latex_to_pdf(latex_code, pdf_path)
        if result['success']:
            messagebox.showinfo("Éxito", f"PDF generado exitosamente en:\n{pdf_path}")
        else:
            messagebox.showerror("Error", f"No se pudo compilar el PDF.\n\nSalida:\n{result['error']}")

    @staticmethod
    def expand_expression_gui(expression: str, is_latex: bool = False):
        """
        Método estático para procesar una expresión desde la GUI (usado en main.py si se llama desde CLI con --from-gui).
        """
        return Expander.process_expression(expression, is_latex)

# Función principal para lanzar la GUI si se ejecuta este archivo directamente

def main():
    root = tk.Tk()
    app = ExpanderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 