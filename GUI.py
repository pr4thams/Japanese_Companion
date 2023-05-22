import threading
from tkinter import Tk, Button, OptionMenu, Text, StringVar
from recorder import Recorder
from STT import transcribe
from translator import translate

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)

        # Create an instance of the Recorder class
        self.recorder = Recorder()

        # Create record button
        self.record_button = Button(self, text="Start Recording", command=self.record)
        self.record_button.pack()

        # Create Dropdown menu for language selection
        self.lang_select = StringVar(self)
        self.lang_select.set("EN")  # default value
        self.option_menu = OptionMenu(self, self.lang_select, "EN", "JA")
        self.option_menu.pack()

        # Create Text widget to display output
        self.text_output = Text(self)
        self.text_output.pack()

    def record(self):
        # Call your record function in a separate thread
        record_thread = threading.Thread(target=self.record_audio)
        record_thread.start()

    def record_audio(self):
        try:
            # Record the audio
            self.recorder.record_audio(output_filename="output.wav")
            
            # Transcribe automatically
            self.text = transcribe("output.wav", self.lang_select.get())
            
            if self.lang_select.get() == 'JA':
                # Translate only if the selected language is Japanese
                translated_text = translate(self.text, "EN")
            else:
                translated_text = self.text

            # Display the translated text
            self.text_output.insert('1.0', translated_text)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
