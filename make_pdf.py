import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        # Do not print page numbers on cover (1) and certificate (2)
        if self._pageNumber > 2:
            self.saveState()
            self.setFont("Times-Roman", 10)
            self.setFillColor(colors.HexColor("#4B5563"))
            self.drawRightString(letter[0] - 54, 36, f"Page {self._pageNumber}")
            self.restoreState()

def create_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#101828")
    )

    sub_title = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=17,
        alignment=1,
        textColor=colors.HexColor("#374151")
    )

    pce_head = ParagraphStyle(
        'PCEHead',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=17,
        leading=22,
        alignment=1,
        textColor=colors.HexColor("#70131D")
    )

    chapter_head = ParagraphStyle(
        'ChapterHead',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=19,
        textColor=colors.HexColor("#111827"),
        spaceAfter=12
    )

    sec_head = ParagraphStyle(
        'SecHead',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1F2937"),
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=16,
        alignment=4,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#111827")
    )

    story = []

    # =========================================================
    # PAGE 1: COVER PAGE
    # =========================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("PILLAI COLLEGE OF ENGINEERING", pce_head))
    story.append(Paragraph("Department of Electronics & Telecommunication<br/>New Panvel – 410206", sub_title))
    story.append(Spacer(1, 35))

    story.append(Paragraph("<b>Java Programming<br/>Mini Project Report<br/>On</b>", sub_title))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>PASSWORD STRENGTH ANALYZER USING JAVA</b>", title_style))
    story.append(Spacer(1, 35))

    story.append(Paragraph("Submitted in partial fulfilment of the requirement<br/>for the Degree of", sub_title))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Bachelor of Technology<br/>In<br/>Electronics & Telecommunication</b>", sub_title))
    story.append(Spacer(1, 35))

    story.append(Paragraph("Submitted By<br/><b>Sara Sachin Ture: [Roll No: ETC656]</b>", sub_title))
    story.append(Spacer(1, 25))

    story.append(Paragraph("Supervisor<br/><b>Dr. Aboli Khedkar</b>", sub_title))
    story.append(Spacer(1, 40))

    story.append(Paragraph("<b>Department of Electronics & Telecommunication<br/>PILLAI COLLEGE OF ENGINEERING<br/>New Panvel – 410206<br/>Academic Year 2026 - 27</b>", sub_title))
    story.append(PageBreak()) # -> Page 2

    # =========================================================
    # PAGE 2: CERTIFICATE
    # =========================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>DEPARTMENT OF ELECTRONICS & TELECOMMUNICATION</b>", ParagraphStyle('CDep', parent=sub_title, fontName='Times-Bold', fontSize=13)))
    story.append(Paragraph("Pillai College of Engineering<br/>New Panvel – 410206", sub_title))
    story.append(Spacer(1, 30))

    story.append(Paragraph("<b>CERTIFICATE</b>", ParagraphStyle('CertT', parent=title_style, fontSize=16)))
    story.append(Spacer(1, 25))

    story.append(Paragraph(
        "This is to certify that the requirements for the Java Programming project entitled "
        "<b>‘Password Strength Analyzer Using Java’</b> have been successfully completed by the following students:",
        body_style
    ))
    story.append(Spacer(1, 15))

    cert_table_data = [
        [Paragraph("<b>Name</b>", body_style), Paragraph("<b>Roll No.</b>", body_style)],
        [Paragraph("Sara Sachin Ture", body_style), Paragraph("ETC656", body_style)]
    ]
    t_cert = Table(cert_table_data, colWidths=[240, 160])
    t_cert.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor("#9CA3AF")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cert)
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "in partial fulfillment of Bachelor of Technology in the Department of Electronics "
        "& Telecommunications, Pillai College of Engineering, New Panvel – 410206 during the "
        "Academic Year 2026 – 2027.",
        body_style
    ))
    story.append(Spacer(1, 120))

    story.append(Paragraph("_____________________<br/><b>Supervisor<br/>Dr. Aboli Khedkar</b>", ParagraphStyle('Sig', parent=body_style, alignment=2, leading=16)))
    story.append(PageBreak()) # -> Page 3

    # =========================================================
    # PAGE 3: ABSTRACT
    # =========================================================
    story.append(Paragraph("CHAPTER 3: ABSTRACT", chapter_head))
    story.append(Paragraph(
        "The <b>Password Strength Analyzer Using Java</b> is an interactive, modern Java desktop GUI application designed "
        "and developed to evaluate the robustness and entropy of user credentials against industry-standard password security "
        "criteria. In modern computing environments, authentication mechanisms remain the primary line of defense against "
        "unauthorized breaches. However, end-users frequently select simplistic or predictable passwords vulnerable to dictionary "
        "attacks, credential stuffing, and brute-force cracking. This project addresses this challenge through an automated, "
        "real-time evaluation engine engineered with Java Swing and AWT.",
        body_style
    ))
    story.append(Paragraph(
        "Built strictly around the modern Java 21 LTS runtime using native Java GUI packages (javax.swing and java.awt), "
        "the application eliminates external dependencies while providing a sleek, responsive interface. The GUI features "
        "anti-aliased rounded cards, real-time DocumentListener keystroke analysis, an animated color-coded strength bar, a show/hide "
        "password toggle, quick test triggers, and live condition badges. To safeguard user confidentiality, all evaluations "
        "occur strictly in-memory: no passwords are ever stored, written to files, transmitted across networks, or logged.",
        body_style
    ))
    story.append(Paragraph(
        "The system evaluates five core security criteria: minimum length (8+ characters), uppercase letters (A-Z), lowercase "
        "letters (a-z), numeric digits (0-9), and special symbols. Each passed test awards 1 point, computing a 0-to-5 score mapped "
        "to 'Weak' (0–2), 'Medium' (3–4), and 'Strong' (5) tiers with dynamic remediation suggestions. The project demonstrates "
        "the effective synthesis of core Java OOP, event-driven GUI development, and secure software design.",
        body_style
    ))
    story.append(PageBreak()) # -> Page 4

    # =========================================================
    # PAGE 4: TABLE OF CONTENTS (PART 1)
    # =========================================================
    story.append(Paragraph("CHAPTER 4: TABLE OF CONTENTS", chapter_head))
    
    toc_p1 = [
        [Paragraph("<b>Chapter 1: Front Page</b>", body_style), Paragraph("<b>1</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Chapter 2: Certificate</b>", body_style), Paragraph("<b>2</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Chapter 3: Abstract</b>", body_style), Paragraph("<b>3</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Chapter 4: Table of Contents</b>", body_style), Paragraph("<b>4 to 5</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Chapter 5: Introduction</b>", body_style), Paragraph("<b>6 to 7</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1- Purpose of Project", body_style), Paragraph("6", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2- Problem Statement", body_style), Paragraph("6", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3- Objectives of Project", body_style), Paragraph("7", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Chapter 6: Tools and Technology Used</b>", body_style), Paragraph("<b>8 to 9</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1- Frontend (Java Swing & AWT Desktop GUI)", body_style), Paragraph("8", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2- Backend (Core Java Architecture & Analysis Engine)", body_style), Paragraph("8", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.3- Object-Oriented Programming Concepts", body_style), Paragraph("9", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.4- Security, Privacy & In-Memory Design Principles", body_style), Paragraph("9", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.5- Development Tools & Environment", body_style), Paragraph("9", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Chapter 7: System Design</b>", body_style), Paragraph("<b>10 to 11</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.1- System Architecture (Pipeline Model)", body_style), Paragraph("10", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.2- System Design Block Diagram", body_style), Paragraph("10", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.3- Step-by-Step Data Flow Description", body_style), Paragraph("11", ParagraphStyle('R', parent=body_style, alignment=2))],
    ]

    t_toc1 = Table(toc_p1, colWidths=[410, 94])
    t_toc1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_toc1)
    story.append(PageBreak()) # -> Page 5

    # =========================================================
    # PAGE 5: TABLE OF CONTENTS (PART 2)
    # =========================================================
    story.append(Paragraph("CHAPTER 4: TABLE OF CONTENTS (Continued)", chapter_head))

    toc_p2 = [
        [Paragraph("<b>Chapter 8: Implementation</b>", body_style), Paragraph("<b>12 to 13</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.1- Architectural Design & Method Decomposition", body_style), Paragraph("12", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.2- Core Method Implementation & Code Listings", body_style), Paragraph("12 to 13", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.3- Strength Scoring & Dynamic Feedback Engine", body_style), Paragraph("13", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Chapter 9: Output & Screen Workflow</b>", body_style), Paragraph("<b>14 to 15</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.1- Startup & Input Prompt Screen", body_style), Paragraph("14", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.2- Weak Password Evaluation & Suggestions", body_style), Paragraph("14", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.3- Medium Password Evaluation & Suggestions", body_style), Paragraph("15", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.4- Strong Password Evaluation & Success State", body_style), Paragraph("15", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Weekly Progress Reports (Week 1, Week 2, Week 3)</b>", body_style), Paragraph("<b>16 to 17</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Chapter 10: Testing and Debugging</b>", body_style), Paragraph("<b>18 to 19</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("<b>Chapter 11: Conclusion and Future Enhancement</b>", body_style), Paragraph("<b>20 to 21</b>", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;11.1- Conclusion", body_style), Paragraph("20", ParagraphStyle('R', parent=body_style, alignment=2))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;11.2- Future Enhancements", body_style), Paragraph("21", ParagraphStyle('R', parent=body_style, alignment=2))],
    ]

    t_toc2 = Table(toc_p2, colWidths=[410, 94])
    t_toc2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_toc2)
    story.append(PageBreak()) # -> Page 6

    # =========================================================
    # PAGE 6: CHAPTER 5: INTRODUCTION (5.1 & 5.2)
    # =========================================================
    story.append(Paragraph("CHAPTER 5: INTRODUCTION", chapter_head))
    story.append(Paragraph("5.1 Purpose of the Project:", sec_head))
    story.append(Paragraph(
        "The Password Strength Analyzer Using Java is engineered to deliver an accessible, objective, and visually "
        "engaging desktop tool for evaluating credential resilience. In contemporary software ecosystems, authentication "
        "acts as the primary barrier defending confidential personal records, business applications, and network infrastructure. "
        "Despite repeated security recommendations, end-users frequently adopt passwords lacking sufficient complexity, "
        "leaving them vulnerable to automated brute-force attacks and dictionary matching.",
        body_style
    ))
    story.append(Paragraph(
        "The primary purpose of this project is to eliminate uncertainty by providing immediate, interactive visual feedback "
        "as credentials are typed. Built with Java Swing and AWT on Java 21 LTS, the application combines desktop GUI responsiveness "
        "with an elegant zero-dependency architecture. Rather than relying on third-party frameworks, it harnesses core Java's native "
        "windowing toolkits, static method decomposition, and character inspection routines. Designed for academic clarity, "
        "every routine is structured with clear viva-explainable logic.",
        body_style
    ))

    story.append(Paragraph("5.2 Problem Statement:", sec_head))
    story.append(Paragraph(
        "Conventional password verification tools frequently suffer from noticeable drawbacks:<br/>"
        "<b>1. Absence of Immediate Visual Feedback:</b> Many systems require full form submissions before highlighting password deficiencies, "
        "rather than providing instant keystroke guidance.<br/>"
        "<b>2. Privacy Concerns & Insecure Caching:</b> Several third-party checkers transmit input over public networks or write test data to local logs, "
        "creating substantial security exposure.<br/>"
        "<b>3. Cluttered & Inscrutable Implementations:</b> Commercial validators often depend on complex regular expressions and heavy external libraries "
        "that students cannot inspect or defend in academic viva examinations.<br/>"
        "<b>4. Insufficient Remediation Guidance:</b> Basic tools declare a generic failure state without pinpointing exactly which requirements remain unsatisfied.<br/><br/>"
        "Consequently, there is a clear demand for a lightweight, secure Java desktop GUI analyzer that delivers real-time evaluation, "
        "maintains strict in-memory privacy, and presents structured remediation advice.",
        body_style
    ))
    story.append(PageBreak()) # -> Page 7

    # =========================================================
    # PAGE 7: CHAPTER 5: INTRODUCTION (5.3 OBJECTIVES)
    # =========================================================
    story.append(Paragraph("CHAPTER 5: INTRODUCTION (Continued)", chapter_head))
    story.append(Paragraph("5.3 Objectives of the Project:", sec_head))
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
        story.append(Paragraph(f"• {o}", ParagraphStyle('ObjP', parent=body_style, leftIndent=12, spaceAfter=8)))

    story.append(PageBreak()) # -> Page 8

    # =========================================================
    # PAGE 8: CHAPTER 6: TOOLS AND TECHNOLOGY (6.1 & 6.2)
    # =========================================================
    story.append(Paragraph("CHAPTER 6: TOOLS AND TECHNOLOGY USED", chapter_head))
    story.append(Paragraph("6.1 Frontend (Java Swing & AWT Desktop GUI):", sec_head))
    story.append(Paragraph(
        "• <b>Java Swing & AWT Framework (javax.swing & java.awt):</b><br/>"
        "The graphical user interface is constructed using Java's built-in Swing and Abstract Window Toolkit (AWT). Swing provides "
        "lightweight, platform-independent GUI components rendered on top of the Java Virtual Machine. Key controls utilized include "
        "JFrame (main container), JPanel with custom anti-aliased rounded cards, JPasswordField (secure masked input), JTextField "
        "(plain-text reveal), JCheckBox (show/hide toggle), JProgressBar (visual strength meter), JButton (preset test triggers), "
        "and JTextArea (suggestions area).<br/><br/>"
        "• <b>Real-Time Event Architecture (DocumentListener):</b><br/>"
        "Implements event-driven architecture using DocumentListener to observe keystroke insertions and deletions in real time, "
        "updating scoring meters and checklist badges synchronously without requiring explicit submit buttons.",
        body_style
    ))

    story.append(Paragraph("6.2 Backend (Core Java Architecture & Analysis Engine):", sec_head))
    story.append(Paragraph(
        "• <b>Core Java (JDK 21 LTS):</b><br/>"
        "Developed strictly on Java 21 LTS without Maven, Gradle, or third-party JARs. Java provides rock-solid memory safety, "
        "strong typing, and portable cross-platform bytecode execution.<br/><br/>"
        "• <b>Character Utility Class (java.lang.Character):</b><br/>"
        "Employs highly optimized character inspection methods (Character.isUpperCase, Character.isLowerCase, Character.isDigit, "
        "Character.isLetter, and Character.isWhitespace), avoiding complex regular expressions and ensuring complete viva clarity.",
        body_style
    ))
    story.append(PageBreak()) # -> Page 9

    # =========================================================
    # PAGE 9: CHAPTER 6: TOOLS AND TECHNOLOGY (6.3, 6.4, 6.5)
    # =========================================================
    story.append(Paragraph("CHAPTER 6: TOOLS AND TECHNOLOGY USED (Continued)", chapter_head))
    story.append(Paragraph("6.3 Object-Oriented & Procedural Programming Concepts:", sec_head))
    story.append(Paragraph(
        "• <b>Modularity & Separation of Concerns:</b> Core evaluation algorithms are encapsulated into static methods separate from GUI rendering logic.<br/>"
        "• <b>Custom Component Extension:</b> Extends JPanel (RoundedPanel, ConditionRow) with custom paintComponent() and anti-aliasing hints for modern aesthetics.<br/>"
        "• <b>Clean Viva-Explainable Procedural Logic:</b> Uses indexed for-loops with password.charAt(i), allowing examiners to review logic step-by-step.",
        body_style
    ))

    story.append(Paragraph("6.4 Security, Privacy & In-Memory Design Principles:", sec_head))
    story.append(Paragraph(
        "• <b>Volatile In-Memory Lifecycle:</b> Input passwords reside solely within heap memory variables during active evaluation. "
        "When the window closes, memory is immediately garbage collected.<br/>"
        "• <b>Zero Persistence Footprint:</b> No disk logging, file serialization, or external network requests occur, safeguarding user credentials.",
        body_style
    ))

    story.append(Paragraph("6.5 Development Tools & Environment:", sec_head))
    story.append(Paragraph(
        "• <b>Visual Studio Code (VS Code):</b> Development IDE equipped with Extension Pack for Java.<br/>"
        "• <b>Java Development Kit (JDK 21.0.12.1):</b> Command-line compiler (javac) and execution runtime (java / javaw).<br/>"
        "• <b>Batch Script (run.bat):</b> One-click Windows automation script for automatic build and GUI launch.",
        body_style
    ))
    story.append(PageBreak()) # -> Page 10

    # =========================================================
    # PAGE 10: CHAPTER 7: SYSTEM DESIGN (7.1 & 7.2)
    # =========================================================
    story.append(Paragraph("CHAPTER 7: SYSTEM DESIGN", chapter_head))
    story.append(Paragraph("7.1 System Architecture (Pipeline Model):", sec_head))
    story.append(Paragraph(
        "The application follows a reactive Event-Driven Architecture paired with a Pipeline Processing Model:<br/>"
        "<b>1. GUI Input Layer:</b> Captures user keystrokes in JPasswordField or JTextField.<br/>"
        "<b>2. Event Dispatching:</b> DocumentListener triggers evaluate() on every character change.<br/>"
        "<b>3. Core Validation Engine:</b> Evaluates the password across five static methods in memory.<br/>"
        "<b>4. Dynamic Scoring & Feedback:</b> Aggregates score (0-5), updates strength bar, condition badges, and suggestions.<br/>"
        "<b>5. Clean Termination:</b> Window close event gracefully disposes frames without lingering threads.",
        body_style
    ))

    story.append(Paragraph("7.2 System Design Block Diagram:", sec_head))
    diagram_box = [
        "+-------------------------------------------------------------------------+",
        "|                    JAVA SWING DESKTOP GUI WINDOW                        |",
        "|         [ JPasswordField / JTextField  with Show/Hide Toggle ]          |",
        "+------------------------------------+------------------------------------+",
        "                                     | Real-Time DocumentListener Event",
        "                                     v",
        "+-------------------------------------------------------------------------+",
        "|                      IN-MEMORY PROCESSING STAGE                         |",
        "|                   String password (Volatile RAM)                        |",
        "+------------------------------------+------------------------------------+",
        "                                     |",
        "        +----------------------------+----------------------------+",
        "        |              |             |             |              |",
        "        v              v             v             v              v",
        "  +-----------+  +-----------+ +-----------+ +-----------+  +-----------+",
        "  |  hasMin-  |  |   has-    | |   has-    | |   has-    |  |hasSpecial-|",
        "  |  Length() |  |Uppercase()| |Lowercase()| | Number()  |  |Character()|",
        "  | (len>=8)  |  |(isUpper)  | |(isLower)  | | (isDigit) |  |(!let!num) |",
        "  +-----+-----+  +-----+-----+ +-----+-----+ +-----+-----+  +-----+-----+",
        "        |              |             |             |              |",
        "        +----------------------------+----------------------------+",
        "                                     | Boolean Results",
        "                                     v",
        "+-------------------------------------------------------------------------+",
        "|                        SCORING & STRENGTH ENGINE                        |",
        "|    Accumulates Score (0..5)  --->  getStrength() [Weak/Medium/Strong]    |",
        "+------------------------------------+------------------------------------+",
        "                                     |",
        "                                     v",
        "+-------------------------------------------------------------------------+",
        "|                    DYNAMIC GUI VIEW REFRESH                             |",
        "|   - Animated JProgressBar Color (Red / Amber / Green)                  |",
        "|   - ConditionRow Badges (Passed ✓ / Failed ○)                           |",
        "|   - Suggestions JTextArea (Instant Actionable Guidance)                 |",
        "+-------------------------------------------------------------------------+"
    ]
    diag_data = [[Paragraph(f"<pre>{'<br/>'.join(diagram_box)}</pre>", code_style)]]
    t_diag = Table(diag_data, colWidths=[504])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9FAFB")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_diag)
    story.append(PageBreak()) # -> Page 11

    # =========================================================
    # PAGE 11: CHAPTER 7: SYSTEM DESIGN (7.3 DATA FLOW)
    # =========================================================
    story.append(Paragraph("CHAPTER 7: SYSTEM DESIGN (Continued)", chapter_head))
    story.append(Paragraph("7.3 Step-by-Step Data Flow Description:", sec_head))
    flow_steps = [
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
    for fs in flow_steps:
        story.append(Paragraph(f"• {fs}", ParagraphStyle('FS', parent=body_style, leftIndent=12, spaceAfter=5)))

    story.append(PageBreak()) # -> Page 12

    # =========================================================
    # PAGE 12: CHAPTER 8: IMPLEMENTATION (8.1 & 8.2 PART 1)
    # =========================================================
    story.append(Paragraph("CHAPTER 8: IMPLEMENTATION", chapter_head))
    story.append(Paragraph("8.1 Architectural Design & Method Decomposition:", sec_head))
    story.append(Paragraph(
        "The application integrates clean OOP modularity with procedural static methods for straightforward viva presentation:<br/>"
        "• <b>hasMinLength(String password):</b> Validates length >= 8.<br/>"
        "• <b>hasUppercase(String password):</b> Scans for uppercase letters with Character.isUpperCase.<br/>"
        "• <b>hasLowercase(String password):</b> Scans for lowercase letters with Character.isLowerCase.<br/>"
        "• <b>hasNumber(String password):</b> Scans for digits with Character.isDigit.<br/>"
        "• <b>hasSpecialCharacter(String password):</b> Detects special non-alphanumeric, non-whitespace symbols.<br/>"
        "• <b>getStrength(int score):</b> Maps total score into 'Weak', 'Medium', or 'Strong'.<br/>"
        "• <b>evaluate():</b> Synchronizes the Swing GUI state with validation results in real time.",
        body_style
    ))

    story.append(Paragraph("8.2 Core Method Implementation & Code Listings (Part 1):", sec_head))
    code_lines_p1 = [
        "// Method 1: Checks minimum length (at least 8 characters)",
        "public static boolean hasMinLength(String password) {",
        "    return password != null && password.length() >= 8;",
        "}",
        "",
        "// Method 2: Checks for uppercase letter (A-Z)",
        "public static boolean hasUppercase(String password) {",
        "    if (password == null) return false;",
        "    for (int i = 0; i < password.length(); i++) {",
        "        if (Character.isUpperCase(password.charAt(i))) return true;",
        "    }",
        "    return false;",
        "}",
        "",
        "// Method 3: Checks for lowercase letter (a-z)",
        "public static boolean hasLowercase(String password) {",
        "    if (password == null) return false;",
        "    for (int i = 0; i < password.length(); i++) {",
        "        if (Character.isLowerCase(password.charAt(i))) return true;",
        "    }",
        "    return false;",
        "}"
    ]
    t_c1 = Table([[Paragraph(f"<pre>{'<br/>'.join(code_lines_p1)}</pre>", code_style)]], colWidths=[504])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_c1)
    story.append(PageBreak()) # -> Page 13

    # =========================================================
    # PAGE 13: CHAPTER 8: IMPLEMENTATION (8.2 PART 2 & 8.3)
    # =========================================================
    story.append(Paragraph("CHAPTER 8: IMPLEMENTATION (Continued)", chapter_head))
    story.append(Paragraph("8.2 Core Method Implementation & Code Listings (Part 2):", sec_head))
    code_lines_p2 = [
        "// Method 4: Checks for numeric digit (0-9)",
        "public static boolean hasNumber(String password) {",
        "    if (password == null) return false;",
        "    for (int i = 0; i < password.length(); i++) {",
        "        if (Character.isDigit(password.charAt(i))) return true;",
        "    }",
        "    return false;",
        "}",
        "",
        "// Method 5: Checks for special character",
        "public static boolean hasSpecialCharacter(String password) {",
        "    if (password == null) return false;",
        "    for (int i = 0; i < password.length(); i++) {",
        "        char c = password.charAt(i);",
        "        if (!Character.isLetter(c) && !Character.isDigit(c) && !Character.isWhitespace(c))",
        "            return true;",
        "    }",
        "    return false;",
        "}",
        "",
        "// Method 6: Strength evaluation",
        "public static String getStrength(int score) {",
        "    if (score <= 2) return \"Weak\";",
        "    else if (score <= 4) return \"Medium\";",
        "    else return \"Strong\";",
        "}"
    ]
    t_c2 = Table([[Paragraph(f"<pre>{'<br/>'.join(code_lines_p2)}</pre>", code_style)]], colWidths=[504])
    t_c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_c2)
    story.append(Spacer(1, 8))

    story.append(Paragraph("8.3 Strength Scoring & Dynamic Feedback Engine:", sec_head))
    story.append(Paragraph(
        "Inside evaluate(), the score is dynamically calculated on every keystroke. When score reaches 5, the progress bar "
        "turns vibrant green, the badge displays 'Strong', and congratulations are rendered. For scores below 5, the suggestions "
        "area lists bulleted guidance for all unsatisfied criteria, giving users immediate feedback to improve security.",
        body_style
    ))
    story.append(PageBreak()) # -> Page 14

    # =========================================================
    # PAGE 14: CHAPTER 9: OUTPUT & WORKFLOW (9.1 & 9.2)
    # =========================================================
    story.append(Paragraph("CHAPTER 9: OUTPUT & SCREEN WORKFLOW", chapter_head))
    story.append(Paragraph(
        "The following sections present the desktop GUI screens and interaction workflow across various test cases. "
        "As requested, clean bordered placeholder boxes are provided for GUI screenshot attachment.<br/>",
        body_style
    ))

    screens_p1 = [
        ("9.1 Startup and Empty State Screen:",
         "Displays the initial desktop GUI window with title badge 'Empty', score 0/5, gray progress bar, and prompt awaiting password input.",
         "[ Space for Screenshot 9.1: Desktop GUI Startup & Empty State Screen ]"),
        ("9.2 Weak Password Evaluation Screen (Input: 'abc' & 'password'):",
         "Demonstrates real-time visual response for weak credentials: red progress bar, Weak badge, failed checklist indicators, and bulleted recommendations.",
         "[ Space for Screenshot 9.2: Weak Password Desktop Screen & Suggestions ]")
    ]
    for title, desc, ph in screens_p1:
        story.append(Paragraph(title, sec_head))
        story.append(Paragraph(desc, body_style))
        t_ph = Table([[Paragraph(f"<font color='#6B7280'>{ph}</font>", ParagraphStyle('PH', parent=body_style, alignment=1))]], colWidths=[504], rowHeights=[140])
        t_ph.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9FAFB")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D1D5DB")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t_ph)
        story.append(Spacer(1, 10))

    story.append(PageBreak()) # -> Page 15

    # =========================================================
    # PAGE 15: CHAPTER 9: OUTPUT & WORKFLOW (9.3 & 9.4)
    # =========================================================
    story.append(Paragraph("CHAPTER 9: OUTPUT & SCREEN WORKFLOW (Continued)", chapter_head))
    screens_p2 = [
        ("9.3 Medium Password Evaluation Screen (Input: 'HELLO123' & 'Hello123'):",
         "Shows intermediate complexity state with amber progress bar, Medium badge, score 3 or 4, and targeted remaining suggestions.",
         "[ Space for Screenshot 9.3: Medium Password Desktop Screen ]"),
        ("9.4 Strong Password Evaluation Screen (Input: 'Hello@123'):",
         "Illustrates optimal execution with vibrant green progress bar, Strong badge, score 5/5, all 5 passed checkmarks, and celebratory success message.",
         "[ Space for Screenshot 9.4: Strong Password Desktop Screen & Success State ]")
    ]
    for title, desc, ph in screens_p2:
        story.append(Paragraph(title, sec_head))
        story.append(Paragraph(desc, body_style))
        t_ph = Table([[Paragraph(f"<font color='#6B7280'>{ph}</font>", ParagraphStyle('PH', parent=body_style, alignment=1))]], colWidths=[504], rowHeights=[140])
        t_ph.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9FAFB")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D1D5DB")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t_ph)
        story.append(Spacer(1, 10))

    story.append(PageBreak()) # -> Page 16

    # =========================================================
    # PAGE 16: WEEKLY PROGRESS REPORTS (WEEK 1 & WEEK 2)
    # =========================================================
    story.append(Paragraph("WEEKLY PROGRESS REPORTS", chapter_head))

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
        story.append(Paragraph(wt, sec_head))
        story.append(Paragraph(f"<b>Objective:</b> {wo}", body_style))
        story.append(Paragraph("<b>Work Done:</b>", body_style))
        for item in wd:
            story.append(Paragraph(f"• {item}", ParagraphStyle('WD', parent=body_style, leftIndent=12, spaceAfter=2)))
        story.append(Paragraph(f"<b>Result:</b> {wr}", body_style))
        story.append(Spacer(1, 8))

    story.append(PageBreak()) # -> Page 17

    # =========================================================
    # PAGE 17: WEEKLY PROGRESS REPORTS (WEEK 3)
    # =========================================================
    story.append(Paragraph("WEEKLY PROGRESS REPORTS (Continued)", chapter_head))
    story.append(Paragraph("WEEK 3 – Java Swing Desktop GUI Development, Testing, and Documentation", sec_head))
    story.append(Paragraph("<b>Objective:</b> To design and build the Java Swing desktop GUI, implement real-time DocumentListener keystroke listeners, configure run.bat launcher, and compile project documentation.", body_style))
    story.append(Paragraph("<b>Work Done:</b>", body_style))
    wd3_items = [
        "1. Developed modern Swing GUI with dark theme styling, anti-aliased rounded cards, and smooth borders.",
        "2. Integrated DocumentListener for real-time keystroke evaluation on both masked and plain-text fields.",
        "3. Built dynamic JProgressBar with color shifting and 5 ConditionRow checklist items.",
        "4. Implemented quick-test preset buttons ('abc', 'password', 'HELLO123', 'Hello123', 'Hello@123').",
        "5. Created one-click Windows launcher run.bat for instant execution.",
        "6. Verified 16 comprehensive test cases and generated project report."
    ]
    for item in wd3_items:
        story.append(Paragraph(f"• {item}", ParagraphStyle('WD3', parent=body_style, leftIndent=12, spaceAfter=4)))

    story.append(Paragraph("<b>Result:</b> Desktop GUI application and documentation completed with 100% test pass rate.", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Milestone Summary:</b>", sec_head))
    story.append(Paragraph(
        "Over the three-week development sprint, the Password Strength Analyzer transitioned from a core rule-based "
        "concept into a sophisticated, modern Java Swing desktop GUI microproject. The final deliverables comprise "
        "the zero-dependency source code, batch launchers, web simulator, and this comprehensive report.",
        body_style
    ))

    story.append(PageBreak()) # -> Page 18

    # =========================================================
    # PAGE 18: CHAPTER 10: TESTING AND DEBUGGING (TC01 - TC08)
    # =========================================================
    story.append(Paragraph("CHAPTER 10: TESTING AND DEBUGGING", chapter_head))
    story.append(Paragraph(
        "Comprehensive testing was conducted across individual methods and the Swing GUI desktop application using JDK 21. "
        "Test cases covered minimal strings, missing criteria combinations, mixed casing, numeric digits, and special characters. "
        "All 16 test cases executed with 100% pass rate.",
        body_style
    ))

    test_data_p1 = [
        ["Test ID", "Feature Tested", "Input", "Expected Output", "Actual Output", "Result"],
        ["TC01", "App Startup & GUI", "Launch run.bat", "Display Swing GUI window", "GUI window rendered", "Pass"],
        ["TC02", "Empty Input", "\"\"", "Score: 0 / 5, Weak, 5 suggestions", "Score: 0 / 5, Weak, 5 suggestions", "Pass"],
        ["TC03", "Single Char Lowercase", "\"a\"", "Score: 1 / 5, Weak", "Score: 1 / 5, Weak", "Pass"],
        ["TC04", "Required Input 1", "\"abc\"", "Score: 1 / 5, Weak, 4 suggestions", "Score: 1 / 5, Weak, 4 suggestions", "Pass"],
        ["TC05", "Required Input 2", "\"password\"", "Score: 2 / 5, Weak, 3 suggestions", "Score: 2 / 5, Weak, 3 suggestions", "Pass"],
        ["TC06", "Length Only (Lowercase)", "\"abcdefghij\"", "Score: 2 / 5, Weak", "Score: 2 / 5, Weak", "Pass"],
        ["TC07", "Short Upper + Lower", "\"Abc\"", "Score: 2 / 5, Weak", "Score: 2 / 5, Weak", "Pass"],
        ["TC08", "Required Input 3", "\"HELLO123\"", "Score: 3 / 5, Medium, 2 suggestions", "Score: 3 / 5, Medium, 2 suggestions", "Pass"],
    ]

    t_tc1_data = []
    for r_idx, row in enumerate(test_data_p1):
        row_cells = []
        for c_idx, val in enumerate(row):
            if r_idx == 0:
                p = Paragraph(f"<b><font color='white'>{val}</font></b>", ParagraphStyle('TH', parent=body_style, alignment=1, fontSize=8.5, leading=10))
            else:
                align = 1 if c_idx in [0, 5] else 0
                color_hex = "#059669" if c_idx == 5 else "#1F2937"
                bold = "<b>" if c_idx == 5 else ""
                end_bold = "</b>" if c_idx == 5 else ""
                p = Paragraph(f"{bold}<font color='{color_hex}'>{val}</font>{end_bold}", ParagraphStyle('TD', parent=body_style, alignment=align, fontSize=8, leading=10))
            row_cells.append(p)
        t_tc1_data.append(row_cells)

    t_tc1 = Table(t_tc1_data, colWidths=[42, 98, 76, 128, 124, 36])
    t_tc1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1F2937")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_tc1)
    story.append(PageBreak()) # -> Page 19

    # =========================================================
    # PAGE 19: CHAPTER 10: TESTING AND DEBUGGING (TC09 - TC16)
    # =========================================================
    story.append(Paragraph("CHAPTER 10: TESTING AND DEBUGGING (Continued)", chapter_head))

    test_data_p2 = [
        ["Test ID", "Feature Tested", "Input", "Expected Output", "Actual Output", "Result"],
        ["TC09", "Required Input 4", "\"Hello123\"", "Score: 4 / 5, Medium, 1 suggestion", "Score: 4 / 5, Medium, 1 suggestion", "Pass"],
        ["TC10", "Required Input 5", "\"Hello@123\"", "Score: 5 / 5, Strong, Great message", "Score: 5 / 5, Strong, Great message", "Pass"],
        ["TC11", "Special Symbol Set 1", "\"Admin#2026\"", "Score: 5 / 5, Strong", "Score: 5 / 5, Strong", "Pass"],
        ["TC12", "Special Symbol Set 2", "\"Secure$99!\"", "Score: 5 / 5, Strong", "Score: 5 / 5, Strong", "Pass"],
        ["TC13", "Whitespace Handling", "\"Hello 123\"", "Space not special, Score: 4/5", "Space not special, Score: 4/5", "Pass"],
        ["TC14", "Show/Hide Password", "Toggle checkbox", "Cards switch plain / masked", "Switched dynamically", "Pass"],
        ["TC15", "Quick Test Preset", "Click Hello@123", "Fills input & updates UI", "UI updated to Strong", "Pass"],
        ["TC16", "CLI Fallback Mode", "Run with --cli", "Executes in terminal mode", "Terminal mode executed", "Pass"]
    ]

    t_tc2_data = []
    for r_idx, row in enumerate(test_data_p2):
        row_cells = []
        for c_idx, val in enumerate(row):
            if r_idx == 0:
                p = Paragraph(f"<b><font color='white'>{val}</font></b>", ParagraphStyle('TH', parent=body_style, alignment=1, fontSize=8.5, leading=10))
            else:
                align = 1 if c_idx in [0, 5] else 0
                color_hex = "#059669" if c_idx == 5 else "#1F2937"
                bold = "<b>" if c_idx == 5 else ""
                end_bold = "</b>" if c_idx == 5 else ""
                p = Paragraph(f"{bold}<font color='{color_hex}'>{val}</font>{end_bold}", ParagraphStyle('TD', parent=body_style, alignment=align, fontSize=8, leading=10))
            row_cells.append(p)
        t_tc2_data.append(row_cells)

    t_tc2 = Table(t_tc2_data, colWidths=[42, 98, 76, 128, 124, 36])
    t_tc2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1F2937")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_tc2)
    story.append(PageBreak()) # -> Page 20

    # =========================================================
    # PAGE 20: CHAPTER 11: CONCLUSION (11.1)
    # =========================================================
    story.append(Paragraph("CHAPTER 11: CONCLUSION AND FUTURE ENHANCEMENT", chapter_head))
    story.append(Paragraph("11.1 Conclusion:", sec_head))
    story.append(Paragraph(
        "The Password Strength Analyzer Using Java was successfully conceptualized, implemented, and rigorously evaluated "
        "using Core Java and Java Swing (JDK 21 LTS). The application accomplishes all stated project objectives, demonstrating "
        "a sleek, modern desktop GUI utility that provides real-time, deterministic password strength evaluation without "
        "unnecessary external dependencies.<br/><br/>"
        "By structuring the evaluation logic into five discrete, self-contained static methods alongside event-driven Swing "
        "listeners, the codebase showcases foundational software engineering best practices including modular design, "
        "procedural character inspection, and clean viva-explainable logic. Furthermore, by enforcing strict in-memory execution, "
        "the project upholds essential cybersecurity privacy principles: no user credentials are ever stored, logged, serialized, "
        "or exposed to persistent media.<br/><br/>"
        "The project serves as an ideal microproject model for undergraduate computer science and engineering coursework, "
        "combining practical security awareness with solid desktop Java proficiency.",
        body_style
    ))
    story.append(PageBreak()) # -> Page 21

    # =========================================================
    # PAGE 21: CHAPTER 11: FUTURE ENHANCEMENTS (11.2)
    # =========================================================
    story.append(Paragraph("CHAPTER 11: CONCLUSION AND FUTURE ENHANCEMENT (Continued)", chapter_head))
    story.append(Paragraph("11.2 Future Enhancements:", sec_head))
    fut_list = [
        ("1. Shannon Entropy Mathematical Estimation: ", "Incorporate mathematical entropy calculation [H = L * log2(R)] to compute password bit-strength and exact time-to-crack estimates."),
        ("2. Common Dictionary & Compromised Credential Filter: ", "Integrate a lightweight lookup against top 1,000 common passwords (e.g. '123456', 'qwerty') to immediately flag known compromised credentials."),
        ("3. Advanced Theme Customization Engine: ", "Provide dynamic visual theme switching (Light Mode, High-Contrast Mode, Cyberpunk Dark) using customizable UI delegates."),
        ("4. Automated Password Generator: ", "Add an interactive password generator using java.security.SecureRandom to automatically construct high-entropy credentials based on user-selected criteria."),
        ("5. Clipboard Copy & Auto-Clear Timer: ", "Include a safe clipboard copy button with an automatic 30-second memory clear timer to prevent clipboard snooping."),
        ("6. Multi-Language & Internationalization (i18n): ", "Support multiple international languages and Unicode character alphabets for worldwide accessibility.")
    ]
    for ft, fd in fut_list:
        story.append(Paragraph(f"• <b>{ft}</b>{fd}", ParagraphStyle('Fut', parent=body_style, leftIndent=12, spaceAfter=8)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated 21-page PDF: {filename}")

if __name__ == "__main__":
    pdf_path = r"c:\Users\Vrund\Downloads\java_mcp\Password_Strength_Analyzer_Project_Report.pdf"
    create_pdf(pdf_path)
