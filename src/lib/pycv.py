import os
import logging
import tomli
import jinja2
from weasyprint import HTML

# Get the logger instance
logger = logging.getLogger(__name__)


class PyCV:
    def __init__(self):
        # Resolve the root directory relative to this file
        # src/lib/pycv.py -> src/lib -> src -> root
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Define absolute paths for assets
        self.path_data = os.path.join(self.root_dir, 'config', 'data.toml')
        self.path_html = os.path.join(self.root_dir, 'config', 'template.html')
        self.path_css = os.path.join(self.root_dir, 'config', 'style.css')
        self.path_output = os.path.join(self.root_dir, 'output')

    def generate_pdf(self):
        if self._validate_structure():
            logger.info("Config found. Generating PDF...")

            # 1. Load Data from TOML
            with open(self.path_data, "rb") as f:
                data = tomli.load(f)

            # 2. Setup Jinja2 Environment
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.root_dir))
            template = jinja_env.get_template("config/template.html")

            # 3. Render HTML with Data
            rendered_html = template.render(data)

            # 4. Generate PDF using WeasyPrint
            output_name = "cv.pdf"
            output_path = os.path.join(self.path_output, output_name)
            logger.info(f"Generating {output_name}...")
            HTML(string=rendered_html, base_url='.').write_pdf(output_path)
            logger.info(f"Done! File saved: {output_path}")

        else:
            logger.info("Aborting PDF generation due to missing files.")

    def _validate_structure(self):
        """Checks if the required config and template files exist."""
        missing = []
        for path in [self.path_data, self.path_html, self.path_css]:
            if not os.path.exists(path):
                missing.append(path)

        if missing:
            logger.info("Warning: The following files are missing:\n" + "\n".join(missing))
            return False
        return True
