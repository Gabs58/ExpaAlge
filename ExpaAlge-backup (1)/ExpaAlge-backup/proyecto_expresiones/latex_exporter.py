from sympy import latex
import os
import subprocess

class LatexExporter:
    @staticmethod
    def to_latex(expr):
        """
        Convierte una expresión sympy a su representación en LaTeX.
        """
        return latex(expr)

    @staticmethod
    def export_latex_to_pdf(latex_code: str, output_path: str) -> dict:
        """
        Exporta un código LaTeX matemático a un archivo PDF usando pdflatex.
        Args:
            latex_code (str): El código LaTeX matemático (sin encabezado de documento).
            output_path (str): Ruta donde se guardará el PDF (debe terminar en .pdf).
        Returns:
            dict: {'success': True/False, 'error': mensaje de error si falla}
        """
        # Crear el archivo .tex temporal en la misma carpeta que el PDF
        tex_path = os.path.splitext(output_path)[0] + '.tex'
        # Estructura básica de un documento LaTeX
        tex_content = (
            "\\documentclass{article}\n"
            "\\usepackage{amsmath}\n"
            "\\begin{document}\n"
            "\\[\n"
            f"{latex_code}\n"
            "\\]\n"
            "\\end{document}\n"
        )
        try:
            # Guardar el archivo .tex
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(tex_content)
            # Compilar a PDF usando pdflatex
            pdf_dir = os.path.dirname(tex_path)
            cmd = f'pdflatex -interaction=nonstopmode -output-directory \"{pdf_dir}\" \"{tex_path}\"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return {'success': True, 'error': None}
            else:
                return {'success': False, 'error': result.stderr}
        except Exception as e:
            return {'success': False, 'error': str(e)}