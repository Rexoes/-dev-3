from PyQt5.QtCore import QThread, pyqtSignal
from pso import PSO

class PSOThread(QThread):
    update_signal = pyqtSignal(str)  # Her iterasyonda mesaj göndermek için
    finished_signal = pyqtSignal(str)  # İşlem tamamlandığında mesaj göndermek için

    def __init__(self, func, dimensions, bounds, num_particles, max_iter, w_max, w_min, c1_init, c1_final, c2_init, c2_final):
        super().__init__()
        self.pso = PSO(func, dimensions, bounds, num_particles, max_iter, w_max, w_min, c1_init, c1_final, c2_init, c2_final, message_callback=self.send_message)

    def send_message(self, message):
        self.update_signal.emit(message)  # Her iterasyonda sinyal gönder

    def run(self):
        self.pso.optimize()
        final_message = f"PSO Completed\nBest Position: {self.pso.global_best_position}\nBest Score: {self.pso.global_best_score}"
        self.finished_signal.emit(final_message)
