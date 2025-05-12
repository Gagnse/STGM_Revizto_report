"""
PDF generator module for Revizto reports
Using fpdf2 library to create PDF reports
"""

from fpdf import FPDF
import base64
import re
import os
import logging
from datetime import datetime
import tempfile
from io import BytesIO

# Set up logger
logger = logging.getLogger(__name__)


class ReviztoPDF(FPDF):
    """
    Custom PDF class for Revizto report generation.
    Extends FPDF from fpdf2 library with custom headers and footers.
    """

    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
        # Set default margins
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(True, margin=15)
        # Initialize variables
        self.title = ""
        self.project_name = ""
        self.report_date = ""
        self.visitNumber = ""


    def header(self):
        """
        Custom header for each page
        """
        # Logo
        try:
            # Check if using a custom logo from static folder
            logo_path = os.path.join('static', 'images', 'STGM_Logotype_RVB_Architecture_Noir.png')
            if os.path.exists(logo_path):
                self.image(logo_path, 6, 8, 50)
            else:
                # Default behavior if no logo found
                self.set_font('helvetica', 'B', 15)
                self.cell(0, 10, 'STGM Architecture', 0, 1, 'C')
        except Exception as e:
            logger.error(f"Error loading logo: {e}")
            # Default behavior if logo loading fails
            self.set_font('helvetica', 'B', 15)
            self.cell(0, 10, 'STGM Architecture', 0, 1, 'C')

        # Project info
        self.set_font('helvetica', 'B', 12)
        if self.project_name:
            self.cell(0, 10, f'{self.project_name}', 0, 1, 'R')
        if self.report_date:
            self.cell(0, 5, f'{self.report_date}', 0, 1, 'R')

        # Set line thickness (width) - default is 0.2 mm
        current_line_width = self.line_width
        self.set_line_width(0.75)  # Adjust this value to your preferred thickness

        # Define line position with padding
        padding_top = 35  # Adjust this value for more/less top padding

        # Draw a line
        self.line(15, padding_top, 195, padding_top)

        # Reset line width to previous value
        self.set_line_width(current_line_width)

        # Line break
        self.ln(4)  # You might want to adjust this too based on your padding

        self.set_font('helvetica', 'B', 10)
        self.cell(0, 10, "NOTE DE VISITE DE CHANTIER", 0, 0, 'R')
        self.ln(5)

    def footer(self):
        """
        Custom footer for each page
        """
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Set font
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')
        # Copyright
        self.cell(0, 10, f'© {datetime.now().year} STGM Architecture', 0, 0, 'R')

    def chapter_title(self, title):
        """
        Add a chapter title
        """
        self.ln(2)
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(255, 225, 255)
        self.cell(30, 6, title, 0, 1, 'L', 0)
        self.ln(2)

    def chapter_body(self, body):
        """
        Add chapter body content
        """
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

    def section_title(self, title):
        """
        Add a section title
        """
        self.set_font('helvetica', 'B', 11)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(2)

    def add_status_badge(self, status_name, bg_color=(0, 123, 255), text_color=(255, 255, 255)):
        """
        Add a status badge with background color and text color

        Args:
            status_name (str): The status name to display
            bg_color (tuple): RGB background color tuple (default: blue)
            text_color (tuple): RGB text color tuple (default: white)
        """
        # Save current position and properties
        x, y = self.get_x(), self.get_y()

        # Store original fill and text colors
        # The fill_color and text_color properties return dictionaries with 'r', 'g', 'b' keys
        # We need to convert them to a format we can use later
        original_fill_color = self.fill_color
        original_text_color = self.text_color

        # Set new colors
        self.set_fill_color(bg_color[0], bg_color[1], bg_color[2])
        self.set_text_color(text_color[0], text_color[1], text_color[2])

        # Draw badge
        self.set_font('helvetica', 'B', 9)
        width = self.get_string_width(status_name) + 6
        self.rect(x, y, width, 5, 'F')
        self.cell(width, 5, status_name, 0, 0, 'C')

        # Restore colors and move position
        # Check if original colors are dictionaries with 'r', 'g', 'b' keys
        if isinstance(original_fill_color, dict) and 'r' in original_fill_color:
            self.set_fill_color(original_fill_color['r'], original_fill_color['g'], original_fill_color['b'])
        else:
            # Default to black if original fill color format is unexpected
            self.set_fill_color(0, 0, 0)

        if isinstance(original_text_color, dict) and 'r' in original_text_color:
            self.set_text_color(original_text_color['r'], original_text_color['g'], original_text_color['b'])
        else:
            # Default to black if original text color format is unexpected
            self.set_text_color(0, 0, 0)

        self.set_xy(x + width + 5, y)

    def add_observation(self, observation):
        """
        Add an observation to the report

        Args:
            observation (dict): The observation data
        """
        # Check required fields
        if not observation.get('id'):
            return

        # Get title - either string or object with value
        title = 'No Title'
        if observation.get('title'):
            if isinstance(observation['title'], str):
                title = observation['title']
            elif isinstance(observation['title'], dict) and observation['title'].get('value'):
                title = observation['title']['value']

        # Get status info
        status_text = "Unknown"
        bg_color = (110, 110, 110)  # Default gray

        if observation.get('customStatus'):
            status_id = observation['customStatus']
            if isinstance(status_id, dict) and status_id.get('value'):
                status_id = status_id['value']

            # Status colors match those in issue-data.js
            if status_id == "2ed005c6-43cd-4907-a4d6-807dbd0197d5":  # Open
                status_text = "Ouvert"
                bg_color = (204, 41, 41)  # Red
            elif status_id == "cd52ac3e-f345-4f99-870f-5be95dc33245":  # In progress
                status_text = "En cours"
                bg_color = (255, 170, 0)  # Orange
            elif status_id == "b8504242-3489-43a2-9831-54f64053b226":  # Solved
                status_text = "Résolu"
                bg_color = (66, 190, 101)  # Green
            elif status_id == "135b58c6-1e14-4716-a134-bbba2bbc90a7":  # Closed
                status_text = "Fermé"
                bg_color = (184, 184, 184)  # Gray

        # Start observation
        self.set_font('helvetica', 'B', 10)
        self.cell(10, 6, f"#{observation['id']}", 0, 0, 'L')
        self.add_status_badge(status_text, bg_color)
        self.ln(8)

        # Title and description
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(2)

        # If there's a preview image, add it
        image_url = None
        if observation.get('preview'):
            if isinstance(observation['preview'], str):
                image_url = observation['preview']
            elif isinstance(observation['preview'], dict) and observation['preview'].get('original'):
                image_url = observation['preview']['original']

        if image_url and image_url.startswith('data:image'):
            try:
                # Extract the base64 data
                img_data = re.sub('^data:image/.+;base64,', '', image_url)
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp:
                    temp_file = temp.name
                    temp.write(base64.b64decode(img_data))
                # Add to PDF
                self.image(temp_file, x=15, y=None, w=80)
                # Clean up
                os.unlink(temp_file)
            except Exception as e:
                logger.error(f"Error adding image: {e}")

        # Add additional information
        self.ln(5)
        self.set_font('helvetica', '', 9)

        # Format creation date if available
        created_date = "N/A"
        if observation.get('created'):
            if isinstance(observation['created'], str):
                created_date = observation['created']
            elif isinstance(observation['created'], dict) and observation['created'].get('value'):
                created_date = observation['created']['value']
            try:
                created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
            except:
                pass

        # Add metadata table
        self.set_fill_color(240, 240, 240)
        self.cell(40, 5, "Posée le:", 1, 0, 'L', 1)
        self.cell(50, 5, created_date, 1, 1, 'L')

        # Sheet information
        sheet_number = "N/A"
        if observation.get('sheet'):
            if isinstance(observation['sheet'], dict) and observation['sheet'].get('value'):
                sheet = observation['sheet']['value']
                if sheet.get('number'):
                    sheet_number = sheet['number']
            elif isinstance(observation['sheet'], str):
                sheet_number = observation['sheet']

        self.cell(40, 5, "Numéro de la feuille:", 1, 0, 'L', 1)
        self.cell(50, 5, str(sheet_number), 1, 1, 'L')

        # End observation section
        self.ln(10)

    def add_instruction(self, instruction):
        """
        Add an instruction to the report

        Args:
            instruction (dict): The instruction data
        """
        # Same structure as observation with slight modifications
        # Check required fields
        if not instruction.get('id'):
            return

        # Get title
        title = 'No Title'
        if instruction.get('title'):
            if isinstance(instruction['title'], str):
                title = instruction['title']
            elif isinstance(instruction['title'], dict) and instruction['title'].get('value'):
                title = instruction['title']['value']

        # Get status info
        status_text = "Unknown"
        bg_color = (110, 110, 110)  # Default gray

        if instruction.get('customStatus'):
            status_id = instruction['customStatus']
            if isinstance(status_id, dict) and status_id.get('value'):
                status_id = status_id['value']

            # Status colors match those in issue-data.js
            if status_id == "2ed005c6-43cd-4907-a4d6-807dbd0197d5":  # Open
                status_text = "Ouvert"
                bg_color = (204, 41, 41)  # Red
            elif status_id == "cd52ac3e-f345-4f99-870f-5be95dc33245":  # In progress
                status_text = "En cours"
                bg_color = (255, 170, 0)  # Orange
            elif status_id == "b8504242-3489-43a2-9831-54f64053b226":  # Solved
                status_text = "Résolu"
                bg_color = (66, 190, 101)  # Green
            elif status_id == "135b58c6-1e14-4716-a134-bbba2bbc90a7":  # Closed
                status_text = "Fermé"
                bg_color = (184, 184, 184)  # Gray

        # Start instruction
        self.set_font('helvetica', 'B', 10)
        self.cell(10, 6, f"#{instruction['id']}", 0, 0, 'L')
        self.add_status_badge(status_text, bg_color)
        self.ln(8)

        # Title and description
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(2)

        # If there's a preview image, add it
        image_url = None
        if instruction.get('preview'):
            if isinstance(instruction['preview'], str):
                image_url = instruction['preview']
            elif isinstance(instruction['preview'], dict) and instruction['preview'].get('original'):
                image_url = instruction['preview']['original']

        if image_url and image_url.startswith('data:image'):
            try:
                # Extract the base64 data
                img_data = re.sub('^data:image/.+;base64,', '', image_url)
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp:
                    temp_file = temp.name
                    temp.write(base64.b64decode(img_data))
                # Add to PDF
                self.image(temp_file, x=15, y=None, w=80)
                # Clean up
                os.unlink(temp_file)
            except Exception as e:
                logger.error(f"Error adding image: {e}")

        # Add additional information
        self.ln(5)
        self.set_font('helvetica', '', 9)

        # Format creation date if available
        created_date = "N/A"
        if instruction.get('created'):
            if isinstance(instruction['created'], str):
                created_date = instruction['created']
            elif isinstance(instruction['created'], dict) and instruction['created'].get('value'):
                created_date = instruction['created']['value']
            try:
                created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
            except:
                pass

        # Add metadata table
        self.set_fill_color(240, 240, 240)
        self.cell(40, 5, "Posée le:", 1, 0, 'L', 1)
        self.cell(50, 5, created_date, 1, 1, 'L')

        # Sheet information
        sheet_number = "N/A"
        if instruction.get('sheet'):
            if isinstance(instruction['sheet'], dict) and instruction['sheet'].get('value'):
                sheet = instruction['sheet']['value']
                if sheet.get('number'):
                    sheet_number = sheet['number']
            elif isinstance(instruction['sheet'], str):
                sheet_number = instruction['sheet']

        self.cell(40, 5, "Numéro de la feuille:", 1, 0, 'L', 1)
        self.cell(50, 5, str(sheet_number), 1, 1, 'L')

        # End instruction section
        self.ln(10)

    def add_deficiency(self, deficiency):
        """
        Add a deficiency to the report

        Args:
            deficiency (dict): The deficiency data
        """
        # Similar structure to observations and instructions
        # Check required fields
        if not deficiency.get('id'):
            return

        # Get title
        title = 'No Title'
        if deficiency.get('title'):
            if isinstance(deficiency['title'], str):
                title = deficiency['title']
            elif isinstance(deficiency['title'], dict) and deficiency['title'].get('value'):
                title = deficiency['title']['value']

        # Get status info
        status_text = "Unknown"
        bg_color = (110, 110, 110)  # Default gray

        if deficiency.get('customStatus'):
            status_id = deficiency['customStatus']
            if isinstance(status_id, dict) and status_id.get('value'):
                status_id = status_id['value']

            # Status colors match those in issue-data.js
            if status_id == "2ed005c6-43cd-4907-a4d6-807dbd0197d5":  # Open
                status_text = "Ouvert"
                bg_color = (204, 41, 41)  # Red
            elif status_id == "cd52ac3e-f345-4f99-870f-5be95dc33245":  # In progress
                status_text = "En cours"
                bg_color = (255, 170, 0)  # Orange
            elif status_id == "b8504242-3489-43a2-9831-54f64053b226":  # Solved
                status_text = "Résolu"
                bg_color = (66, 190, 101)  # Green
            elif status_id == "135b58c6-1e14-4716-a134-bbba2bbc90a7":  # Closed
                status_text = "Fermé"
                bg_color = (184, 184, 184)  # Gray

        # Start deficiency
        self.set_font('helvetica', 'B', 10)
        self.cell(10, 6, f"#{deficiency['id']}", 0, 0, 'L')
        self.add_status_badge(status_text, bg_color)
        self.ln(8)

        # Title and description
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(2)

        # If there's a preview image, add it
        image_url = None
        if deficiency.get('preview'):
            if isinstance(deficiency['preview'], str):
                image_url = deficiency['preview']
            elif isinstance(deficiency['preview'], dict) and deficiency['preview'].get('original'):
                image_url = deficiency['preview']['original']

        if image_url and image_url.startswith('data:image'):
            try:
                # Extract the base64 data
                img_data = re.sub('^data:image/.+;base64,', '', image_url)
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp:
                    temp_file = temp.name
                    temp.write(base64.b64decode(img_data))
                # Add to PDF
                self.image(temp_file, x=15, y=None, w=80)
                # Clean up
                os.unlink(temp_file)
            except Exception as e:
                logger.error(f"Error adding image: {e}")

        # Add additional information
        self.ln(5)
        self.set_font('helvetica', '', 9)

        # Format creation date if available
        created_date = "N/A"
        if deficiency.get('created'):
            if isinstance(deficiency['created'], str):
                created_date = deficiency['created']
            elif isinstance(deficiency['created'], dict) and deficiency['created'].get('value'):
                created_date = deficiency['created']['value']
            try:
                created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
            except:
                pass

        # Add metadata table
        self.set_fill_color(240, 240, 240)
        self.cell(40, 5, "Posée le:", 1, 0, 'L', 1)
        self.cell(50, 5, created_date, 1, 1, 'L')

        # Sheet information
        sheet_number = "N/A"
        if deficiency.get('sheet'):
            if isinstance(deficiency['sheet'], dict) and deficiency['sheet'].get('value'):
                sheet = deficiency['sheet']['value']
                if sheet.get('number'):
                    sheet_number = sheet['number']
            elif isinstance(deficiency['sheet'], str):
                sheet_number = deficiency['sheet']

        self.cell(40, 5, "Numéro de la feuille:", 1, 0, 'L', 1)
        self.cell(50, 5, str(sheet_number), 1, 1, 'L')

        # Add assignee if available
        assignee = "Non assignée"
        if deficiency.get('assignee'):
            if isinstance(deficiency['assignee'], str):
                assignee = deficiency['assignee']
            elif isinstance(deficiency['assignee'], dict) and deficiency['assignee'].get('value'):
                assignee = deficiency['assignee']['value']

        self.cell(40, 5, "Assignée à:", 1, 0, 'L', 1)
        self.cell(50, 5, assignee, 1, 1, 'L')

        # End deficiency section
        self.ln(10)

    def add_general_notes(self):
        """
        Add the general notes section to the PDF
        """
        self.add_page()
        self.chapter_title("NOTES GÉNÉRALES")

        # Section A: Observations
        self.section_title("A. Observations")
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 5, "Généralités:", 0, 1)
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5,
                        "Les éléments listés ci-dessous documentent l'état général d'avancement du chantier et ils ne nécessitent donc aucun suivi de la part de l'Entrepreneur.")
        self.ln(5)

        # Section B: Instructions
        self.section_title("B. Instructions")
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 5, "Généralités:", 0, 1)
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5,
                        "Les éléments listés ci-dessous documentent les instructions données à l'Entrepreneur et ils nécessitent donc un suivi de sa part.")
        self.ln(5)

        # Section C: Déficiences
        self.section_title("C. Déficiences")
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 5, "Généralités:", 0, 1)
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5,
                        "La liste de Déficiences ci-dessous est non-limitative et ne relève pas l'Entrepreneur et ses Sous-traitants de leurs responsabilités de se conformer aux exigences des plans, devis et autres Documents contractuels et notamment en ce qui concerne la complétion de l'Ouvrage. En outre, elle doit être complétée par celles des autres Professionnels concernés.")
        self.ln(5)

        self.set_font('helvetica', 'B', 10)
        self.cell(0, 5, "Procédure:", 0, 1)
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5,
                        "Les Déficiences doivent être corrigés dans les dix (10) jours ouvrables suivant la réception du présent document. Le surintendant de l'Entrepreneur doit traiter les Déficiences sur cette liste et la faire suivre à l'Architecte dès que les travaux correctifs ont été effectués. Aucune retenue monétaire ne sera libérée tant et aussi longtemps que les Déficiences n'auront été entièrement et parfaitement corrigées.")
        self.ln(5)

        self.set_font('helvetica', 'B', 10)
        self.cell(0, 5, "Honoraires supplémentaires:", 0, 1)
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5,
                        "Après la Réception provisoire de l'ouvrage, l'Architecte prévoit une seule visite pour procéder à l'acceptation finale des travaux correctifs et il facturera, au Maître de l'ouvrage, des honoraires supplémentaires de 1 000 $/visite supplémentaire. Le montant total des honoraires supplémentaire sera prélevé par le Maître de l'ouvrage à même les sommes dues à l'Entrepreneur en vertu de son Contrat. L'Entrepreneur est responsable de s'assurer que toutes les Déficiences, incluant celles de ses Sous-traitants et de ses Fournisseurs, ont bel et bien été entièrement et parfaitement corrigées.")
        self.ln(5)

        self.set_font('helvetica', 'B', 10)
        self.cell(0, 5, "Classement des couleurs des pastilles:", 0, 1)
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5,
                        "Rouge (Ouvert) : Nouvelle observation/instruction/déficience constatée par l'Architecte.\nOrange (En cours) : observation/instruction/déficience d'une visite précédente dont l'entrepreneur travaille à sa résolution.\nMauve (Corrigé) : déficience traitée par l'entrepreneur, prête à être validée par l'Architecte.\nJaune (En attente) : Status lorsque le problème dépend d'une décision externe à l'entrepreneur.\nVert (Résolu) : déficience dont la correction est approuvée par l'Architecte.")

    def add_info_page(self, project_data):
        """
        Add the project information page with information in a single column on the left
        and the image on the right

        Args:
            project_data (dict): The project data dictionary
        """
        self.add_page()

        # Set up page layout
        page_width = self.w - 2 * self.l_margin
        info_column_width = page_width * 0.55  # 55% of page width for information
        image_column_width = page_width * 0.45  # 45% of page width for image

        # Visit number at the top
        self.set_font('helvetica', 'B', 25)
        self.cell(0, 10, project_data.get('visitNumber', ''), 0, 1, 'L')
        self.ln(10)

        # Save starting y position for the image column
        starting_y = self.get_y()

        # -- LEFT COLUMN (Project Information) --

        # Project information
        self.set_font('helvetica', 'B', 12)
        self.cell(info_column_width, 10, "NOTES", 0, 1, 'L')

        # Format dates if provided
        report_date = project_data.get('reportDate', '')
        if report_date:
            try:
                report_date = datetime.strptime(report_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            except:
                pass

        visit_date = project_data.get('visitDate', '')
        if visit_date:
            try:
                visit_date = datetime.strptime(visit_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            except:
                pass

        # Project details in a table (single column format)
        self.set_font('helvetica', '', 10)
        self.set_fill_color(255, 255, 255)
        row_height = 7

        # Row settings
        label_width = 35
        field_width = info_column_width - label_width

        # Dossier Architecte
        self.set_fill_color(255, 255, 255)
        self.cell(label_width, row_height, "Dossier Architecte:", 0, 0, 'L', 1)
        self.cell(field_width, row_height, project_data.get('architectFile', ''), 0, 1, 'L')

        # Projet
        self.cell(label_width, row_height, "Projet:", 0, 0, 'L', 1)
        self.cell(field_width, row_height, project_data.get('projectName', ''), 0, 1, 'L')

        # Maitre de l'ouvrage
        self.cell(label_width, row_height, "Maitre de l'ouvrage:", 0, 0, 'L', 1)
        self.cell(field_width, row_height, project_data.get('projectOwner', ''), 0, 1, 'L')

        # Entrepreneur
        self.cell(label_width, row_height, "Entrepreneur:", 0, 0, 'L', 1)
        self.cell(field_width, row_height, project_data.get('contractor', ''), 0, 1, 'L')

        # Visite no.
        self.cell(label_width, row_height, "Visite no.:", 0, 0, 'L', 1)
        self.cell(field_width, row_height, project_data.get('visitNumber', ''), 0, 1, 'L')

        # Date du rapport
        self.cell(label_width, row_height, "Date du rapport:", 0, 0, 'L', 1)
        self.cell(field_width, row_height, report_date, 0, 1, 'L')

        # Visite effectuée par
        self.cell(label_width, row_height, "Visite effectuée par:", 0, 0, 'L', 1)
        self.cell(field_width, row_height, project_data.get('visitBy', ''), 0, 1, 'L')

        # Date de la visite
        self.cell(label_width, row_height, "Date de la visite:", 0, 0, 'L', 1)
        self.cell(field_width, row_height, visit_date, 0, 1, 'L')

        # En présence de
        self.cell(label_width, row_height, "En présence de:", 0, 0, 'L', 1)
        self.cell(field_width, row_height, project_data.get('inPresenceOf', ''), 0, 1, 'L')

        # -- RIGHT COLUMN (Project Image) --

        # Save current position before moving to image column
        info_end_y = self.get_y()

        # Project image
        if project_data.get('imageUrl'):
            try:
                # Move to the right column position at the same starting Y
                self.set_xy(self.l_margin + info_column_width + 10, starting_y + 10)

                # Extract the base64 data if it's a data URL
                image_url = project_data['imageUrl']
                if image_url.startswith('data:image'):
                    img_data = re.sub('^data:image/.+;base64,', '', image_url)

                    # Create temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp:
                        temp_file = temp.name
                        temp.write(base64.b64decode(img_data))

                    # Calculate image dimensions to fit in the right column
                    image_width = image_column_width - 10  # Leave some margin

                    # Add to PDF
                    self.image(temp_file, x=self.l_margin + info_column_width + 10, y=None, w=image_width)

                    # Clean up
                    os.unlink(temp_file)
            except Exception as e:
                logger.error(f"Error adding project image: {e}")

        # Move cursor position back to the end of the left column content
        self.set_y(max(self.get_y(), info_end_y) + 10)

        # Add horizontal line
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.l_margin + page_width, self.get_y())
        self.ln(1)  # Add space after the line

        # Description section
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 10, "DESCRIPTION DU PROJET", 0, 1, 'L')

        # Project description if available
        if project_data.get('description'):
            self.set_font('helvetica', '', 10)
            self.multi_cell(page_width, 5, project_data.get('description', ''))
        else:
            self.ln(5)  # Add some space if no description

        # Add another horizontal line
        self.ln(3)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.l_margin + page_width, self.get_y())
        self.ln(1)  # Add space after the line

        # Distribution section
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 10, "LISTE DE DISTRIBUTION", 0, 1, 'L')

        # Distribution content if available
        if project_data.get('distribution'):
            self.set_font('helvetica', '', 10)
            self.multi_cell(page_width, 5, project_data.get('distribution', ''))

        # Reset line width to default
        self.set_line_width(0.2)

