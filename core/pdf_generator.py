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

    # In core/pdf_generator.py, update the add_observation method

    def add_observation(self, observation, comments=None):
        """
        Add an observation to the report with the layout:
        - Top: Two columns (image + information)
        - Bottom: Full-width history section
        - Ensures no card is ever split between pages

        Args:
            observation (dict): The observation data
            comments (list, optional): List of comments/history for this observation
        """
        # Check required fields
        if not observation.get('id'):
            return

        # Get title - either string or object with value
        title = 'Sans titre'
        if observation.get('title'):
            if isinstance(observation['title'], str):
                title = observation['title']
            elif isinstance(observation['title'], dict) and observation['title'].get('value'):
                title = observation['title']['value']

        # Get status info
        status_text = "Inconnu"
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
            elif status_id == "5947b7d1-70b9-425b-aba6-7187eb0251ff":  # En attente
                status_text = "En attente"
                bg_color = (255, 211, 46)  # Yellow
            elif status_id == "912abbbf-3155-4e3c-b437-5778bdfd73f4":  # non-problème
                status_text = "Non-problème"
                bg_color = (43, 43, 43)  # Dark gray
            elif status_id == "337e2fe6-e2a3-4e3f-b098-30aac68a191c":  # Corrigé
                status_text = "Corrigé"
                bg_color = (137, 46, 251)  # Purple

        # Calculate page dimensions
        page_width = self.w - 2 * self.l_margin

        # Check if we have comments to determine the total height
        comment_section_height = 0
        if comments and len(comments) > 0:
            # Ensure comments is a list of dicts, not strings
            valid_comments = []
            for comment in comments:
                if isinstance(comment, dict):
                    valid_comments.append(comment)
                elif isinstance(comment, str):
                    try:
                        # If it's a JSON string, try to parse it
                        import json
                        comment_dict = json.loads(comment)
                        if isinstance(comment_dict, dict):
                            valid_comments.append(comment_dict)
                    except:
                        # If parsing fails, skip this comment
                        logger.warning(f"Skipping invalid comment format: {comment[:50]}...")

            # Only proceed if we have valid comments
            if valid_comments:
                # Estimate about 10mm per comment, with a minimum of 30mm
                comment_section_height = max(30, min(100, len(valid_comments) * 10))  # min 30mm, max 100mm

        # Estimate card height - this is an important step to avoid page breaks within cards
        estimated_card_height = 120 + comment_section_height  # Base height + comment height

        # Force a page break if the card won't fit on the current page
        if self.get_y() + estimated_card_height > self.h - self.b_margin:
            self.add_page()
            # Set a proper top margin after page break
            self.set_y(self.t_margin + 30)

        # Remember the start position of the card
        card_start_y = self.get_y()

        # ===== HEADER SECTION =====

        # Header height
        header_height = 10

        # Header background (light gray)
        self.set_fill_color(240, 240, 240)
        self.rect(self.l_margin, card_start_y, page_width, header_height, 'F')

        # Header border
        self.rect(self.l_margin, card_start_y, page_width, header_height)

        # ID in header
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.set_xy(self.l_margin + 4, card_start_y + 2)
        self.cell(25, 6, f"#{observation['id']}", 0, 0, 'L')

        # Status badge in header
        badge_width = self.get_string_width(status_text) + 10
        badge_x = self.w - self.r_margin - badge_width - 5

        self.set_xy(badge_x, card_start_y + 2)
        self.set_fill_color(bg_color[0], bg_color[1], bg_color[2])
        self.set_text_color(255, 255, 255)
        self.set_font('helvetica', 'B', 9)
        self.rect(badge_x, card_start_y + 2, badge_width, 6, 'F')
        self.cell(badge_width, 6, status_text, 0, 0, 'C')

        # Reset text color
        self.set_text_color(0, 0, 0)

        # ===== TOP SECTION - TWO COLUMNS =====

        # Top section starts below header
        top_section_y = card_start_y + header_height
        top_section_height = 60

        # Column widths
        image_col_width = page_width * 0.33  # 33% for image
        info_col_width = page_width * 0.66  # 66% for information

        # Column positions
        image_col_x = self.l_margin
        info_col_x = image_col_x + image_col_width

        # Top section background (white)
        self.set_fill_color(255, 255, 255)
        self.rect(self.l_margin, top_section_y, page_width, top_section_height, 'FD')

        # Vertical divider between image and info
        self.line(info_col_x, top_section_y, info_col_x, top_section_y + top_section_height)

        # ===== IMAGE COLUMN =====

        # Check if there's a preview image
        image_url = None
        if observation.get('preview'):
            if isinstance(observation['preview'], str):
                image_url = observation['preview']
            elif isinstance(observation['preview'], dict) and observation['preview'].get('original'):
                image_url = observation['preview']['original']

        # Add image if available
        if image_url:
            try:
                # Handle base64 data URLs
                if image_url.startswith('data:image'):
                    # Extract the base64 data
                    img_data = re.sub('^data:image/.+;base64,', '', image_url)
                    # Create temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp:
                        temp_file = temp.name
                        temp.write(base64.b64decode(img_data))
                # Handle HTTP URLs by downloading the image
                elif image_url.startswith(('http://', 'https://')):
                    import urllib.request
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp:
                        temp_file = temp.name
                        urllib.request.urlretrieve(image_url, temp_file)
                else:
                    # Assume it's a local file path
                    temp_file = image_url

                # Fixed top padding
                top_padding = 2  # Space from the top edge of column
                side_padding = 2  # Space from the sides

                # Maximum available space for the image
                max_width = image_col_width - (side_padding * 2)
                max_height = top_section_height - (top_padding * 2)

                # Get original image dimensions to maintain aspect ratio
                try:
                    from PIL import Image
                    img = Image.open(temp_file)
                    img_width, img_height = img.size
                    aspect_ratio = img_width / img_height
                except:
                    # If PIL not available or error, use a default aspect ratio
                    aspect_ratio = 4 / 3  # Common default

                # Calculate dimensions while preserving aspect ratio
                if aspect_ratio > 1:  # Wider than tall
                    # Width is the limiting factor
                    image_width = max_width
                    image_height = image_width / aspect_ratio
                    # Check if height exceeds maximum
                    if image_height > max_height:
                        image_height = max_height
                        image_width = image_height * aspect_ratio
                else:  # Taller than wide or square
                    # Height is the limiting factor
                    image_height = max_height
                    image_width = image_height * aspect_ratio
                    # Check if width exceeds maximum
                    if image_width > max_width:
                        image_width = max_width
                        image_height = image_width / aspect_ratio

                # Calculate Y position - fixed at top with padding
                image_y = top_section_y + top_padding

                # Center the image horizontally
                image_x = image_col_x + ((image_col_width - image_width) / 2)

                # Add image to PDF (without specifying height will maintain aspect ratio)
                self.image(temp_file, x=image_x, y=image_y, w=image_width)

                # Clean up if we created a temp file
                if image_url.startswith(('data:image', 'http://', 'https://')):
                    os.unlink(temp_file)
            except Exception as e:
                logger.error(f"Error adding image: {e}")

        else:
            # Display placeholder if no image
            self.set_xy(image_col_x + 5, top_section_y + 10)  # Fixed top position
            self.set_font('helvetica', 'I', 8)
            self.cell(image_col_width - 10, 10, "Pas d'image", 0, 0, 'C')

        # ===== INFORMATION COLUMN =====

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

        # Get assignee
        assignee = "Non assignée"
        if observation.get('assignee'):
            if isinstance(observation['assignee'], str):
                assignee = observation['assignee']
            elif isinstance(observation['assignee'], dict) and observation['assignee'].get('value'):
                assignee = observation['assignee']['value']

        # Sheet information
        sheet_number = "N/A"
        sheet_name = "N/A"
        if observation.get('sheet'):
            if isinstance(observation['sheet'], dict) and observation['sheet'].get('value'):
                sheet = observation['sheet']['value']
                if sheet.get('number'):
                    sheet_number = sheet['number']
                if sheet.get('name'):
                    sheet_name = sheet['name']
            elif isinstance(observation['sheet'], str):
                sheet_number = observation['sheet']

        # Title at the top of info column
        self.set_xy(info_col_x + 5, top_section_y + 5)
        self.set_font('helvetica', 'B', 10)
        self.multi_cell(info_col_width - 10, 5, title, 0, 'L')

        # Start position for metadata
        info_y = self.get_y() + 2

        # Metadata layout - using a more efficient layout with proper spacing
        # UPDATED: Modified field widths and layout to bring values closer to labels
        # and prevent overlapping by ensuring proper cell widths

        # Calculate optimal field widths for the two columns
        col_padding = 5  # Padding for each column
        col_width = (info_col_width - (col_padding * 2)) / 2  # Width of each column

        # Adjust label and value widths (make label width smaller to allow more space for values)
        label_width = col_width * 0.4  # 40% of column width for label
        value_width = col_width * 0.6  # 60% of column width for value

        # First row
        # Left column: Assignee
        self.set_xy(info_col_x + col_padding, info_y)
        self.set_font('helvetica', 'B', 8)
        self.cell(label_width, 5, "Assignée à:", 0, 0, 'L')
        self.set_font('helvetica', '', 8)
        # Use multi_cell for value to handle text wrapping for long values
        current_x = self.get_x()
        current_y = self.get_y()
        self.multi_cell(value_width, 5, assignee, 0, 'L')
        max_y1 = self.get_y()

        # Right column: Date created
        self.set_xy(info_col_x + col_padding + col_width, info_y)
        self.set_font('helvetica', 'B', 8)
        self.cell(label_width, 5, "Posée le:", 0, 0, 'L')
        self.set_font('helvetica', '', 8)
        current_x = self.get_x()
        current_y = self.get_y()
        self.multi_cell(value_width, 5, created_date, 0, 'L')
        max_y2 = self.get_y()

        # Find max Y position after first row
        info_y = max(max_y1, max_y2) + 2

        # Second row
        # Left column: Sheet Name
        self.set_xy(info_col_x + col_padding, info_y)
        self.set_font('helvetica', 'B', 8)
        self.cell(label_width, 5, "Nom feuille:", 0, 0, 'L')
        self.set_font('helvetica', '', 8)
        current_x = self.get_x()
        current_y = self.get_y()
        self.multi_cell(value_width, 5, str(sheet_name), 0, 'L')
        max_y1 = self.get_y()

        # Right column: Sheet Number
        self.set_xy(info_col_x + col_padding + col_width, info_y)
        self.set_font('helvetica', 'B', 8)
        self.cell(label_width, 5, "No feuille:", 0, 0, 'L')
        self.set_font('helvetica', '', 8)
        current_x = self.get_x()
        current_y = self.get_y()
        self.multi_cell(value_width, 5, str(sheet_number), 0, 'L')
        max_y2 = self.get_y()

        # Find max Y position after second row
        info_y = max(max_y1, max_y2) + 2

        # Third row - Revizto links
        links = {}
        if observation.get('openLinks'):
            if isinstance(observation['openLinks'], dict):
                # For the web link, use it directly
                if observation['openLinks'].get('web'):
                    links["Web"] = observation['openLinks']['web']

                # For the desktop/application link, prepend the Revizto API redirect URL
                if observation['openLinks'].get('desktop'):
                    desktop_link = observation['openLinks']['desktop']
                    # Use the Revizto API redirect service to handle the custom protocol
                    redirect_url = f"https://api.canada.revizto.com/v5/region/redirect?url={desktop_link}"
                    links["Application"] = redirect_url

        if links:
            self.set_xy(info_col_x + col_padding, info_y)
            self.set_font('helvetica', 'B', 8)
            self.cell(label_width, 5, "Ouvrir dans :", 0, 0, 'L')

            # Position for links
            link_x = self.get_x()
            link_y = self.get_y()

            # Display and create clickable links
            self.set_font('helvetica', '', 8)
            self.set_text_color(0, 0, 255)  # Blue for links

            # Keep track of current x position
            current_x = link_x

            # Add each link as a separate clickable element
            for i, (label, url) in enumerate(links.items()):
                # Get width of this link text
                link_width = self.get_string_width(label) + 1

                # Add text with link - mark all links as clickable
                self.set_xy(current_x, link_y)
                # Use PDF link annotation to create the hyperlink
                self.cell(link_width, 5, label, 0, 0, 'L', 0, url)

                # Update x position
                current_x += link_width

                # Add separator comma if not the last link
                if i < len(links) - 1:
                    self.set_xy(current_x, link_y)
                    self.cell(2, 5, ", ", 0, 0, 'L')
                    current_x += 2

            # Reset to black text color and move to next line
            self.set_text_color(0, 0, 0)
            self.ln(5)

        # ===== HISTORY SECTION (FULL WIDTH) =====

        # History section start position
        history_y = top_section_y + top_section_height

        # Dynamic height based on comments
        history_height = max(30, comment_section_height)

        # Set light gray background for history section
        self.set_fill_color(250, 250, 250)  # Very light gray
        self.rect(self.l_margin, history_y, page_width, history_height, 'FD')

        # Horizontal divider between top section and history
        self.line(self.l_margin, history_y, self.l_margin + page_width, history_y)

        # History title
        self.set_xy(self.l_margin + 5, history_y + 3)
        self.set_font('helvetica', 'B', 9)
        self.cell(page_width - 10, 5, "Historique", 0, 1, 'L')

        # Show comments if available
        if comments and len(comments) > 0:
            # Ensure comments is a list of dicts, not strings
            valid_comments = []
            for comment in comments:
                if isinstance(comment, dict):
                    valid_comments.append(comment)
                elif isinstance(comment, str):
                    try:
                        # If it's a JSON string, try to parse it
                        import json
                        comment_dict = json.loads(comment)
                        if isinstance(comment_dict, dict):
                            valid_comments.append(comment_dict)
                    except:
                        # If parsing fails, skip this comment
                        logger.warning(f"Skipping invalid comment format: {comment[:50]}...")

            # Only proceed if we have valid comments
            if valid_comments:
                # Sort comments by date (newest first)
                sorted_comments = sorted(valid_comments, key=lambda x: x.get('created', ''), reverse=True)

                # Start position for comments
                comment_y = self.get_y() + 2
                self.set_xy(self.l_margin + 5, comment_y)

                # Display comments (limit to first 5 to save space)
                for i, comment in enumerate(sorted_comments[:5]):
                    if i > 0:
                        # Add a light separator line between comments
                        self.set_draw_color(200, 200, 200)  # Light gray
                        self.line(self.l_margin + 10, self.get_y() - 1, self.l_margin + page_width - 10,
                                  self.get_y() - 1)
                        self.set_draw_color(0, 0, 0)  # Reset to black

                    # Extract author info
                    author_name = 'Utilisateur inconnu'
                    if comment.get('author'):
                        if isinstance(comment['author'], str):
                            author_name = comment['author']
                        elif isinstance(comment['author'], dict):
                            if comment['author'].get('firstname') and comment['author'].get('lastname'):
                                author_name = f"{comment['author']['firstname']} {comment['author']['lastname']}"
                            elif comment['author'].get('email'):
                                author_name = comment['author']['email']

                    # Format date
                    comment_date = "Date inconnue"
                    if comment.get('created'):
                        try:
                            date_obj = datetime.fromisoformat(comment['created'].replace('Z', '+00:00'))
                            comment_date = date_obj.strftime('%d/%m/%Y %H:%M')
                        except:
                            comment_date = comment['created']

                    # Author and date header
                    self.set_font('helvetica', 'B', 8)
                    self.cell(50, 4, author_name, 0, 0, 'L')
                    self.set_font('helvetica', 'I', 7)
                    self.cell(page_width - 65, 4, comment_date, 0, 1, 'R')

                    # Comment content based on type
                    comment_type = comment.get('type', 'unknown')

                    if comment_type == 'text':
                        # Text comment
                        self.set_font('helvetica', '', 8)
                        self.set_xy(self.l_margin + 10, self.get_y())
                        self.multi_cell(page_width - 20, 4, comment.get('text', ''), 0, 'L')

                    elif comment_type == 'diff':
                        # Handle diff comment (status changes, etc.)
                        if comment.get('diff'):
                            self.set_font('helvetica', '', 8)
                            self.set_xy(self.l_margin + 10, self.get_y())

                            diff_text = ""
                            for key, change in comment['diff'].items():
                                # Format change description
                                if key == 'customStatus':
                                    old_status = format_status_value(change.get('old', '-'))
                                    new_status = format_status_value(change.get('new', '-'))
                                    diff_text += f"État: {old_status} → {new_status}\n"
                                elif key == 'assignee':
                                    diff_text += f"Assigné à: {change.get('old', '-')} → {change.get('new', '-')}\n"
                                elif key not in ['status', 'statusAuto']:  # Skip these fields
                                    # Format other field names
                                    field_name = re.sub(r'([A-Z])', r' \1', key).lower()
                                    field_name = field_name[0].upper() + field_name[1:] if field_name else key
                                    diff_text += f"{field_name}: {change.get('old', '-')} → {change.get('new', '-')}\n"

                            self.multi_cell(page_width - 20, 4, diff_text.strip(), 0, 'L')

                    elif comment_type == 'file' or comment_type == 'markup':
                        # Just show a simple indication for files and markups
                        self.set_font('helvetica', 'I', 8)
                        self.set_xy(self.l_margin + 10, self.get_y())

                        if comment_type == 'file':
                            file_text = f"Fichier joint: {comment.get('filename', 'Sans nom')}"
                            self.cell(page_width - 20, 4, file_text, 0, 1, 'L')
                        else:
                            self.cell(page_width - 20, 4, "Markup ajouté", 0, 1, 'L')

                    else:
                        # Default for unknown types
                        self.set_font('helvetica', 'I', 8)
                        self.set_xy(self.l_margin + 10, self.get_y())
                        self.cell(page_width - 20, 4, f"Activité: {comment_type}", 0, 1, 'L')

                    # Add space after each comment
                    self.ln(2)

                # If there are more comments than shown
                if len(sorted_comments) > 5:
                    self.set_font('helvetica', 'I', 7)
                    self.set_xy(self.l_margin + 5, self.get_y())
                    self.cell(page_width - 10, 4,
                              f"+ {len(sorted_comments) - 5} commentaires supplémentaires dans Revizto", 0, 1, 'R')

            else:
                # Default message if no valid comments
                self.set_xy(self.l_margin + 5, self.get_y() + 2)
                self.set_font('helvetica', 'I', 8)
                self.multi_cell(page_width - 10, 4, "Aucun historique disponible pour cet élément.", 0, 'L')

        else:
            # Default message if no comments
            self.set_xy(self.l_margin + 5, self.get_y() + 2)
            self.set_font('helvetica', 'I', 8)
            self.multi_cell(page_width - 10, 4, "Aucun historique disponible pour cet élément.", 0, 'L')

        # ===== CARD BOTTOM BORDER =====

        # Calculate total card height (dynamic based on content)
        total_card_height = header_height + top_section_height + history_height

        # Draw a border around the entire card
        self.rect(self.l_margin, card_start_y, page_width, total_card_height)

        # Move to the end of the card with extra spacing to prevent overlap
        self.set_y(card_start_y + total_card_height + 5)  # 5px gap between cards

    def add_instruction(self, instruction, comments=None):
        """
        Add an instruction to the report with a layout matching the HTML version

        Args:
            instruction (dict): The instruction data
            comments (list, optional): List of comments for this instruction
        """
        # We can reuse the same implementation as add_observation
        self.add_observation(instruction, comments)

    def add_deficiency(self, deficiency, comments=None):
        """
        Add a deficiency to the report with a layout matching the HTML version

        Args:
            deficiency (dict): The deficiency data
            comments (list, optional): List of comments for this deficiency
        """
        # We can reuse the same implementation as add_observation
        self.add_observation(deficiency, comments)

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

