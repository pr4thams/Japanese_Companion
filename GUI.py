import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QComboBox

from recorder import Recorder
from STT import transcribe
from translator import translate

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create an instance of the Recorder class
        self.recorder = Recorder()
        
        # Create record button
        self.record_button = QPushButton('Start Recording', self)
        self.record_button.move(50, 50)
        self.record_button.clicked.connect(self.record)
        
        # Create ComboBox for language selection
        self.lang_select = QComboBox(self)
        self.lang_select.addItems(['EN', 'JA'])
        self.lang_select.move(150, 200)

        # Create TextEdit to display output
        self.text_output = QTextEdit(self)
        self.text_output.move(200, 50)

    def record(self):
        # Call your record function here
        self.audio_file = self.recorder.record_audio()
        
        # Transcribe and translate automatically
        self.text = transcribe(self.audio_file, self.lang_select.currentText())
        translated_text = translate(self.text, self.lang_select.currentText())
        
        # Display the translated text
        self.text_output.setText(translated_text)

app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())