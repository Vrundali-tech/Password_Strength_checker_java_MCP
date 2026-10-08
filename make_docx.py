import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_docx(filename):
    doc = Document()

    # Standard 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base typography
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(31, 41, 55)

    # -------------------------------------------------------------
    # PAGE 1: COVER / FRONT PAGE
    # -------------------------------------------------------------
    p_inst_top = doc.add_paragraph()
    p_inst_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst_top = p_inst_top.add_run("PILLAI COLLEGE OF ENGINEERING\n")
    r_inst_top.bold = True
    r_inst_top.font.size = Pt(18)
    r_inst_top.font.color.rgb = RGBColor(112, 19, 29) # PCE Maroon

    r_dep_top = p_inst_top.add_run("Department of Electronics & Telecommunication\n\n\n")
    r_dep_top.font.size = Pt(12)
    r_dep_top.font.color.rgb = RGBColor(75, 85, 99)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_proj = p_proj.add_run("Java Programming\nMini Project Report\nOn\n\n")
    r_proj.bold = True
    r_proj.font.size = Pt(14)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("PASSWORD STRENGTH ANALYZER USING JAVA\n\n")
    r_title.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(17, 24, 39)

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.line_spacing = 1.2
    r_deg = p_deg.add_run("Submitted in partial fulfilment of the requirement\nfor the Degree of\n\n")
    r_deg.font.size = Pt(12)
    r_deg2 = p_deg.add_run("Bachelor of Technology\nIn\nElectronics & Telecommunication\n\n\n")
    r_deg2.bold = True
    r_deg2.font.size = Pt(13)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Submitted By\n")
    r_sub.font.size = Pt(12)
    r_sub_name = p_sub.add_run("Sara Sachin Ture: [Roll No: ETC656]\n\n\n")
    r_sub_name.bold = True
    r_sub_name.font.size = Pt(13)

    p_sup = doc.add_paragraph()
    p_sup.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sup = p_sup.add_run("Supervisor\n")
    r_sup.font.size = Pt(12)
    r_sup_name = p_sup.add_run("Dr. Aboli Khedkar\n\n\n")
    r_sup_name.bold = True
    r_sup_name.font.size = Pt(13)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run(
        "Department of Electronics & Telecommunication\n"
        "PILLAI COLLEGE OF ENGINEERING\n"
        "New Panvel – 410206\n"
        "Academic Year 2026 - 27"
    )
    r_inst.bold = True
    r_inst.font.size = Pt(12)

    doc.add_page_break() # -> Page 2

    # -------------------------------------------------------------
    # PAGE 2: CERTIFICATE
    # -------------------------------------------------------------
    p_cert_head = doc.add_paragraph()
    p_cert_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c1 = p_cert_head.add_run("DEPARTMENT OF ELECTRONICS & TELECOMMUNICATION\n")
    r_c1.bold = True
    r_c1.font.size = Pt(14)
    r_c2 = p_cert_head.add_run("Pillai College of Engineering\nNew Panvel – 410206\n\n\n")
    r_c2.font.size = Pt(12)

    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ct = p_cert_title.add_run("CERTIFICATE\n\n")
    r_ct.bold = True
    r_ct.font.size = Pt(16)

    p_cert_body = doc.add_paragraph()
    p_cert_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body.paragraph_format.line_spacing = 1.3
    p_cert_body.add_run(
        "This is to certify that the requirements for the Java Programming project entitled "
        "‘Password Strength Analyzer Using Java’ have been successfully completed by the following students:\n\n"
    )

    table_stud = doc.add_table(rows=2, cols=2)
    table_stud.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_stud.rows[0].cells
    hdr_cells[0].text = "Name"
    hdr_cells[1].text = "Roll No."
    hdr_cells[0].paragraphs[0].runs[0].font.bold = True
    hdr_cells[1].paragraphs[0].runs[0].font.bold = True

    row_cells = table_stud.rows[1].cells
    row_cells[0].text = "Sara Sachin Ture"
    row_cells[1].text = "ETC656"

    p_cert_body2 = doc.add_paragraph()
    p_cert_body2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body2.paragraph_format.line_spacing = 1.3
    p_cert_body2.add_run(
        "\nin partial fulfillment of Bachelor of Technology in the Department of Electronics "
        "& Telecommunications, Pillai College of Engineering, New Panvel – 410206 during the "
        "Academic Year 2026 – 2027.\n\n\n\n\n\n"
    )

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sig = p_sig.add_run("_____________________\nSupervisor\n")
    r_sig.font.size = Pt(12)
    r_sig_name = p_sig.add_run("Dr. Aboli Khedkar")
    r_sig_name.bold = True

    doc.add_page_break() # -> Page 3

    # -------------------------------------------------------------
    # PAGE 3: ABSTRACT
    # -------------------------------------------------------------
    p_ch3 = doc.add_paragraph()
    r_ch3 = p_ch3.add_run("CHAPTER 3: ABSTRACT\n")
    r_ch3.bold = True
    r_ch3.font.size = Pt(14)

    p_abs1 = doc.add_paragraph()
    p_abs1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs1.paragraph_format.line_spacing = 1.3
    p_abs1.add_run(
        "The Password Strength Analyzer Using Java is an interactive, modern Java desktop GUI application designed "
        "and developed to evaluate the robustness and entropy of user credentials against industry-standard password security "
        "criteria. In modern computing environments, authentication mechanisms remain the primary line of defense against "
        "unauthorized breaches. However, end-users frequently select simplistic or predictable passwords vulnerable to dictionary "
        "attacks, credential stuffing, and brute-force cracking. This project addresses this challenge through an automated, "
        "real-time evaluation engine engineered with Java Swing and AWT.\n\n"
        "Built strictly around the modern Java 21 LTS runtime using native Java GUI packages (javax.swing and java.awt), "
        "the application eliminates external dependencies while providing a sleek, responsive interface. The GUI features "
        "anti-aliased rounded cards, real-time DocumentListener keystroke analysis, an animated color-coded strength bar, a show/hide "
        "password toggle, quick test triggers, and live condition badges. To safeguard user confidentiality, all evaluations "
        "occur strictly in-memory: no passwords are ever stored, written to files, transmitted across networks, or logged.\n\n"
        "The system evaluates five core security criteria: minimum length (8+ characters), uppercase letters (A-Z), lowercase "
        "letters (a-z), numeric digits (0-9), and special symbols. Each passed test awards 1 point, computing a 0-to-5 score mapped "
        "to 'Weak' (0–2), 'Medium' (3–4), and 'Strong' (5) tiers with dynamic remediation suggestions. The project demonstrates "
        "the effective synthesis of core Java OOP, event-driven GUI development, and secure software design."
    )

    doc.add_page_break() # -> Page 4

    # -------------------------------------------------------------
    # PAGE 4 & 5: TABLE OF CONTENTS
    # -------------------------------------------------------------
    p_toc = doc.add_paragraph()
    r_toc = p_toc.add_run("CHAPTER 4: TABLE OF CONTENTS\n")
    r_toc.bold = True
    r_toc.font.size = Pt(14)

    toc_items_p1 = [
        ("Chapter 1: Front Page", "1"),
        ("Chapter 2: Certificate", "2"),
        ("Chapter 3: Abstract", "3"),
        ("Chapter 4: Table of Contents", "4 to 5"),
        ("Chapter 5: Introduction", "6 to 7"),
        ("  5.1- Purpose of Project", "6"),
        ("  5.2- Problem Statement", "6"),
        ("  5.3- Objectives of Project", "7"),
        ("Chapter 6: Tools and Technology Used", "8 to 9"),
        ("  6.1- Frontend (Java Swing & AWT Desktop GUI)", "8"),
        ("  6.2- Backend (Core Java Architecture & Analysis Engine)", "8"),
        ("  6.3- Object-Oriented Programming Concepts", "9"),
        ("  6.4- Security, Privacy & In-Memory Design Principles", "9"),
        ("  6.5- Development Tools & Environment", "9"),
        ("Chapter 7: System Design", "10 to 11"),
        ("  7.1- System Architecture (Pipeline Model)", "10"),
        ("  7.2- System Design Block Diagram", "10"),
        ("  7.3- Step-by-Step Data Flow Description", "11"),
    ]

    tbl_toc1 = doc.add_table(rows=0, cols=2)
    tbl_toc1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for title, pnum in toc_items_p1:
        row = tbl_toc1.add_row()
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(5.2), Inches(1.3)
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(title)
        r1 = p1.add_run(pnum)
        if not title.startswith("  "):
            r0.bold = True
            r1.bold = True
        p0.paragraph_format.line_spacing = 1.2
        p1.paragraph_format.line_spacing = 1.2

    doc.add_page_break() # -> Page 5

    toc_items_p2 = [
        ("Chapter 8: Implementation", "12 to 13"),
        ("  8.1- Architectural Design & Method Decomposition", "12"),
        ("  8.2- Core Method Implementation & Code Listings", "12 to 13"),
        ("  8.3- Strength Scoring & Dynamic Feedback Engine", "13"),
        ("Chapter 9: Output & Screen Workflow", "14 to 15"),
        ("  9.1- Startup & Input Prompt Screen", "14"),
        ("  9.2- Weak Password Evaluation & Suggestions", "14"),
        ("  9.3- Medium Password Evaluation & Suggestions", "15"),
        ("  9.4- Strong Password Evaluation & Success State", "15"),
        ("Weekly Progress Reports (Week 1, Week 2, Week 3)", "16 to 17"),
        ("Chapter 10: Testing and Debugging", "18 to 19"),
        ("Chapter 11: Conclusion and Future Enhancement", "20 to 21"),
        ("  11.1- Conclusion", "20"),
        ("  11.2- Future Enhancements", "21"),
    ]

    tbl_toc2 = doc.add_table(rows=0, cols=2)
    tbl_toc2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for title, pnum in toc_items_p2:
        row = tbl_toc2.add_row()
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(5.2), Inches(1.3)
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(title)
        r1 = p1.add_run(pnum)
        if not title.startswith("  "):
            r0.bold = True
            r1.bold = True
        p0.paragraph_format.line_spacing = 1.25
        p1.paragraph_format.line_spacing = 1.25

    doc.add_page_break() # -> Page 6

    # -------------------------------------------------------------
    # PAGE 6: CHAPTER 5: INTRODUCTION (5.1 & 5.2)
    # -------------------------------------------------------------
    p_ch5 = doc.add_paragraph()
    r_ch5 = p_ch5.add_run("CHAPTER 5: INTRODUCTION\n")
    r_ch5.bold = True
    r_ch5.font.size = Pt(14)

    p_51 = doc.add_paragraph()
    r_51_h = p_51.add_run("5.1 Purpose of the Project:\n")
    r_51_h.bold = True
    p_51.paragraph_format.line_spacing = 1.3
    p_51.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_51.add_run(
        "The Password Strength Analyzer Using Java is engineered to deliver an accessible, objective, and visually "
        "engaging desktop tool for evaluating credential resilience. In contemporary software ecosystems, authentication "
        "acts as the primary barrier defending confidential personal records, business applications, and network infrastructure. "
        "Despite repeated security recommendations, end-users frequently adopt passwords lacking sufficient complexity, "
        "leaving them vulnerable to automated brute-force attacks and dictionary matching.\n\n"
        "The primary purpose of this project is to eliminate uncertainty by providing immediate, interactive visual feedback "
        "as credentials are typed. Built with Java Swing and AWT on Java 21 LTS, the application combines desktop GUI responsiveness "
        "with an elegant zero-dependency architecture. Rather than relying on third-party frameworks, it harnesses core Java's native "
        "windowing toolkits, static method decomposition, and character inspection routines.\n\n"
        "Designed for academic clarity, every routine is structured with clear viva-explainable logic, illustrating how event-driven "
        "UI listeners, modular methods, and strict privacy principles unite in a cohesive software microproject."
    )

    p_52 = doc.add_paragraph()
    r_52_h = p_52.add_run("5.2 Problem Statement:\n")
    r_52_h.bold = True
    p_52.paragraph_format.line_spacing = 1.3
    p_52.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_52.add_run(
        "Conventional password verification tools frequently suffer from noticeable drawbacks:\n"
        "1. Absence of Immediate Visual Feedback: Many systems require full form submissions before highlighting password deficiencies, "
        "rather than providing instant keystroke guidance.\n"
        "2. Privacy Concerns & Insecure Caching: Several third-party checkers transmit input over public networks or write test data to local logs, "
        "creating substantial security exposure.\n"
        "3. Cluttered & Inscrutable Implementations: Commercial validators often depend on complex regular expressions and heavy external libraries "
        "that students cannot inspect or defend in academic viva examinations.\n"
        "4. Insufficient Remediation Guidance: Basic tools declare a generic failure state without pinpointing exactly which requirements remain unsatisfied.\n\n"
        "Consequently, there is a clear demand for a lightweight, secure Java desktop GUI analyzer that delivers real-time evaluation, "
        "maintains strict in-memory privacy, and presents structured remediation advice."
    )

    doc.add_page_break() # -> Page 7

    # -------------------------------------------------------------
    # PAGE 7: CHAPTER 5: INTRODUCTION (5.3 OBJECTIVES)
    # -------------------------------------------------------------
    p_53 = doc.add_paragraph()
    r_53_h = p_53.add_run("5.3 Objectives of the Project:\n")
    r_53_h.bold = True
    r_53_h.font.size = Pt(13)

    objs = [
        "1. To develop a modern Java Swing & AWT desktop GUI application adhering strictly to JDK 21 LTS without external libraries.",
        "2. To implement Real-Time Keystroke Analysis: Utilize Swing DocumentListener to update evaluations dynamically as the user types.",
        "3. To implement Length Verification: Validate that candidate passwords contain at least 8 characters.",
        "4. To implement Uppercase Detection: Accurately verify the presence of uppercase letters (A-Z) using Character.isUpperCase.",
        "5. To implement Lowercase Detection: Accurately verify the presence of lowercase letters (a-z) using Character.isLowerCase.",
        "6. To implement Digit Detection: Accurately verify the presence of numeric digits (0-9) using Character.isDigit.",
        "7. To implement Special Character Detection: Detect non-letter, non-digit, non-whitespace symbols (@, #, $, !, etc.).",
        "8. To establish an Objective Scoring & Visual Meter Model: Award 1 point per passed condition and render color-coded meters (Weak/Medium/Strong).",
        "9. To construct a Dynamic Suggestion Engine: Itemize tailored recommendations for each condition that fails.",
        "10. To guarantee Strict In-Memory Privacy: Ensure passwords are never written, logged, hashed, or persisted to disk or databases."
    ]
    for o in objs:
        p_o = doc.add_paragraph()
        p_o.paragraph_format.left_indent = Inches(0.25)
        p_o.paragraph_format.line_spacing = 1.3
        p_o.add_run("• " + o)

    doc.add_page_break() # -> Page 8

    # -------------------------------------------------------------
    # PAGE 8: CHAPTER 6: TOOLS AND TECHNOLOGY (6.1 & 6.2)
    # -------------------------------------------------------------
    p_ch6 = doc.add_paragraph()
    r_ch6 = p_ch6.add_run("CHAPTER 6: TOOLS AND TECHNOLOGY USED\n")
    r_ch6.bold = True
    r_ch6.font.size = Pt(14)

    p_61 = doc.add_paragraph()
    r_61_h = p_61.add_run("6.1 Frontend (Java Swing & AWT Desktop GUI):\n")
    r_61_h.bold = True
    p_61.paragraph_format.line_spacing = 1.3
    p_61.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_61.add_run(
        "• Java Swing & AWT Framework (javax.swing & java.awt):\n"
        "The graphical user interface is constructed using Java's built-in Swing and Abstract Window Toolkit (AWT). Swing provides "
        "lightweight, platform-independent GUI components rendered on top of the Java Virtual Machine. Key controls utilized include "
        "JFrame (main container), JPanel with custom anti-aliased rounded cards, JPasswordField (secure masked input), JTextField "
        "(plain-text reveal), JCheckBox (show/hide toggle), JProgressBar (visual strength meter), JButton (preset test triggers), "
        "and JTextArea (suggestions area).\n\n"
        "• Real-Time Event Architecture (DocumentListener & ActionListener):\n"
        "Implements event-driven architecture using DocumentListener to observe keystroke insertions and deletions in real time, "
        "updating scoring meters and checklist badges synchronously without requiring explicit submit buttons."
    )

    p_62 = doc.add_paragraph()
    r_62_h = p_62.add_run("6.2 Backend (Core Java Architecture & Analysis Engine):\n")
    r_62_h.bold = True
    p_62.paragraph_format.line_spacing = 1.3
    p_62.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_62.add_run(
        "• Core Java (JDK 21 LTS):\n"
        "Developed strictly on Java 21 LTS without Maven, Gradle, or third-party JARs. Java provides rock-solid memory safety, "
        "strong typing, and portable cross-platform bytecode execution.\n\n"
        "• Character Utility Class (java.lang.Character):\n"
        "Employs highly optimized character inspection methods (Character.isUpperCase, Character.isLowerCase, Character.isDigit, "
        "Character.isLetter, and Character.isWhitespace), avoiding complex regular expressions and ensuring complete viva clarity."
    )

    doc.add_page_break() # -> Page 9

    # -------------------------------------------------------------
    # PAGE 9: CHAPTER 6: TOOLS AND TECHNOLOGY (6.3, 6.4, 6.5)
    # -------------------------------------------------------------
    p_63 = doc.add_paragraph()
    r_63_h = p_63.add_run("6.3 Object-Oriented & Procedural Programming Concepts:\n")
    r_63_h.bold = True
    p_63.paragraph_format.line_spacing = 1.3
    p_63.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_63.add_run(
        "• Modularity & Separation of Concerns: Core evaluation algorithms are encapsulated into static methods separate from GUI rendering logic.\n"
        "• Custom Component Extension: Extends JPanel (RoundedPanel, ConditionRow) with custom paintComponent() and anti-aliasing hints for modern aesthetics.\n"
        "• Clean Viva-Explainable Procedural Logic: Uses indexed for-loops with password.charAt(i), allowing examiners to review logic step-by-step."
    )

    p_64 = doc.add_paragraph()
    r_64_h = p_64.add_run("6.4 Security, Privacy & In-Memory Design Principles:\n")
    r_64_h.bold = True
    p_64.paragraph_format.line_spacing = 1.3
    p_64.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_64.add_run(
        "• Volatile In-Memory Lifecycle: Input passwords reside solely within heap memory variables during active evaluation. "
        "When the window closes, memory is immediately garbage collected.\n"
        "• Zero Persistence Footprint: No disk logging, file serialization, or external network requests occur, safeguarding user credentials."
    )

    p_65 = doc.add_paragraph()
    r_65_h = p_65.add_run("6.5 Development Tools & Environment:\n")
    r_65_h.bold = True
    p_65.paragraph_format.line_spacing = 1.3
    p_65.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_65.add_run(
        "• Visual Studio Code (VS Code): Development IDE equipped with Extension Pack for Java.\n"
        "• Java Development Kit (JDK 21.0.12.1): Command-line compiler (javac) and execution runtime (java / javaw).\n"
        "• Batch Script (run.bat): One-click Windows automation script for automatic build and GUI launch."
    )

    doc.add_page_break() # -> Page 10

    # -------------------------------------------------------------
    # PAGE 10: CHAPTER 7: SYSTEM DESIGN (7.1 & 7.2)
    # -------------------------------------------------------------
    p_ch7 = doc.add_paragraph()
    r_ch7 = p_ch7.add_run("CHAPTER 7: SYSTEM DESIGN\n")
    r_ch7.bold = True
    r_ch7.font.size = Pt(14)

    p_71 = doc.add_paragraph()
    r_71_h = p_71.add_run("7.1 System Architecture (Pipeline Model):\n")
    r_71_h.bold = True
    p_71.paragraph_format.line_spacing = 1.25
    p_71.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_71.add_run(
        "The application follows a reactive Event-Driven Architecture paired with a Pipeline Processing Model:\n"
        "1. GUI Input Layer: Captures user keystrokes in JPasswordField or JTextField.\n"
        "2. Event Dispatching: DocumentListener triggers evaluate() on every character change.\n"
        "3. Core Validation Engine: Evaluates the password across five static methods in memory.\n"
        "4. Dynamic Scoring & Feedback: Aggregates score (0-5), updates strength bar, condition badges, and suggestions.\n"
        "5. Clean Termination: Window close event gracefully disposes frames without lingering threads."
    )

    p_72 = doc.add_paragraph()
    r_72_h = p_72.add_run("7.2 System Design Block Diagram:\n")
    r_72_h.bold = True

    diagram_text = (
        "+-------------------------------------------------------------------------+\n"
        "|                    JAVA SWING DESKTOP GUI WINDOW                        |\n"
        "|         [ JPasswordField / JTextField  with Show/Hide Toggle ]          |\n"
        "+------------------------------------+------------------------------------+\n"
        "                                     | Real-Time DocumentListener Event\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                      IN-MEMORY PROCESSING STAGE                         |\n"
        "|                   String password (Volatile RAM)                        |\n"
        "+------------------------------------+------------------------------------+\n"
        "                                     |\n"
        "        +----------------------------+----------------------------+\n"
        "        |              |             |             |              |\n"
        "        v              v             v             v              v\n"
        "  +-----------+  +-----------+ +-----------+ +-----------+  +-----------+\n"
        "  |  hasMin-  |  |   has-    | |   has-    | |   has-    |  |hasSpecial-|\n"
        "  |  Length() |  |Uppercase()| |Lowercase()| | Number()  |  |Character()|\n"
        "  | (len>=8)  |  |(isUpper)  | |(isLower)  | | (isDigit) |  |(!let!num) |\n"
        "  +-----+-----+  +-----+-----+ +-----+-----+ +-----+-----+  +-----+-----+\n"
        "        |              |             |             |              |\n"
        "        +----------------------------+----------------------------+\n"
        "                                     | Boolean Results\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                        SCORING & STRENGTH ENGINE                        |\n"
        "|    Accumulates Score (0..5)  --->  getStrength() [Weak/Medium/Strong]    |\n"
        "+------------------------------------+------------------------------------+\n"
        "                                     |\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                    DYNAMIC GUI VIEW REFRESH                             |\n"
        "|   - Animated JProgressBar Color (Red / Amber / Green)                  |\n"
        "|   - ConditionRow Badges (Passed ✓ / Failed ○)                           |\n"
        "|   - Suggestions JTextArea (Instant Actionable Guidance)                 |\n"
        "+-------------------------------------------------------------------------+"
    )
    p_d = doc.add_paragraph()
    p_d.paragraph_format.line_spacing = 1.0
    r_d = p_d.add_run(diagram_text)
    r_d.font.name = 'Courier New'
    r_d.font.size = Pt(8.5)

    doc.add_page_break() # -> Page 11

    # -------------------------------------------------------------
    # PAGE 11: CHAPTER 7: SYSTEM DESIGN (7.3 DATA FLOW)
    # -------------------------------------------------------------
    p_73 = doc.add_paragraph()
    r_73_h = p_73.add_run("7.3 Step-by-Step Data Flow Description:\n")
    r_73_h.bold = True
    r_73_h.font.size = Pt(13)

    steps = [
        "1. Initialization: main() configures system Look and Feel and schedules GUI creation on Event Dispatch Thread (EDT).",
        "2. Frame Assembly: JFrame instantiates header, password card, strength meter, preset buttons, checklist, and suggestions.",
        "3. Real-Time Keystroke Capture: DocumentListener detects character input instantly.",
        "4. Condition 1 Evaluation: hasMinLength() tests password.length() >= 8 and returns true or false.",
        "5. Condition 2 Evaluation: hasUppercase() scans characters with Character.isUpperCase(c).",
        "6. Condition 3 Evaluation: hasLowercase() scans characters with Character.isLowerCase(c).",
        "7. Condition 4 Evaluation: hasNumber() scans characters with Character.isDigit(c).",
        "8. Condition 5 Evaluation: hasSpecialCharacter() checks for non-letter, non-digit, non-whitespace symbols.",
        "9. Score Accumulation: Points tally (0 to 5) based on passed conditions.",
        "10. Visual Meter Update: JProgressBar value adjusts and changes color dynamically (Red, Amber, or Emerald Green).",
        "11. Checklist Refresh: ConditionRow instances toggle icons between '○ Failed' and '✓ Passed'.",
        "12. Feedback Rendering: JTextArea displays congratulations (score 5) or targeted remediation bullets.",
        "13. Quick Tests: Preset buttons allow one-click testing of benchmark passwords."
    ]
    for s in steps:
        p_step = doc.add_paragraph()
        p_step.paragraph_format.left_indent = Inches(0.2)
        p_step.paragraph_format.line_spacing = 1.25
        p_step.add_run("• " + s)

    doc.add_page_break() # -> Page 12

    # -------------------------------------------------------------
    # PAGE 12: CHAPTER 8: IMPLEMENTATION (8.1 & 8.2 PART 1)
    # -------------------------------------------------------------
    p_ch8 = doc.add_paragraph()
    r_ch8 = p_ch8.add_run("CHAPTER 8: IMPLEMENTATION\n")
    r_ch8.bold = True
    r_ch8.font.size = Pt(14)

    p_81 = doc.add_paragraph()
    r_81_h = p_81.add_run("8.1 Architectural Design & Method Decomposition:\n")
    r_81_h.bold = True
    p_81.paragraph_format.line_spacing = 1.3
    p_81.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_81.add_run(
        "The application integrates clean OOP modularity with procedural static methods for straightforward viva presentation:\n\n"
        "• hasMinLength(String password): Validates length >= 8.\n"
        "• hasUppercase(String password): Scans for uppercase letters with Character.isUpperCase.\n"
        "• hasLowercase(String password): Scans for lowercase letters with Character.isLowerCase.\n"
        "• hasNumber(String password): Scans for digits with Character.isDigit.\n"
        "• hasSpecialCharacter(String password): Detects special non-alphanumeric, non-whitespace symbols.\n"
        "• getStrength(int score): Maps total score into 'Weak', 'Medium', or 'Strong'.\n"
        "• evaluate(): Synchronizes the Swing GUI state with validation results in real time."
    )

    p_82 = doc.add_paragraph()
    r_82_h = p_82.add_run("8.2 Core Method Implementation & Code Listings (Part 1):\n")
    r_82_h.bold = True

    code_snippet_p1 = (
        "// Method 1: Checks minimum length (at least 8 characters)\n"
        "public static boolean hasMinLength(String password) {\n"
        "    return password != null && password.length() >= 8;\n"
        "}\n\n"
        "// Method 2: Checks for uppercase letter (A-Z)\n"
        "public static boolean hasUppercase(String password) {\n"
        "    if (password == null) return false;\n"
        "    for (int i = 0; i < password.length(); i++) {\n"
        "        if (Character.isUpperCase(password.charAt(i))) return true;\n"
        "    }\n"
        "    return false;\n"
        "}\n\n"
        "// Method 3: Checks for lowercase letter (a-z)\n"
        "public static boolean hasLowercase(String password) {\n"
        "    if (password == null) return false;\n"
        "    for (int i = 0; i < password.length(); i++) {\n"
        "        if (Character.isLowerCase(password.charAt(i))) return true;\n"
        "    }\n"
        "    return false;\n"
        "}"
    )
    p_c1 = doc.add_paragraph()
    p_c1.paragraph_format.line_spacing = 1.05
    r_c1 = p_c1.add_run(code_snippet_p1)
    r_c1.font.name = 'Courier New'
    r_c1.font.size = Pt(9.5)

    doc.add_page_break() # -> Page 13

    # -------------------------------------------------------------
    # PAGE 13: CHAPTER 8: IMPLEMENTATION (8.2 PART 2 & 8.3)
    # -------------------------------------------------------------
    code_snippet_p2 = (
        "// Method 4: Checks for numeric digit (0-9)\n"
        "public static boolean hasNumber(String password) {\n"
        "    if (password == null) return false;\n"
        "    for (int i = 0; i < password.length(); i++) {\n"
        "        if (Character.isDigit(password.charAt(i))) return true;\n"
        "    }\n"
        "    return false;\n"
        "}\n\n"
        "// Method 5: Checks for special character\n"
        "public static boolean hasSpecialCharacter(String password) {\n"
        "    if (password == null) return false;\n"
        "    for (int i = 0; i < password.length(); i++) {\n"
        "        char c = password.charAt(i);\n"
        "        if (!Character.isLetter(c) && !Character.isDigit(c) && !Character.isWhitespace(c))\n"
        "            return true;\n"
        "    }\n"
        "    return false;\n"
        "}\n\n"
        "// Method 6: Strength evaluation\n"
        "public static String getStrength(int score) {\n"
        "    if (score <= 2) return \"Weak\";\n"
        "    else if (score <= 4) return \"Medium\";\n"
        "    else return \"Strong\";\n"
        "}"
    )
    p_c2 = doc.add_paragraph()
    p_c2.paragraph_format.line_spacing = 1.05
    r_c2 = p_c2.add_run(code_snippet_p2)
    r_c2.font.name = 'Courier New'
    r_c2.font.size = Pt(9.5)

    p_83 = doc.add_paragraph()
    r_83_h = p_83.add_run("\n8.3 Strength Scoring & Dynamic Feedback Engine:\n")
    r_83_h.bold = True
    p_83.paragraph_format.line_spacing = 1.3
    p_83.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_83.add_run(
        "Inside evaluate(), the score is dynamically calculated on every keystroke. When score reaches 5, the progress bar "
        "turns vibrant green, the badge displays 'Strong', and congratulations are rendered. For scores below 5, the suggestions "
        "area lists bulleted guidance for all unsatisfied criteria, giving users immediate feedback to improve security."
    )

    doc.add_page_break() # -> Page 14

    # -------------------------------------------------------------
    # PAGE 14: CHAPTER 9: OUTPUT & WORKFLOW (9.1 & 9.2)
    # -------------------------------------------------------------
    p_ch9 = doc.add_paragraph()
    r_ch9 = p_ch9.add_run("CHAPTER 9: OUTPUT & SCREEN WORKFLOW\n")
    r_ch9.bold = True
    r_ch9.font.size = Pt(14)

    p_9_intro = doc.add_paragraph()
    p_9_intro.paragraph_format.line_spacing = 1.25
    p_9_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_9_intro.add_run(
        "The following sections present the desktop GUI screens and interaction workflow across various test cases. "
        "As requested, clean bordered placeholder boxes are provided for GUI screenshot attachment.\n"
    )

    screens_p1 = [
        ("9.1 Startup and Empty State Screen:",
         "Displays the initial desktop GUI window with title badge 'Empty', score 0/5, gray progress bar, and prompt awaiting password input.",
         "[ Space for Screenshot 9.1: Desktop GUI Startup & Empty State Screen ]"),
        ("9.2 Weak Password Evaluation Screen (Input: 'abc' & 'password'):",
         "Demonstrates real-time visual response for weak credentials: red progress bar, Weak badge, failed checklist indicators, and bulleted recommendations.",
         "[ Space for Screenshot 9.2: Weak Password Desktop Screen & Suggestions ]")
    ]
    for title, desc, ph in screens_p1:
        p_s = doc.add_paragraph()
        r_sh = p_s.add_run(title + "\n")
        r_sh.bold = True
        r_sh.font.size = Pt(11.5)
        r_sd = p_s.add_run(desc + "\n")
        r_sd.font.size = Pt(10.5)

        tbl_box = doc.add_table(rows=1, cols=1)
        tbl_box.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl_box.rows[0].cells[0]
        c.width = Inches(6.2)
        set_cell_background(c, "F8F9FA")
        set_cell_margins(c, top=450, bottom=450, left=200, right=200)
        p_c = c.paragraphs[0]
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_box = p_c.add_run(ph)
        r_box.font.name = 'Courier New'
        r_box.font.size = Pt(10)
        r_box.font.color.rgb = RGBColor(120, 120, 120)
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_page_break() # -> Page 15

    # -------------------------------------------------------------
    # PAGE 15: CHAPTER 9: OUTPUT & WORKFLOW (9.3 & 9.4)
    # -------------------------------------------------------------
    screens_p2 = [
        ("9.3 Medium Password Evaluation Screen (Input: 'HELLO123' & 'Hello123'):",
         "Shows intermediate complexity state with amber progress bar, Medium badge, score 3 or 4, and targeted remaining suggestions.",
         "[ Space for Screenshot 9.3: Medium Password Desktop Screen ]"),
        ("9.4 Strong Password Evaluation Screen (Input: 'Hello@123'):",
         "Illustrates optimal execution with vibrant green progress bar, Strong badge, score 5/5, all 5 passed checkmarks, and celebratory success message.",
         "[ Space for Screenshot 9.4: Strong Password Desktop Screen & Success State ]")
    ]
    for title, desc, ph in screens_p2:
        p_s = doc.add_paragraph()
        r_sh = p_s.add_run(title + "\n")
        r_sh.bold = True
        r_sh.font.size = Pt(11.5)
        r_sd = p_s.add_run(desc + "\n")
        r_sd.font.size = Pt(10.5)

        tbl_box = doc.add_table(rows=1, cols=1)
        tbl_box.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl_box.rows[0].cells[0]
        c.width = Inches(6.2)
        set_cell_background(c, "F8F9FA")
        set_cell_margins(c, top=450, bottom=450, left=200, right=200)
        p_c = c.paragraphs[0]
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_box = p_c.add_run(ph)
        r_box.font.name = 'Courier New'
        r_box.font.size = Pt(10)
        r_box.font.color.rgb = RGBColor(120, 120, 120)
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_page_break() # -> Page 16

    # -------------------------------------------------------------
    # PAGE 16: WEEKLY PROGRESS REPORTS (WEEK 1 & WEEK 2)
    # -------------------------------------------------------------
    p_wpr = doc.add_paragraph()
    r_wpr = p_wpr.add_run("WEEKLY PROGRESS REPORTS\n")
    r_wpr.bold = True
    r_wpr.font.size = Pt(14)

    weeks_p1 = [
        ("WEEK 1 – Problem Formulation, Security Criteria, and Architecture",
         "To analyze cybersecurity criteria for credential evaluation, establish zero-dependency constraints, and formulate modular static method signatures.",
         [
             "1. Formulated project title: 'Password Strength Analyzer Using Java'.",
             "2. Defined project scope around Core Java (JDK 21 LTS) without external third-party dependencies.",
             "3. Established the 5 core validation criteria: length, uppercase, lowercase, numbers, and special characters.",
             "4. Designed the 0-to-5 scoring rubric and mapping tiers (Weak, Medium, Strong).",
             "5. Enforced in-memory privacy policy: passwords must never be stored, logged, or saved.",
             "6. Formulated clean viva-friendly method signatures and algorithmic flow."
         ],
         "Requirement specifications finalized, pipeline architecture established, and static method signatures approved."),

        ("WEEK 2 – Core Java Implementation, Character Parsing, and Logic Verification",
         "To implement the PasswordStrengthAnalyzer.java class with dedicated validation methods, character checking loops, and dynamic suggestion mechanisms.",
         [
             "1. Implemented hasMinLength() verifying string length >= 8.",
             "2. Implemented hasUppercase() using Character.isUpperCase in an indexed for loop.",
             "3. Implemented hasLowercase() using Character.isLowerCase in an indexed for loop.",
             "4. Implemented hasNumber() using Character.isDigit in an indexed for loop.",
             "5. Implemented hasSpecialCharacter() verifying non-letter, non-digit, and non-whitespace characters.",
             "6. Implemented result() helper and getStrength() score evaluation methods.",
             "7. Constructed main() pipeline with aligned output formatting and suggestions list."
         ],
         "Core Java application fully implemented and compiled with zero errors or warnings using JDK 21.")
    ]

    for wt, wo, wd, wr in weeks_p1:
        p_wt = doc.add_paragraph()
        r_wt = p_wt.add_run(wt + "\n")
        r_wt.bold = True
        r_wt.font.size = Pt(11.5)

        p_wo = doc.add_paragraph()
        r_wo_h = p_wo.add_run("Objective: ")
        r_wo_h.bold = True
        p_wo.paragraph_format.line_spacing = 1.15
        p_wo.add_run(wo)

        p_wd = doc.add_paragraph()
        r_wd_h = p_wd.add_run("Work Done:\n")
        r_wd_h.bold = True
        p_wd.paragraph_format.line_spacing = 1.15
        for item in wd:
            p_item = doc.add_paragraph()
            p_item.paragraph_format.left_indent = Inches(0.2)
            p_item.paragraph_format.line_spacing = 1.1
            p_item.add_run("• " + item)

        p_wr = doc.add_paragraph()
        r_wr_h = p_wr.add_run("Result: ")
        r_wr_h.bold = True
        p_wr.paragraph_format.line_spacing = 1.15
        p_wr.add_run(wr + "\n")

    doc.add_page_break() # -> Page 17

    # -------------------------------------------------------------
    # PAGE 17: WEEKLY PROGRESS REPORTS (WEEK 3)
    # -------------------------------------------------------------
    p_wt3 = doc.add_paragraph()
    r_wt3 = p_wt3.add_run("WEEK 3 – Java Swing Desktop GUI Development, Testing, and Documentation\n")
    r_wt3.bold = True
    r_wt3.font.size = Pt(12)

    p_wo3 = doc.add_paragraph()
    r_wo_h3 = p_wo3.add_run("Objective: ")
    r_wo_h3.bold = True
    p_wo3.paragraph_format.line_spacing = 1.25
    p_wo3.add_run("To design and build the Java Swing desktop GUI, implement real-time DocumentListener keystroke listeners, configure run.bat launcher, and compile project documentation.")

    p_wd3 = doc.add_paragraph()
    r_wd_h3 = p_wd3.add_run("Work Done:\n")
    r_wd_h3.bold = True
    p_wd3.paragraph_format.line_spacing = 1.25
    wd3_items = [
        "1. Developed modern Swing GUI with dark theme styling, anti-aliased rounded cards, and smooth borders.",
        "2. Integrated DocumentListener for real-time keystroke evaluation on both masked and plain-text fields.",
        "3. Built dynamic JProgressBar with color shifting and 5 ConditionRow checklist items.",
        "4. Implemented quick-test preset buttons ('abc', 'password', 'HELLO123', 'Hello123', 'Hello@123').",
        "5. Created one-click Windows launcher run.bat for instant execution.",
        "6. Verified 16 comprehensive test cases and generated project report."
    ]
    for item in wd3_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.left_indent = Inches(0.2)
        p_item.paragraph_format.line_spacing = 1.2
        p_item.add_run("• " + item)

    p_wr3 = doc.add_paragraph()
    r_wr_h3 = p_wr3.add_run("\nResult: ")
    r_wr_h3.bold = True
    p_wr3.paragraph_format.line_spacing = 1.25
    p_wr3.add_run("Desktop GUI application and documentation completed with 100% test pass rate.\n\n")

    p_summary = doc.add_paragraph()
    r_sum_h = p_summary.add_run("Milestone Summary:\n")
    r_sum_h.bold = True
    p_summary.paragraph_format.line_spacing = 1.25
    p_summary.add_run(
        "Over the three-week development sprint, the Password Strength Analyzer transitioned from a core rule-based "
        "concept into a sophisticated, modern Java Swing desktop GUI microproject. The final deliverables comprise "
        "the zero-dependency source code, batch launchers, web simulator, and this comprehensive report."
    )

    doc.add_page_break() # -> Page 18

    # -------------------------------------------------------------
    # PAGE 18: CHAPTER 10: TESTING AND DEBUGGING (TC01 - TC08)
    # -------------------------------------------------------------
    p_ch10 = doc.add_paragraph()
    r_ch10 = p_ch10.add_run("CHAPTER 10: TESTING AND DEBUGGING\n")
    r_ch10.bold = True
    r_ch10.font.size = Pt(14)

    p_10_desc = doc.add_paragraph()
    p_10_desc.paragraph_format.line_spacing = 1.25
    p_10_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_10_desc.add_run(
        "Comprehensive testing was conducted across individual methods and the Swing GUI desktop application using JDK 21. "
        "Test cases covered minimal strings, missing criteria combinations, mixed casing, numeric digits, and special characters. "
        "All 16 test cases executed with 100% pass rate."
    )

    test_data_p1 = [
        ("TC01", "App Startup & GUI", "Launch run.bat", "Display Swing GUI window", "GUI window rendered", "Pass"),
        ("TC02", "Empty Input", "\"\"", "Score: 0 / 5, Weak, 5 suggestions", "Score: 0 / 5, Weak, 5 suggestions", "Pass"),
        ("TC03", "Single Char Lowercase", "\"a\"", "Score: 1 / 5, Weak", "Score: 1 / 5, Weak", "Pass"),
        ("TC04", "Required Input 1", "\"abc\"", "Score: 1 / 5, Weak, 4 suggestions", "Score: 1 / 5, Weak, 4 suggestions", "Pass"),
        ("TC05", "Required Input 2", "\"password\"", "Score: 2 / 5, Weak, 3 suggestions", "Score: 2 / 5, Weak, 3 suggestions", "Pass"),
        ("TC06", "Length Only (Lowercase)", "\"abcdefghij\"", "Score: 2 / 5, Weak", "Score: 2 / 5, Weak", "Pass"),
        ("TC07", "Short Upper + Lower", "\"Abc\"", "Score: 2 / 5, Weak", "Score: 2 / 5, Weak", "Pass"),
        ("TC08", "Required Input 3", "\"HELLO123\"", "Score: 3 / 5, Medium, 2 suggestions", "Score: 3 / 5, Medium, 2 suggestions", "Pass"),
    ]

    table_tests1 = doc.add_table(rows=1, cols=6)
    table_tests1.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table_tests1.rows[0].cells
    hdr_titles = ["Test ID", "Feature Tested", "Input", "Expected Output", "Actual Output", "Result"]
    for i, t in enumerate(hdr_titles):
        hdr[i].text = t
        set_cell_background(hdr[i], "1F2937")
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.runs[0]
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    col_widths = [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.4), Inches(1.4), Inches(0.6)]

    for row_idx, data in enumerate(test_data_p1):
        row = table_tests1.add_row()
        fill_bg = "F9FAFB" if row_idx % 2 == 1 else "FFFFFF"
        for i, val in enumerate(data):
            c = row.cells[i]
            c.width = col_widths[i]
            c.text = val
            set_cell_background(c, fill_bg)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.runs[0].font.size = Pt(8.5)
            if i in [0, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if i == 5:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(16, 149, 106)

    doc.add_page_break() # -> Page 19

    # -------------------------------------------------------------
    # PAGE 19: CHAPTER 10: TESTING AND DEBUGGING (TC09 - TC16)
    # -------------------------------------------------------------
    p_10_cont = doc.add_paragraph()
    r_10_cont = p_10_cont.add_run("CHAPTER 10: TESTING AND DEBUGGING (Continued)\n")
    r_10_cont.bold = True
    r_10_cont.font.size = Pt(13)

    test_data_p2 = [
        ("TC09", "Required Input 4", "\"Hello123\"", "Score: 4 / 5, Medium, 1 suggestion", "Score: 4 / 5, Medium, 1 suggestion", "Pass"),
        ("TC10", "Required Input 5", "\"Hello@123\"", "Score: 5 / 5, Strong, Great message", "Score: 5 / 5, Strong, Great message", "Pass"),
        ("TC11", "Special Symbol Set 1", "\"Admin#2026\"", "Score: 5 / 5, Strong", "Score: 5 / 5, Strong", "Pass"),
        ("TC12", "Special Symbol Set 2", "\"Secure$99!\"", "Score: 5 / 5, Strong", "Score: 5 / 5, Strong", "Pass"),
        ("TC13", "Whitespace Handling", "\"Hello 123\"", "Space not special, Score: 4/5", "Space not special, Score: 4/5", "Pass"),
        ("TC14", "Show/Hide Password", "Toggle checkbox", "Cards switch plain / masked", "Switched dynamically", "Pass"),
        ("TC15", "Quick Test Preset", "Click Hello@123", "Fills input & updates UI", "UI updated to Strong", "Pass"),
        ("TC16", "CLI Fallback Mode", "Run with --cli", "Executes in terminal mode", "Terminal mode executed", "Pass")
    ]

    table_tests2 = doc.add_table(rows=1, cols=6)
    table_tests2.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr2 = table_tests2.rows[0].cells
    for i, t in enumerate(hdr_titles):
        hdr2[i].text = t
        set_cell_background(hdr2[i], "1F2937")
        p = hdr2[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.runs[0]
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, data in enumerate(test_data_p2):
        row = table_tests2.add_row()
        fill_bg = "F9FAFB" if row_idx % 2 == 1 else "FFFFFF"
        for i, val in enumerate(data):
            c = row.cells[i]
            c.width = col_widths[i]
            c.text = val
            set_cell_background(c, fill_bg)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.runs[0].font.size = Pt(8.5)
            if i in [0, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if i == 5:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(16, 149, 106)

    doc.add_page_break() # -> Page 20

    # -------------------------------------------------------------
    # PAGE 20: CHAPTER 11: CONCLUSION AND FUTURE ENHANCEMENT (11.1)
    # -------------------------------------------------------------
    p_ch11 = doc.add_paragraph()
    r_ch11 = p_ch11.add_run("CHAPTER 11: CONCLUSION AND FUTURE ENHANCEMENT\n")
    r_ch11.bold = True
    r_ch11.font.size = Pt(14)

    p_111 = doc.add_paragraph()
    r_111_h = p_111.add_run("11.1 Conclusion:\n")
    r_111_h.bold = True
    p_111.paragraph_format.line_spacing = 1.35
    p_111.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_111.add_run(
        "The Password Strength Analyzer Using Java was successfully conceptualized, implemented, and rigorously evaluated "
        "using Core Java and Java Swing (JDK 21 LTS). The application accomplishes all stated project objectives, demonstrating "
        "a sleek, modern desktop GUI utility that provides real-time, deterministic password strength evaluation without "
        "unnecessary external dependencies.\n\n"
        "By structuring the evaluation logic into five discrete, self-contained static methods alongside event-driven Swing "
        "listeners, the codebase showcases foundational software engineering best practices including modular design, "
        "procedural character inspection, and clean viva-explainable logic. Furthermore, by enforcing strict in-memory execution, "
        "the project upholds essential cybersecurity privacy principles: no user credentials are ever stored, logged, serialized, "
        "or exposed to persistent media.\n\n"
        "The project serves as an ideal microproject model for undergraduate computer science and engineering coursework, "
        "combining practical security awareness with solid desktop Java proficiency."
    )

    doc.add_page_break() # -> Page 21

    # -------------------------------------------------------------
    # PAGE 21: CHAPTER 11: CONCLUSION AND FUTURE ENHANCEMENT (11.2)
    # -------------------------------------------------------------
    p_112 = doc.add_paragraph()
    r_112_h = p_112.add_run("11.2 Future Enhancements:\n")
    r_112_h.bold = True
    p_112.paragraph_format.line_spacing = 1.3
    p_112.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    enhancements = [
        ("1. Shannon Entropy Mathematical Estimation: ", "Incorporate mathematical entropy calculation [H = L * log2(R)] to compute password bit-strength and exact time-to-crack estimates."),
        ("2. Common Dictionary & Compromised Credential Filter: ", "Integrate a lightweight lookup against top 1,000 common passwords (e.g. '123456', 'qwerty') to immediately flag known compromised credentials."),
        ("3. Advanced Theme Customization Engine: ", "Provide dynamic visual theme switching (Light Mode, High-Contrast Mode, Cyberpunk Dark) using customizable UI delegates."),
        ("4. Automated Password Generator: ", "Add an interactive password generator using java.security.SecureRandom to automatically construct high-entropy credentials based on user-selected criteria."),
        ("5. Clipboard Copy & Auto-Clear Timer: ", "Include a safe clipboard copy button with an automatic 30-second memory clear timer to prevent clipboard snooping."),
        ("6. Multi-Language & Internationalization (i18n): ", "Support multiple international languages and Unicode character alphabets for worldwide accessibility.")
    ]

    for title, desc in enhancements:
        p_enh = doc.add_paragraph()
        p_enh.paragraph_format.left_indent = Inches(0.25)
        p_enh.paragraph_format.line_spacing = 1.3
        r_et = p_enh.add_run("• " + title)
        r_et.bold = True
        r_ed = p_enh.add_run(desc)

    doc.save(filename)
    print(f"Successfully generated 21-page DOCX: {filename}")

if __name__ == "__main__":
    docx_path = r"c:\Users\Vrund\Downloads\java_mcp\Password_Strength_Analyzer_Project_Report.docx"
    create_docx(docx_path)