def generate_report_pdf(project_id, project_data, observations, instructions, deficiencies, issue_comments=None):
    """
    Generate a PDF report for the project

    Args:
        project_id (int): Project ID
        project_data (dict): Project information
        observations (list): List of observations
        instructions (list): List of instructions
        deficiencies (list): List of deficiencies
        issue_comments (dict, optional): Dictionary mapping issue IDs to comments

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

    # Initialize issue_comments dict if not provided
    if issue_comments is None:
        issue_comments = {}

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
                # Get comments for this observation if available
                obs_comments = issue_comments.get(str(observation.get('id')), [])
                pdf.add_observation(observation, obs_comments)
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
                # Get comments for this instruction if available
                ins_comments = issue_comments.get(str(instruction.get('id')), [])
                pdf.add_instruction(instruction, ins_comments)
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
                # Get comments for this deficiency if available
                def_comments = issue_comments.get(str(deficiency.get('id')), [])
                pdf.add_deficiency(deficiency, def_comments)
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


def format_status_value(value):
    """
    Format a status ID or value object to a display string.

    Args:
        value: Status ID (string) or value object

    Returns:
        str: Formatted display string
    """
    # If value is None or empty, return default
    if not value:
        return "Inconnu"

    # If value is an object with 'value' property (from API)
    if isinstance(value, dict) and 'value' in value:
        value = value['value']

    # Status ID to display name mapping
    status_map = {
        "2ed005c6-43cd-4907-a4d6-807dbd0197d5": "Ouvert",
        "cd52ac3e-f345-4f99-870f-5be95dc33245": "En cours",
        "b8504242-3489-43a2-9831-54f64053b226": "Résolu",
        "135b58c6-1e14-4716-a134-bbba2bbc90a7": "Fermé",
        "5947b7d1-70b9-425b-aba6-7187eb0251ff": "En attente",
        "912abbbf-3155-4e3c-b437-5778bdfd73f4": "Non-problème",
        "337e2fe6-e2a3-4e3f-b098-30aac68a191c": "Corrigé",
    }

    # Check if the value is a known UUID
    if isinstance(value, str) and value in status_map:
        return status_map[value]

    # Basic string translations
    if isinstance(value, str):
        lower_value = value.lower()
        if lower_value == "open" or lower_value == "opened":
            return "Ouvert"
        elif lower_value == "closed":
            return "Fermé"
        elif lower_value == "solved":
            return "Résolu"
        elif lower_value == "in progress" or lower_value == "in_progress":
            return "En cours"
        # Return the value as is if no translation
        return value

    # If we still don't know how to handle it, convert to string
    return str(value)