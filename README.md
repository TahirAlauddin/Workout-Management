# Workout Management System

A comprehensive PyQt5-based desktop application for managing workouts, exercises, and gym fees. This system provides an intuitive interface for users to create, track, and analyze their fitness routines.

## Features

- **Workout Creation**: Design custom workouts with specific exercises, sets, and reps
- **Exercise Catalog**: Browse and manage a diverse catalog of exercises
- **Fee Management**: Track and manage gym membership fees
- **Workout History**: View and analyze previous workout sessions
- **Calendar Integration**: Schedule workouts and track progress over time
- **Drag-and-Drop Interface**: Easily build workouts using a drag-and-drop system
- **Exercise Details**: View detailed information about each exercise, including recommended duration and video links

## Technical Overview

This application is built using PyQt5 and incorporates various advanced programming concepts:

1. **Object-Oriented Programming (OOP)**:
   - Extensive use of classes for different windows and functionalities
   - Inheritance in UI components and custom widgets

2. **Event-Driven Programming**:
   - Utilizes Qt's signal-slot mechanism for handling user interactions

3. **Model-View-Controller (MVC) Pattern**:
   - Separation of data (model), user interface (view), and business logic (controller)

4. **Database Integration**:
   - Simulated database operations for storing and retrieving workout data

5. **GUI Programming**:
   - Complex UI design using PyQt5 widgets and layouts

6. **Date and Time Manipulation**:
   - Custom date handling for scheduling and tracking workouts

7. **Custom Widgets**:
   - Implementation of custom Qt widgets like WorkoutLabel

8. **Drag and Drop Functionality**:
   - Custom implementation of drag-and-drop for exercise management

9. **State Management**:
   - Handling of application state across different windows and views

10. **Data Validation and Error Handling**:
    - Input validation and error messaging in various forms

11. **Dynamic UI Generation**:
    - Runtime creation and modification of UI elements

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/TahirAlauddin/Workout-Management.git
   ```
2. Install required dependencies:
   ```
   pip install PyQt5
   ```
3. Run the main application:
   ```
   python main.py
   ```

## Main Components

- `HomeWindow`: The main dashboard of the application
- `WorkoutWindow`: For creating and managing workouts
- `ExerciseWindow`: Displays details of individual exercises
- `FeeManagementWindow`: For managing gym membership fees
- `CatalogOfExercisesWindow`: Browse and manage the exercise catalog
- `ViewPreviousWorkoutsWindow`: Review past workout sessions

## Contributing

Contributions to improve the Workout Management System are welcome. Please feel free to fork the repository and submit pull requests.
