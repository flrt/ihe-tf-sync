import darkdetect

ICONS = { "files": ":/img/files.svg"}

icon_fill = "black"
if darkdetect.isDark():
    ICONS["files"] = ":/img/files_darker.svg"

STYLES = {"Windows": """
QWidget   { font-family:'Segoe UI';font-size:9pt; }
QLineEdit { font-family:font-family:'Segoe UI';font-size:9pt; }
QTextEdit { font-family:font-family:'Segoe UI';font-size:9pt; }
""",
          "Darwin": """
QWidget   { font-family:'Lucida Grande';font-size:12pt; }
QLineEdit { font-family:"Menlo";font-size:12pt; }
QTextEdit { font-family:"Menlo";font-size:12pt; }
QLabel#modifed_label { color: red; }
""",
          "Linux": """
QWidget   { font-family:'Lucida Grande';font-size:9pt; }
QLineEdit { font-family:"Menlo";font-size:9pt; }
QTextEdit { font-family:"Menlo";font-size:9pt; }"""}

