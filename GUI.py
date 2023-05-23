import threading
from tkinter import Tk, Button, OptionMenu, Text, StringVar
from recorder import Recorder
from STS import transcribe
from translator import translate
from chatbot import get_ai_response, separate_sentences

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
            self.recorder.record_audio(output_filename="output/output.wav")
            
            # Transcribe automatically
            self.text = transcribe("output/output.wav", self.lang_select.get())
            
            if self.lang_select.get() == 'JA':
                # Translate only if the selected language is Japanese
                translated_text = translate(self.text, "EN")
            else:
                translated_text = self.text
                
            get_ai_response(translated_text)
            try:
                with open('output/AI_response.txt', 'r') as file:
                    ai_response = file.read()
            except FileNotFoundError:
                print("AI_response.txt not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
            ai_response = translate(ai_response, "JA")
            with open('output/AI_response.txt', 'w', encoding="utf-8") as file:
                separated_text = separate_sentences(ai_response)
                file.write(separated_text)

            # Display the translated text
            self.text_output.insert('1.0', ai_response)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
