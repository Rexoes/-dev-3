import sys

from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox, \
    QDoubleSpinBox, QHBoxLayout, QMessageBox, QSizePolicy, QGroupBox, QFormLayout, QTextEdit
# from functions import rastrigin, ackley, sphere, rosenbrock, bounds_dict
from pso import PSO
from functions import *
from pso_thread import PSOThread

class PSOApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.animation_path = 'combined_animation.gif'

    def initUI(self):
        main_layout = QVBoxLayout()

        # Fonksiyon Seçimi Grubu
        function_group = QGroupBox("Test Function")
        function_layout = QFormLayout()
        self.functionBox = QComboBox()

        # Fonksiyonları hem isim hem de veri olarak ekleyelim
        function_dict = {
            "Rastrigin": rastrigin,
            "Ackley": ackley,
            "Sphere": sphere,
            "Rosenbrock": rosenbrock,
            "Griewank": griewank,
            "Schaffer N.2": schaffer_n2,
            "Beale": beale,
            "Levi N.13": levi_n13,
            "Easom": easom,
            "Michalewicz": michalewicz,
            "Booth": booth,
            "Himmelblau": himmelblau
        }
        for name, func in function_dict.items():
            self.functionBox.addItem(name, func)  # Hem isim hem de fonksiyon nesnesini ekleyin

        function_layout.addRow("Fonksiyon Seç:", self.functionBox)
        function_group.setLayout(function_layout)

        # main_layout.addWidget(function_group)

        # PSO Parametre Grubu
        param_group = QGroupBox("PSO Kontrol Parametreleri")
        param_layout = QVBoxLayout()

        # Parçacık Sayısı ve Maksimum İterasyon Grubu (Yatay Düzen)
        general_group = QGroupBox("Genel Parametreler")
        general_layout = QHBoxLayout()

        self.particleSpinBox = QSpinBox()
        self.particleSpinBox.setRange(10, 100)
        self.particleSpinBox.setValue(30)
        self.particleSpinBox.setSingleStep(5)
        general_layout.addWidget(QLabel("Parçacık Sayısı:"))
        general_layout.addWidget(self.particleSpinBox)

        self.iterationSpinBox = QSpinBox()
        self.iterationSpinBox.setRange(10, 1000)
        self.iterationSpinBox.setValue(50)
        self.iterationSpinBox.setSingleStep(5)
        general_layout.addWidget(QLabel("Maksimum İterasyon:"))
        general_layout.addWidget(self.iterationSpinBox)
        general_group.setLayout(general_layout)

        # Adaptif W Parametreleri Grubu
        w_group = QGroupBox("Atalet Katsayısı (W)")
        w_layout = QHBoxLayout()
        self.wMinSpinBox = QDoubleSpinBox()
        self.wMinSpinBox.setRange(0.0, 1.0)
        self.wMinSpinBox.setValue(0.4)
        self.wMinSpinBox.setSingleStep(0.1)
        w_layout.addWidget(QLabel("W Min:"))
        w_layout.addWidget(self.wMinSpinBox)

        self.wMaxSpinBox = QDoubleSpinBox()
        self.wMaxSpinBox.setRange(0.0, 1.0)
        self.wMaxSpinBox.setValue(0.9)
        self.wMaxSpinBox.setSingleStep(0.1)
        w_layout.addWidget(QLabel("W Max:"))
        w_layout.addWidget(self.wMaxSpinBox)
        w_group.setLayout(w_layout)

        # Adaptif C1 Parametreleri Grubu
        c1_group = QGroupBox("Bilişsel Katsayı (C1)")
        c1_layout = QHBoxLayout()
        self.c1InitSpinBox = QDoubleSpinBox()
        self.c1InitSpinBox.setRange(0.0, 5.0)
        self.c1InitSpinBox.setValue(2.5)
        self.c1InitSpinBox.setSingleStep(0.1)
        c1_layout.addWidget(QLabel("C1 Initial:"))
        c1_layout.addWidget(self.c1InitSpinBox)

        self.c1FinalSpinBox = QDoubleSpinBox()
        self.c1FinalSpinBox.setRange(0.0, 5.0)
        self.c1FinalSpinBox.setValue(0.5)
        self.c1FinalSpinBox.setSingleStep(0.1)
        c1_layout.addWidget(QLabel("C1 Final:"))
        c1_layout.addWidget(self.c1FinalSpinBox)
        c1_group.setLayout(c1_layout)

        # Adaptif C2 Parametreleri Grubu
        c2_group = QGroupBox("Sosyal Katsayı (C2)")
        c2_layout = QHBoxLayout()
        self.c2InitSpinBox = QDoubleSpinBox()
        self.c2InitSpinBox.setRange(0.0, 5.0)
        self.c2InitSpinBox.setValue(0.5)
        self.c2InitSpinBox.setSingleStep(0.1)
        c2_layout.addWidget(QLabel("C2 Initial:"))
        c2_layout.addWidget(self.c2InitSpinBox)

        self.c2FinalSpinBox = QDoubleSpinBox()
        self.c2FinalSpinBox.setRange(0.0, 5.0)
        self.c2FinalSpinBox.setValue(2.5)
        self.c2FinalSpinBox.setSingleStep(0.1)
        c2_layout.addWidget(QLabel("C2 Final:"))
        c2_layout.addWidget(self.c2FinalSpinBox)
        c2_group.setLayout(c2_layout)

        # Hepsini Yatay Olarak Tek Bir Satıra Ekleyelim
        param_horizontal_layout = QHBoxLayout()
        param_horizontal_layout.addWidget(function_group)  # Parçacık ve iterasyon grubu
        param_horizontal_layout.addWidget(general_group)  # Parçacık ve iterasyon grubu
        param_horizontal_layout.addWidget(w_group)  # W parametreleri
        param_horizontal_layout.addWidget(c1_group)  # C1 parametreleri
        param_horizontal_layout.addWidget(c2_group)  # C2 parametreleri

        param_layout.addLayout(param_horizontal_layout)
        param_group.setLayout(param_layout)

        # Ana layout'a ekle
        main_layout.addWidget(param_group)

        # Görsel Alanı Grubu
        animation_group = QGroupBox("Animasyon Görüntüsü")
        animation_layout = QVBoxLayout()

        # Görsel alanı için QLabel (sabit boyut ayarlama)
        self.imageLabel = QLabel("Animasyon Görüntüsü")
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setFixedHeight(600)  # Görsel için sabit yükseklik
        #self.imageLabel.setFixedSize(800,600);     # Genişlik, Yükseklik
        animation_layout.addWidget(self.imageLabel)
        animation_group.setLayout(animation_layout)
        main_layout.addWidget(animation_group, stretch=1)

        # Komut Ekranı için QTextEdit
        self.commandOutput = QTextEdit()
        self.commandOutput.setReadOnly(True)  # Sadece okunabilir hale getiriyoruz
        self.commandOutput.setFixedHeight(100)  # Yüksekliğini sabitliyoruz
        self.commandOutput.setStyleSheet("background-color: #2b2b2b; color: white;")
        main_layout.addWidget(self.commandOutput)

        # Kontrol Butonları Grubu
        button_group = QGroupBox("Kontrol")
        button_layout = QHBoxLayout()

        self.animationButton = QPushButton("PSO Animation")
        self.animationButton.setFixedSize(90, 50)  # Genişlik: 150, Yükseklik: 100
        self.animationButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.animationButton.clicked.connect(self.showOptimumOnly)
        button_layout.addWidget(self.animationButton)

        self.initButton = QPushButton("PSO Init")
        self.initButton.setFixedSize(90, 50)  # Genişlik: 150, Yükseklik: 100
        self.initButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.initButton.clicked.connect(self.runPSOInitialization)
        button_layout.addWidget(self.initButton)

        self.startButton = QPushButton("PSO Start")
        self.startButton.setFixedSize(90, 50)  # Genişlik: 150, Yükseklik: 100
        self.startButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.startButton.clicked.connect(self.showAnimation)
        button_layout.addWidget(self.startButton)

        self.restartButton = QPushButton("PSO Restart")
        self.restartButton.setFixedSize(90, 50)  # Genişlik: 150, Yükseklik: 100
        self.restartButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.restartButton.clicked.connect(self.restartApplication)
        button_layout.addWidget(self.restartButton)

        button_group.setLayout(button_layout)
        main_layout.addWidget(button_group)
        main_layout.addStretch()  # Boş alanın kontrol kısmına genişlemesini önler

        self.setLayout(main_layout)
        self.setWindowTitle("PSO Görselleştirme Uygulaması")

    def show_message(self, message):
        #QMessageBox.information(self, "Bilgilendirme", message)

        if not message:
            return
        self.commandOutput.append(message)
        self.commandOutput.verticalScrollBar().setValue(self.commandOutput.verticalScrollBar().maximum())

        # Komut ekranına mesaj ekleyelim
        #self.commandOutput.append(message)
        #self.commandOutput.verticalScrollBar().setValue(self.commandOutput.verticalScrollBar().maximum())

    def get_selected_function_and_bounds(self):
        selected_function_name = self.functionBox.currentText()
        func = self.functionBox.currentData()

        # Eğer `currentData()` None dönerse `currentText()` kullanarak fonksiyon alalım
        if func is None:
            print(f"Fonksiyon '{selected_function_name}' currentData() ile bulunamadı, currentText() ile arıyoruz.")
            func = globals().get(selected_function_name)

        bounds = bounds_dict.get(func, (-5.12, 5.12))
        return func, bounds

    def showOptimumOnly(self):
        try:
            # Seçilen fonksiyonu ve parametreleri kontrol et
            func, bounds = self.get_selected_function_and_bounds()
            print(f"Selected Function: {func.__name__ if func else 'None'}")
            print(f"Bounds: {bounds}")

            dimensions = 2
            num_particles = self.particleSpinBox.value()
            max_iter = self.iterationSpinBox.value()
            w_max = self.wMaxSpinBox.value()
            w_min = self.wMinSpinBox.value()
            c1_init = self.c1InitSpinBox.value()
            c1_final = self.c1FinalSpinBox.value()
            c2_init = self.c2InitSpinBox.value()
            c2_final = self.c2FinalSpinBox.value()

            print(
                f"Parameters -> Particles: {num_particles}, Iterations: {max_iter}, w_max: {w_max}, w_min: {w_min}, c1: {c1_init}-{c1_final}, c2: {c2_init}-{c2_final}")

            self.pso = PSO(func, dimensions, bounds, num_particles, max_iter, w_max, w_min, c1_init, c1_final, c2_init,
                           c2_final)

            # Başlangıç durumunu çiz
            self.pso.initialize_plot(show_particles=False)
            combined_frames = self.pso.combine_gifs()

            # Görsel güncellenmesi
            if combined_frames:
                self.update_image(combined_frames[0])
            else:
                self.show_message("PSO Animation error: No frames generated.")
                print("No frames were generated during PSO Animation.")
        except Exception as e:
            self.show_message(f"PSO Animation error: {e}")
            print(f"Error in showOptimumOnly: {e}")

    def runPSOInitialization(self):
        try:
            # Eğer önceki bir iş parçacığı varsa durdur ve temizle
            if hasattr(self, 'pso_thread') and self.pso_thread.isRunning():
                self.pso_thread.quit()
                self.pso_thread.wait()
                self.pso_thread.deleteLater()
                del self.pso_thread

            # Parametreleri arayüzden al
            func, bounds = self.get_selected_function_and_bounds()
            dimensions = 2
            num_particles = self.particleSpinBox.value()
            max_iter = self.iterationSpinBox.value()
            w_max = self.wMaxSpinBox.value()
            w_min = self.wMinSpinBox.value()
            c1_init = self.c1InitSpinBox.value()
            c1_final = self.c1FinalSpinBox.value()
            c2_init = self.c2InitSpinBox.value()
            c2_final = self.c2FinalSpinBox.value()

            # PSOThread iş parçacığını başlat
            self.pso_thread = PSOThread(
                func, dimensions, bounds, num_particles, max_iter,
                w_max, w_min, c1_init, c1_final, c2_init, c2_final
            )

            # İş parçacığından gelen sinyalleri bağlayın
            self.pso_thread.update_signal.connect(self.show_message)
            self.pso_thread.finished_signal.connect(self.show_message)
            self.pso_thread.finished_signal.connect(self.update_final_image)

            # İş parçacığını başlat
            self.pso_thread.start()

        except Exception as e:
            self.show_message(f"PSO Init error: {e}")
            print(f"PSO Init error: {e}")

    def update_final_image(self):
        """Optimizasyon tamamlandığında animasyonu güncelle."""
        combined_frames = self.pso_thread.pso.combine_gifs(output_path=self.animation_path)
        if combined_frames:
            self.update_image(combined_frames[0])

    def showAnimation(self):
        try:
            self.movie = QMovie(self.animation_path)
            if self.movie.isValid():
                self.imageLabel.setMovie(self.movie)
                self.movie.start()
            else:
                raise ValueError("Animasyon dosyası yüklenemedi.")
        except Exception as e:
            self.show_message(f"Animasyon gösteriminde hata: {e}")

    def restartApplication(self):
        try:
            # Mevcut iş parçacığını durdur ve temizle
            if hasattr(self, 'pso_thread'):
                if self.pso_thread.isRunning():
                    self.pso_thread.quit()
                    self.pso_thread.wait()
                    self.pso_thread.deleteLater()
                del self.pso_thread

            QApplication.processEvents()

            # Uygulamayı yeniden başlatmadan önce tüm kaynakları temizleyin
            self.close()  # Mevcut pencereyi kapat
            QProcess.startDetached(sys.executable, sys.argv)
            sys.exit()

        except Exception as e:
            self.show_message(f"Restart error: {e}")
            print(f"Restart error: {e}")

    def update_image(self, frame):
        try:
            qimage = self.convert_to_qimage(frame)
            pixmap = QPixmap.fromImage(qimage)
            self.imageLabel.setPixmap(pixmap)
        except Exception as e:
            self.show_message(f"Görsel güncellenirken hata: {e}")

    def convert_to_qimage(self, pil_image):
        try:
            data = pil_image.tobytes("raw", "RGBA")
            qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
            return qimage
        except Exception as e:
            print(f"Error in convert_to_qimage: {e}")
            return QImage()

# app = QApplication([])
# window = PSOApp()
# window.show()
# app.exec_()
