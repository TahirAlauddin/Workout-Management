from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from constants import *
from datetime import datetime
import datetime as datetime_module


class MyButton(QPushButton):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            print('press')
        elif event.button() == Qt.RightButton:
            # save the click position to keep it consistent when dragging
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.RightButton:
            return
        mimeData = QMimeData()
        # create a byte array and a stream that is used to write into
        byteArray = QByteArray()
        stream = QDataStream(byteArray, QIODevice.WriteOnly)
        # set the objectName and click position to keep track of the widget
        # that we're moving and it's click position to ensure that it will
        # be moved accordingly
        stream.writeQString(self.objectName())
        stream.writeQVariant(self.mousePos)
        # create a custom mimeData format to save the drag info
        mimeData.setData('myApp/QtWidget', byteArray)
        drag = QDrag(self)
        # add a pixmap of the widget to show what's actually moving
        drag.setPixmap(self.grab())
        drag.setMimeData(mimeData)
        # set the hotspot according to the mouse press position
        # drag.setHotSpot(self.mousePos - self.rect().topLeft())
        drag.setHotSpot(self.mousePos)
        drag.exec_()



def Ui_components_CreateNewWorkoutWindow(window):


    #? /////////////////////////
    #? Destroy static desgin
    window.ui.stackedWidget.close()
    window.ui.frame_2.close()
    window.ui.frame_6.close()
    window.ui.frame_7.close()
    #? /////////////////////////


    #? ////////////////////////////////////////////
    #? Dynamic Exercise Labels    DATA PREPARATION
    list_exercises = []
    for exercise_type in EXERCISE_TYPES:
        # exercise = [(1,'pushup', 'chest', 'easy', 10, 'https://link'), (3, 'abc', ...)]
        exercise = window.db.exercises_table.list_exercises_by_type(exercise_type)
        print(exercise)
        # exercise = [char for char in exercise[0]]
        list_exercises.append(exercise)
    
    #? /////////////////////////
    window.ui.stackedWidget = QStackedWidget(window.ui.frame_3)
    window.ui.stackedWidget.setStyleSheet(
        STACKED_WIDGET_STYLE_SHEET
    )

    #? /////////////////////////
    #? Group/Category Navigator Frame
    group_frame = QFrame(window.ui.frame_3)
    group_frame.setStyleSheet(
        FRAME_STYLE_SHEET
    )
    group_frame.setFrameShape(QFrame.StyledPanel)
    group_frame.setFrameShadow(QFrame.Raised)
    
    window.groups_verticalLayout = QVBoxLayout(group_frame)
    window.groups_verticalLayout.setContentsMargins(0, 0, 0, 0)
    window.groups_verticalLayout.setSpacing(0)
    #? /////////////////////////
    

    #? ////////////////////////////////
    #? Workout Workspace Frame
    workout_frame = QFrame(window.ui.frame_5)
    workout_frame.setFrameShape(QFrame.StyledPanel)
    workout_frame.setFrameShadow(QFrame.Raised)
    workout_outer_vertical_layout = QVBoxLayout(workout_frame)
    window.workout_scrollArea = QScrollArea(workout_frame)
    window.workout_scrollArea.setWidgetResizable(True)
    workout_scrollAreaWidgetContents = QWidget()
    workout_scrollAreaWidgetContents.setGeometry(QRect(0, 0, 384, 361))
    window.workout_inner_vertical_layout = QVBoxLayout(workout_scrollAreaWidgetContents)
    window.workout_inner_vertical_layout.setSpacing(30)
    
    window.workout_scrollArea.setWidget(workout_scrollAreaWidgetContents)
    window.workout_scrollArea.setWidgetResizable(True)
    workout_outer_vertical_layout.addWidget(window.workout_scrollArea)
    window.ui.horizontalLayout_4.addWidget(workout_frame)

    #! self.workout_frame can be used in CreateNewWorkoutWindow -> main.py
    window.workout_frame = workout_frame
    #? /////////////////////////////////////////////////


    #? ///////////////////////////////
    #? CREATE and DELETE workout Frame
    frame_7 = QFrame(window.ui.frame_5)
    frame_7.setFrameShape(QFrame.StyledPanel)
    frame_7.setFrameShadow(QFrame.Raised)
    verticalLayout_5 = QVBoxLayout(frame_7)
    spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    verticalLayout_5.addItem(spacerItem)
    window.create_button = QPushButton(frame_7)
    window.create_button.setText("Create \nWorkout")
    window.create_button.setMinimumSize(QSize(90, 0))
    verticalLayout_5.addWidget(window.create_button)
    window.delete_button = QPushButton(frame_7)
    window.delete_button.setText("Delete \nWorkout")
    window.delete_button.setMinimumSize(QSize(90, 0))
    verticalLayout_5.addWidget(window.delete_button)
    window.ui.horizontalLayout_4.setStretch(0, 3)
    window.ui.horizontalLayout_4.addWidget(frame_7)
    window.ui.horizontalLayout_4.setStretch(1, 1)
    window.create_button.setObjectName("create_button")
    window.delete_button.setObjectName("delete_button")

    window.ui.create_new_exercise_button.clicked.connect(window.create_new_exercise)
    window.create_button.clicked.connect(window.create_workout)
    # window.ui.create_button.setStyleSheet("QPushButton::pressed {background: black;}")
    # window.ui.delete_button.clicked.connect(window.delete_workout)

    #? /////////////////////////////////////////////
        
    for idx, group in enumerate(EXERCISE_TYPES):
        page = QWidget()
        page.setStyleSheet(
            PAGE_STYLE_SHEET
        )
        vertical_layout = QVBoxLayout(page)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.setSpacing(0)
        scrollArea = QScrollArea(page)
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        scrollAreaWidgetContents = QWidget()
        scrollAreaWidgetContents.setGeometry(QRect(0, 0, 166, 363))

        exercise_layout = QVBoxLayout(scrollAreaWidgetContents)
        exercise_layout.setContentsMargins(20, -1, 20, -1)
        exercise_layout.setSpacing(50)

        #? Old version with buttons and less data
        # for j, exercise in enumerate(list_exercises[idx]):
        #     exercise_button = MyButton(scrollAreaWidgetContents)
        #     exercise_button.setMinimumSize(QSize(0, 0))
        #     exercise_button.setFlat(False)
        #     exercise_layout.addWidget(exercise_button)
        #     exercise_button.setText(exercise)
        #     exercise_button.setObjectName(f"exercise_button_{idx}_{j}")

            
        for j, exercise in enumerate(list_exercises):
            if exercise:
                exercise = exercise[0]
            name, category, *_ = exercise
            text = f"{name}\n({category})"
            label = QPushButton(scrollAreaWidgetContents)
            # label.setAlignment(Qt.AlignCenter)
            label.setText(text)
            # label.setWordWrap(True)
            label.setMaximumWidth(150)
            label.setMaximumHeight(150)
            label.setFlat(False)
            exercise_layout.addWidget(label)

            label.mousePressEvent = lambda event, exercise=exercise: window.open_individual_exercise_window(event, exercise)


        scrollArea.setWidget(scrollAreaWidgetContents)
        vertical_layout.addWidget(scrollArea)
        window.ui.stackedWidget.addWidget(page)

        #? Add a group button as well
        group_button = QPushButton(group_frame)
        group_button.setObjectName(f"group_button_{idx}")
        group_button.setText(group)
        window.groups_verticalLayout.addWidget(group_button)
        #? button click event
        group_button.clicked.connect(lambda _, button=group_button: window.select_group(button))
        

    spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    window.groups_verticalLayout.addItem(spacerItem)
    window.ui.gridLayout_3.addWidget(group_frame, 0, 0, 2, 1)            
    window.ui.gridLayout_3.addWidget(window.ui.stackedWidget, 0, 1, 1, 1)


