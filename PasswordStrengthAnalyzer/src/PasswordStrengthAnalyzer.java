import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Scanner;

/**
 * College Microproject: Password Strength Analyzer Using Java
 * 
 * An interactive, beginner-friendly desktop GUI application built using
 * Java Swing and AWT (built-in standard Java libraries) to evaluate password
 * strength in real-time according to standard security criteria.
 * 
 * Privacy Assurance: The password is processed strictly in-memory during execution
 * and is NEVER saved, stored, logged, or written to any file or database.
 */
public class PasswordStrengthAnalyzer extends JFrame {

    // -------------------------------------------------------------
    // Core Static Logic Methods (Viva-Friendly Core Java)
    // -------------------------------------------------------------

    // Checks if the password has at least 8 characters
    public static boolean hasMinLength(String password) {
        return password != null && password.length() >= 8;
    }

    // Checks if the password contains at least one uppercase letter (A-Z)
    public static boolean hasUppercase(String password) {
        if (password == null) return false;
        for (int i = 0; i < password.length(); i++) {
            if (Character.isUpperCase(password.charAt(i))) {
                return true;
            }
        }
        return false;
    }

    // Checks if the password contains at least one lowercase letter (a-z)
    public static boolean hasLowercase(String password) {
        if (password == null) return false;
        for (int i = 0; i < password.length(); i++) {
            if (Character.isLowerCase(password.charAt(i))) {
                return true;
            }
        }
        return false;
    }

    // Checks if the password contains at least one numeric digit (0-9)
    public static boolean hasNumber(String password) {
        if (password == null) return false;
        for (int i = 0; i < password.length(); i++) {
            if (Character.isDigit(password.charAt(i))) {
                return true;
            }
        }
        return false;
    }

    // Checks if the password contains at least one special character
    // A special character is not a letter, not a digit, and not whitespace
    public static boolean hasSpecialCharacter(String password) {
        if (password == null) return false;
        for (int i = 0; i < password.length(); i++) {
            char c = password.charAt(i);
            if (!Character.isLetter(c) && !Character.isDigit(c) && !Character.isWhitespace(c)) {
                return true;
            }
        }
        return false;
    }

    // Converts a boolean condition result into a readable "Passed" or "Failed" string
    public static String result(boolean passed) {
        return passed ? "Passed" : "Failed";
    }

    // Determines the overall password strength based on the total score (0 to 5)
    public static String getStrength(int score) {
        if (score <= 2) {
            return "Weak";
        } else if (score <= 4) {
            return "Medium";
        } else {
            return "Strong";
        }
    }

    // -------------------------------------------------------------
    // Swing GUI Components & Palette
    // -------------------------------------------------------------
    private static final Color BG_DARK = new Color(15, 23, 42);       // #0F172A
    private static final Color CARD_BG = new Color(30, 41, 59);       // #1E293B
    private static final Color BORDER_COLOR = new Color(51, 65, 85);  // #334155
    private static final Color TEXT_MAIN = new Color(248, 250, 252);  // #F8FAFC
    private static final Color TEXT_MUTED = new Color(148, 163, 184); // #94A3B8
    private static final Color ACCENT_BLUE = new Color(56, 189, 248); // #38BDF8
    private static final Color COLOR_WEAK = new Color(239, 68, 68);   // #EF4444
    private static final Color COLOR_MED = new Color(245, 158, 11);   // #F59E0B
    private static final Color COLOR_STRONG = new Color(16, 185, 129);// #10B981

    private JPasswordField passwordField;
    private JTextField plainTextField;
    private JCheckBox showPasswordCheckbox;
    private JProgressBar strengthBar;
    private JLabel scoreLabel;
    private JLabel strengthBadge;
    private ConditionRow[] conditionRows;
    private JTextArea suggestionsArea;

    // Custom Rounded Panel for sleek modern card UI
    static class RoundedPanel extends JPanel {
        private final int radius;
        private final Color bgColor;
        private final Color borderColor;

        public RoundedPanel(int radius, Color bgColor, Color borderColor) {
            this.radius = radius;
            this.bgColor = bgColor;
            this.borderColor = borderColor;
            setOpaque(false);
        }

        @Override
        protected void paintComponent(Graphics g) {
            Graphics2D g2 = (Graphics2D) g.create();
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g2.setColor(bgColor);
            g2.fillRoundRect(0, 0, getWidth() - 1, getHeight() - 1, radius, radius);
            if (borderColor != null) {
                g2.setColor(borderColor);
                g2.setStroke(new BasicStroke(1.2f));
                g2.drawRoundRect(0, 0, getWidth() - 1, getHeight() - 1, radius, radius);
            }
            g2.dispose();
            super.paintComponent(g);
        }
    }

