from PyQt5.QtWidgets import QLabel

class WorkoutLabel(QLabel):
    duration = None
    reps = None
    sets = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_duration(self, duration):   self.duration = duration
    def set_sets(self, sets):           self.sets = sets
    def set_reps(self, reps):           self.reps = reps

    def get_duration(self):         return self.duration
    def get_reps(self):             return self.reps
    def get_sets(self):             return self.sets
    