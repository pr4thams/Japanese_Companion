import threading
import tkinter as tk
from tkinter import Tk, Button, OptionMenu, Text, StringVar, messagebox
from recorder import Recorder
from STS import transcribe, text_to_speech, audioPlayer
from translator import translate
from chatbot import get_ai_response

class Application:
    def __init__(self, window):
        self.window = window
        self.window.title("My Companion")

        # Create an instance of the Recorder class
        self.recorder = Recorder()
        
        # Create TextEdit to display output
        self.text_output = tk.Text(self.window, width=50, height=25)
        self.text_output.grid(row=0, column=0, rowspan=6, padx=5, pady=5)

        # Create record button
        self.record_button = tk.Button(self.window, text='Start Recording', command=self.record)
        self.record_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Create ComboBox for language selection
        self.lang_select = tk.StringVar(self.window)
        self.lang_select.set("EN") # default value
        lang_menu = tk.OptionMenu(self.window, self.lang_select, "EN", "JA")
        lang_menu.grid(row=1, column=1, padx=5, pady=5)

        # Create a label below the record button
        self.instruction_label = tk.Label(self.window, text="")
        self.instruction_label.grid(row=2, column=1, padx=5, pady=5)

    def record(self):
        # Call your record function in a separate thread
        record_thread = threading.Thread(target=self.record_audio)
        record_thread.start()

    def record_audio(self):
        self.instruction_label['text'] = "Press and hold 'space' key to start recording..."
        try:
            # Record the audio
            self.recorder.record_audio(output_filename="output/output.wav")
            self.instruction_label['text'] = ""  # clear the instruction label            
            # Transcribe automatically
            self.text = transcribe("output/output.wav", self.lang_select.get())
            
            if self.lang_select.get() == 'JA':
                # Translate only if the selected language is Japanese
                translated_text = translate(self.text, "EN")
            else:
                translated_text = self.text
                
            get_ai_response(translated_text)
            try:
                with open('output/AI_response.txt', 'r', encoding="utf-8") as file:
                    ai_response = file.read()
            except FileNotFoundError:
                print("AI_response.txt not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
            ai_response = translate(ai_response, "JA")
            with open('output/AI_response.txt', 'w', encoding="utf-8") as file:
                file.write(ai_response)
            text_to_speech("output/AI_response.txt")
            audioPlayer("output/audioResponse.wav")
            # Display the translated text
            self.text_output.insert('1.0', ai_response)
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    window = tk.Tk()
    app = Application(window)
    window.mainloop()