def Ui_components_HomeWindow(window):
    window.ui.workout_button.clicked.connect(window.goto_workout_window)
    window.ui.fee_management_button.clicked.connect(window.goto_fee_management_window)


def Ui_components_ExerciseWindow(window):
    _id, exercise_name, target_muscle, exercise_type, recommended_time, video_link = window.exercise
     
    window.ui.exercise_name_label.setText(str(exercise_name))
    window.ui.target_muscle_label.setText(str(target_muscle))
    window.ui.exercise_type_label.setText(str(exercise_type))
    window.ui.recommended_time_label.setText(str(recommended_time))
    window.ui.video_link_label.setText(str(video_link))

    window.ui.close_button.clicked.connect(lambda: window.close())


def Ui_components_CreateExerciseForWorkoutWindow(window):
       
    #? On Toggle Event for radioButton
    window.ui.duration_radioButton.toggled.connect(window.enable_duration)
    window.ui.reps_sets_radioButton.toggled.connect(window.enable_reps_sets)

    window.ui.duration_radioButton.toggle()
    window.ui.ok_button.clicked.connect(lambda: create_exercise(window))
    window.ui.cancel_button.clicked.connect(lambda: window.close())


def Ui_components_UpdateExerciseForWorkoutWindow(window):
    window.ui.duration_radioButton.toggled.connect(window.enable_duration)
    window.ui.reps_sets_radioButton.toggled.connect(window.enable_reps_sets)

    if window.duration:
        window.ui.duration_radioButton.toggle()
    else:
        window.ui.reps_sets_radioButton.toggle()
    window.ui.ok_button.clicked.connect(lambda: update_exercise(window))
    window.ui.cancel_button.clicked.connect(lambda: window.close())

    #? Set Text function must be called after `toggle`
    #? because of enable and disable
    window.ui.input_reps.setText(window.reps or '')
    window.ui.input_sets.setText(window.sets or '')
    window.ui.input_duration.setText(window.duration or '')



