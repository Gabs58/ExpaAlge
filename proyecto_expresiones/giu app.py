import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pytesseract
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from config import GUI_CONFIG, EXAMPLE_EXPRESSIONS, ERROR_MESSAGES, FILE_CONFIG
import threading
from expander import Expander  # Importa la clase Expander que ahora centraliza el procesamiento
from latex_exporter import LatexExporter  # Importa la clase LatexExporter para exportar a PDF

class ExpanderGUI:
    """
    Interfaz gráfica para el Expansor Algebraico.
    Se encarga únicamente de la interacción con el usuario y delega el procesamiento a AlgebraService.
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(GUI_CONFIG['window_title'])
        self.root.geometry(GUI_CONFIG['window_size'])
        self.root.minsize(*GUI_CONFIG['min_window_size'])
        self.root.resizable(True, True)

        self.image_path = None
        self.current_expression = None

        self.setup_gui()
        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=(GUI_CONFIG['font_family'], GUI_CONFIG['title_font_size'], 'bold'))
        style.configure('Result.TLabel', font=(GUI_CONFIG['monospace_font'], GUI_CONFIG['normal_font_size']))

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding=str(GUI_CONFIG['padding']))
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        input_frame = ttk.LabelFrame(main_frame, text="Entrada Manual", padding=str(GUI_CONFIG['padding']))
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Expresión:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

        self.expression_var = tk.StringVar()
        self.expression_entry = ttk.Entry(input_frame, textvariable=self.expression_var, width=50)
        self.expression_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.expression_entry.bind('<Return>', lambda e: self.process_manual_expression())

        self.latex_input_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Entrada LaTeX", variable=self.latex_input_var).grid(row=0, column=2, padx=(5, 0))
        ttk.Button(input_frame, text="Expandir", command=self.process_manual_expression).grid(row=0, column=3, padx=(5, 0))

        examples_frame = ttk.Frame(input_frame)
        examples_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        ttk.Label(examples_frame, text="Ejemplos:", font=(GUI_CONFIG['font_family'], 9, 'italic')).pack(anchor=tk.W)

        for example in EXAMPLE_EXPRESSIONS[:4]:
            btn = ttk.Button(examples_frame, text=example, command=lambda ex=example: self.load_example(ex))
            btn.pack(side=tk.LEFT, padx=(0, 5), pady=2)

        self.latex_canvas_label = ttk.Label(main_frame)
        self.latex_canvas_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=str(GUI_CONFIG['padding']))
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80, font=(GUI_CONFIG['monospace_font'], GUI_CONFIG['normal_font_size']))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.rowconfigure(0, weight=1)

        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Button(controls_frame, text="Limpiar Resultados", command=self.clear_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="Copiar LaTeX", command=self.copy_latex).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="Exportar a PDF", command=self.export_to_pdf).pack(side=tk.LEFT, padx=(0, 5))

        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def load_example(self, example: str):
        self.expression_var.set(example)
        self.latex_input_var.set(False)

    def update_status(self, message: str):
        self.status_var.set(message)
        self.root.update()

    def add_result(self, title: str, content: str):
        self.results_text.insert(tk.END, f"\n=== {title} ===\n")
        self.results_text.insert(tk.END, f"{content}\n")
        self.results_text.see(tk.END)

    def render_latex_image(self, latex_code: str):
        fig = plt.figure(figsize=(5, 1))
        fig.text(0.1, 0.5, f"${latex_code}$", fontsize=20)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        image = Image.open(buf)
        photo = ImageTk.PhotoImage(image)
        self.latex_canvas_label.config(image=photo)
        self.latex_canvas_label.image = photo

    def process_manual_expression(self):
        expression = self.expression_var.get().strip()  # Obtiene la expresión ingresada
        if not expression:
            messagebox.showwarning("Advertencia", ERROR_MESSAGES['no_expression'])
            return
        is_latex = self.latex_input_var.get()  # Determina si la entrada es LaTeX
        self.update_status("Procesando expresión...")
        # Llama al método centralizado de Expander
        result = Expander.process_expression(expression, is_latex)
        if result["success"]:
            self.current_expression = result
            self.add_result("EXPRESIÓN ORIGINAL", result['original'])
            self.add_result("EXPRESIÓN EXPANDIDA", result['expanded'])
            self.add_result("LATEX EXPANDIDA", result['expanded_latex'])
            self.render_latex_image(result['expanded_latex'])
            self.update_status("Procesamiento completado")
        else:
            self.update_status(f"Error: {result['error']}")
            messagebox.showerror("Error", f"Error al procesar la expresión:\n{result['error']}")

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
        # Llama al método centralizado de Expander
        return Expander.process_expression(expression, is_latex)

def main():
    root = tk.Tk()
    app = ExpanderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 