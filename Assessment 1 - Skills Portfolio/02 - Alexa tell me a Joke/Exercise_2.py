import tkinter as tk
from tkinter import messagebox
import random
import os
import pygame

class JokeAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa's Joke Shack")
        self.root.geometry("500x475")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
        # Load jokes from file
        self.jokes = self.load_jokes()
        self.current_joke = None
        
        # Title Label
        self.title_label = tk.Label(
            root,
            text="🎭 Joke Telling Assistant 🎭",
            font=("Comic Sans MS", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.title_label.pack(pady=20)
        
        # Setup Label (for displaying joke setup)
        self.setup_label = tk.Label(
            root,
            text="Click the button below to hear a joke!",
            font=("Comic Sans MS", 12),
            bg="#f0f0f0",
            fg="#34495e",
            wraplength=450,
            justify="center",
            height=4
        )
        self.setup_label.pack(pady=10)
        
        # Punchline Label (for displaying punchline)
        self.punchline_label = tk.Label(
            root,
            text="",
            font=("Comic Sans MS", 12, "italic"),
            bg="#f0f0f0",
            fg="#e74c3c",
            wraplength=450,
            justify="center",
            height=3
        )
        self.punchline_label.pack(pady=10)
        
        # Button Frame
        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack(pady=20)
        
        # "Alexa tell me a Joke" Button
        self.tell_joke_button = tk.Button(
            self.button_frame,
            text="Alexa tell me a Joke",
            font=("Comic Sans MS", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=15,
            pady=10,
            command=self.tell_joke,
            cursor="hand2"
        )
        self.tell_joke_button.grid(row=0, column=0, padx=5, pady=5)
        
        # "Show Punchline" Button
        self.show_punchline_button = tk.Button(
            self.button_frame,
            text="Show Punchline",
            font=("Comic Sans MS", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=10,
            command=self.show_punchline,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.show_punchline_button.grid(row=0, column=1, padx=5, pady=5)
        
        # "Next Joke" Button
        self.next_joke_button = tk.Button(
            self.button_frame,
            text="Next Joke",
            font=("Comic Sans MS", 11, "bold"),
            bg="#f39c12",
            fg="white",
            padx=15,
            pady=10,
            command=self.next_joke,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.next_joke_button.grid(row=1, column=0, padx=5, pady=5)
        
        # "Quit" Button
        self.quit_button = tk.Button(
            self.button_frame,
            text="Quit",
            font=("Comic Sans MS", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=10,
            command=self.quit_app,
            cursor="hand2"
        )
        self.quit_button.grid(row=1, column=1, padx=5, pady=5)
    
    def load_jokes(self):
        # Load jokes from the randomJokes.txt file 
        jokes = []
        file_path = os.path.join("Assessment 1 - Skills Portfolio","A1 - Resources", "randomJokes.txt")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('-'):
                        line = line[1:].strip()
                    
                    # Split by question mark to separate setup and punchline
                    if '?' in line:
                        parts = line.split('?', 1)
                        setup = parts[0].strip() + '?'
                        punchline = parts[1].strip()
                        jokes.append((setup, punchline))
            
            if not jokes:
                messagebox.showerror("Error", "No jokes found in the file!")
                
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                f"File not found: {file_path}\nPlease ensure the file exists in the resources folder."
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        return jokes
    
    def tell_joke(self):
        # Select and display a random joke setup
        if not self.jokes:
            messagebox.showwarning("No Jokes", "No jokes available!")
            return
        
        # Selects a random joke
        self.current_joke = random.choice(self.jokes)
        
        # Displays the setup
        self.setup_label.config(text=self.current_joke[0])
        
        # Clear the punchline
        self.punchline_label.config(text="")
        
        # Enable "Show Punchline" button
        self.show_punchline_button.config(state=tk.NORMAL)
        
        # Enable "Next Joke" button
        self.next_joke_button.config(state=tk.NORMAL)
    
    def next_joke(self):
        # Stops any playing audio and shows the next joke
        # Stops the laugh track if it's still playing
        pygame.mixer.music.stop()
        
        # Call tell_joke to show a new joke
        self.tell_joke()
    
    def show_punchline(self):
        # Displays the punchline of the current joke
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke[1])
            # Disables the button after showing punchline
            self.show_punchline_button.config(state=tk.DISABLED)
            # Plays a laugh track
            self.play_laugh_track()
    
    def play_laugh_track(self):
        # Play a random laugh track audio file
        try:
            # List of laugh track files
            laugh_tracks = [
                "laugh_track1.mp3",
                "laugh_track2.mp3",
                "laugh_track3.mp3",
            ]
            
            # Randomly selects a laugh track
            selected_track = random.choice(laugh_tracks)
            # Build the path the same way as load_jokes
            laugh_track_path = os.path.join("Assessment 1 - Skills Portfolio", "02 - Alexa tell me a Joke", selected_track)
            
            # Plays the selected laugh track
            pygame.mixer.music.load(laugh_track_path)
            pygame.mixer.music.play()
        except FileNotFoundError:
            print(f"Laugh track file not found: {laugh_track_path}")
        except Exception as e:
            print(f"Error playing laugh track: {str(e)}")

    def quit_app(self):
        # Closes the application
        pygame.mixer.music.stop()  # Stops audio before quitting
        self.root.quit()

def main():
    root = tk.Tk()
    app = JokeAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()