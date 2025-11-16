from tkinter import *
from tkinter import messagebox
import pygame
from random import randint, choice

# ---------- MAIN WINDOW ----------
# Creates the Main window
root = Tk()
root.geometry("700x600")
root.title("Astral Express Math Challenge")
root.resizable(False, False)

# Adds Colors to Window
bg_color = "#0a0e27"
accent_gold = "#f4d03f"
accent_purple = "#8e44ad"
accent_blue = "#3498db"
text_color = "#ecf0f1"
root.configure(bg=bg_color)

# ---------- GLOBAL VARIABLES ----------
difficulty = StringVar() #Stores Difficulties Easy, Medium, Advanced
score = IntVar(value=0) #Displays players current score 
current_question = 0 # Current level user is on
total_questions = 10 # Keeps questions always constant (Change value if need more questions) 
attempt = 1  
current_answer = IntVar() # Used to check if users answer is correct 
num1 = 0 #num1 and num2 contains two values displayed on screen 
num2 = 0
operation = StringVar() #chooses between + and - 

# Power-ups
# Shows remaining amout of power ups (Change value if want more power ups :3)
double_points_remaining = IntVar(value=2) 
reveal_answer_remaining = IntVar(value=1) 
skip_question_remaining = IntVar(value=1) 
double_points_active = False


# ---------- FUNCTIONS ----------
def create_starry_background(parent):
    # Creates the starry background 
    canvas = Canvas(parent, width=700, height=600, bg=bg_color, highlightthickness=0)
    canvas.place(x=0, y=0)
    
    for _ in range(90): # Value decides amount of Stars
        x = randint(0, 700)
        y = randint(0, 600)
        size = randint(1, 3)
        canvas.create_oval(x, y, x + size, y + size, fill="#ffffff", outline="")
    
    return canvas

def clear_window(): # Clears window screen 
    for widget in root.winfo_children():
        widget.destroy()

def reset_game(): # Resets all game variables  to default settings
    global current_question, double_points_remaining, reveal_answer_remaining, skip_question_remaining, double_points_active
    score.set(0)
    current_question = 0
    double_points_remaining.set(2)
    reveal_answer_remaining.set(1)
    skip_question_remaining.set(1)
    double_points_active = False

def display_menu(): # Shows the main menu of the game
    clear_window()
    reset_game()
    create_starry_background(root)
    
    main_frame = Frame(root, bg=bg_color)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    title = Label(main_frame, text="⭐ ASTRAL EXPRESS ⭐", font=("Comic Sans MS", 28, "bold"), fg=accent_gold, bg=bg_color)
    title.pack(pady=10)
    
    subtitle = Label(main_frame, text="MATH CHALLENGE", font=("Comic Sans MS", 18, "bold"), fg=text_color, bg=bg_color)
    subtitle.pack(pady=5)
    
    message = Label(main_frame, text="🚀 Choose Your Path, Trailblazer! 🚀", font=("Comic Sans MS", 12), fg=accent_blue, bg=bg_color)
    message.pack(pady=15)
    
    btn_frame = Frame(main_frame, bg=bg_color)
    btn_frame.pack(pady=10)
    
    btn1 = Button(btn_frame, text="🌟 BEGINNER PATH\n(Single Digit Numbers)", font=("Comic Sans MS", 12, "bold"), width=28, height=3, bg="#27ae60", fg="white", cursor="hand2", command=lambda: start_quiz("Easy"))
    btn1.pack(pady=8)
    
    btn2 = Button(btn_frame, text="⚡ CHALLENGER PATH\n(Double Digit Numbers)", font=("Comic Sans MS", 12, "bold"), width=28, height=3, bg="#f39c12", fg="white", cursor="hand2", command=lambda: start_quiz("Moderate"))
    btn2.pack(pady=8)
    
    btn3 = Button(btn_frame, text="💫 TRAILBLAZER PATH\n(4-Digit Numbers)", font=("Comic Sans MS", 12, "bold"), width=28, height=3, bg="#8e44ad", fg="white", cursor="hand2", command=lambda: start_quiz("Advanced"))
    btn3.pack(pady=8)

