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
        self.status_map = {}


    def header(self):
        """
        Custom header for each page
        """
        try:
            # Check if using a custom logo from static folder
            from django.conf import settings
            import os

            # Try to find logo in static files
            logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'STGM_Logotype_RVB_Architecture_Noir.png')

            # If not in STATIC_ROOT, try STATICFILES_DIRS
            if not os.path.exists(logo_path) and hasattr(settings, 'STATICFILES_DIRS'):
                for static_dir in settings.STATICFILES_DIRS:
                    test_path = os.path.join(static_dir, 'images', 'STGM_Logotype_RVB_Architecture_Noir.png')
                    if os.path.exists(test_path):
                        logo_path = test_path
                        break

            if os.path.exists(logo_path):
                self.image(logo_path, 6, 8, 50)
            else:
                # Default behavior if no logo found
                logger.warning(f"Logo file not found at {logo_path}")
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

        self.set_y(padding_top + 1)
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

    def add_observation(self, observation, comments=None, status_map=None):
        """
        Add an observation to the report with the layout:
        - Top: Two columns (image + information)
        - Bottom: Full-width history section with comments
        - Ensures no card is ever split between pages and properly expands for content

        Args:
            observation (dict): The observation data
            comments (list, optional): List of comments/history for this observation
            status_map (dict, optional): Map of status UUIDs to status display data
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

        # Get status info - updated to use the status_map
        status_text = "Inconnu"
        bg_color = (110, 110, 110)  # Default gray
        text_color = (255, 255, 255)  # Default white

        # Extract status ID using the same method as in the JS
        status_id = None
        if observation.get('customStatus'):
            if isinstance(observation['customStatus'], str):
                status_id = observation['customStatus']
            elif isinstance(observation['customStatus'], dict) and observation['customStatus'].get('value'):
                status_id = observation['customStatus']['value']
        elif observation.get('status'):
            if isinstance(observation['status'], str):
                status_id = observation['status']
            elif isinstance(observation['status'], dict) and observation['status'].get('value'):
                status_id = observation['status']['value']

        # Log the detected status ID for debugging
        print(f"[PDF-DEBUG] Detected status ID for issue {observation.get('id')}: {status_id}")

        # Special handling for the "En attente" status which often has issues
        if status_id == "5947b7d1-70b9-425b-aba6-7187eb0251ff" or status_id == "c70f7d38-1d60-4df3-b85b-14e59174d7ba":
            print(f"[PDF-DEBUG] Using special handling for En attente status")
            status_text = "En attente"
            bg_color = (255, 211, 46)  # Yellow
        # Look up status in the provided status map
        elif status_map and status_id in status_map:
            status_info = status_map[status_id]
            status_text = status_info.get('displayName', status_info.get('name', 'Inconnu'))
            print(f"[PDF-DEBUG] Found status in map: {status_text}")

            # Parse background color
            bg_str = status_info.get('backgroundColor', '#6F7E93')
            if bg_str.startswith('#') and len(bg_str) == 7:
                try:
                    bg_color = (
                        int(bg_str[1:3], 16),
                        int(bg_str[3:5], 16),
                        int(bg_str[5:7], 16)
                    )
                    print(f"[PDF-DEBUG] Parsed bg color: {bg_color}")
                except ValueError:
                    print(f"[PDF-DEBUG] Could not parse bg color: {bg_str}")

            # Parse text color
            text_str = status_info.get('textColor', '#FFFFFF')
            if text_str.startswith('#') and len(text_str) == 7:
                try:
                    text_color = (
                        int(text_str[1:3], 16),
                        int(text_str[3:5], 16),
                        int(text_str[5:7], 16)
                    )
                    print(f"[PDF-DEBUG] Parsed text color: {text_color}")
                except ValueError:
                    print(f"[PDF-DEBUG] Could not parse text color: {text_str}")
        # Fallback status handling for common statuses - using the same logic as JS
        elif status_id == "2ed005c6-43cd-4907-a4d6-807dbd0197d5":  # Open
            status_text = "Ouvert"
            bg_color = (204, 41, 41)  # Red
            print(f"[PDF-DEBUG] Using fallback for Open status")
        elif status_id == "cd52ac3e-f345-4f99-870f-5be95dc33245":  # In progress
            status_text = "En cours"
            bg_color = (255, 170, 0)  # Orange
            print(f"[PDF-DEBUG] Using fallback for In progress status")
        elif status_id == "b8504242-3489-43a2-9831-54f64053b226":  # Solved
            status_text = "Resolu"
            bg_color = (66, 190, 101)  # Green
            print(f"[PDF-DEBUG] Using fallback for Solved status")
        elif status_id == "135b58c6-1e14-4716-a134-bbba2bbc90a7":  # Closed
            status_text = "Ferme"
            bg_color = (184, 184, 184)  # Gray
            print(f"[PDF-DEBUG] Using fallback for Closed status")
        elif status_id == "912abbbf-3155-4e3c-b437-5778bdfd73f4":  # non-problème
            status_text = "Non-probleme"
            bg_color = (43, 43, 43)  # Dark gray
            print(f"[PDF-DEBUG] Using fallback for Non-probleme status")
        elif status_id == "337e2fe6-e2a3-4e3f-b098-30aac68a191c":  # Corrigé
            status_text = "Corrige"
            bg_color = (137, 46, 251)  # Purple
            print(f"[PDF-DEBUG] Using fallback for Corrige status")
        else:
            print(f"[PDF-DEBUG] No status match found, using default")

        # Get preview image URL if exists
        imageUrl = ''
        if observation.get('preview'):
            if isinstance(observation['preview'], str):
                imageUrl = observation['preview']
            elif observation['preview'].get('original'):
                imageUrl = observation['preview']['original']

        # Calculate page dimensions
        page_width = self.w - 2 * self.l_margin

        # Initialize heights
        header_height = 10
        top_section_height = 60

        # First, calculate how much space we have left on the current page
        space_left = self.h - self.b_margin - self.get_y()

        # If less than minimum required space, start a new page
        min_required_space = header_height + top_section_height + 30  # minimum 30mm for history
        if space_left < min_required_space:
            self.add_page()
            # Set a proper top margin after page break
            self.set_y(self.t_margin + 30)

        # Remember the start position of the card
        card_start_y = self.get_y()

        # ===== HEADER SECTION =====

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
        self.set_text_color(text_color[0], text_color[1], text_color[2])
        self.set_font('helvetica', 'B', 9)
        self.rect(badge_x, card_start_y + 2, badge_width, 6, 'F')
        self.cell(badge_width, 6, status_text, 0, 0, 'C')

        # Reset text color
        self.set_text_color(0, 0, 0)

        # ===== TOP SECTION - TWO COLUMNS =====

        # Top section starts below header
        top_section_y = card_start_y + header_height

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
        image_url = get_best_image_for_issue(observation, comments)

        # Add image if available
        if image_url:
            try:
                temp_file = None
                try:
                    # Handle base64 data URLs
                    if image_url.startswith('data:image'):
                        # Extract the base64 data
                        img_data = re.sub('^data:image/.+;base64,', '', image_url)
                        # Create temporary file with unique name
                        import uuid
                        temp_file = os.path.join(tempfile.gettempdir(), f"revizto_img_{uuid.uuid4()}.png")
                        with open(temp_file, 'wb') as f:
                            f.write(base64.b64decode(img_data))
                    # Handle HTTP URLs by downloading the image
                    elif image_url.startswith(('http://', 'https://')):
                        import urllib.request
                        import uuid
                        temp_file = os.path.join(tempfile.gettempdir(), f"revizto_img_{uuid.uuid4()}.png")
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
                        img.close()  # Important: Close the PIL Image after getting dimensions
                    except Exception as img_err:
                        logger.error(f"Error getting image dimensions: {img_err}")
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

                finally:
                    # Clean up temp file in a finally block to ensure it happens even if there was an error
                    if temp_file and temp_file != image_url and os.path.exists(temp_file):
                        try:
                            # Close any open file handles before deleting
                            import gc
                            gc.collect()  # Force garbage collection to release any file handles

                            # Try to remove the temp file
                            os.remove(temp_file)
                            logger.info(f"Successfully removed temp file: {temp_file}")
                        except Exception as cleanup_err:
                            logger.warning(f"Could not remove temp file {temp_file}: {cleanup_err}")
                            # If we can't remove it, try to use the Windows del command as a fallback
                            if os.name == 'nt':  # Windows
                                try:
                                    import subprocess
                                    subprocess.run(f'del /f /q "{temp_file}"', shell=True)
                                    logger.info(f"Used del command to remove temp file: {temp_file}")
                                except Exception as del_err:
                                    logger.warning(f"Windows del command also failed: {del_err}")
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

        # History section starts below top section
        history_y = top_section_y + top_section_height

        # IMPORTANT: First draw the history section background without a fixed height
        # We'll redraw it later with the correct height
        # Just draw the horizontal divider line for now
        self.line(self.l_margin, history_y, self.l_margin + page_width, history_y)

        # History title
        self.set_xy(self.l_margin + 5, history_y + 3)
        self.set_font('helvetica', 'B', 9)
        self.cell(page_width - 10, 5, "Historique", 0, 1, 'L')

        # Save position BEFORE rendering comments - this is crucial for measurement
        history_start_position = self.get_y()

        # Remember the start position for comments
        history_content_start_y = self.get_y() + 2

        # Show comments if available
        if comments and len(comments) > 0:
            # Debug comments information
            print(f"[DEBUG PDF] Processing {len(comments)} comments for issue {observation.get('id')}")
            print(f"[DEBUG PDF] First comment type: {type(comments[0]) if comments else 'None'}")

            # Process the comments list - filter out diff comments
            valid_comments = []

            # First, ensure we have valid comments data
            for comment in comments:
                # Handle both string and dict formats
                if isinstance(comment, dict):
                    # Skip diff comments
                    if comment.get('type') != 'diff':
                        valid_comments.append(comment)
                elif isinstance(comment, str):
                    try:
                        # If it's a JSON string, try to parse it
                        import json
                        comment_dict = json.loads(comment)
                        if isinstance(comment_dict, dict) and comment_dict.get('type') != 'diff':
                            valid_comments.append(comment_dict)
                    except:
                        # If parsing fails, skip this comment
                        continue

            # Only proceed if we have valid comments
            if valid_comments:
                print(f"[DEBUG PDF] Valid non-diff comments: {len(valid_comments)}")

                # Sort comments by date (newest first)
                sorted_comments = sorted(valid_comments,
                                         key=lambda x: x.get('created', ''),
                                         reverse=True)

                print(f"[DEBUG PDF] Sorted non-diff comments: {len(sorted_comments)}")

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
                            author_name = sanitize_text_for_pdf(comment['author'])
                        elif isinstance(comment['author'], dict):
                            if comment['author'].get('firstname') and comment['author'].get('lastname'):
                                author_name = sanitize_text_for_pdf(
                                    f"{comment['author']['firstname']} {comment['author']['lastname']}"
                                )
                            elif comment['author'].get('email'):
                                author_name = sanitize_text_for_pdf(comment['author']['email'])

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
                        # Sanitize the text before adding to PDF
                        safe_text = sanitize_text_for_pdf(comment.get('text', ''))
                        self.multi_cell(page_width - 20, 4, safe_text, 0, 'L')

                    elif comment_type == 'file':
                        # Handle file comment (status changes, etc.)
                        self.set_font('helvetica', 'I', 8)
                        self.set_xy(self.l_margin + 10, self.get_y())

                        filename = sanitize_text_for_pdf(comment.get('filename', 'Sans nom'))
                        file_text = f"Fichier joint: {filename}"
                        self.cell(page_width - 20, 4, file_text, 0, 1, 'L')

                        # Si le fichier est une image, afficher l'image
                        if comment.get('mimetype', '').startswith('image/') and comment.get('preview'):
                            preview = comment.get('preview')
                            image_url = preview.get('original') or preview.get('middle')

                            if image_url:
                                try:
                                    import uuid
                                    temp_file = os.path.join(tempfile.gettempdir(), f"comment_img_{uuid.uuid4()}.png")

                                    if image_url.startswith('data:image'):
                                        img_data = re.sub('^data:image/.+;base64,', '', image_url)
                                        with open(temp_file, 'wb') as f:
                                            f.write(base64.b64decode(img_data))
                                    else:
                                        import urllib.request
                                        urllib.request.urlretrieve(image_url, temp_file)

                                    # Définir les dimensions max de l'image
                                    max_width = 40  # marges
                                    max_height = 40

                                    from PIL import Image
                                    img = Image.open(temp_file)
                                    img_width, img_height = img.size
                                    aspect_ratio = img_width / img_height
                                    img.close()

                                    if aspect_ratio > 1:
                                        image_width = min(max_width, img_width)
                                        image_height = image_width / aspect_ratio
                                    else:
                                        image_height = min(max_height, img_height)
                                        image_width = image_height * aspect_ratio

                                    x = self.l_margin + 10
                                    y = self.get_y()

                                    self.image(temp_file, x=x, y=y, w=image_width)
                                    self.ln(image_height + 2)

                                    os.remove(temp_file)
                                except Exception as e:
                                    logger.warning(f"Erreur lors de l'affichage de l'image dans les commentaires: {e}")

                    elif comment_type == 'markup':
                        # Just show a simple indication for markups
                        self.set_font('helvetica', 'I', 8)
                        self.set_xy(self.l_margin + 10, self.get_y())
                        self.cell(page_width - 20, 4, "Markup ajoute", 0, 1, 'L')  # Avoid "é" for PDF compatibility

                    else:
                        # Default for unknown types
                        self.set_font('helvetica', 'I', 8)
                        self.set_xy(self.l_margin + 10, self.get_y())
                        self.cell(page_width - 20, 4, f"Activite: {comment_type}", 0, 1,
                                  'L')  # Avoid "é" for PDF compatibility

                    # Add space after each comment
                    self.ln(2)

                # If there are more comments than shown
                if len(sorted_comments) > 5:
                    self.set_font('helvetica', 'I', 7)
                    self.set_xy(self.l_margin + 5, self.get_y())
                    self.cell(page_width - 10, 4,
                              f"+ {len(sorted_comments) - 5} commentaires supplementaires dans Revizto", 0, 1,
                              'R')  # Avoid "é" for PDF compatibility

            else:
                # Default message if no valid comments
                self.set_xy(self.l_margin + 5, self.get_y() + 2)
                self.set_font('helvetica', 'I', 8)
                self.multi_cell(page_width - 10, 4, "Aucun historique disponible pour cet element.", 0,
                                'L')  # Avoid "é" for PDF compatibility

        else:
            # Default message if no comments
            self.set_xy(self.l_margin + 5, self.get_y() + 2)
            self.set_font('helvetica', 'I', 8)
            self.multi_cell(page_width - 10, 4, "Aucun historique disponible pour cet element.", 0,
                            'L')  # Avoid "é" for PDF compatibility

        # CRITICAL FIX: Measure actual content height AFTER rendering all content
        history_section_height = max(20, self.get_y() - history_y + 5)  # Add small padding

        # Draw full history section background + border (including title and comments)
        self.set_fill_color(255, 255, 255)
        self.rect(self.l_margin, history_y, page_width, history_section_height, 'D')

        # ----- STEP 4: DRAW FINAL BORDER AFTER ALL CONTENT -----

        # Calculate total card height based on actual content
        total_card_height = header_height + top_section_height + history_section_height + 5

        # Draw outer border LAST - this ensures it encompasses all content
        self.rect(self.l_margin, card_start_y, page_width, total_card_height)

        # Move position to after the card with spacing
        self.set_y(card_start_y + total_card_height + 5)  # 10mm gap between cards

    def get_status_display(self, status_id):
        """
        Get display information for a status ID.

        Args:
            status_id: Status ID (string, dict, or object)

        Returns:
            tuple: (status_text, background_color, text_color)
        """
        # Default values
        status_text = "Inconnu"
        bg_color = (110, 110, 110)  # Default gray
        text_color = (255, 255, 255)  # Default white

        # Extract status value from different formats
        status_value = None

        if isinstance(status_id, dict):
            # Extract from customStatus
            if status_id.get('customStatus'):
                if isinstance(status_id['customStatus'], str):
                    status_value = status_id['customStatus']
                elif isinstance(status_id['customStatus'], dict) and status_id['customStatus'].get('value'):
                    status_value = status_id['customStatus']['value']
            # Extract from status
            elif status_id.get('status'):
                if isinstance(status_id['status'], str):
                    status_value = status_id['status']
                elif isinstance(status_id['status'], dict) and status_id['status'].get('value'):
                    status_value = status_id['status']['value']
            # Extract from value
            elif status_id.get('value'):
                status_value = status_id['value']
        elif isinstance(status_id, str):
            status_value = status_id

        # Look up in status map if we have a value
        if status_value and self.status_map and status_value in self.status_map:
            status_info = self.status_map[status_value]
            status_text = status_info.get('displayName', status_info.get('name', "Inconnu"))

            # Convert hex colors to RGB tuples
            bg_hex = status_info.get('backgroundColor', '#6F7E93')
            text_hex = status_info.get('textColor', '#FFFFFF')

            bg_color = self._hex_to_rgb(bg_hex)
            text_color = self._hex_to_rgb(text_hex)

        return status_text, bg_color, text_color

    def _hex_to_rgb(self, hex_color):
        """Convert hex color string to RGB tuple."""
        if not hex_color or not isinstance(hex_color, str):
            return (110, 110, 110)  # Default gray

        # Remove # if present
        hex_color = hex_color.lstrip('#')

        # Parse hex to RGB
        try:
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return (r, g, b)
            else:
                return (110, 110, 110)  # Default gray
        except ValueError:
            return (110, 110, 110)  # Default gray

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

        # Projet - Use multi_cell for this field to allow wrapping
        self.cell(label_width, row_height, "Projet:", 0, 0, 'L', 1)

        # Save current position and use multi_cell for the value to allow wrapping
        x_pos = self.get_x()
        y_pos = self.get_y()
        self.multi_cell(field_width, row_height, project_data.get('projectName', ''), 0, 'L')

        # If multi_cell created multiple lines, y position will have changed
        new_y_pos = self.get_y()

        # Maitre de l'ouvrage
        self.set_xy(self.l_margin, new_y_pos)  # Reset to left margin at current Y
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

        # En présence de - Use multi_cell for this field to allow wrapping
        self.cell(label_width, row_height, "En présence de:", 0, 0, 'L', 1)

        # Save current position and use multi_cell for the value to allow wrapping
        x_pos = self.get_x()
        y_pos = self.get_y()
        self.multi_cell(field_width, row_height, project_data.get('inPresenceOf', ''), 0, 'L')

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


def generate_report_pdf(project_id, project_data, observations, instructions, deficiencies, issue_comments=None, status_map=None):
    """
    Generate a PDF report for the project

    Args:
        project_id (int): Project ID
        project_data (dict): Project information
        observations (list): List of observations
        instructions (list): List of instructions
        deficiencies (list): List of deficiencies
        issue_comments (dict, optional): Dictionary mapping issue IDs to comments
        status_map (dict, optional): Custom status mapping for enhanced status display

    Returns:
        BytesIO: PDF file as a BytesIO object
    """
    # Create PDF
    pdf = ReviztoPDF()

    # If custom status mapping is provided, add it to the PDF instance
    if status_map:
        pdf.status_map = status_map

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


def format_status_value(self, observation):
    """
    Format a status ID or value object to a display string.
    Uses a combination of the dynamic status map and fallback hardcoded values.

    Args:
        observation: The complete observation object

    Returns:
        tuple: (display_string, bg_color, text_color)
    """
    # Default values
    default_status = ("Inconnu", (110, 110, 110), (255, 255, 255))

    # Add debug output for the observation
    print(f"[DEBUG PDF] Processing observation status: {observation.get('id')}")

    # Extract status from observation
    status_id = None

    # Check for customStatus first (priority over regular status)
    if observation.get('customStatus'):
        print(f"[DEBUG PDF] Found customStatus in observation {observation.get('id')}")
        if isinstance(observation['customStatus'], str):
            status_id = observation['customStatus']
            print(f"[DEBUG PDF] customStatus is string: {status_id}")
        elif isinstance(observation['customStatus'], dict) and observation['customStatus'].get('value'):
            status_id = observation['customStatus']['value']
            print(f"[DEBUG PDF] customStatus is object with value: {status_id}")
    # Then check for regular status
    elif observation.get('status'):
        print(f"[DEBUG PDF] Found regular status in observation {observation.get('id')}")
        if isinstance(observation['status'], str):
            status_id = observation['status']
            print(f"[DEBUG PDF] status is string: {status_id}")
        elif isinstance(observation['status'], dict) and observation['status'].get('value'):
            status_id = observation['status']['value']
            print(f"[DEBUG PDF] status is object with value: {status_id}")

    print(f"[DEBUG PDF] Extracted status_id: {status_id}")

    # If we found a status ID, try to look it up
    if status_id:
        # First, check if we have a status map from the API
        if hasattr(self, 'status_map') and self.status_map:
            print(f"[DEBUG PDF] Found status_map with {len(self.status_map)} entries")

            # First, try the dynamic status map from the API
            if status_id in self.status_map:
                status_info = self.status_map[status_id]
                print(f"[DEBUG PDF] Found status in dynamic map: {status_id} -> {status_info.get('name')}")

                # Get the name from the dynamically loaded status
                status_name = status_info.get('displayName', status_info.get('name', "Inconnu"))

                # Convert hex colors to RGB tuples
                bg_hex = status_info.get('backgroundColor', '#6F7E93')
                text_hex = status_info.get('textColor', '#FFFFFF')

                bg_color = self._hex_to_rgb(bg_hex)
                text_color = self._hex_to_rgb(text_hex)

                return (status_name, bg_color, text_color)
            else:
                print(f"[DEBUG PDF] Status not found in dynamic map: {status_id}")
                print(f"[DEBUG PDF] Available keys in status_map: {list(self.status_map.keys())}")
        else:
            print(f"[DEBUG PDF] No status_map available or it's empty")

        # If not found in dynamic map, use our hardcoded mappings
        # Direct mapping of known status UUIDs
        hardcoded_map = {
            "2ed005c6-43cd-4907-a4d6-807dbd0197d5": ("Ouvert", (204, 41, 41), (255, 255, 255)),  # Open - Red
            "cd52ac3e-f345-4f99-870f-5be95dc33245": ("En cours", (255, 170, 0), (255, 255, 255)),
            # In progress - Orange
            "b8504242-3489-43a2-9831-54f64053b226": ("Résolu", (66, 190, 101), (255, 255, 255)),  # Solved - Green
            "135b58c6-1e14-4716-a134-bbba2bbc90a7": ("Fermé", (184, 184, 184), (255, 255, 255)),  # Closed - Gray
            "5947b7d1-70b9-425b-aba6-7187eb0251ff": ("En attente", (255, 211, 46), (255, 255, 255)),  # Waiting - Yellow
            "c70f7d38-1d60-4df3-b85b-14e59174d7ba": ("En attente", (255, 211, 46), (255, 255, 255)),
            # Alt Waiting - Yellow
            "912abbbf-3155-4e3c-b437-5778bdfd73f4": ("Non-problème", (43, 43, 43), (255, 255, 255)),
            # Non-issue - Dark Gray
            "337e2fe6-e2a3-4e3f-b098-30aac68a191c": ("Corrigé", (137, 46, 251), (255, 255, 255)),  # Fixed - Purple
        }

        # Check hardcoded map
        if status_id in hardcoded_map:
            print(f"[DEBUG PDF] Found status in hardcoded map: {status_id} -> {hardcoded_map[status_id][0]}")
            return hardcoded_map[status_id]
        else:
            print(f"[DEBUG PDF] Status not found in hardcoded map: {status_id}")
            print(f"[DEBUG PDF] Available keys in hardcoded_map: {list(hardcoded_map.keys())}")

        # If UUID not recognized, try name-based matching
        if isinstance(status_id, str):
            lower_value = status_id.lower()
            if lower_value == "open" or lower_value == "opened":
                return ("Ouvert", (204, 41, 41), (255, 255, 255))
            elif lower_value == "closed":
                return ("Fermé", (184, 184, 184), (255, 255, 255))
            elif lower_value == "solved":
                return ("Résolu", (66, 190, 101), (255, 255, 255))
            elif lower_value == "in progress" or lower_value == "in_progress":
                return ("En cours", (255, 170, 0), (255, 255, 255))
            elif lower_value == "en attente" or lower_value == "waiting":
                return ("En attente", (255, 211, 46), (255, 255, 255))
            elif lower_value == "corrigé" or lower_value == "fixed":
                return ("Corrigé", (137, 46, 251), (255, 255, 255))
            elif lower_value == "non-problème" or lower_value == "non-issue":
                return ("Non-problème", (43, 43, 43), (255, 255, 255))
    else:
        print(f"[DEBUG PDF] No status_id found for observation {observation.get('id')}")

    # If all lookups failed, return default
    print(f"[DEBUG PDF] All lookups failed, returning default status for observation {observation.get('id')}")
    return default_status

def format_diff_value(value):
    """
    Format a diff value for display in a comment

    Args:
        value: Value to format

    Returns:
        str: Formatted value for display
    """
    # Handle None, empty strings, etc.
    if value is None:
        return "-"

    # If value is a dictionary with 'value' key, extract it
    if isinstance(value, dict):
        if 'value' in value:
            return format_diff_value(value['value'])  # Recursive call with the inner value

        # If it has name or display fields, use those
        if 'name' in value:
            return sanitize_text_for_pdf(value['name'])
        if 'displayName' in value:
            return sanitize_text_for_pdf(value['displayName'])

        # If it has firstname/lastname fields (for users)
        if 'firstname' in value and 'lastname' in value:
            return sanitize_text_for_pdf(f"{value['firstname']} {value['lastname']}".strip())

        # If we still have a dict but don't know how to handle it, convert to string
        return sanitize_text_for_pdf(str(value))

    # Convert to string for display and sanitize
    return sanitize_text_for_pdf(str(value))


def filter_comments_for_display(comments):
    """
    Filter and sort comments for display in the PDF report
    Filters out all diff comments

    Args:
        comments (list): List of comments from the API

    Returns:
        list: Filtered and sorted list of comments
    """
    if not comments or not isinstance(comments, list):
        print("[DEBUG PDF] No comments to filter or invalid type")
        return []

    # Debug
    print(f"[DEBUG PDF] Filtering {len(comments)} comments")

    # Process the comments list
    valid_comments = []

    # First, ensure we have valid comments data
    for comment in comments:
        # Handle both string and dict formats
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
                continue

    # Filter out 'diff' type comments - this is the key change
    filtered_comments = [comment for comment in valid_comments if comment.get('type') != 'diff']

    # Sort comments by date (newest first)
    sorted_comments = sorted(filtered_comments,
                             key=lambda x: x.get('created', ''),
                             reverse=True)

    print(f"[DEBUG PDF] After filtering: {len(sorted_comments)} comments")
    return sorted_comments


def sanitize_text_for_pdf(text):
    """
    Sanitize text by replacing problematic Unicode characters with ASCII alternatives
    and filtering out any characters not supported by the Helvetica font.

    Args:
        text (str): Text to sanitize

    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        text = str(text)

    # Replace French accented characters and other special characters
    replacements = {
        # Smart quotes and apostrophes
        '\u2019': "'",  # Right single quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u201C': '"',  # Left double quotation mark
        '\u201D': '"',  # Right double quotation mark
        '\u201E': '"',  # Double low-9 quotation mark
        '\u201F': '"',  # Double high-reversed-9 quotation mark
        '\u2039': '<',  # Single left-pointing angle quotation mark
        '\u203A': '>',  # Single right-pointing angle quotation mark
        '\u00AB': '<<',  # Left-pointing double angle quotation mark
        '\u00BB': '>>',  # Right-pointing double angle quotation mark

        # Dashes and hyphens
        '\u2013': '-',  # En dash
        '\u2014': '--',  # Em dash
        '\u2015': '--',  # Horizontal bar
        '\u2212': '-',  # Minus sign

        # French characters
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'î': 'i', 'ï': 'i',
        'ô': 'o', 'ö': 'o',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'À': 'A', 'Â': 'A', 'Ä': 'A',
        'Î': 'I', 'Ï': 'I',
        'Ô': 'O', 'Ö': 'O',
        'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'Ç': 'C',

        # Other European characters
        'ñ': 'n', 'Ñ': 'N',
        'ß': 'ss',
        'æ': 'ae', 'Æ': 'AE',
        'œ': 'oe', 'Œ': 'OE',
        'ø': 'o', 'Ø': 'O',
        'å': 'a', 'Å': 'A',

        # Other problematic characters
        '→': '-->', '⟶': '-->', '➜': '-->',
        '⇒': '=>', '⇨': '=>',
        '–': '-', '—': '--',
        '…': '...', '•': '*', '·': '*',
        '×': 'x', '÷': '/',
        '≤': '<=', '≥': '>=', '≠': '!=', '≈': '~=',
        '√': 'sqrt', '∑': 'sum', '∏': 'prod', '∂': 'd',
        '¼': '1/4', '½': '1/2', '¾': '3/4',
        '−': '-', '±': '+/-',

        # Other special characters
        '®': '(R)', '©': '(C)', '™': '(TM)',
        '£': 'GBP', '€': 'EUR', '¥': 'JPY',
        '°': ' degrees ',
        '\u00A0': ' ',  # Non-breaking space
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    # Filter out any remaining characters not in the basic Latin-1 range (0-255)
    # This ensures compatibility with the standard PDF fonts
    result = ''
    for char in text:
        # Only keep characters within the Latin-1 range
        if ord(char) < 256:
            result += char
        else:
            # Replace any other Unicode character with a question mark or space
            result += '?'

    return result



def get_best_image_for_issue(issue, comments):
    """
    Gets the best available image for an issue based on priority:
    1. Last uploaded image from comments
    2. Last markup image
    3. Default image from issue data

    Args:
        issue (dict): The issue object
        comments (list): Comments for this issue

    Returns:
        str: URL of the best available image or empty string if none found
    """
    logger.info(f"Finding best image for issue {issue.get('id')}")

    # First check if we have comments
    if comments and isinstance(comments, list) and len(comments) > 0:
        logger.info(f"Checking {len(comments)} comments for images")

        # First priority: Find the most recent file comment with an image
        # Sort comments newest first
        sorted_comments = sorted(
            comments,
            key=lambda c: c.get('created', ''),
            reverse=True
        )

        # Look for a file comment with an image preview
        for comment in sorted_comments:
            if (comment.get('type') == 'file' and
                    comment.get('mimetype') and
                    isinstance(comment.get('mimetype'), str) and
                    comment.get('mimetype').startswith('image/') and
                    comment.get('preview')):

                preview = comment.get('preview')
                if isinstance(preview, dict):
                    if preview.get('original'):
                        logger.info(f"Found image in file comment: {preview.get('original')}")
                        return preview.get('original')
                    elif preview.get('middle'):
                        logger.info(f"Found image in file comment: {preview.get('middle')}")
                        return preview.get('middle')

        # Second priority: Find the most recent markup with a preview
        for comment in sorted_comments:
            if (comment.get('type') == 'markup' and
                    comment.get('preview')):

                preview = comment.get('preview')
                if isinstance(preview, dict):
                    if preview.get('original'):
                        logger.info(f"Found image in markup comment: {preview.get('original')}")
                        return preview.get('original')
                    elif preview.get('middle'):
                        logger.info(f"Found image in markup comment: {preview.get('middle')}")
                        return preview.get('middle')

    # Third priority: Use the default issue preview image
    if issue.get('preview'):
        if isinstance(issue['preview'], str):
            logger.info(f"Using issue's string preview: {issue['preview']}")
            return issue['preview']
        elif isinstance(issue['preview'], dict):
            if issue['preview'].get('original'):
                logger.info(f"Using issue's preview.original: {issue['preview'].get('original')}")
                return issue['preview'].get('original')
            elif issue['preview'].get('middle'):
                logger.info(f"Using issue's preview.middle: {issue['preview'].get('middle')}")
                return issue['preview'].get('middle')

    # No image found
    logger.info(f"No image found for issue {issue.get('id')}")
    return ''


def generate_report_pdf_with_status_fix(project_id, project_data, observations, instructions, deficiencies,
                                        issue_comments=None):
    """
    Generate a PDF report with additional status mapping to handle problematic status UUIDs.
    Particularly focuses on the 'En attente' status which has caused issues.

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
    print(f"[DEBUG-START] =====================================================")
    print(f"[DEBUG] Starting generate_report_pdf_with_status_fix")
    print(f"[DEBUG] Received project_id: {project_id} (type: {type(project_id)})")
    print(f"[DEBUG] Project data keys: {list(project_data.keys()) if project_data else 'None'}")
    print(f"[DEBUG] Observations count: {len(observations) if observations else 'None'}")
    print(f"[DEBUG] Instructions count: {len(instructions) if instructions else 'None'}")
    print(f"[DEBUG] Deficiencies count: {len(deficiencies) if deficiencies else 'None'}")
    print(f"[DEBUG] Issue comments keys count: {len(issue_comments) if issue_comments else 'None'}")

    try:
        # Import services - with debug information
        print(f"[DEBUG] Importing ReviztoService")
        from .api.service import ReviztoService
        print(f"[DEBUG] ReviztoService imported successfully")

        # DEBUG: Check if the method exists and what parameters it takes
        try:
            import inspect
            method = getattr(ReviztoService, 'get_project_workflow_settings', None)
            if method:
                print(f"[DEBUG] Method 'get_project_workflow_settings' exists")
                sig = inspect.signature(method)
                print(f"[DEBUG] Method signature: {sig}")
                print(f"[DEBUG] Method parameters: {list(sig.parameters.keys())}")
            else:
                print(f"[DEBUG] Method 'get_project_workflow_settings' does NOT exist in ReviztoService")
                # List available methods
                methods = [name for name in dir(ReviztoService) if
                           callable(getattr(ReviztoService, name)) and not name.startswith('__')]
                print(f"[DEBUG] Available methods in ReviztoService: {methods}")
        except Exception as e:
            print(f"[DEBUG] Error inspecting method: {e}")

        print(f"[DEBUG] About to call ReviztoService.get_project_workflow_settings with project_id={project_id}")
        status_response = None  # Default to None

        # Try to call the method safely
        try:
            # If project_id is None, try to extract it from other sources
            if project_id is None:
                print(f"[DEBUG] project_id is None, attempting to extract from other sources")
                # Try to get from project_data
                if project_data and 'id' in project_data:
                    project_id = project_data['id']
                    print(f"[DEBUG] Extracted project_id from project_data: {project_id}")
                # Check observations for project_id
                elif observations and len(observations) > 0 and 'projectId' in observations[0]:
                    project_id = observations[0]['projectId']
                    print(f"[DEBUG] Extracted project_id from first observation: {project_id}")
                # If still None, see if we can get it from activeProjectId in the database
                if project_id is None:
                    print(f"[DEBUG] Could not extract project_id from available data")
                    print(f"[DEBUG] Skipping workflow settings fetch")
                    status_response = None
                else:
                    print(f"[DEBUG] Calling with extracted project_id: {project_id}")
                    status_response = ReviztoService.get_project_workflow_settings(project_id)
            else:
                print(f"[DEBUG] Calling with provided project_id: {project_id}")
                status_response = ReviztoService.get_project_workflow_settings(project_id)

            print(f"[DEBUG] Call to get_project_workflow_settings returned successfully")
            print(f"[DEBUG] Response type: {type(status_response)}")
            if isinstance(status_response, dict):
                print(f"[DEBUG] Response keys: {list(status_response.keys())}")
                print(f"[DEBUG] Result value: {status_response.get('result')}")
        except Exception as call_error:
            print(f"[DEBUG] Error calling get_project_workflow_settings: {call_error}")
            import traceback
            print(f"[DEBUG] Call error traceback: {traceback.format_exc()}")
            status_response = None

        # Enhanced status mapping
        print(f"[DEBUG] Creating status map")
        status_map = {}

        # Default statuses (fallbacks)
        status_map.update({
            "2ed005c6-43cd-4907-a4d6-807dbd0197d5": {  # Open
                "name": "Ouvert",
                "color": (204, 41, 41)  # Red
            },
            "cd52ac3e-f345-4f99-870f-5be95dc33245": {  # In progress
                "name": "En cours",
                "color": (255, 170, 0)  # Orange
            },
            "b8504242-3489-43a2-9831-54f64053b226": {  # Solved
                "name": "Resolu",
                "color": (66, 190, 101)  # Green
            },
            "135b58c6-1e14-4716-a134-bbba2bbc90a7": {  # Closed
                "name": "Ferme",
                "color": (184, 184, 184)  # Gray
            },
            # Special case - 'En attente' UUID that has been problematic
            "5947b7d1-70b9-425b-aba6-7187eb0251ff": {  # En attente
                "name": "En attente",
                "color": (255, 211, 46)  # Yellow
            },
            # Alternate UUID that has been seen for 'En attente'
            "c70f7d38-1d60-4df3-b85b-14e59174d7ba": {
                "name": "En attente",
                "color": (255, 211, 46)  # Yellow
            }
        })
        print(f"[DEBUG] Default status map created with {len(status_map)} entries")

        # Add statuses from API response if available
        if status_response and status_response.get('result') == 0 and status_response.get('data'):
            statuses = status_response['data'].get('statuses', [])
            print(f"[DEBUG] Found {len(statuses)} statuses in API response")
            for status in statuses:
                if 'uuid' in status and 'name' in status:
                    # Convert hex color to RGB tuple
                    bg_color = status.get('backgroundColor', '#808080')
                    if bg_color.startswith('#'):
                        try:
                            r = int(bg_color[1:3], 16)
                            g = int(bg_color[3:5], 16)
                            b = int(bg_color[5:7], 16)
                            color = (r, g, b)
                        except:
                            color = (128, 128, 128)  # Default gray
                    else:
                        color = (128, 128, 128)  # Default gray

                    # Add to status map
                    status_map[status['uuid']] = {
                        "name": status['name'],
                        "color": color
                    }
            print(f"[DEBUG] Status map updated with API data, now has {len(status_map)} entries")
        else:
            print(f"[DEBUG] No valid status data from API, using default status map only")

        # Generate PDF with enhanced status mapping
        print(f"[DEBUG] Calling generate_report_pdf with enhanced status map")
        from io import BytesIO

        # First check if generate_report_pdf can accept the status_map parameter
        import inspect
        from .pdf_generator import generate_report_pdf
        try:
            pdf_sig = inspect.signature(generate_report_pdf)
            pdf_params = list(pdf_sig.parameters.keys())
            print(f"[DEBUG] generate_report_pdf parameters: {pdf_params}")

            if 'status_map' in pdf_params:
                print(f"[DEBUG] generate_report_pdf accepts status_map parameter")
                result = generate_report_pdf(
                    project_id,
                    project_data,
                    observations,
                    instructions,
                    deficiencies,
                    issue_comments,
                    status_map
                )
            else:
                print(f"[DEBUG] generate_report_pdf does NOT accept status_map parameter, calling without it")
                result = generate_report_pdf(
                    project_id,
                    project_data,
                    observations,
                    instructions,
                    deficiencies,
                    issue_comments
                )
        except Exception as pdf_sig_error:
            print(f"[DEBUG] Error checking generate_report_pdf signature: {pdf_sig_error}")
            print(f"[DEBUG] Calling generate_report_pdf without status_map to be safe")
            result = generate_report_pdf(
                project_id,
                project_data,
                observations,
                instructions,
                deficiencies,
                issue_comments
            )

        print(f"[DEBUG] PDF generation successful")
        print(f"[DEBUG-END] =====================================================")
        return result
    except Exception as e:
        import traceback
        print(f"[DEBUG] Error generating PDF: {e}")
        print(f"[DEBUG] Error traceback: {traceback.format_exc()}")
        print(f"[DEBUG] Falling back to standard PDF generation")

        # Fall back to standard PDF generation without enhanced status handling
        try:
            from .pdf_generator import generate_report_pdf
            result = generate_report_pdf(
                project_id,
                project_data,
                observations,
                instructions,
                deficiencies,
                issue_comments
            )
            print(f"[DEBUG] Fallback PDF generation successful")
            return result
        except Exception as fallback_error:
            print(f"[DEBUG] Fallback PDF generation failed: {fallback_error}")
            print(f"[DEBUG] Returning empty PDF")
            # Return empty PDF as last resort
            from io import BytesIO
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("helvetica", size=12)
            pdf.cell(200, 10, txt="Error generating PDF report", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Error: {str(e)}", ln=True, align="C")
            buffer = BytesIO()
            pdf.output(buffer)
            buffer.seek(0)
            print(f"[DEBUG-END] =====================================================")
            return buffer

def sanitize_dict_for_pdf(data_dict):
    """
    Recursively sanitize all string values in a dictionary for PDF compatibility.

    Args:
        data_dict (dict): Dictionary to sanitize

    Returns:
        dict: Sanitized dictionary
    """
    if not isinstance(data_dict, dict):
        # If it's a string, sanitize it
        if isinstance(data_dict, str):
            return sanitize_text_for_pdf(data_dict)
        # If it's a list, recursively sanitize each item
        elif isinstance(data_dict, list):
            return [sanitize_dict_for_pdf(item) for item in data_dict]
        # Otherwise return as is
        return data_dict

    result = {}
    for key, value in data_dict.items():
        # Recursively sanitize nested dictionaries
        if isinstance(value, dict):
            result[key] = sanitize_dict_for_pdf(value)
        # Sanitize lists by processing each item
        elif isinstance(value, list):
            result[key] = [sanitize_dict_for_pdf(item) for item in value]
        # Sanitize string values
        elif isinstance(value, str):
            result[key] = sanitize_text_for_pdf(value)
        # Keep other values as they are
        else:
            result[key] = value

    return result


def create_error_pdf(project_id, project_data, error_message):
    """
    Create a simple PDF reporting that an error occurred during generation.

    Args:
        project_id (int): Project ID
        project_data (dict): Project information (used for title)
        error_message (str): Error message to include

    Returns:
        BytesIO: PDF file as a BytesIO object
    """
    from fpdf import FPDF

    # Create a simpler PDF
    pdf = FPDF()
    pdf.add_page()

    # Set basic metadata
    project_name = sanitize_text_for_pdf(project_data.get('projectName', f"Projet {project_id}"))
    pdf.set_title(f"Rapport d'erreur - {project_name}")

    # Add error information
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, "Rapport de visite - Erreur de generation", 0, 1, 'C')

    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, f"Projet: {project_name}", 0, 1, 'L')

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, "Une erreur est survenue lors de la generation du PDF:", 0, 1, 'L')

    pdf.set_font('helvetica', '', 10)
    # Make sure the error message is sanitized
    safe_error = sanitize_text_for_pdf(str(error_message))
    pdf.multi_cell(0, 10, safe_error, 0, 'L')

    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 10)
    pdf.cell(0, 10, "Veuillez contacter le support technique pour assistance.", 0, 1, 'L')

    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    return buffer