def Ui_components_DatabaseFeePaymentWindow(window):    

    window.ui.year_comboBox.addItems(YEARS)
    window.ui.month_comboBox.addItems(MONTHS)

    window.ui.year_comboBox.currentTextChanged.connect(lambda text: window.render_data_in_table(text))
    window.ui.month_comboBox.currentTextChanged.connect(lambda text: window.render_data_in_table(text))


def Ui_components_WorkoutWindow(window):

    window.ui.create_new_workout_button.clicked.connect(window.goto_create_workout_window)
    window.ui.view_previous_workout_button.clicked.connect(window.goto_previous_workouts_window)
    window.ui.view_catalog_of_exercises_button.clicked.connect(window.goto_catalog_of_exercises_window)


def Ui_components_CreateNewExerciseWindow(window):
    
    window.ui.input_exercise_name
    window.ui.input_recommended_duration
    window.ui.input_reference_video_link

    window.ui.muscle_groups_combobox.addItems(MUSCLE_GROUPS)
    window.ui.categories_exercises_combobox.addItems(EXERCISE_TYPES)
    
    window.ui.create_exercise_button.clicked.connect(window.create_exercise)
    
    

def Ui_components_CatalogOfExercisesWindow(window):    
    window.ui.create_exercise_button.clicked.connect(window.goto_create_exercise_button)
    window.ui.view_exercises_button.clicked.connect(window.goto_view_exercises_button)


def Ui_components_ViewAllExercisesWindow(window):
    #? ////////////////////////////////////////////
    #? Group Navigation Buttons
    window.resize(900,400)
    

    #? DELETE Static group_frame to create Dynamic one later    
    window.ui.group_frame.close()

    #? CREATE group_frame 
    window.group_frame = QFrame(window.ui.outer_group_frame)
    window.group_frame.setStyleSheet(
        MENU_GROUP_BUTTONS
    )
    window.group_frame.setFrameShape(QFrame.StyledPanel)
    window.group_frame.setFrameShadow(QFrame.Raised)
    window.verticalLayout_inner_group = QVBoxLayout(window.group_frame)
    window.verticalLayout_inner_group.setContentsMargins(0, 0, 0, 0)
    window.verticalLayout_inner_group.setSpacing(0)   

    window.ui.verticalLayout_outer_group.addWidget(window.group_frame) 

    #? Adding menu group buttons
    for idx, group in enumerate(EXERCISE_TYPES):
        group_button = QPushButton(window.group_frame)
        group_button.setText(group)
        group_button.setObjectName(f"group_button_{idx}")
        window.verticalLayout_inner_group.addWidget(group_button)

        group_button.clicked.connect(lambda _, button=group_button: window.switch_groups_stacked_widget(button))
    
    spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    window.verticalLayout_inner_group.addItem(spacerItem)
    #? ////////////////////////////////////////////


    #? ////////////////////////////////////////////
    #? Delete old StackedWidget
    window.ui.stackedWidget.close()
    window.stackedWidget = QStackedWidget(window.ui.stackedWidget_frame)
    window.stackedWidget.setStyleSheet(
        STACKED_WIDGET_STYLE_SHEET3
    )
    window.ui.horizontalLayout_3.addWidget(window.stackedWidget)


    #? ////////////////////////////////////////////
    #? Dynamic Exercise Labels
    list_exercises = []
    for exercise_type in EXERCISE_TYPES:
        # exercise = [(1,'pushup', 'chest', 'easy', 10, 'https://link'), (3, 'abc', ...)]
        exercise = window.db.exercises_table.list_exercises_by_type(exercise_type)
        list_exercises.append(exercise)
    

    for exercises in list_exercises:
        page = QWidget()
        
        verticalLayout = QVBoxLayout(page)
        scrollArea = QScrollArea(page)
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        
        scrollAreaWidgetContents = QWidget()
        gridLayout = QGridLayout(scrollAreaWidgetContents)
        gridLayout.setContentsMargins(20, 10, 20, 10)
        gridLayout.setHorizontalSpacing(50)
        gridLayout.setVerticalSpacing(20)

        for j, exercise in enumerate(exercises):
            name, category, *_ = exercise
            text = f"{name}\n({category})"
            label = QLabel(scrollAreaWidgetContents)
            label.setAlignment(Qt.AlignCenter)
            label.setText(text)
            label.setWordWrap(True)
            label.setMaximumWidth(150)
            label.setMaximumHeight(150)

            label.mousePressEvent = lambda event, exercise=exercise: window.open_individual_exercise_window(event, exercise)

            if j % 2 == 0:
                column = 0
            else:
                column = 1
            row = j // 2

            gridLayout.addWidget(label, row, column, 1, 1)
        scrollArea.setWidget(scrollAreaWidgetContents)
        verticalLayout.addWidget(scrollArea)
        window.stackedWidget.addWidget(page)
    #? ////////////////////////////////////////////
    


