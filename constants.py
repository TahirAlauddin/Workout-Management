from datetime import datetime

FRAME_STYLE_SHEET = """QPushButton {\n
background: #C0E2F5;\n
border: none;\n
border-top: 1px solid black;\n
padding: 5px;\n
font: 70 8pt \"Segoe UI Black\";\n
color: #5F5F5F;\n
}\n
QFrame {\n
border: 1px solid black;\n
}"""

MENU_GROUP_BUTTONS = """
QPushButton {
background: transparent;
border: none;
border-top: 1px solid black;
padding: 5px;
font: 70 8pt "Segoe UI Black";
color: #5F5F5F;
}
QFrame {
border: 1px solid black;
}
"""


STACKED_WIDGET_STYLE_SHEET = """QPushButton { \n
background: #EADFF2;\n
border: 1px solid #8A6FA6;\n
padding-left: 10px;\n
padding-right: 10px;\n
padding-top: 15px;\n
padding-bottom: 15px;\n
border-radius: 10px;\n
font: 75 10pt \"MS Shell Dlg 2\";\n
}\n
\n"""

PAGE_STYLE_SHEET = """QWidget {\n
background: #C0E2F5;\n
border-left: 4px solid #3098F2;\n
}\n
QPushButton {\n
background: #EADFF2;\n
border: 1px solid #8A6FA6;\n
}\n"""

STACKED_WIDGET_STYLE_SHEET2 = """QLabel { 
background: #EADFF2;
border: 1px solid #8A6FA6;
padding-left: 10px;
padding-right: 10px;
padding-top: 15px;
padding-bottom: 15px;
border-radius: 10px;
font: 75 10pt "MS Shell Dlg 2";
}"""

STACKED_WIDGET_STYLE_SHEET3 = """QLabel { 
background: #EADFF2;
border: 1px solid #8A6FA6;
padding-left: 20px;
padding-right: 20px;
padding-top: 25px;
padding-bottom: 25px;
border-radius: 10px;
font: 75 10pt "MS Shell Dlg 2";
}"""


VIEW_EXERCISES_DUMMY_DATA = [
    ["Exercise 1 Group1", "Exercise 2 Group1", "Exercise 3 Group1", "Exercise 4 Group1"],
    
    ["Exercise 1 Group2", "Exercise 2 Group2", "Exercise 3 Group2", "Exercise 4 Group2",
        "Exercise 5 Group2", "Exercise 6 Group2", "Exercise 7 Group2", "Exercise 8 Group2"],
    
    ["Exercise 1 Group3", "Exercise 2 Group3", "Exercise 3 Group3", "Exercise 4 Group3",
    "Exercise 10 Group3"],

    ["Exercise 1 Group4", "Exercise 2 Group4", "Exercise 3 Group4"],
]

MUSCLE_GROUPS = ["Bicep", "Tricep", "Chest", "Abs"]
EXERCISE_TYPES = ["Easy", "Intermediate", "Hard"]

MONTHS = [datetime.strptime(f"{i}", "%m").strftime("%B") for i in range(1,12+1)]
YEARS = [str(i) for i in range(2000, datetime.now().year+1)]
DAYS = [str(i) for i in range(1, 31+1)]

#? DATABASE CONSTANTS
HOST = "localhost"
USER = "root"
PASSWORD = "29mid"
PORT = '3306'

