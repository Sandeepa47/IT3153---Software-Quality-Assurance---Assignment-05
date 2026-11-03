import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_document():
    doc = Document()

    # ---------------- PAGE SETUP (A4, 0.75" Margins) ----------------
    section = doc.sections[0]
    section.page_width = Inches(8.27)   # A4 width
    section.page_height = Inches(11.69) # A4 height
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    # ---------------- COLOR DEFINITIONS ----------------
    COLOR_PRIMARY = RGBColor(11, 61, 145)    # Navy Blue #0B3D91
    COLOR_ACCENT = RGBColor(10, 102, 194)    # LinkedIn / Tech Blue #0A66C2
    COLOR_TEXT = RGBColor(36, 41, 47)        # Dark Charcoal #24292F
    COLOR_MUTED = RGBColor(100, 116, 139)    # Slate #64748B
    COLOR_DARK = RGBColor(15, 23, 42)        # Slate Dark #0F172A
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_CODE = RGBColor(14, 116, 144)      # Cyan / Code Accent #0E7490

    HEX_PRIMARY = "0B3D91"
    HEX_ACCENT = "0A66C2"
    HEX_LIGHT_BG = "F8FAFC"
    HEX_ALT_ROW = "F1F5F9"
    HEX_BORDER = "CBD5E1"
    HEX_CALLOUT_BG = "EFF6FF"
    HEX_CALLOUT_BORDER = "0A66C2"
    HEX_SUCCESS_BG = "DCFCE7"
    HEX_SUCCESS_TXT = "166534"

    # Default Style font
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Segoe UI'
    font.size = Pt(10)
    font.color.rgb = COLOR_TEXT

    # ---------------- HEADER & FOOTER ----------------
    header = section.header
    p_head = header.paragraphs[0]
    p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_head = p_head.add_run("IT3153: Software Quality Assurance — Assignment 04 | Faculty of Computing, KDU")
    r_head.font.name = 'Segoe UI'
    r_head.font.size = Pt(8.5)
    r_head.font.color.rgb = COLOR_MUTED
    r_head.font.italic = True

    footer = section.footer
    p_foot = footer.paragraphs[0]
    p_foot.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_foot_left = p_foot.add_run("Automated UI Test Suite Report: LinkedIn Web Application\t\tPage ")
    r_foot_left.font.name = 'Segoe UI'
    r_foot_left.font.size = Pt(8.5)
    r_foot_left.font.color.rgb = COLOR_MUTED

    # Add dynamic PAGE field
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    r_foot_left._r.append(fldChar1)
    r_foot_left._r.append(instrText)
    r_foot_left._r.append(fldChar2)
    r_foot_left._r.append(fldChar3)

    r_foot_of = p_foot.add_run(" of ")
    r_foot_of.font.name = 'Segoe UI'
    r_foot_of.font.size = Pt(8.5)
    r_foot_of.font.color.rgb = COLOR_MUTED

    r_foot_num = p_foot.add_run()
    fldChar1_n = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText_n = parse_xml(r'<w:instrText %s xml:space="preserve"> NUMPAGES </w:instrText>' % nsdecls('w'))
    fldChar2_n = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3_n = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    r_foot_num._r.append(fldChar1_n)
    r_foot_num._r.append(instrText_n)
    r_foot_num._r.append(fldChar2_n)
    r_foot_num._r.append(fldChar3_n)
    r_foot_num.font.name = 'Segoe UI'
    r_foot_num.font.size = Pt(8.5)
    r_foot_num.font.color.rgb = COLOR_MUTED

    # ---------------- HELPER FUNCTIONS ----------------
    def set_cell_background(cell, hex_color):
        tcPr = cell._element.get_or_add_tcPr()
        for ch in tcPr.findall(qn('w:shd')):
            tcPr.remove(ch)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._element.get_or_add_tcPr()
        for ch in tcPr.findall(qn('w:tcMar')):
            tcPr.remove(ch)
        tcMar = parse_xml(f'''
            <w:tcMar {nsdecls("w")}>
                <w:top w:w="{top}" w:type="dxa"/>
                <w:bottom w:w="{bottom}" w:type="dxa"/>
                <w:left w:w="{left}" w:type="dxa"/>
                <w:right w:w="{right}" w:type="dxa"/>
            </w:tcMar>
        ''')
        tcPr.append(tcMar)

    def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
        tcPr = cell._element.get_or_add_tcPr()
        for ch in tcPr.findall(qn('w:tcBorders')):
            tcPr.remove(ch)
        borders_elm = OxmlElement('w:tcBorders')
        borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
        for b_name, b_val in borders.items():
            if b_val:
                elm = OxmlElement(f'w:{b_name}')
                for k, v in b_val.items():
                    elm.set(qn(f'w:{k}'), str(v))
                borders_elm.append(elm)
            else:
                elm = OxmlElement(f'w:{b_name}')
                elm.set(qn('w:val'), 'none')
                borders_elm.append(elm)
        tcPr.append(borders_elm)

    def make_row_cant_split(row):
        trPr = row._tr.get_or_add_trPr()
        cantSplit = OxmlElement('w:cantSplit')
        trPr.append(cantSplit)

    def make_row_header(row):
        trPr = row._tr.get_or_add_trPr()
        tblHeader = OxmlElement('w:tblHeader')
        trPr.append(tblHeader)

    def add_section_heading(title, number_str=None, space_before=16):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True

        if number_str:
            r_num = p.add_run(f"{number_str}  ")
            r_num.font.name = 'Segoe UI Semibold'
            r_num.font.size = Pt(13)
            r_num.font.bold = True
            r_num.font.color.rgb = COLOR_ACCENT

        r_txt = p.add_run(title)
        r_txt.font.name = 'Segoe UI Semibold'
        r_txt.font.size = Pt(13)
        r_txt.font.bold = True
        r_txt.font.color.rgb = COLOR_ACCENT

        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(f'''
            <w:pBdr {nsdecls("w")}>
                <w:bottom w:val="single" w:sz="6" w:space="3" w:color="{HEX_ACCENT}"/>
            </w:pBdr>
        ''')
        pPr.append(pBdr)

    def add_code_run(paragraph, text):
        r = paragraph.add_run(text)
        r.font.name = 'Consolas'
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_CODE
        return r

    # ==================== PAGE 1 ====================
    # Institution Header
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(0)
    p_uni.paragraph_format.space_after = Pt(2)
    r_uni = p_uni.add_run("GENERAL SIR JOHN KOTELAWALA DEFENCE UNIVERSITY")
    r_uni.font.name = 'Segoe UI'
    r_uni.font.size = Pt(15)
    r_uni.font.bold = True
    r_uni.font.color.rgb = COLOR_PRIMARY

    p_fac = doc.add_paragraph()
    p_fac.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fac.paragraph_format.space_before = Pt(0)
    p_fac.paragraph_format.space_after = Pt(4)
    r_fac = p_fac.add_run("Faculty of Computing  •  Department of Information Technology")
    r_fac.font.name = 'Segoe UI'
    r_fac.font.size = Pt(11)
    r_fac.font.bold = True
    r_fac.font.color.rgb = RGBColor(51, 65, 85)

    # Badge: Module / Assignment
    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_before = Pt(2)
    p_badge.paragraph_format.space_after = Pt(6)
    r_badge = p_badge.add_run("IT3153 - Software Quality Assurance  •  Assignment 04")
    r_badge.font.name = 'Segoe UI Semibold'
    r_badge.font.size = Pt(10)
    r_badge.font.color.rgb = COLOR_ACCENT

    # Main Report Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("Automated UI Test Suite Report: LinkedIn Web Application")
    r_title.font.name = 'Segoe UI'
    r_title.font.size = Pt(14)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_ACCENT

    # Decorative separator under title
    pPr = p_title._p.get_or_add_pPr()
    pBdr = parse_xml(f'''
        <w:pBdr {nsdecls("w")}>
            <w:bottom w:val="single" w:sz="12" w:space="8" w:color="{HEX_ACCENT}"/>
        </w:pBdr>
    ''')
    pPr.append(pBdr)

    # Metadata Table
    meta_table = doc.add_table(rows=3, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_items = [
        [("Student Name:", "[Enter Your Name Here]"), ("Index Number:", "[Enter Your Index No Here]")],
        [("Degree Programme:", "B.Sc. (Hons) in IT / IS"), ("Intake:", "[Enter Intake Here]")],
        [("Submission Date:", "07th November 2026"), ("GitHub Repository:", "[Insert GitHub URL Here]")]
    ]

    border_slate = {'val': 'single', 'sz': '4', 'space': '0', 'color': HEX_BORDER}
    
    for row_idx, row_data in enumerate(meta_items):
        row = meta_table.rows[row_idx]
        make_row_cant_split(row)
        for col_idx, (label, val) in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.width = Inches(3.38)
            set_cell_background(cell, HEX_ALT_ROW)
            set_cell_margins(cell, top=70, bottom=70, left=140, right=140)
            set_cell_borders(cell, top=border_slate, bottom=border_slate, left=border_slate, right=border_slate)

            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15

            r_lbl = p.add_run(f"{label} ")
            r_lbl.font.name = 'Segoe UI'
            r_lbl.font.size = Pt(9.5)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = COLOR_DARK

            r_val = p.add_run(val)
            r_val.font.name = 'Segoe UI'
            r_val.font.size = Pt(9.5)
            if "GitHub" in label:
                r_val.font.color.rgb = COLOR_ACCENT
                r_val.font.underline = True
            else:
                r_val.font.color.rgb = COLOR_TEXT

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(6)
    p_spacer.paragraph_format.space_after = Pt(0)

    # Section 1: Architecture
    add_section_heading("Test Suite Architecture & Design Strategy", "1", space_before=10)

    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.space_before = Pt(4)
    p_s1.paragraph_format.space_after = Pt(6)
    p_s1.paragraph_format.line_spacing = 1.2
    p_s1.add_run("The test automation framework was built following the industry-standard ")
    r_pom = p_s1.add_run("Page Object Model (POM)")
    r_pom.bold = True
    p_s1.add_run(" design pattern, ensuring clean separation of concerns, high maintainability, and reusability. The test framework is powered by ")
    p_s1.add_run("Java 17+").bold = True
    p_s1.add_run(", ")
    p_s1.add_run("Selenium WebDriver 4.25").bold = True
    p_s1.add_run(", and ")
    p_s1.add_run("TestNG 7.10").bold = True
    p_s1.add_run(".")

    # Highlight Callout Box for Architecture
    tbl_callout1 = doc.add_table(rows=1, cols=1)
    tbl_callout1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_callout1.autofit = False
    c_cell = tbl_callout1.cell(0, 0)
    c_cell.width = Inches(6.77)
    set_cell_background(c_cell, HEX_CALLOUT_BG)
    set_cell_margins(c_cell, top=100, bottom=100, left=160, right=140)
    set_cell_borders(c_cell, 
                     left={'val': 'single', 'sz': '24', 'space': '0', 'color': HEX_CALLOUT_BORDER},
                     top={'val': 'single', 'sz': '4', 'space': '0', 'color': 'D0E2FF'},
                     bottom={'val': 'single', 'sz': '4', 'space': '0', 'color': 'D0E2FF'},
                     right={'val': 'single', 'sz': '4', 'space': '0', 'color': 'D0E2FF'})

    cp = c_cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(4)
    r_cph = cp.add_run("Key Architectural Highlights:")
    r_cph.font.name = 'Segoe UI'
    r_cph.font.size = Pt(10)
    r_cph.font.bold = True
    r_cph.font.color.rgb = COLOR_PRIMARY

    bullets1 = [
        ("Page Object Model (POM):", [
            (" Each web page (Login, Feed, Search Results) is encapsulated in a dedicated page class (", False),
            ("LoginPage", True),
            (", ", False),
            ("FeedPage", True),
            (", ", False),
            ("SearchResultsPage", True),
            ("). Locators and low-level DOM manipulations remain private to each page class.", False)
        ]),
        ("Lifecycle Management:", [
            (" BaseTest utilizes TestNG lifecycle annotations (", False),
            ("@BeforeMethod", True),
            (" and ", False),
            ("@AfterMethod", True),
            (") to instantiate an isolated, clean browser session before every test and quit it gracefully upon completion.", False)
        ]),
        ("Pure Explicit Synchronization:", [
            (" No hardcoded ", False),
            ("Thread.sleep()", True),
            (" or ambiguous implicit waits were used. All synchronization is managed through ", False),
            ("WebDriverWait", True),
            (" combined with ", False),
            ("ExpectedConditions", True),
            (" (e.g., ", False),
            ("visibilityOfElementLocated", True),
            (", ", False),
            ("elementToBeClickable", True),
            (", ", False),
            ("urlContains", True),
            (").", False)
        ]),
        ("Credential & Configuration Security:", [
            (" Credentials are externalized via ", False),
            ("config.properties", True),
            (" and environment variables (", False),
            ("LINKEDIN_USERNAME", True),
            (", ", False),
            ("LINKEDIN_PASSWORD", True),
            ("). The configuration file is explicitly ignored in ", False),
            (".gitignore", True),
            (" to prevent credential leaks.", False)
        ])
    ]

    for title, desc_parts in bullets1:
        bp = c_cell.add_paragraph()
        bp.paragraph_format.left_indent = Inches(0.2)
        bp.paragraph_format.space_before = Pt(2)
        bp.paragraph_format.space_after = Pt(3)
        bp.paragraph_format.line_spacing = 1.15
        
        r_bullet = bp.add_run("•  ")
        r_bullet.bold = True
        r_bullet.font.color.rgb = COLOR_ACCENT

        r_bt = bp.add_run(title)
        r_bt.font.name = 'Segoe UI'
        r_bt.font.size = Pt(9.5)
        r_bt.font.bold = True
        r_bt.font.color.rgb = COLOR_DARK

        for text, is_code in desc_parts:
            if is_code:
                add_code_run(bp, text)
            else:
                r_bd = bp.add_run(text)
                r_bd.font.name = 'Segoe UI'
                r_bd.font.size = Pt(9.5)
                r_bd.font.color.rgb = COLOR_TEXT

    # ==================== PAGE BREAK TO PAGE 2 ====================
    doc.add_page_break()

    # Section 2: Test Cases Table
    add_section_heading("Test Case Specifications & Execution Summary", "2", space_before=0)

    tbl_tc = doc.add_table(rows=5, cols=5)
    tbl_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_tc.autofit = False

    tc_col_widths = [Inches(0.65), Inches(1.5), Inches(2.22), Inches(1.6), Inches(0.8)]
    tc_headers = ["ID", "Test Case Description", "Test Steps", "Expected Result", "Status"]

    # Header Row
    hdr_row = tbl_tc.rows[0]
    make_row_header(hdr_row)
    make_row_cant_split(hdr_row)
    for col_idx, (text, w) in enumerate(zip(tc_headers, tc_col_widths)):
        cell = hdr_row.cells[col_idx]
        cell.width = w
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=90, bottom=90, left=90, right=90)
        set_cell_borders(cell, top=border_slate, bottom=border_slate, left=border_slate, right=border_slate)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 4] else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_WHITE

    tc_data = [
        ("TC-01", "Positive Login Verification", 
         [("1. Navigate to ", False), ("/login", True), (".\n2. Enter valid test username & password.\n3. Click Sign in.\n4. Check URL and feed navigation bar.", False)],
         [("Redirects to ", False), ("/feed", True), ("; navigation bar and global search box are visible.", False)], 
         "PASSED"),
        ("TC-02", "Negative Login (Invalid Password)",
         [("1. Navigate to ", False), ("/login", True), (".\n2. Enter valid email and incorrect password (", False), ("Wrong#Password_123!", True), (").\n3. Click Sign in.", False)],
         [("Error alert/label is displayed; browser remains on login or checkpoint page.", False)], 
         "PASSED"),
        ("TC-03", "Global Search Execution",
         [("1. Authenticate to Feed.\n2. Focus global search input.\n3. Type keyword (", False), ("\"software testing\"", True), (").\n4. Press Enter.", False)],
         [("URL updates to ", False), ("/search/results/", True), (" and at least one search result item/card is visible.", False)], 
         "PASSED"),
        ("TC-04", "Click First Search Result",
         [("1. Perform search for specific query (", False), ("\"Sundar Pichai\"", True), (").\n2. Wait for results.\n3. Click first entity link.\n4. Verify loaded page.", False)],
         [("Opened URL contains target path (", False), ("/in/...", True), (" or ", False), ("/company/...", True), ("); page title contains LinkedIn.", False)], 
         "PASSED")
    ]

    for row_idx, (tc_id, tc_desc, steps_parts, exp_parts, status) in enumerate(tc_data, start=1):
        row = tbl_tc.rows[row_idx]
        make_row_cant_split(row)
        bg = "FFFFFF" if row_idx % 2 != 0 else HEX_LIGHT_BG

        # ID
        cell_id = row.cells[0]
        cell_id.width = tc_col_widths[0]
        set_cell_background(cell_id, bg)
        set_cell_margins(cell_id, top=80, bottom=80, left=60, right=60)
        set_cell_borders(cell_id, top=border_slate, bottom=border_slate, left=border_slate, right=border_slate)
        p = cell_id.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(tc_id)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_DARK

        # Description
        cell_desc = row.cells[1]
        cell_desc.width = tc_col_widths[1]
        set_cell_background(cell_desc, bg)
        set_cell_margins(cell_desc, top=80, bottom=80, left=90, right=90)
        set_cell_borders(cell_desc, top=border_slate, bottom=border_slate, left=border_slate, right=border_slate)
        p = cell_desc.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(tc_desc)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = COLOR_TEXT

        # Steps
        cell_steps = row.cells[2]
        cell_steps.width = tc_col_widths[2]
        set_cell_background(cell_steps, bg)
        set_cell_margins(cell_steps, top=80, bottom=80, left=90, right=90)
        set_cell_borders(cell_steps, top=border_slate, bottom=border_slate, left=border_slate, right=border_slate)
        p = cell_steps.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        for t, is_c in steps_parts:
            if is_c:
                add_code_run(p, t)
            else:
                r = p.add_run(t)
                r.font.name = 'Segoe UI'
                r.font.size = Pt(8.5)
                r.font.color.rgb = COLOR_TEXT

        # Expected
        cell_exp = row.cells[3]
        cell_exp.width = tc_col_widths[3]
        set_cell_background(cell_exp, bg)
        set_cell_margins(cell_exp, top=80, bottom=80, left=90, right=90)
        set_cell_borders(cell_exp, top=border_slate, bottom=border_slate, left=border_slate, right=border_slate)
        p = cell_exp.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        for t, is_c in exp_parts:
            if is_c:
                add_code_run(p, t)
            else:
                r = p.add_run(t)
                r.font.name = 'Segoe UI'
                r.font.size = Pt(8.5)
                r.font.color.rgb = COLOR_TEXT

        # Status
        cell_st = row.cells[4]
        cell_st.width = tc_col_widths[4]
        set_cell_background(cell_st, HEX_SUCCESS_BG)
        set_cell_margins(cell_st, top=80, bottom=80, left=40, right=40)
        set_cell_borders(cell_st, top=border_slate, bottom=border_slate, left=border_slate, right=border_slate)
        p = cell_st.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(status)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(22, 101, 52)

    # Section 3: Locator Strategy
    add_section_heading("Locator Strategy & Rationale", "3", space_before=16)

    p_s3 = doc.add_paragraph()
    p_s3.paragraph_format.space_before = Pt(4)
    p_s3.paragraph_format.space_after = Pt(6)
    p_s3.paragraph_format.line_spacing = 1.2
    p_s3.add_run("LinkedIn employs frequent frontend redeployments with dynamic, obfuscated CSS classes. To maintain high locator stability and avoid test flakiness, locators were chosen based on uniqueness and resilience:")

    tbl_loc = doc.add_table(rows=6, cols=3)
    tbl_loc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_loc.autofit = False

    loc_widths = [Inches(1.6), Inches(2.57), Inches(2.6)]
    loc_headers = ["Target Element", "Chosen Locator", "Engineering Rationale"]

    hdr_loc = tbl_loc.rows[0]
    make_row_header(hdr_loc)
    make_row_cant_split(hdr_loc)
    for col_idx, (text, w) in enumerate(zip(loc_headers, loc_widths)):
        cell = hdr_loc.cells[col_idx]
        cell.width = w
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=90, bottom=90, left=90, right=90)
        set_cell_borders(cell, top=border_slate, bottom=border_slate, left=border_slate, right=border_slate)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_WHITE

    loc_data = [
        ("Login Username & Password",
         "By.id(\"username\")\nBy.id(\"password\")",
         "Standard HTML IDs are unique, fast to locate, and have remained consistently stable across LinkedIn's authentication redesigns."),
        ("Sign In Button",
         "By.cssSelector(\"button[type='submit']\")",
         "Identifies the form submission trigger by semantic attribute rather than button text, ensuring stability across language/localization changes."),
        ("Login Error Banner",
         "By.cssSelector(\"#error-for-password,\ndiv[role='alert'],\n.form__label--error,\n[data-test-form-alert]\")",
         "Multi-selector fallback strategy handles both inline field validation errors and top-level authentication warning alerts."),
        ("Global Search Input",
         "By.cssSelector(\"input.search-global-typeahead__input,\ninput[placeholder*='Search']\")",
         "Uses the semantic typeahead class with an attribute wildcard fallback ([placeholder*='Search']) to guard against frontend refactoring."),
        ("Search Result Links",
         "By.cssSelector(\"main a[href*='/in/'],\nmain a[href*='/company/'],\ndiv[data-view-name*='search-entity'] a\")",
         "Matches domain routing patterns (/in/ for profiles, /company/ for corporate pages) within <main>, ignoring dynamic hash classes.")
    ]

    for row_idx, (el, loc, rat) in enumerate(loc_data, start=1):
        row = tbl_loc.rows[row_idx]
        make_row_cant_split(row)
        bg = "FFFFFF" if row_idx % 2 != 0 else HEX_LIGHT_BG
        for col_idx, (val, w) in enumerate(zip([el, loc, rat], loc_widths)):
            cell = row.cells[col_idx]
            cell.width = w
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=75, bottom=75, left=90, right=90)
            set_cell_borders(cell, top=border_slate, bottom=border_slate, left=border_slate, right=border_slate)

            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15

            if col_idx == 0:
                r = p.add_run(val)
                r.font.name = 'Segoe UI'
                r.font.size = Pt(9)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK
            elif col_idx == 1:
                r = p.add_run(val)
                r.font.name = 'Consolas'
                r.font.size = Pt(8.5)
                r.font.color.rgb = COLOR_PRIMARY
            else:
                r = p.add_run(val)
                r.font.name = 'Segoe UI'
                r.font.size = Pt(8.5)
                r.font.color.rgb = COLOR_TEXT

    # ==================== PAGE BREAK TO PAGE 3 ====================
    doc.add_page_break()

    # Section 4: Challenges & Solutions
    add_section_heading("Challenges Faced & Solutions Implemented", "4", space_before=0)

    challenges = [
        ("Bot Detection & CAPTCHA Checkpoints:",
         " LinkedIn enforces stringent automated bot detection.",
         " In accordance with assignment ethics, the suite never attempts to circumvent security mechanisms. Instead, a dynamic checkpoint detection mechanism monitors the URL for /checkpoint or /uas/ and triggers a polite human-in-the-loop wait (up to 180 seconds), allowing manual verification in the open browser before resuming automation."),
        ("Element Click Interception & Sticky Navigation:",
         " LinkedIn's fixed global navigation bar and floating chat drawers frequently overlap search result elements, causing Selenium's native click to throw ElementClickInterceptedException.",
         " Implemented smooth JavaScript scrolling into view (scrollIntoView({block: 'center'})) combined with an automated JavaScript click fallback."),
        ("Single Page Application (SPA) Asynchronous Rendering:",
         " Content and search cards are rendered client-side via React/Ember after the initial HTML document loads.",
         " Employed explicit ExpectedConditions.visibilityOfElementLocated and elementToBeClickable rather than implicit sleeps."),
        ("New Window / Tab Handling:",
         " Depending on user settings, clicking a profile result may spawn a new tab.",
         " Automated window handle inspection and switched WebDriver focus to the active tab automatically.")
    ]

    for title, problem, solution in challenges:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.2

        r_bullet = p.add_run("•  ")
        r_bullet.bold = True
        r_bullet.font.color.rgb = COLOR_ACCENT

        r_title = p.add_run(title)
        r_title.font.name = 'Segoe UI'
        r_title.font.size = Pt(9.5)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_DARK

        r_prob = p.add_run(problem)
        r_prob.font.name = 'Segoe UI'
        r_prob.font.size = Pt(9.5)
        r_prob.font.color.rgb = COLOR_TEXT

        r_sol_lbl = p.add_run(" Solution:")
        r_sol_lbl.font.name = 'Segoe UI'
        r_sol_lbl.font.size = Pt(9.5)
        r_sol_lbl.font.bold = True
        r_sol_lbl.font.italic = True
        r_sol_lbl.font.color.rgb = COLOR_PRIMARY

        r_sol = p.add_run(solution)
        r_sol.font.name = 'Segoe UI'
        r_sol.font.size = Pt(9.5)
        r_sol.font.color.rgb = COLOR_TEXT

    # Section 5: Reflection
    add_section_heading("Reflection: Limits of UI Automation Against 3rd-Party Applications", "5", space_before=16)

    tbl_callout5 = doc.add_table(rows=1, cols=1)
    tbl_callout5.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_callout5.autofit = False
    c5_cell = tbl_callout5.cell(0, 0)
    c5_cell.width = Inches(6.77)
    set_cell_background(c5_cell, HEX_CALLOUT_BG)
    set_cell_margins(c5_cell, top=110, bottom=110, left=160, right=140)
    set_cell_borders(c5_cell, 
                     left={'val': 'single', 'sz': '24', 'space': '0', 'color': HEX_CALLOUT_BORDER},
                     top={'val': 'single', 'sz': '4', 'space': '0', 'color': 'D0E2FF'},
                     bottom={'val': 'single', 'sz': '4', 'space': '0', 'color': 'D0E2FF'},
                     right={'val': 'single', 'sz': '4', 'space': '0', 'color': 'D0E2FF'})

    cp5 = c5_cell.paragraphs[0]
    cp5.paragraph_format.space_before = Pt(0)
    cp5.paragraph_format.space_after = Pt(6)
    r_cp5h = cp5.add_run("Automating UI interactions against enterprise third-party platforms presents inherent engineering challenges:")
    r_cp5h.font.name = 'Segoe UI'
    r_cp5h.font.size = Pt(9.5)
    r_cp5h.font.bold = True
    r_cp5h.font.color.rgb = COLOR_PRIMARY

    reflection_points = [
        ("High Maintenance Overhead:", " Unannounced UI deployments, A/B testing variations, and obfuscated CSS classes render locators brittle, demanding continuous maintenance."),
        ("Anti-Bot & Rate Limiting Constraints:", " Commercial platforms deploy heuristic security filters (Cloudflare, Arkose Labs, behavioral biometrics). Automated test execution in CI/CD pipelines without mock servers quickly results in account temporary restrictions or IP blacklisting."),
        ("Non-Deterministic Data States:", " Dynamic search results fluctuate based on network location, time, and live user activity, necessitating flexible assertion logic rather than static equality checks."),
        ("Testing Pyramid Hierarchy:", " UI automation should be reserved for critical user journeys (smoke / end-to-end regression). For robust and scalable Quality Assurance, backend API testing and contract testing provide greater speed, stability, and deterministic outcomes.")
    ]

    for idx, (title, desc) in enumerate(reflection_points, start=1):
        bp = c5_cell.add_paragraph()
        bp.paragraph_format.left_indent = Inches(0.2)
        bp.paragraph_format.space_before = Pt(2)
        bp.paragraph_format.space_after = Pt(3)
        bp.paragraph_format.line_spacing = 1.15

        r_num = bp.add_run(f"{idx}.  ")
        r_num.font.bold = True
        r_num.font.color.rgb = COLOR_ACCENT

        r_title = bp.add_run(title)
        r_title.font.name = 'Segoe UI'
        r_title.font.size = Pt(9.5)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_DARK

        r_desc = bp.add_run(desc)
        r_desc.font.name = 'Segoe UI'
        r_desc.font.size = Pt(9.5)
        r_desc.font.color.rgb = COLOR_TEXT

    # ==================== PAGE BREAK TO PAGE 4 ====================
    doc.add_page_break()

    # Section 6: Screenshots
    add_section_heading("Automated Test Execution Screenshots (All Tasks)", "6", space_before=0)

    p_s6 = doc.add_paragraph()
    p_s6.paragraph_format.space_before = Pt(4)
    p_s6.paragraph_format.space_after = Pt(8)
    p_s6.paragraph_format.line_spacing = 1.15
    p_s6.add_run("Screenshots are captured automatically by ")
    add_code_run(p_s6, "ScreenshotUtil")
    p_s6.add_run(" for every test flow and on test failure, saved into the ")
    add_code_run(p_s6, "target/screenshots/")
    p_s6.add_run(" directory.")

    figures = [
        ("screenshots/task1_execution_summary.png", "Figure 1 (Task 1):", " TestNG & Maven Suite Execution Summary (100% Pass Rate)"),
        ("screenshots/task2_positive_feed.png", "Figure 2 (Task 2 - Positive):", " Successful Authentication & LinkedIn Feed Page (/feed)"),
        ("screenshots/task2_negative_error.png", "Figure 3 (Task 2 - Negative):", " Invalid Password Error Message Assertion"),
        ("screenshots/task3_search_results.png", "Figure 4 (Task 3):", " Global Search Results Page for keyword \"software testing\""),
        ("screenshots/task4_click_result.png", "Figure 5 (Task 4):", " Opened Target Profile Page (/in/sundarpichai/)"),
        ("screenshots/failure_capture_code.png", "Figure 6 (Task 6 Requirement):", " Automatic Screenshot Captured on Failure by Code (FAIL_...)")
    ]

    tbl_imgs = doc.add_table(rows=3, cols=2)
    tbl_imgs.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_imgs.autofit = False

    fig_idx = 0
    border_card = {'val': 'single', 'sz': '4', 'space': '0', 'color': HEX_BORDER}

    for row_i in range(3):
        row = tbl_imgs.rows[row_i]
        make_row_cant_split(row)
        for col_j in range(2):
            cell = row.cells[col_j]
            cell.width = Inches(3.38)
            set_cell_background(cell, HEX_LIGHT_BG)
            set_cell_margins(cell, top=70, bottom=70, left=70, right=70)
            set_cell_borders(cell, top=border_card, bottom=border_card, left=border_card, right=border_card)

            img_path, fig_lbl, fig_cap = figures[fig_idx]
            fig_idx += 1

            p_img = cell.paragraphs[0]
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(2)
            p_img.paragraph_format.space_after = Pt(3)
            p_img.paragraph_format.keep_with_next = True

            if os.path.exists(img_path):
                r_img = p_img.add_run()
                r_img.add_picture(img_path, width=Inches(3.2))

            p_cap = cell.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(1)
            p_cap.paragraph_format.space_after = Pt(2)
            p_cap.paragraph_format.line_spacing = 1.1

            r_fl = p_cap.add_run(fig_lbl)
            r_fl.font.name = 'Segoe UI'
            r_fl.font.size = Pt(8.5)
            r_fl.font.bold = True
            r_fl.font.color.rgb = COLOR_DARK

            r_fc = p_cap.add_run(fig_cap)
            r_fc.font.name = 'Segoe UI'
            r_fc.font.size = Pt(8.5)
            r_fc.font.color.rgb = COLOR_MUTED

    output_path = "IT3153_SQA_Assignment_04_Test_Report.docx"
    doc.save(output_path)
    print(f"Successfully generated {output_path}!")

if __name__ == "__main__":
    create_document()
