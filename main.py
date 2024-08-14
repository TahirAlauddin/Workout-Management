import enum
from turtle import pos
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# Builtin modules
from datetime import datetime
import datetime as datetime_module
from custom_classes import WorkoutLabel
# Packages
from interface import *
from interface import view_all_exercises
# Modules
from utils import *
from modules.db import *


class CreateNewWorkoutWindow(QMainWindow):
    
    def __init__(self, name, date):
        QMainWindow.__init__(self)
        self.name, self.date = name, date
        self.reps, self.sets, self.duration = None, None, None
        self.db = DataBaseSimulator()
        self.ui = Ui_CreateNewWorkoutWindow()
        self.ui.setupUi(self)

        self.workout_inner_vertical_layout:QVBoxLayout = None
        self.workout_frame:QFrame = None
        self.setAcceptDrops(True)

        #? Setup dynamic UI (User Interface) 
        Ui_components_CreateNewWorkoutWindow(self)
        self.show()

        exercises = []
        for category in EXERCISE_TYPES:
            result = self.db.exercises_table.list_exercises_by_type(category)
            exercises.append(result)


    def dragEnterEvent(self, event):
        # only accept our mimeData format, ignoring any other data content
        if event.mimeData().hasFormat('myApp/QtWidget'):
            event.accept()

    def dropEvent(self, event):
        stream = QDataStream(event.mimeData().data('myApp/QtWidget'))
        # QDataStream objects should be read in the same order as they were written
        objectName = stream.readQString()
        # find the child widget that has the objectName set within the drag event
        self.widget = self.findChild(QWidget, objectName)
        print(self.widget)
        if not self.widget:
            return
        drop_exercise_into_workspace(self, event)


    def open_create_exercise_for_workout_window(self):
        global x
        x = CreateExerciseForWorkoutWindow(self)
    

    def open_update_exercise_for_workout_window(self, event, label):
        global x
        x = UpdateExerciseForWorkoutWindow(self, label)


    def copy_exercise_to_workspace(self, duration, reps, sets):
        text = self.widget.text()
        text += '\n(Click to change the properties)'
        label = WorkoutLabel(text, self.workout_frame)
        label.set_duration(duration)
        label.set_reps(reps)
        label.set_sets(sets)
        #? Sizing policy for Labels
        label.setAlignment(Qt.AlignCenter)
        label.setMaximumHeight(100)
        label.setMinimumHeight(80)
        label.setMaximumWidth(200)
        label.setMinimumWidth(100)
        label.setWordWrap(True)

        label.mouseDoubleClickEvent = lambda event, label=label: self.open_update_exercise_for_workout_window(event, label)

        self.workout_inner_vertical_layout.addWidget(label)
        self.workout_inner_vertical_layout.setAlignment(label, Qt.AlignHCenter)


    def select_group(self, group_button:QPushButton):
        groups = ["Group1", "Group2", "Group3"]
        #? ObjectName is named after the number of index for each Group Button
        index = group_button.objectName().split("_")[-1]
        self.ui.stackedWidget.setCurrentIndex(int(index))

        for idx in range(len(groups)):
            objectName = f"group_button_{idx}"
            button = self.findChild(QPushButton, objectName)
            button.setStyleSheet("")
        group_button.setStyleSheet("background: #3098F2;\n"
            "color: white;")

    def create_workout(self):
        children = self.workout_scrollArea.findChildren(QLabel)
        for child in children:
            exercise_name = child.text().split('\n')[0]
            duration = child.get_duration()
            reps = child.get_reps()
            sets = child.get_sets()
            if duration:
                pass
            else:
                pass

        #TODO: figure out a way to get workout_id and exercise_id
        self.db.workouts_table.insert(self.name, self.date)
        workout_id = self.db.workouts_table.get_last_insert_id()[0]
        self.db.workout_has_exercise_table.insert(workout_id, exercise_id, duration, sets, reps)


    def create_new_exercise(self):
        global x
        x = CreateNewExerciseWindow()

class HomeWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        
        self.ui = Ui_HomeWindow()
        self.ui.setupUi(self)
        Ui_components_HomeWindow(self)
        self.show()

    def goto_workout_window(self):
        global x
        x = WorkoutWindow()
        # self.close()

    def goto_fee_management_window(self):
        global x
        x = FeeManagementWindow()
        # self.close()



class FeeManagementWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        
        self.ui = Ui_FeeManagementWindow()
        self.ui.setupUi(self)
        self.show()
        Ui_components_FeeManagementWindow(self)

    def goto_view_database_fee_payment_window(self):
        global x
        x = DatabaseFeePaymentWindow()

    def goto_add_fees_window(self):
        global x
        x = AddFeeWindow()

    
class AddFeeWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        
        self.ui = Ui_AddFeeWindow()
        self.db = DataBaseSimulator()
        self.ui.setupUi(self)
        Ui_components_AddFeeWindow(self)
        self.show()


    def open_calendar_window(self):
        global x
        x = CalendarWindow(self)

    def add_fees(self):
        #TODO: save Name, amount and date in the database
        name = self.ui.input_name.text()
        amount = self.ui.input_amount.text()
        try:
            self.db.fees_table.insert(name, amount, self.date)
        except:
            self.ui.open_calendar_button.setText("Please choose a date")
            self.ui.open_calendar_button.setStyleSheet("background: red;")


class WorkoutWindow(QMainWindow):
  
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.ui = Ui_WorkoutWindow()
        self.ui.setupUi(self)

        #? Setup dynamic UI (User Interface) 
        Ui_components_WorkoutWindow(self)

        self.show()

    
    def goto_create_workout_window(self):
        global x
        x = CreateWorkoutWindow()
        self.close()

    def goto_catalog_of_exercises_window(self):
        global x
        x = CatalogOfExercisesWindow()
        self.close()

    def goto_previous_workouts_window(self):
        global x
        x = ViewPreviousWorkoutsWindow()
        self.close()


class ExerciseWindow(QMainWindow):
  
    def __init__(self, exercise):
        QMainWindow.__init__(self)
        self.exercise = exercise
        self.ui = Ui_ExerciseWindow()
        self.ui.setupUi(self)

        #? Setup dynamic UI (User Interface) 
        Ui_components_ExerciseWindow(self)

        self.show()




class CreateExerciseForWorkoutWindow(QMainWindow):
  
    def __init__(self, mainWindow):
        QMainWindow.__init__(self)


        self.mainWindow = mainWindow
        self.ui = Ui_CreateExerciseForWorkoutWindow()
        self.ui.setupUi(self)

        #? Setup dynamic UI (User Interface) 
        Ui_components_CreateExerciseForWorkoutWindow(self)
        self.show()


    def enable_reps_sets(self):
        self.disable_duration()
        self.ui.input_reps.setEnabled(True)
        self.ui.input_sets.setEnabled(True)

    def enable_duration(self):
        self.disable_reps_sets()
        self.ui.input_duration.setEnabled(True)


    def disable_reps_sets(self):
        self.ui.input_reps.setDisabled(True)
        self.ui.input_sets.setDisabled(True)

    def disable_duration(self):
        self.ui.input_duration.setDisabled(True)