    // Condition Item Row in the Checklist
    static class ConditionRow extends JPanel {
        private final JLabel iconLabel;
        private final JLabel nameLabel;
        private final JLabel statusLabel;

        public ConditionRow(String text) {
            setLayout(new BorderLayout(8, 0));
            setOpaque(false);
            setBorder(new EmptyBorder(6, 10, 6, 10));

            iconLabel = new JLabel("○");
            iconLabel.setFont(new Font("Segoe UI", Font.BOLD, 14));
            iconLabel.setForeground(TEXT_MUTED);

            nameLabel = new JLabel(text);
            nameLabel.setFont(new Font("Segoe UI", Font.PLAIN, 13));
            nameLabel.setForeground(TEXT_MAIN);

            statusLabel = new JLabel("Failed");
            statusLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
            statusLabel.setForeground(TEXT_MUTED);

            JPanel left = new JPanel(new FlowLayout(FlowLayout.LEFT, 8, 0));
            left.setOpaque(false);
            left.add(iconLabel);
            left.add(nameLabel);

            add(left, BorderLayout.WEST);
            add(statusLabel, BorderLayout.EAST);
        }

        public void setPassed(boolean passed) {
            if (passed) {
                iconLabel.setText("✓");
                iconLabel.setForeground(COLOR_STRONG);
                statusLabel.setText("Passed");
                statusLabel.setForeground(COLOR_STRONG);
            } else {
                iconLabel.setText("○");
                iconLabel.setForeground(TEXT_MUTED);
                statusLabel.setText("Failed");
                statusLabel.setForeground(TEXT_MUTED);
            }
        }
    }

    // Constructor: Builds the Java Swing UI Window
    public PasswordStrengthAnalyzer() {
        setTitle("Password Strength Analyzer - Core Java");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(650, 780);
        setMinimumSize(new Dimension(580, 700));
        setLocationRelativeTo(null);
        getContentPane().setBackground(BG_DARK);

        initUI();
    }

