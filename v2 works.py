import sys
import mido
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QProgressBar

class MidiProcessor(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('MIDI Importer and Exporter')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.import_button = QPushButton('Import MIDI Files', self)
        self.import_button.clicked.connect(self.import_midi_files)
        layout.addWidget(self.import_button)

        self.info_label = QLabel('')
        layout.addWidget(self.info_label)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def import_midi_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_names, _ = QFileDialog.getOpenFileNames(self, "Import MIDI Files", "", "MIDI Files (*.mid *.midi);;All Files (*)", options=options)

        if file_names:
            self.process_midi_files(file_names)

    def process_midi_files(self, file_names):
        midi_data = []

        for index, file_name in enumerate(file_names):
            try:
                midi_file = mido.MidiFile(file_name)
                tracks_data = []

                for track in midi_file.tracks:
                    track_data = []

                    for msg in track:
                        msg_dict = msg.dict()
                        msg_dict['type'] = msg.type
                        track_data.append(msg_dict)

                    tracks_data.append(track_data)

                midi_data.append(tracks_data)

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

            progress = int((index + 1) / len(file_names) * 100)
            self.progress_bar.setValue(progress)

        self.export_data(midi_data)

    def export_data(self, data):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "NumPy Array (*.npy)")

        if file_name:
            np.save(file_name, np.array(data, dtype=object))
            self.info_label.setText(f'Data exported to {file_name}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MidiProcessor()
    ex.show()
    sys.exit(app.exec_())