def generate_numbers(level): # Generates two random numbers depending on user chosen difficulty
    if level == "Easy":
        return randint(1, 9), randint(1, 9)
    elif level == "Moderate":
        return randint(10, 99), randint(10, 99)
    else:
        return randint(1000, 9999), randint(1000, 9999)

def pick_operation(): # randomly picks between + and - 
    return choice(['+', '-'])

def start_quiz(level): # Stars the quiz after user picks a difficulty 
    global current_question
    difficulty.set(level)
    current_question = 0
    score.set(0)
    show_question()

def activate_double_points():
    global double_points_active
    if double_points_remaining.get() > 0:
        double_points_active = True
        double_points_remaining.set(double_points_remaining.get() - 1)
        messagebox.showinfo("🌟 Powerup Activated!", "Double Points active for this question!\nEarn 20 points (1st try) or 10 points (2nd try)!")
        update_powerup_display()
    else:
        messagebox.showwarning("⚠️ No Charges left", "You've used all Double Points powerups!")

def reveal_correct_answer():
    if reveal_answer_remaining.get() > 0:
        reveal_answer_remaining.set(reveal_answer_remaining.get() - 1)
        answer_entry.delete(0, END)
        answer_entry.insert(0, str(current_answer.get()))
        messagebox.showinfo("💡 Answer Revealed!", f"The answer is: {current_answer.get()}\nSubmit to continue!")
        update_powerup_display()
    else:
        messagebox.showwarning("⚠️ No Charges left", "You've used all your Reveal Answers powerup!")

def skip_current_question():
    global current_question
    if skip_question_remaining.get() > 0:
        skip_question_remaining.set(skip_question_remaining.get() - 1)
        score.set(score.get() + 5)
        messagebox.showinfo("⏭️ Question Skipped!", "Question skipped! +5 Stellar Jades earned!")
        current_question += 1
        show_question()
    else:
        messagebox.showwarning("⚠️ No Charges left ", "You've used your Skip Question powerup!")

def update_powerup_display():
    if double_points_remaining.get() > 0 and not double_points_active:
        double_btn.config(state="normal", bg="#f39c12")
    else:
        double_btn.config(state="disabled", bg="#7f8c8d")
    
    if reveal_answer_remaining.get() > 0:
        reveal_btn.config(state="normal", bg="#9b59b6")
    else:
        reveal_btn.config(state="disabled", bg="#7f8c8d")
    
    if skip_question_remaining.get() > 0:
        skip_btn.config(state="normal", bg="#3498db")
    else:
        skip_btn.config(state="disabled", bg="#7f8c8d")
    
    powerup_label.config(text=f"⚡ Powerups: 2x Points ({double_points_remaining.get()}) | Reveal ({reveal_answer_remaining.get()}) | Skip ({skip_question_remaining.get()})")