class UpdateExerciseForWorkoutWindow(QMainWindow):
  
    def __init__(self, mainWindow, label):
        QMainWindow.__init__(self)

        self.label = label
        self.duration, self.reps, self.sets = label.get_duration(), label.get_reps(), label.get_sets()

        self.mainWindow = mainWindow
        self.ui = Ui_CreateExerciseForWorkoutWindow()
        self.ui.setupUi(self)

        #? Setup dynamic UI (User Interface) 
        Ui_components_UpdateExerciseForWorkoutWindow(self)
        self.show()


    def update_exercise_in_workspace(self, duration, reps, sets):
        self.label.set_duration(duration)
        self.label.set_reps(reps)
        self.label.set_sets(sets)
    

    def enable_reps_sets(self):
        self.disable_duration()
        self.ui.input_reps.setEnabled(True)
        self.ui.input_sets.setEnabled(True)

    def enable_duration(self):
        self.disable_reps_sets()
        self.ui.input_duration.setEnabled(True)


    def disable_reps_sets(self):
        self.ui.input_reps.setText("")
        self.ui.input_sets.setText("")
        self.ui.input_reps.setDisabled(True)
        self.ui.input_sets.setDisabled(True)


    def disable_duration(self):
        self.ui.input_duration.setText("")
        self.ui.input_duration.setDisabled(True)



class CreateNewExerciseWindow(QMainWindow):
  
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.db = DataBaseSimulator()
        self.ui = Ui_CreateNewExerciseWindow()
        self.ui.setupUi(self)

        #? Setup dynamic UI (User Interface) 
        Ui_components_CreateNewExerciseWindow(self)

        self.show()

    def create_exercise(self):
        exercise_name = self.ui.input_exercise_name.text()
        recommended_duration = self.ui.input_recommended_duration.text()
        reference_video_link = self.ui.input_reference_video_link.text()
        muscle_groups = self.ui.muscle_groups_combobox.currentText()
        categories_exercises = self.ui.categories_exercises_combobox.currentText()

        self.db.exercises_table.insert(exercise_name, muscle_groups, categories_exercises, recommended_duration, reference_video_link)


class CatalogOfExercisesWindow(QMainWindow):
  
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.ui = Ui_CatalogOfExercisesWindow()
        self.ui.setupUi(self)

        #? Setup dynamic UI (User Interface) 
        Ui_components_CatalogOfExercisesWindow(self)
        self.show()

    def goto_create_exercise_button(self):
        global x
        x = CreateNewExerciseWindow()
        self.close()

    def goto_view_exercises_button(self):
        global x
        x = ViewAllExercisesWindow()
        self.close()


class DatabaseFeePaymentWindow(QMainWindow):
  
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.ui = Ui_DatabaseFeePaymentWindow()
        self.ui.setupUi(self)

        #? Setup dynamic UI (User Interface) 
        Ui_components_DatabaseFeePaymentWindow(self)

        self.show()


    def render_data_in_table(self, text):
        print(text)
        # Name, Amount
        # John, 100
        # Alice, 50
        data = [
            ["John", "100"],
            ["Alice", "50"],
        ]
        
        # UI Changes
        header = self.ui.tableWidget.horizontalHeader()       
        
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
    
        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(column))


class ViewAllExercisesWindow(QMainWindow):
  
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.db = DataBaseSimulator()
        self.ui = Ui_ViewAllExercisesWindow()
        self.ui.setupUi(self)

        #? Setup dynamic UI (User Interface) 
        Ui_components_ViewAllExercisesWindow(self)
        self.show()


    def switch_groups_stacked_widget(self, button):
        old_object_name = button.objectName()
        idx = old_object_name.split('_')[-1]
        self.stackedWidget.setCurrentIndex(int(idx))
        
        #? ///////////////////////////////////////////
        #? (DELETE) old group_frame and create new one again
        self.group_frame.close()

        self.group_frame = QFrame(self.ui.outer_group_frame)
        self.group_frame.setStyleSheet(
            MENU_GROUP_BUTTONS
        )
        self.group_frame.setFrameShape(QFrame.StyledPanel)
        self.group_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_inner_group = QVBoxLayout(self.group_frame)
        self.verticalLayout_inner_group.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_inner_group.setSpacing(0)   

        self.ui.verticalLayout_outer_group.addWidget(self.group_frame) 

        #? ////////////////////////////////////////////
        #? Group Navigation Buttons (CREATE)
        for idx, group in enumerate(EXERCISE_TYPES):
            new_object_name = f"group_button_{idx}"
            group_button = QPushButton(self.group_frame)
            group_button.setText(group)
            group_button.setObjectName(new_object_name)
            if old_object_name == new_object_name:
                group_button.setStyleSheet("background: #3098F2;\n"
                            "color: white;")

            self.verticalLayout_inner_group.addWidget(group_button)
            
            if button.text() == group_button.text():
                spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                self.verticalLayout_inner_group.addItem(spacerItem)
                
            group_button.clicked.connect(lambda _, button=group_button: self.switch_groups_stacked_widget(button))
        
        #? ////////////////////////////////////////////

    def open_individual_exercise_window(self, event, exercise):
        global x
        x = ExerciseWindow(exercise)
        #? ////////////////////////////////////////////
        