    private void initUI() {
        JPanel rootPanel = new JPanel();
        rootPanel.setLayout(new BoxLayout(rootPanel, BoxLayout.Y_AXIS));
        rootPanel.setOpaque(false);
        rootPanel.setBorder(new EmptyBorder(20, 24, 20, 24));

        // 1. Header Panel
        RoundedPanel headerPanel = new RoundedPanel(16, CARD_BG, BORDER_COLOR);
        headerPanel.setLayout(new BorderLayout(12, 0));
        headerPanel.setBorder(new EmptyBorder(12, 16, 12, 16));
        headerPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 64));

        JLabel titleLabel = new JLabel("🛡️  Password Strength Analyzer");
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 18));
        titleLabel.setForeground(TEXT_MAIN);

        JLabel subtitleLabel = new JLabel("Core Java 21 • In-Memory Privacy");
        subtitleLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        subtitleLabel.setForeground(TEXT_MUTED);

        JPanel headerText = new JPanel();
        headerText.setLayout(new BoxLayout(headerText, BoxLayout.Y_AXIS));
        headerText.setOpaque(false);
        headerText.add(titleLabel);
        headerText.add(subtitleLabel);

        strengthBadge = new JLabel("Empty");
        strengthBadge.setFont(new Font("Segoe UI", Font.BOLD, 12));
        strengthBadge.setForeground(TEXT_MUTED);
        strengthBadge.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(BORDER_COLOR, 1, true),
            new EmptyBorder(4, 10, 4, 10)
        ));

        headerPanel.add(headerText, BorderLayout.WEST);
        headerPanel.add(strengthBadge, BorderLayout.EAST);
        rootPanel.add(headerPanel);
        rootPanel.add(Box.createVerticalStrut(16));

        // 2. Input Box Panel
        RoundedPanel inputPanel = new RoundedPanel(16, CARD_BG, BORDER_COLOR);
        inputPanel.setLayout(new BoxLayout(inputPanel, BoxLayout.Y_AXIS));
        inputPanel.setBorder(new EmptyBorder(14, 16, 14, 16));
        inputPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 130));

        JPanel labelRow = new JPanel(new BorderLayout());
        labelRow.setOpaque(false);
        JLabel inputTitle = new JLabel("Enter a password:");
        inputTitle.setFont(new Font("Segoe UI", Font.BOLD, 13));
        inputTitle.setForeground(TEXT_MUTED);

        scoreLabel = new JLabel("Score: 0 / 5");
        scoreLabel.setFont(new Font("Segoe UI", Font.BOLD, 13));
        scoreLabel.setForeground(TEXT_MAIN);

        labelRow.add(inputTitle, BorderLayout.WEST);
        labelRow.add(scoreLabel, BorderLayout.EAST);
        inputPanel.add(labelRow);
        inputPanel.add(Box.createVerticalStrut(8));

        // Input field with card stack (password or plain text)
        JPanel inputStack = new JPanel(new CardLayout());
        inputStack.setOpaque(false);

        passwordField = new JPasswordField();
        passwordField.setFont(new Font("Consolas", Font.PLAIN, 15));
        passwordField.setBackground(new Color(11, 17, 32));
        passwordField.setForeground(TEXT_MAIN);
        passwordField.setCaretColor(ACCENT_BLUE);
        passwordField.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(BORDER_COLOR, 1, true),
            new EmptyBorder(8, 10, 8, 10)
        ));

        plainTextField = new JTextField();
        plainTextField.setFont(new Font("Consolas", Font.PLAIN, 15));
        plainTextField.setBackground(new Color(11, 17, 32));
        plainTextField.setForeground(TEXT_MAIN);
        plainTextField.setCaretColor(ACCENT_BLUE);
        plainTextField.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(BORDER_COLOR, 1, true),
            new EmptyBorder(8, 10, 8, 10)
        ));

        inputStack.add(passwordField, "PASSWORD");
        inputStack.add(plainTextField, "PLAIN");
        inputPanel.add(inputStack);
        inputPanel.add(Box.createVerticalStrut(6));

        JPanel toggleRow = new JPanel(new FlowLayout(FlowLayout.RIGHT, 0, 0));
        toggleRow.setOpaque(false);
        showPasswordCheckbox = new JCheckBox("Show Password");
        showPasswordCheckbox.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        showPasswordCheckbox.setForeground(TEXT_MUTED);
        showPasswordCheckbox.setOpaque(false);
        showPasswordCheckbox.setFocusPainted(false);
        showPasswordCheckbox.addActionListener(e -> {
            CardLayout cl = (CardLayout) inputStack.getLayout();
            if (showPasswordCheckbox.isSelected()) {
                plainTextField.setText(new String(passwordField.getPassword()));
                cl.show(inputStack, "PLAIN");
                plainTextField.requestFocus();
            } else {
                passwordField.setText(plainTextField.getText());
                cl.show(inputStack, "PASSWORD");
                passwordField.requestFocus();
            }
        });
        toggleRow.add(showPasswordCheckbox);
        inputPanel.add(toggleRow);

        rootPanel.add(inputPanel);
        rootPanel.add(Box.createVerticalStrut(14));

        // 3. Strength Progress Meter
        JPanel meterPanel = new JPanel();
        meterPanel.setLayout(new BoxLayout(meterPanel, BoxLayout.Y_AXIS));
        meterPanel.setOpaque(false);
        meterPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 40));

        strengthBar = new JProgressBar(0, 5);
        strengthBar.setValue(0);
        strengthBar.setPreferredSize(new Dimension(100, 10));
        strengthBar.setForeground(Color.GRAY);
        strengthBar.setBackground(new Color(11, 17, 32));
        strengthBar.setBorder(BorderFactory.createLineBorder(BORDER_COLOR, 1, true));

        JPanel meterLabels = new JPanel(new BorderLayout());
        meterLabels.setOpaque(false);
        JLabel l0 = new JLabel("0");
        JLabel lWeak = new JLabel("Weak (1-2)");
        JLabel lMed = new JLabel("Medium (3-4)");
        JLabel lStr = new JLabel("Strong (5)");

        for (JLabel l : new JLabel[]{l0, lWeak, lMed, lStr}) {
            l.setFont(new Font("Segoe UI", Font.PLAIN, 11));
            l.setForeground(TEXT_MUTED);
        }

        meterLabels.add(l0, BorderLayout.WEST);
        JPanel midLabels = new JPanel(new FlowLayout(FlowLayout.CENTER, 40, 0));
        midLabels.setOpaque(false);
        midLabels.add(lWeak);
        midLabels.add(lMed);
        meterLabels.add(midLabels, BorderLayout.CENTER);
        meterLabels.add(lStr, BorderLayout.EAST);

        meterPanel.add(strengthBar);
        meterPanel.add(Box.createVerticalStrut(4));
        meterPanel.add(meterLabels);

        rootPanel.add(meterPanel);
        rootPanel.add(Box.createVerticalStrut(14));

        // 4. Quick Sample Test Buttons
        JPanel presetsPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 6, 0));
        presetsPanel.setOpaque(false);
        presetsPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 36));

        JLabel presetLabel = new JLabel("Quick Tests:");
        presetLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        presetLabel.setForeground(TEXT_MUTED);
        presetsPanel.add(presetLabel);

        String[] samplePresets = {"abc", "password", "HELLO123", "Hello123", "Hello@123"};
        for (String sample : samplePresets) {
            JButton btn = new JButton(sample);
            btn.setFont(new Font("Consolas", Font.PLAIN, 11));
            btn.setBackground(CARD_BG);
            btn.setForeground(sample.equals("Hello@123") ? ACCENT_BLUE : TEXT_MAIN);
            btn.setFocusPainted(false);
            btn.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(BORDER_COLOR, 1, true),
                new EmptyBorder(3, 8, 3, 8)
            ));
            btn.addActionListener(e -> setPasswordValue(sample));
            presetsPanel.add(btn);
        }

        JButton clearBtn = new JButton("Clear");
        clearBtn.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        clearBtn.setBackground(new Color(239, 68, 68, 40));
        clearBtn.setForeground(COLOR_WEAK);
        clearBtn.setFocusPainted(false);
        clearBtn.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(239, 68, 68, 80), 1, true),
            new EmptyBorder(3, 8, 3, 8)
        ));
        clearBtn.addActionListener(e -> setPasswordValue(""));
        presetsPanel.add(clearBtn);

        rootPanel.add(presetsPanel);
        rootPanel.add(Box.createVerticalStrut(14));

        // 5. Conditions Checklist Panel
        RoundedPanel condPanel = new RoundedPanel(16, CARD_BG, BORDER_COLOR);
        condPanel.setLayout(new BoxLayout(condPanel, BoxLayout.Y_AXIS));
        condPanel.setBorder(new EmptyBorder(10, 12, 10, 12));
        condPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 190));

        conditionRows = new ConditionRow[]{
            new ConditionRow("1. At least 8 characters"),
            new ConditionRow("2. Uppercase letter (A-Z)"),
            new ConditionRow("3. Lowercase letter (a-z)"),
            new ConditionRow("4. Number (0-9)"),
            new ConditionRow("5. Special character (e.g. @, #, $, !)")
        };

        for (ConditionRow row : conditionRows) {
            condPanel.add(row);
        }
        rootPanel.add(condPanel);
        rootPanel.add(Box.createVerticalStrut(14));

        // 6. Dynamic Suggestions & Remediation Panel
        RoundedPanel sugPanel = new RoundedPanel(16, CARD_BG, BORDER_COLOR);
        sugPanel.setLayout(new BorderLayout(0, 6));
        sugPanel.setBorder(new EmptyBorder(12, 14, 12, 14));

        JLabel sugTitle = new JLabel("SUGGESTIONS & FEEDBACK");
        sugTitle.setFont(new Font("Segoe UI", Font.BOLD, 12));
        sugTitle.setForeground(TEXT_MUTED);
        sugPanel.add(sugTitle, BorderLayout.NORTH);

        suggestionsArea = new JTextArea("Enter a password above to begin analysis.");
        suggestionsArea.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        suggestionsArea.setForeground(TEXT_MUTED);
        suggestionsArea.setOpaque(false);
        suggestionsArea.setEditable(false);
        suggestionsArea.setLineWrap(true);
        suggestionsArea.setWrapStyleWord(true);
        sugPanel.add(suggestionsArea, BorderLayout.CENTER);

        rootPanel.add(sugPanel);

        add(rootPanel);

        // Document Listeners for real-time keystroke evaluation
        DocumentListener listener = new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) { evaluate(); }
            @Override
            public void removeUpdate(DocumentEvent e) { evaluate(); }
            @Override
            public void changedUpdate(DocumentEvent e) { evaluate(); }
        };

        passwordField.getDocument().addDocumentListener(listener);
        plainTextField.getDocument().addDocumentListener(listener);

        evaluate();
    }

    private void setPasswordValue(String val) {
        passwordField.setText(val);
        plainTextField.setText(val);
        evaluate();
    }

    private String getCurrentPassword() {
        if (showPasswordCheckbox.isSelected()) {
            return plainTextField.getText();
        } else {
            return new String(passwordField.getPassword());
        }
    }

    // Evaluates the current password and dynamically refreshes the Swing UI
    private void evaluate() {
        String pwd = getCurrentPassword();

        if (pwd.isEmpty()) {
            strengthBar.setValue(0);
            strengthBar.setForeground(Color.GRAY);
            scoreLabel.setText("Score: 0 / 5");
            strengthBadge.setText("Empty");
            strengthBadge.setForeground(TEXT_MUTED);
            for (ConditionRow row : conditionRows) {
                row.setPassed(false);
            }
            suggestionsArea.setForeground(TEXT_MUTED);
            suggestionsArea.setText("Enter a password above to begin analysis.");
            return;
        }

        boolean c1 = hasMinLength(pwd);
        boolean c2 = hasUppercase(pwd);
        boolean c3 = hasLowercase(pwd);
        boolean c4 = hasNumber(pwd);
        boolean c5 = hasSpecialCharacter(pwd);

        conditionRows[0].setPassed(c1);
        conditionRows[1].setPassed(c2);
        conditionRows[2].setPassed(c3);
        conditionRows[3].setPassed(c4);
        conditionRows[4].setPassed(c5);

        int score = 0;
        if (c1) score++;
        if (c2) score++;
        if (c3) score++;
        if (c4) score++;
        if (c5) score++;

        String strength = getStrength(score);
        strengthBar.setValue(score);
        scoreLabel.setText("Score: " + score + " / 5");
        strengthBadge.setText(strength);

        if (strength.equals("Weak")) {
            strengthBar.setForeground(COLOR_WEAK);
            strengthBadge.setForeground(COLOR_WEAK);
        } else if (strength.equals("Medium")) {
            strengthBar.setForeground(COLOR_MED);
            strengthBadge.setForeground(COLOR_MED);
        } else {
            strengthBar.setForeground(COLOR_STRONG);
            strengthBadge.setForeground(COLOR_STRONG);
        }

        if (score == 5) {
            suggestionsArea.setForeground(COLOR_STRONG);
            suggestionsArea.setText("🎉 Great! Your password meets all the requirements.");
        } else {
            suggestionsArea.setForeground(TEXT_MUTED);
            StringBuilder sb = new StringBuilder();
            if (!c1) sb.append("• Use at least 8 characters.\n");
            if (!c2) sb.append("• Add at least one uppercase letter (A-Z).\n");
            if (!c3) sb.append("• Add at least one lowercase letter (a-z).\n");
            if (!c4) sb.append("• Add at least one number (0-9).\n");
            if (!c5) sb.append("• Add at least one special character (e.g. @, #, $, !).\n");
            suggestionsArea.setText(sb.toString().trim());
        }
    }

    // -------------------------------------------------------------
    // Console Fallback Routine
    // -------------------------------------------------------------
    public static void runConsoleMode(Scanner scanner) {
        System.out.println("===== Password Strength Analyzer =====");
        System.out.print("Enter a password: ");
        String password = scanner.nextLine();

        boolean minLength = hasMinLength(password);
        boolean uppercase = hasUppercase(password);
        boolean lowercase = hasLowercase(password);
        boolean number = hasNumber(password);
        boolean specialChar = hasSpecialCharacter(password);

        int score = 0;
        if (minLength) score++;
        if (uppercase) score++;
        if (lowercase) score++;
        if (number) score++;
        if (specialChar) score++;

        System.out.println("\n----- Condition Results -----");
        System.out.println("1. At least 8 characters : " + result(minLength));
        System.out.println("2. Uppercase letter      : " + result(uppercase));
        System.out.println("3. Lowercase letter      : " + result(lowercase));
        System.out.println("4. Number                : " + result(number));
        System.out.println("5. Special character     : " + result(specialChar));

        System.out.println("\nScore    : " + score + " / 5");
        System.out.println("Strength : " + getStrength(score));

        if (score == 5) {
            System.out.println("\nGreat! Your password meets all the requirements.");
        } else {
            System.out.println("\n----- Suggestions -----");
            if (!minLength) {
                System.out.println("- Use at least 8 characters.");
            }
            if (!uppercase) {
                System.out.println("- Add at least one uppercase letter (A-Z).");
            }
            if (!lowercase) {
                System.out.println("- Add at least one lowercase letter (a-z).");
            }
            if (!number) {
                System.out.println("- Add at least one number (0-9).");
            }
            if (!specialChar) {
                System.out.println("- Add at least one special character (e.g. @, #, $, !).");
            }
        }
    }

    // Main Method: Launches modern Swing GUI by default, or Console mode if specified
    public static void main(String[] args) {
        boolean cliMode = (args.length > 0 && (args[0].equalsIgnoreCase("--cli") || args[0].equalsIgnoreCase("-c")))
                          || GraphicsEnvironment.isHeadless();

        if (cliMode) {
            Scanner scanner = new Scanner(System.in);
            runConsoleMode(scanner);
            scanner.close();
        } else {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception ignored) {}

            SwingUtilities.invokeLater(() -> {
                PasswordStrengthAnalyzer app = new PasswordStrengthAnalyzer();
                app.setVisible(true);
            });
        }
    }
}