def show_question(): # Displays the Questions 
    global num1, num2, attempt, answer_entry, powerup_label, double_btn, reveal_btn, skip_btn, feedback_label, double_points_active
    
    clear_window() # Starts by clearing the window first 
    
    if current_question >= total_questions: # Checks if quiz is done if yes it shows the final results 
        show_final_results()
        return
    
    num1, num2 = generate_numbers(difficulty.get()) # Generates the random number and operation
    operation.set(pick_operation())
    
    if operation.get() == '+':
        current_answer.set(num1 + num2)
    else:
        current_answer.set(num1 - num2)
    
    attempt = 1 # Sets the attempts back to 1 (first try)
    
    create_starry_background(root) 
    
    main_frame = Frame(root, bg=bg_color)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    progress = Label(main_frame, text=f"🌠 Node {current_question + 1}/{total_questions} | Stellar Jades: {score.get()} 💎", font=("Comic Sans MS", 13, "bold"), fg=accent_gold, bg=bg_color)
    progress.pack(pady=10)
    
    powerup_label = Label(main_frame, text=f"⚡ Powerups: 2x Points ({double_points_remaining.get()}) | Reveal ({reveal_answer_remaining.get()}) | Skip ({skip_question_remaining.get()})", font=("Arial", 10), fg=accent_blue, bg=bg_color)
    powerup_label.pack(pady=5)
    
    if double_points_active:
        active_indicator = Label(main_frame, text="🌟 DOUBLE POINTS ACTIVE! 🌟", font=("Comic Sans MS", 11, "bold"), fg="#f39c12", bg=bg_color)
        active_indicator.pack(pady=5)
    
    problem_box = Frame(main_frame, bg="#1a1f3a", borderwidth=3, relief="solid", highlightbackground=accent_gold, highlightthickness=2)
    problem_box.pack(pady=15, padx=20)
    
    problem_title = Label(problem_box, text="⚔️ COMBAT CALCULATION ⚔️", font=("Comic Sans MS", 12, "bold"), bg="#1a1f3a", fg=accent_blue)
    problem_title.pack(pady=10)
    
    problem_display = Label(problem_box, text=f"{num1} {operation.get()} {num2} = ?", font=("Comic Sans MS", 36, "bold"), bg="#1a1f3a", fg=text_color, padx=40, pady=20)
    problem_display.pack()
    
    entry_area = Frame(main_frame, bg=bg_color)
    entry_area.pack(pady=10)
    
    answer_prompt = Label(entry_area, text="Your Answer:", font=("Comic Sans MS", 11), fg=text_color, bg=bg_color)
    answer_prompt.pack()
    
    answer_entry = Entry(entry_area, font=("Comic Sans MS", 20), width=12, justify="center", bg="#2c3e50", fg=accent_gold, insertbackground=accent_gold)
    answer_entry.pack(pady=5)
    answer_entry.focus()
    answer_entry.bind('<Return>', lambda e: check_user_answer())
    
    submit_button = Button(main_frame, text=" UNLEASH TECHNIQUE ⚡", font=("Comic Sans MS", 12, "bold"), bg="#27ae60", fg="white", width=25, height=2, cursor="hand2", command=check_user_answer)
    submit_button.pack(pady=8)
    
    powerup_section = Frame(main_frame, bg=bg_color)
    powerup_section.pack(pady=10)
    
    powerup_title = Label(powerup_section, text=" ABILITIES 🎯", font=("Comic Sans MS", 10, "bold"), fg=accent_purple, bg=bg_color)
    powerup_title.pack(pady=5)
    
    button_container = Frame(powerup_section, bg=bg_color)
    button_container.pack()
    
    double_btn = Button(button_container, text=f"🌟 2x Points\n({double_points_remaining.get()})", font=("Comic Sans MS", 9, "bold"), bg="#f39c12", fg="white", width=12, height=3, cursor="hand2", command=activate_double_points)
    double_btn.grid(row=0, column=0, padx=5)
    
    reveal_btn = Button(button_container, text=f"💡 Reveal\n({reveal_answer_remaining.get()})", font=("Comic Sans MS", 9, "bold"), bg="#9b59b6", fg="white", width=12, height=3, cursor="hand2", command=reveal_correct_answer)
    reveal_btn.grid(row=0, column=1, padx=5)
    
    skip_btn = Button(button_container, text=f"⏭️ Skip\n({skip_question_remaining.get()})", font=("Comic Sans MS", 9, "bold"), bg="#3498db", fg="white", width=12, height=3, cursor="hand2", command=skip_current_question)
    skip_btn.grid(row=0, column=2, padx=5)
    
    update_powerup_display()
    
    feedback_label = Label(main_frame, text="", font=("Comic Sans MS", 11, "bold"), fg="#e74c3c", bg=bg_color)
    feedback_label.pack(pady=5)