def generate_report_pdf(project_id, project_data, observations, instructions, deficiencies):
    """
    Generate a PDF report for the project

    Args:
        project_id (int): Project ID
        project_data (dict): Project information
        observations (list): List of observations
        instructions (list): List of instructions
        deficiencies (list): List of deficiencies

    Returns:
        BytesIO: PDF file as a BytesIO object
    """
    # Create PDF
    pdf = ReviztoPDF()

    # Set metadata
    pdf.set_title(f"Rapport de visite - Projet {project_data.get('projectName', project_id)}")
    pdf.set_author("STGM Architecture")
    pdf.set_creator("STGM Revizto Report Generator")

    # Set PDF properties
    pdf.project_name = project_data.get('projectName', f"Projet {project_id}")
    if project_data.get('reportDate'):
        try:
            pdf.report_date = datetime.strptime(project_data['reportDate'], '%Y-%m-%d').strftime(
                '%d/%m/%Y')
        except:
            pdf.report_date = project_data['reportDate']

    # Add project information page
    pdf.add_info_page(project_data)

    # Add general notes
    pdf.add_general_notes()

    # Add observations section if any observations
    if observations and len(observations) > 0:
        pdf.add_page()
        pdf.chapter_title("1 - OBSERVATIONS")

        # Filter out closed issues
        open_observations = [obs for obs in observations if not is_closed_issue(obs)]

        if len(open_observations) > 0:
            for observation in open_observations:
                pdf.add_observation(observation)
        else:
            pdf.set_font('helvetica', 'I', 10)
            pdf.cell(0, 6, "Aucune observation trouvée", 0, 1, 'L')

    # Add instructions section if any instructions
    if instructions and len(instructions) > 0:
        pdf.add_page()
        pdf.chapter_title("2 - INSTRUCTIONS")

        # Filter out closed issues
        open_instructions = [ins for ins in instructions if not is_closed_issue(ins)]

        if len(open_instructions) > 0:
            for instruction in open_instructions:
                pdf.add_instruction(instruction)
        else:
            pdf.set_font('helvetica', 'I', 10)
            pdf.cell(0, 6, "Aucune instruction trouvée", 0, 1, 'L')

    # Add deficiencies section if any deficiencies
    if deficiencies and len(deficiencies) > 0:
        pdf.add_page()
        pdf.chapter_title("3 - DÉFICIENCES")

        # Filter out closed issues
        open_deficiencies = [df for df in deficiencies if not is_closed_issue(df)]

        if len(open_deficiencies) > 0:
            for deficiency in open_deficiencies:
                pdf.add_deficiency(deficiency)
        else:
            pdf.set_font('helvetica', 'I', 10)
            pdf.cell(0, 6, "Aucune déficience trouvée", 0, 1, 'L')

    # Create a BytesIO object to store the PDF
    pdf_buffer = BytesIO()

    # Save PDF to BytesIO object
    pdf.output(pdf_buffer)

    # Reset buffer position to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer

def is_closed_issue(issue):
    """
    Check if an issue is closed

    Args:
        issue (dict): Issue data

    Returns:
        bool: True if issue is closed, False otherwise
    """
    # Check for status id from customStatus or status
    status_id = None

    if issue.get('customStatus'):
        if isinstance(issue['customStatus'], str):
            status_id = issue['customStatus']
        elif isinstance(issue['customStatus'], dict) and issue['customStatus'].get('value'):
            status_id = issue['customStatus']['value']
    elif issue.get('status'):
        if isinstance(issue['status'], str):
            status_id = issue['status']
        elif isinstance(issue['status'], dict) and issue['status'].get('value'):
            status_id = issue['status']['value']

    # Check if status is "Closed" (UUID match or string match)
    if status_id:
        # Direct UUID match for Closed
        if status_id == "135b58c6-1e14-4716-a134-bbba2bbc90a7":
            return True

        # String comparison for "closed"
        if isinstance(status_id, str) and status_id.lower() == "closed":
            return True

    return False