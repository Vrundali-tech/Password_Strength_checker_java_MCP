# Password Strength Analyzer Using Java (Swing GUI)

A modern, beginner-friendly desktop graphical user interface (GUI) application built using **Java Swing and AWT** to analyze the strength and security of passwords in real time based on industry-standard criteria.

---

## Features

- **Modern Desktop GUI**: Designed with custom rounded cards, dark theme styling (`#0F172A`), anti-aliased graphics, and clean typography using native Java Swing & AWT.
- **Real-Time Dynamic Evaluation**: Instant keystroke listeners (`DocumentListener`) calculate and update score, strength level, and conditions as you type.
- **Show / Hide Password Toggle**: Secure masking by default with an instant reveal checkbox.
- **Visual Strength Meter**: Color-coded progress bar (Red for Weak, Amber for Medium, Green for Strong).
- **Condition Checklist**: 5 live cards indicating Passed (`✓`) or Failed (`○`) with color-coded status badges.
- **Quick Test Buttons**: One-click preset testing (`abc`, `password`, `HELLO123`, `Hello123`, `Hello@123`, and `Clear`).
- **Actionable Remediation**: Dynamic suggestions box providing specific tips when criteria fail.
- **Strict In-Memory Privacy**: The entered password is never logged, stored, written to disk, or sent over a network.
- **Dual Mode Support**: Launches modern Swing GUI by default, while retaining full terminal CLI support via `--cli` flag.

---

## Conditions Checked

The application checks five fundamental criteria:

1. **Length**: At least 8 characters.
2. **Uppercase Letter**: Contains uppercase letter (`A-Z`) via `Character.isUpperCase()`.
3. **Lowercase Letter**: Contains lowercase letter (`a-z`) via `Character.isLowerCase()`.
4. **Number**: Contains numeric digit (`0-9`) via `Character.isDigit()`.
5. **Special Character**: Contains symbol (`@`, `#`, `$`, `!`, etc.) via non-letter, non-digit, non-whitespace check.

---

## Scoring Table

| Score Range | Strength Level | Meter Color | Status Description |
| :---: | :---: | :---: | :--- |
| **0 – 2** | **Weak** | Red (`#EF4444`) | Fails multiple core criteria; vulnerable to brute-force attacks. |
| **3 – 4** | **Medium** | Amber (`#F59E0B`) | Meets several criteria; good baseline complexity. |
| **5** | **Strong** | Emerald (`#10B981`) | Meets all 5 security conditions; optimal defense. |

---

## Technologies Used

- **Java 21 LTS**
- **Java Swing & AWT** (`javax.swing.*`, `java.awt.*`) - standard built-in GUI toolkit (no external downloads needed)
- **Visual Studio Code (VS Code)** / Command-line Terminal

---

## Project Structure

```text
PasswordStrengthAnalyzer/
├── src/
│   └── PasswordStrengthAnalyzer.java
├── run.bat
└── README.md
```

---

## How to Run

### Method 1: One-Click Execution (Recommended)

Double-click the **`run.bat`** file in the project folder (or in the root folder).  
The script compiles the Java files and opens the desktop Swing GUI window immediately.

---

### Method 2: Using Visual Studio Code

1. Install **JDK 21** and the **Extension Pack for Java** in VS Code.
2. Open the `PasswordStrengthAnalyzer` folder in VS Code.
3. Open `src/PasswordStrengthAnalyzer.java`.
4. Click **Run** above the `main` method (or press `F5`).
5. The desktop GUI window will appear.

---

### Method 3: Using Terminal / Command Prompt

Navigate to the `PasswordStrengthAnalyzer` directory:

1. **Compile the source code:**
   ```bash
   javac -d out src/PasswordStrengthAnalyzer.java
   ```

2. **Launch the Desktop GUI:**
   ```bash
   java -cp out PasswordStrengthAnalyzer
   ```

3. *(Optional)* **Run in Console / Terminal Mode:**
   ```bash
   java -cp out PasswordStrengthAnalyzer --cli
   ```

---

## Note

> **Privacy & Memory Safety**:  
> The password is held strictly in volatile RAM for the duration of analysis. No data is ever saved, logged, encrypted to disk, or sent across any network.