def check_user_answer(): # Checks users answers
    global attempt, current_question, double_points_active
    
    try:
        user_answer = int(answer_entry.get()) 
    except ValueError:
        feedback_label.config(text="⚠️ Invalid input! Enter a number, Trailblazer!", fg="#e74c3c")
        return
    
    if user_answer == current_answer.get(): # If the user gets the correct answer in 1 try they get more points 
        if attempt == 1:
            points = 20 if double_points_active else 10
            score.set(score.get() + points)
            message = f"Critical Hit! 💥\n+{points} Stellar Jades earned! ✨"
        else:
            points = 10 if double_points_active else 5
            score.set(score.get() + points)
            message = f"Success! ⚡\n+{points} Stellar Jades earned! 💎"
        
        messagebox.showinfo("Correct!", message)
        double_points_active = False
        current_question += 1
        show_question()
    else:
        if attempt == 1:
            attempt = 2
            feedback_label.config(text="❌ Missed! try again Trailblazer!", fg="#e74c3c")
            answer_entry.delete(0, END)
            answer_entry.focus()
        else:
            messagebox.showinfo("Defeat...", f"The correct answer was {current_answer.get()}\nKeep training, Trailblazer! 🌟")
            double_points_active = False
            current_question += 1
            show_question()

def show_final_results(): # Shows the final grade the user gets
    clear_window()
    create_starry_background(root)
    
    if score.get() >= 90:
        grade = "S+"
        rank_title = "LEGENDARY TRAILBLAZER"
        color = accent_gold
        emoji = "👑"
    elif score.get() >= 80:
        grade = "S"
        rank_title = "MASTER TRAILBLAZER"
        color = "#9b59b6"
        emoji = "⭐"
    elif score.get() >= 70:
        grade = "A"
        rank_title = "SKILLED NAVIGATOR"
        color = "#3498db"
        emoji = "🌟"
    elif score.get() >= 60:
        grade = "B"
        rank_title = "PROMISING ADVENTURER"
        color = "#2ecc71"
        emoji = "✨"
    else:
        grade = "C"
        rank_title = "NOVICE TRAVELER"
        color = "#95a5a6"
        emoji = "🌠"
    
    main_frame = Frame(root, bg=bg_color)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    title = Label(main_frame, text="🎊 JOURNEY COMPLETE! 🎊", font=("Comic Sans MS", 26, "bold"), fg=accent_gold, bg=bg_color)
    title.pack(pady=20)
    
    score_display = Label(main_frame, text=f"💎 Stellar Jades Earned: {score.get()} / 100", font=("Comic Sans MS", 18, "bold"), fg=text_color, bg=bg_color)
    score_display.pack(pady=10)
    
    grade_display = Label(main_frame, text=f"{emoji} Rank: {grade} {emoji}", font=("Comic Sans MS", 32, "bold"), fg=color, bg=bg_color)
    grade_display.pack(pady=15)
    
    rank_display = Label(main_frame, text=rank_title, font=("Comic Sans MS", 16, "bold"), fg=color, bg=bg_color)
    rank_display.pack(pady=5)
    
    if score.get() >= 90:
        message = "Outstanding! The Astral Express welcomes you! 🚂✨"
    elif score.get() >= 70:
        message = "Well done! Your journey continues! 🌌"
    else:
        message = "Keep exploring! Every Trailblazer starts somewhere! 🌠"
    
    encouragement = Label(main_frame, text=message, font=("Comic Sans MS", 12), fg=accent_blue, bg=bg_color, wraplength=450)
    encouragement.pack(pady=15)
    
    button_area = Frame(main_frame, bg=bg_color)
    button_area.pack(pady=20)
    
    play_again = Button(button_area, text="🔄 New Adventure", font=("Comic Sans MS", 12, "bold"), bg="#27ae60", fg="white", width=20, height=2, cursor="hand2", command=display_menu)
    play_again.pack(pady=5)
    
    exit_button = Button(button_area, text="🚪 Exit", font=("Comic Sans MS", 12, "bold"), bg="#7f8c8d", fg="white", width=20, height=2, cursor="hand2", command=root.quit)
    exit_button.pack(pady=5)

# ---------- START PROGRAM ----------
display_menu()
root.mainloop() 