from gui import PSOApp
from PyQt5.QtWidgets import QApplication
import sys
import qdarkstyle

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.setStyleSheet(app.styleSheet() + """
            QWidget {
                font-size: 14px;  /* Genel metin boyutunu ayarla */
            }
            QLabel {
                font-size: 12px;  /* Özellikle QLabel için ayar */
            }
            QPushButton {
                font-size: 14px;  /* Butonların metin boyutunu ayarla */
            }
            QTextEdit {
                font-size: 14px;  /* QTextEdit metin boyutu */
            }
        """)
    window = PSOApp()
    #window.show()
    window.showMaximized()  # Uygulamayı tam ekran başlatmak için
    sys.exit(app.exec_())