class ViewPreviousWorkoutsWindow(QMainWindow):
  
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.db = DataBaseSimulator()
        self.ui = Ui_ViewPreviousWorkoutsWindow()
        self.ui.setupUi(self)

        #? Setup dynamic UI (User Interface) 
        Ui_components_ViewPreviousWorkoutsWindow(self)

        self.show()


    def render_data_in_table(self, text):
        # Name, Duration
        # John, 100
        # Alice, 50
        day = self.ui.day_comboBox.currentText()
        month = month_name_to_int(self.ui.month_comboBox.currentText())
        year = self.ui.year_comboBox.currentText()
        date = datetime_module.date(int(year), int(month), int(day))

        data = self.db.workouts_table.list_workouts_by_date(date)

        workouts = []

        for workout in data:
            workout_id = workout[0]
            exercises = self.db.workout_has_exercise_table.list_exercises_by_workout(workout_id)
            workouts.append([workout[1], exercises])
        
        # UI Changes
        header = self.ui.tableWidget.horizontalHeader()       
        
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.ui.tableWidget.setRowCount(1)
    
        for i, row in enumerate(workouts):
            for j, column in enumerate(row):
                if j == 1:
                    text = ""
                    #? All exercises of a workout
                    for exercise in column:
                        text += f"{exercise[1]},"
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(text[:-1]))
                else:
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(column))
            self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount() + 1)

    
class CalendarWindow(QMainWindow):
    def __init__(self, mainWindow):
        QMainWindow.__init__(self)
        self.mainWindow = mainWindow
        self.ui = Ui_CalendarWindow()
        self.ui.setupUi(self)

        Ui_components_CalendarWindow(self)
        self.show()

    def get_selected_date(self):
        # QDate(2022, 9, 25)
        date = self.ui.calendarWidget.selectedDate()
        # datetime.date(2022, 9, 25)
        date = datetime_module.date(date.year(), date.month(), date.day())
        self.mainWindow.date = date
        self.close()


class CreateWorkoutWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_CreateWorkoutWindow()
        self.ui.setupUi(self)
        self.date = None

        Ui_components_CreateWorkoutWindow(self)
        self.show()


    def open_calendar_window(self):
        global x
        x = CalendarWindow(self)

    def create_workout_window(self):
        if not self.date:
            self.ui.open_calendar_button.setText("Please choose a date")
            self.ui.open_calendar_button.setStyleSheet("background: red;")
            return
        date = qdate_to_python_date(self.date)
        x = CreateNewWorkoutWindow(
            self.ui.input_name.text(),
            self.date
            )


        self.close()

    def cancel_workout_window(self):
        global x
        x = HomeWindow()
        self.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # x = HomeWindow()  
    # x = AddFeeWindow()
    x = CreateNewWorkoutWindow("ABC", datetime_module.date(2022, 10, 1))
    # x = ViewAllExercisesWindow()
    # x = FeeManagementWindow()
    # x = ViewPreviousWorkoutsWindow()

    sys.exit(app.exec_())

