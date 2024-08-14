from datetime import datetime
import mysql.connector
from constants import *


class Fee:

    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor(buffered=True)
        self.create_table()

    def create_table(self):
        self.cur.execute("""
              CREATE TABLE IF NOT EXISTS `WorkoutAppDB`.`Fee` (
                `idFee` INT NOT NULL AUTO_INCREMENT,
                `payeeName` VARCHAR(45) NULL,
                `amountReceived` INT NULL,
                `date` DATE NULL,
                PRIMARY KEY (`idFee`))
          """)

    def insert(self, payeeName, amountReceived, date):
        #? It's an important line of code
        formatted_date = date.strftime('%Y-%m-%d')
        print(formatted_date)
        self.cur.execute("INSERT INTO Fee (payeeName, amountReceived, date) VALUES (%s,%s,%s)",
                         [payeeName, amountReceived, formatted_date])
        self.conn.commit()

    def delete(self, _id):
        self.cur.execute("DELETE FROM Fee WHERE idFee = %s", [_id])
        self.conn.commit()

    def list_fees_by_payee(self, payeeName):
        results = self.cur.execute(
            "SELECT * FROM Fee WHERE payeeName = %s", [payeeName], multi=True)
        return results.fetchall()

    def list_fees_by_year(self, year):
        results = self.cur.execute(
            "SELECT * FROM Fee WHERE year(date) = %s ", [year])
        results =  results.fetchall()
        return results

    def list_fees_by_month(self, month):
        results = self.cur.execute(
            "SELECT * FROM Fee WHERE monthname(date) = %s ", [month])
        results =  results.fetchall()
        return results

    def list_fees(self):
        results = self.cur.execute("SELECT * FROM Fee")
        return results.fetchall()


class Workout:

    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor(buffered=True)
        self.create_table()

    def create_table(self):
        self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS `WorkoutAppDB`.`Workout` (
                    `idWorkout` INT NOT NULL AUTO_INCREMENT,
                    `name` VARCHAR(45) NULL,
                    `date` DATE NULL,
                    PRIMARY KEY (`idWorkout`))
                    ENGINE = InnoDB;
                """)

    def insert(self, name, date):
        formatted_date = date.strftime('%Y-%m-%d')
        self.cur.execute("INSERT INTO Workout (name, date) VALUES (%s,%s)",
                         [name, formatted_date])
        self.conn.commit()

    def list_workouts(self):
        self.cur.execute("SELECT * FROM Workout")
        return self.cur.fetchall()
        

    def list_workouts_by_date(self, date):
        formatted_date = date.strftime('%Y-%m-%d')
        self.cur.execute("SELECT * FROM Workout WHERE date = %s", [formatted_date])
        return self.cur.fetchall()

    def get_last_insert_id(self):
        self.cur.execute("SELECT LAST_INSERT_ID();")
        return self.cur.fetchone()


class Exercise:
    
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor(buffered=True)
        self.create_table()

    def create_table(self):
        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS `WorkoutAppDB`.`Exercise` (
                                    `idExercise` INT NOT NULL AUTO_INCREMENT,
                                    `name` VARCHAR(45) NULL,
                                    `targetMuscle` VARCHAR(45) NULL,
                                    `exerciseType` VARCHAR(45) NULL,
                                    `recommendedTime` INT NULL,
                                    `videoLink` VARCHAR(45) NULL,
                                    PRIMARY KEY (`idExercise`))
                                ENGINE = InnoDB;
                        """)

    def insert(self, name, targetMuscle, exerciseType, recommendedTime, videoLink):
        self.cur.execute("INSERT INTO Exercise (name, targetMuscle, exerciseType, recommendedTime, videoLink) \
                                VALUES (%s,%s,%s,%s,%s)", [name, targetMuscle, exerciseType, recommendedTime, videoLink])
        self.conn.commit()

        
    def list_exercises(self):        
        result = self.cur.execute("SELECT * FROM exercise")
        exercises = result.fetchall()
        return exercises

    def list_exercises_by_type(self, exercise_type):
        self.cur.execute(f"SELECT * FROM exercise WHERE exerciseType = '{exercise_type}'")
        result = self.cur.fetchall()
        if result:
            return result
        return [[]]

    def get(self, exercise_id):
        self.cur.execute(f"SELECT * FROM Exercise WHERE idExercise = '{exercise_id}'")
        result = self.cur.fetchone()
        return result


class WorkoutHasExercise:

    def __init__(self, conn):
        self.conn =  conn
        self.cur = self.conn.cursor(buffered=True)
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS `WorkoutAppDB`.`Workout_has_Exercise` (
                        `Workout_idWorkout` INT NOT NULL,
                        `Exercise_idExercise` INT NOT NULL,
                        `duration` VARCHAR(45) NULL,
                        `reps` VARCHAR(45) NULL,
                        `sets` VARCHAR(45) NULL,
                        PRIMARY KEY (`Workout_idWorkout`, `Exercise_idExercise`),
                        INDEX `fk_Workout_has_Exercise_Exercise1_idx` (`Exercise_idExercise` ASC) VISIBLE,
                        INDEX `fk_Workout_has_Exercise_Workout_idx` (`Workout_idWorkout` ASC) VISIBLE,
                        CONSTRAINT `fk_Workout_has_Exercise_Workout`
                            FOREIGN KEY (`Workout_idWorkout`)
                            REFERENCES `WorkoutAppDB`.`Workout` (`idWorkout`)
                            ON DELETE NO ACTION
                            ON UPDATE NO ACTION,
                        CONSTRAINT `fk_Workout_has_Exercise_Exercise1`
                            FOREIGN KEY (`Exercise_idExercise`)
                            REFERENCES `WorkoutAppDB`.`Exercise` (`idExercise`)
                            ON DELETE NO ACTION
                            ON UPDATE NO ACTION)
                        ENGINE = InnoDB;
                        """)

    def list_exercises_by_workout(self, workout_id):
        self.cur.execute(f"SELECT Exercise_idExercise FROM Workout_has_Exercise WHERE Workout_idWorkout = '{workout_id}'")
        exercises_ids = self.cur.fetchall()
        exercises = []

        for exercise_id in exercises_ids:
            # exercise_id i.e (1,) (2,)
            exercise = Exercise(self.conn).get(exercise_id[0])
            exercises.append(exercise)
        return exercises


    def insert(self, workout_id, exercise_id, duration, sets, reps):
        self.cur.execute(f"INSERT INTO Workout_has_Exercise (Workout_idWorkout, Exercise_idExercise, duration, sets, reps) \
                            VALUES ({workout_id}, {exercise_id}, {duration}, {sets}, {reps}) ")
        self.conn.commit()
                        

class DataBaseSimulator:
    def __init__(self) -> None:
        
        self.conn =  mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=PORT
        )

        self.create_db()

        self.fees_table = Fee(self.conn)
        self.workouts_table = Workout(self.conn)
        self.exercises_table = Exercise(self.conn)
        self.workout_has_exercise_table = WorkoutHasExercise(self.conn)

    def create_db(self):
        #? One way
        # self.cur.executemany("CREATE SCHEMA IF NOT EXISTS `WorkoutAppDB` DEFAULT CHARACTER SET utf8 ; \
        #                 USE `WorkoutAppDB` ;", [])
        #? Other way
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE SCHEMA IF NOT EXISTS `WorkoutAppDB` DEFAULT CHARACTER SET utf8 ;")
        self.cur.execute("USE `WorkoutAppDB` ;")



def main():
    pass

if __name__ == '__main__':
    main()