def Ui_components_ViewPreviousWorkoutsWindow(window):

    window.ui.year_comboBox.addItems(YEARS)
    window.ui.month_comboBox.addItems(MONTHS)
    window.ui.day_comboBox.addItems(DAYS)

    window.ui.year_comboBox.currentTextChanged.connect(lambda text: window.render_data_in_table(text))
    window.ui.month_comboBox.currentTextChanged.connect(lambda text: window.render_data_in_table(text))
    window.ui.day_comboBox.currentTextChanged.connect(lambda text: window.render_data_in_table(text))



def Ui_components_AddFeeWindow(window):
    window.date: datetime = None
    window.ui.open_calendar_button.clicked.connect(window.open_calendar_window)
    window.ui.add_fees_button.clicked.connect(window.add_fees)


def Ui_components_CalendarWindow(window):
    window.ui.selectButton.clicked.connect(window.get_selected_date)
    

def Ui_components_CreateWorkoutWindow(window):
    window.ui.open_calendar_button.clicked.connect(window.open_calendar_window)
    window.ui.create_button.clicked.connect(window.create_workout_window)
    window.ui.cancel_button.clicked.connect(window.cancel_workout_window)



def Ui_components_FeeManagementWindow(window):
    
    income = "$500"
    window.ui.monthly_income_label.setText(income)
    window.ui.database_fee_payment_button.clicked.connect(window.goto_view_database_fee_payment_window)
    window.ui.add_fees_button.clicked.connect(window.goto_add_fees_window)



def drop_exercise_into_workspace(window, event):

    cf = window.workout_frame
    wf_position = cf.pos()

    while True:
        if not cf.parent():
            break
        # Don't include the position of MainWindow relative to screen
        if isinstance(cf.parent(), QMainWindow):
            break
        cf = cf.parent()
        wf_position += cf.pos()

    position = event.pos()

    wf_position_bottom_right_x = wf_position.x() + window.workout_frame.width()
    wf_position_bottom_right_y = wf_position.y() + window.workout_frame.height()

    #? Drop only with the workspace boundary
    if position.x() > wf_position.x() and position.y() > wf_position.y():
        if position.x() < wf_position_bottom_right_x \
            and position.y() < wf_position_bottom_right_y:
            #? Open Duration Or Reps/Sets Window
             window.open_create_exercise_for_workout_window()

def qdate_to_python_date(qdate):
    date = datetime_module.date(qdate.year, qdate.month, qdate.day)
    return date


def create_exercise(window):
    input_duration = window.ui.input_duration
    input_reps = window.ui.input_reps
    input_sets = window.ui.input_sets
    input_duration.setStyleSheet("")
    input_sets.setStyleSheet("")
    input_reps.setStyleSheet("")
    duration = input_duration.text()
    reps = input_reps.text()
    sets = input_sets.text()
    
    returnable = False
    if window.ui.reps_sets_radioButton.isChecked():
        
        if not reps:
            input_reps.setStyleSheet("border: 1px solid red;")
            returnable = True
        if not sets:
            input_sets.setStyleSheet("border: 1px solid red;")
            returnable = True
    else:
        
        if not duration:
            input_duration.setStyleSheet("border: 1px solid red;")
            returnable = True
    if returnable:
        return
    window.close()

    #? Copy the exercise material to workspace
    window.mainWindow.copy_exercise_to_workspace(duration, reps, sets)
    #? /////////////////////////////////////////


def update_exercise(window):
    input_duration = window.ui.input_duration
    input_reps = window.ui.input_reps
    input_sets = window.ui.input_sets
    input_duration.setStyleSheet("")
    input_sets.setStyleSheet("")
    input_reps.setStyleSheet("")
    duration = input_duration.text()
    reps = input_reps.text()
    sets = input_sets.text()
    
    returnable = False
    if window.ui.reps_sets_radioButton.isChecked():
        
        if not reps:
            input_reps.setStyleSheet("border: 1px solid red;")
            returnable = True
        if not sets:
            input_sets.setStyleSheet("border: 1px solid red;")
            returnable = True
    else:
        
        if not duration:
            input_duration.setStyleSheet("border: 1px solid red;")
            returnable = True
    if returnable:
        return
    window.close()

    #? Copy the exercise material to workspace
    window.update_exercise_in_workspace(duration, reps, sets)
    #? /////////////////////////////////////////

def month_name_to_int(month_name):
    datetime_object = datetime.strptime(month_name, "%B")
    return datetime_object.month
