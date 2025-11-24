import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# Represents students marks and information
class Student:
    def __init__(self, student_number, name, mark1, mark2, mark3, exam_mark):
        self.student_number = int(student_number)
        self.name = name
        self.mark1 = int(mark1)
        self.mark2 = int(mark2)
        self.mark3 = int(mark3)
        self.exam_mark = int(exam_mark)
    
    # Total coursework = sum of 3 coursework marks
    @property
    def total_coursework(self):
        return self.mark1 + self.mark2 + self.mark3
    
    # Calculates students overall percentage (out of 160)
    @property
    def overall_percentage(self):
        total_marks = self.total_coursework + self.exam_mark
        return (total_marks / 160) * 100
    
    # Converts the percentage into grade
    @property
    def grade(self):
        percentage = self.overall_percentage
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    # Format for saving into the text file
    def to_file_format(self):
        return f"{self.student_number},{self.name},{self.mark1},{self.mark2},{self.mark3},{self.exam_mark}"

# Handles the loading, saving, updating and storing student objects
class StudentManager:
    def __init__(self):
        self.students = []
        self.file_path = r"C:\Users\markh\Documents\GitHub\skills-portfolio-AbigTheGoat\Assessment 1 - Skills Portfolio\03 - Student Manager\studentMarks.txt"
        self.load_data()
    
    # Load students from text file (studentMarks.txt)
    def load_data(self):
        try:
            if not os.path.exists(self.file_path):
                messagebox.showerror("Error", f"studentMarks.txt file not found at: {self.file_path}")
                return
            
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                
                if not lines:
                    messagebox.showwarning("Warning", "studentMarks.txt file is empty.")
                    return
                
                num_students = int(lines[0].strip())  # First line = number of students
                
                # Read each student line and create Student objects
                for i in range(1, num_students + 1):
                    if i < len(lines):
                        data = lines[i].strip().split(',')
                        if len(data) == 6:
                            student = Student(*data)
                            self.students.append(student)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    # Save student list back to the text file
    def save_data(self):
        try:
            with open(self.file_path, 'w') as file:
                file.write(f"{len(self.students)}\n")
                for student in self.students:
                    file.write(student.to_file_format() + "\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False
    
    # Lets you add a student into txt (has to have unique student ID)
    def add_student(self, student_number, name, mark1, mark2, mark3, exam_mark):
        if any(s.student_number == int(student_number) for s in self.students):
            return False, "Student number already exists"
        
        student = Student(student_number, name, mark1, mark2, mark3, exam_mark)
        self.students.append(student)
        return True, "Student added successfully"
    
    # Delete a student by calling the student number
    def delete_student(self, student_number):
        student_number = int(student_number)
        for i, student in enumerate(self.students):
            if student.student_number == student_number:
                del self.students[i]
                return True, "Student deleted successfully"
        return False, "Student not found"
    
    # Lets you update specific student fields
    def update_student(self, student_number, **updates):
        student_number = int(student_number)
        for student in self.students:
            if student.student_number == student_number:
                for key, value in updates.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                return True, "Student updated successfully"
        return False, "Student not found"
    
    # Sorts students based on chosen key
    def sort_students(self, key, ascending=True):
        reverse = not ascending
        if key == 'name':
            self.students.sort(key=lambda s: s.name.lower(), reverse=reverse)
        elif key == 'number':
            self.students.sort(key=lambda s: s.student_number, reverse=reverse)
        elif key == 'percentage':
            self.students.sort(key=lambda s: s.overall_percentage, reverse=reverse)
        elif key == 'grade':
            self.students.sort(key=lambda s: s.grade, reverse=reverse)

# GUI Application
class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1000x700")
        
        # Color palette
        self.colors = {
            'bg_main': '#1a1d2e',
            'bg_sidebar': '#252836',
            'accent_cyan': '#4dd9e8',
            'accent_gold': '#d4af37',
            'text_light': '#e8e8e8',
            'text_dark': '#2e2e3e',
            'button_hover': '#3aa8b5',
            'gray': '#8b8b9b'
        }
        
        self.root.configure(bg=self.colors['bg_main'])
        
        # UI fonts
        self.button_font = ('Comic Sans MS', 11, 'bold')
        self.title_font = ('Comic Sans MS', 18, 'bold')
        self.label_font = ('Comic Sans MS', 10)
        
        # Student data manager
        self.manager = StudentManager()
        
        # Builds the UI
        self.setup_ui()
    
    # Builds the entire GUI structure with the sidebar and output area
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side menu
        sidebar = tk.Frame(main_container, bg=self.colors['bg_sidebar'], width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Adds Sidebar title
        title_label = tk.Label(sidebar, text="Student Manager", 
                              font=self.title_font, 
                              bg=self.colors['bg_sidebar'], 
                              fg=self.colors['accent_cyan'])
        title_label.pack(pady=20)
        
        # Sidebar buttons
        self.create_sidebar_button(sidebar, "View All Students", self.view_all_students)
        self.create_sidebar_button(sidebar, "View Individual", self.view_individual_student)
        self.create_sidebar_button(sidebar, "Highest Score", self.show_highest_student)
        self.create_sidebar_button(sidebar, "Lowest Score", self.show_lowest_student)
        
        tk.Frame(sidebar, height=2, bg=self.colors['accent_cyan']).pack(fill=tk.X, padx=20, pady=15)
        
        self.create_sidebar_button(sidebar, "Sort Records", self.sort_students, self.colors['accent_gold'])
        self.create_sidebar_button(sidebar, "Add Student", self.add_student, self.colors['accent_gold'])
        self.create_sidebar_button(sidebar, "Delete Student", self.delete_student, '#e74c3c')
        self.create_sidebar_button(sidebar, "Update Student", self.update_student, self.colors['accent_gold'])
        
        # Right area where it'll show results 
        content_area = tk.Frame(main_container, bg=self.colors['bg_main'])
        content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        output_frame = tk.Frame(content_area, bg=self.colors['bg_sidebar'], 
                               bd=2, relief=tk.RAISED)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(output_frame, text="Output Display", 
                font=('Comic Sans MS', 12, 'bold'),
                bg=self.colors['bg_sidebar'], 
                fg=self.colors['accent_cyan']).pack(pady=10)
        
        # Text widget for output results
        text_frame = tk.Frame(output_frame, bg=self.colors['bg_sidebar'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.output_text = tk.Text(text_frame, height=25, width=70, wrap=tk.WORD,
                                   font=self.label_font,
                                   bg=self.colors['bg_main'],
                                   fg=self.colors['text_light'],
                                   insertbackground=self.colors['accent_cyan'],
                                   selectbackground=self.colors['accent_cyan'],
                                   selectforeground=self.colors['text_dark'])
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Creates buttons in the sidebar
    def create_sidebar_button(self, parent, text, command, color=None):
        if color is None:
            color = self.colors['accent_cyan']
        
        btn = tk.Button(parent, text=text, command=command,
                       font=self.button_font,
                       bg=color,
                       fg=self.colors['text_dark'],
                       activebackground=self.colors['button_hover'],
                       activeforeground='white',
                       relief=tk.FLAT,
                       cursor='hand2',
                       pady=12,
                       padx=10)
        btn.pack(fill=tk.X, padx=15, pady=6)
        
        return btn
    
    # Clears the output display if theres anything on it
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
    
    # Inserts a students info into the output window
    def display_student_info(self, student, show_header=False):
        if show_header:
            self.output_text.insert(tk.END, f"{'Name':<20} {'Number':<8} {'Coursework':<12} {'Exam':<8} {'Percentage':<12} {'Grade':<6}\n")
            self.output_text.insert(tk.END, "-" * 70 + "\n")
        
        self.output_text.insert(
            tk.END,
            f"{student.name:<20} {student.student_number:<8} "
            f"{student.total_coursework:<12} {student.exam_mark:<8} "
            f"{student.overall_percentage:<12.1f} {student.grade:<6}\n"
        )
    
    # Displays all students with their info summary
    def view_all_students(self):
        self.clear_output()
        self.output_text.insert(tk.END, "ALL STUDENT RECORDS\n")
        self.output_text.insert(tk.END, "=" * 70 + "\n\n")
        
        if not self.manager.students:
            self.output_text.insert(tk.END, "No student records found.\n")
            return
        
        # Header row
        self.display_student_info(self.manager.students[0], show_header=True)
        
        total_percentage = 0
        for student in self.manager.students:
            self.display_student_info(student)
            total_percentage += student.overall_percentage
        
        avg_percentage = total_percentage / len(self.manager.students)
        
        self.output_text.insert(tk.END, "\n" + "=" * 70 + "\n")
        self.output_text.insert(tk.END, f"Number of students: {len(self.manager.students)}\n")
        self.output_text.insert(tk.END, f"Average percentage: {avg_percentage:.1f}%\n")
    
    # Selects a student and views their details
    def view_individual_student(self):
        if not self.manager.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        student = self.select_student_dialog("Select Student to View")
        if student:
            self.display_individual_student(student)
    
    # Prints the detailed information of a chosen student
    def display_individual_student(self, student):
        self.clear_output()
        self.output_text.insert(tk.END, "INDIVIDUAL STUDENT RECORD\n")
        self.output_text.insert(tk.END, "=" * 70 + "\n\n")
        
        self.output_text.insert(tk.END, f"Student Name: {student.name}\n")
        self.output_text.insert(tk.END, f"Student Number: {student.student_number}\n")
        self.output_text.insert(tk.END, f"Coursework Marks: {student.mark1}, {student.mark2}, {student.mark3}\n")
        self.output_text.insert(tk.END, f"Total Coursework Mark: {student.total_coursework}/60\n")
        self.output_text.insert(tk.END, f"Exam Mark: {student.exam_mark}/100\n")
        self.output_text.insert(tk.END, f"Overall Percentage: {student.overall_percentage:.1f}%\n")
        self.output_text.insert(tk.END, f"Grade: {student.grade}\n")
    
    # Shows the highest-performing student
    def show_highest_student(self):
        self.clear_output()
        self.output_text.insert(tk.END, "STUDENT WITH HIGHEST OVERALL MARK\n")
        self.output_text.insert(tk.END, "=" * 70 + "\n\n")
        
        if not self.manager.students:
            self.output_text.insert(tk.END, "No student records found.\n")
            return
        
        highest_student = max(self.manager.students, key=lambda s: s.overall_percentage)
        self.display_individual_student(highest_student)
    
    # Shows the lowest-performing student
    def show_lowest_student(self):
        self.clear_output()
        self.output_text.insert(tk.END, "STUDENT WITH LOWEST OVERALL MARK\n")
        self.output_text.insert(tk.END, "=" * 70 + "\n\n")
        
        if not self.manager.students:
            self.output_text.insert(tk.END, "No student records found.\n")
            return
        
        lowest_student = min(self.manager.students, key=lambda s: s.overall_percentage)
        self.display_individual_student(lowest_student)
    
    # Pop-up window that let users pick a sort method
    def sort_students(self):
        if not self.manager.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Students")
        sort_window.geometry("350x450")
        sort_window.configure(bg=self.colors['bg_main'])
        sort_window.transient(self.root)
        sort_window.grab_set()
        
        tk.Label(sort_window, text="Sort Students", 
                font=('Comic Sans MS', 14, 'bold'),
                bg=self.colors['bg_main'], 
                fg=self.colors['accent_cyan']).pack(pady=15)
        
        sort_var = tk.StringVar(value="name")
        
        options_frame = tk.Frame(sort_window, bg=self.colors['bg_main'])
        options_frame.pack(pady=10)
        
        # Sorting options to choose from
        for text, value in [("Name", "name"), ("Student Number", "number"), 
                           ("Percentage", "percentage"), ("Grade", "grade")]:
            tk.Radiobutton(options_frame, text=text, variable=sort_var, value=value,
                          font=self.label_font, bg=self.colors['bg_main'], 
                          fg=self.colors['text_light']).pack(anchor=tk.W, padx=20, pady=3)
        
        order_var = tk.StringVar(value="ascending")
        
        tk.Label(sort_window, text="Order:", font=self.label_font,
                bg=self.colors['bg_main'], fg=self.colors['gray']).pack(pady=(10, 5))
        
        # Ascending/descending selection
        for text, value in [("Ascending", "ascending"), ("Descending", "descending")]:
            tk.Radiobutton(options_frame, text=text, variable=order_var, value=value,
                          font=self.label_font, bg=self.colors['bg_main'], 
                          fg=self.colors['text_light']).pack(anchor=tk.W, padx=20, pady=3)
        
        # Applys sorting
        def perform_sort():
            ascending = order_var.get() == "ascending"
            self.manager.sort_students(sort_var.get(), ascending)
            if self.manager.save_data():
                self.view_all_students()
                sort_window.destroy()
                messagebox.showinfo("Success", "Students sorted successfully!")
        
        self.create_dialog_button(sort_window, "Sort", perform_sort)
    
    # Creates buttons for pop-up dialogs
    def create_dialog_button(self, parent, text, command, color=None):
        if color is None:
            color = self.colors['accent_cyan']
        
        btn = tk.Button(parent, text=text, command=command,
                       font=self.button_font,
                       bg=color,
                       fg=self.colors['text_dark'],
                       activebackground=self.colors['button_hover'],
                       activeforeground='white',
                       relief=tk.FLAT,
                       cursor='hand2',
                       pady=10,
                       padx=30)
        btn.pack(pady=15)
        return btn
    
    # Window to add a new students
    def add_student(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Student")
        add_window.geometry("500x500")
        add_window.configure(bg=self.colors['bg_main'])
        add_window.transient(self.root)
        add_window.grab_set()
        
        tk.Label(add_window, text="Add New Student", 
                font=('Comic Sans MS', 14, 'bold'),
                bg=self.colors['bg_main'], 
                fg=self.colors['accent_cyan']).pack(pady=15)
        
        fields_frame = tk.Frame(add_window, bg=self.colors['bg_main'])
        fields_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        entries = {}
        
        # All student input fields
        fields = [
            ("Student Number:", "number"),
            ("Name:", "name"),
            ("Coursework Mark 1 (0-20):", "mark1"),
            ("Coursework Mark 2 (0-20):", "mark2"),
            ("Coursework Mark 3 (0-20):", "mark3"),
            ("Exam Mark (0-100):", "exam")
        ]
        
        # Creates input boxes
        for i, (label_text, key) in enumerate(fields):
            tk.Label(fields_frame, text=label_text, font=self.label_font,
                    bg=self.colors['bg_main'], fg=self.colors['text_light']).grid(
                        row=i, column=0, sticky=tk.W, pady=8)
            
            entry = tk.Entry(fields_frame, font=self.label_font, width=25,
                           bg=self.colors['bg_sidebar'], fg=self.colors['text_light'],
                           insertbackground=self.colors['accent_cyan'])
            entry.grid(row=i, column=1, sticky=tk.W, pady=8, padx=10)
            entries[key] = entry
        
        # Saves the new student information
        def save_student():
            try:
                success, message = self.manager.add_student(
                    entries['number'].get(),
                    entries['name'].get(),
                    entries['mark1'].get(),
                    entries['mark2'].get(),
                    entries['mark3'].get(),
                    entries['exam'].get()
                )
                
                if success:
                    if self.manager.save_data():
                        add_window.destroy()
                        self.view_all_students()
                        messagebox.showinfo("Success", message)
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for marks")
        
        self.create_dialog_button(add_window, "Save Student", save_student, self.colors['accent_gold'])
    
    # Deletes a student 
    def delete_student(self):
        if not self.manager.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        student = self.select_student_dialog("Select Student to Delete")
        if student:
            confirm = messagebox.askyesno("Confirm Delete", 
                                         f"Are you sure you want to delete {student.name} ({student.student_number})?")
            if confirm:
                success, message = self.manager.delete_student(student.student_number)
                if success:
                    if self.manager.save_data():
                        self.view_all_students()
                        messagebox.showinfo("Success", message)
                else:
                    messagebox.showerror("Error", message)
    
    # Updates a students information
    def update_student(self):
        if not self.manager.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        student = self.select_student_dialog("Select Student to Update")
        if student:
            self.show_update_dialog(student)
    
    # The update pop-up window
    def show_update_dialog(self, student):
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update {student.name}")
        update_window.geometry("400x450")
        update_window.configure(bg=self.colors['bg_main'])
        update_window.transient(self.root)
        update_window.grab_set()
        
        tk.Label(update_window, text=f"Update {student.name}", 
                font=('Comic Sans MS', 14, 'bold'),
                bg=self.colors['bg_main'], 
                fg=self.colors['accent_cyan']).pack(pady=15)
        
        # Helper for updating fields
        def update_field(field_name, current_value, max_value=None):
            new_value = simpledialog.askstring("Update Field", 
                                             f"Enter new {field_name}:\n(Current: {current_value})" + 
                                             (f"\nMax: {max_value}" if max_value else ""))
            if new_value is not None:
                try:
                    if field_name in ['mark1', 'mark2', 'mark3'] and max_value:
                        value = int(new_value)
                        if 0 <= value <= max_value:
                            updates = {field_name: value}
                            success, message = self.manager.update_student(student.student_number, **updates)
                            if success:
                                if self.manager.save_data():
                                    self.view_all_students()
                                    messagebox.showinfo("Success", message)
                                    update_window.destroy()
                            else:
                                messagebox.showerror("Error", message)
                        else:
                            messagebox.showerror("Error", f"Value must be between 0 and {max_value}")
                    elif field_name == 'exam_mark':
                        value = int(new_value)
                        if 0 <= value <= 100:
                            updates = {field_name: value}
                            success, message = self.manager.update_student(student.student_number, **updates)
                            if success:
                                if self.manager.save_data():
                                    self.view_all_students()
                                    messagebox.showinfo("Success", message)
                                    update_window.destroy()
                            else:
                                messagebox.showerror("Error", message)
                        else:
                            messagebox.showerror("Error", "Exam mark must be between 0 and 100")
                    elif field_name == 'name':
                        updates = {field_name: new_value}
                        success, message = self.manager.update_student(student.student_number, **updates)
                        if success:
                            if self.manager.save_data():
                                self.view_all_students()
                                messagebox.showinfo("Success", message)
                                update_window.destroy()
                        else:
                            messagebox.showerror("Error", message)
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number")
        
        # Buttons inside the update window
        buttons_info = [
            ("Update Name", 'name', student.name, None),
            ("Update Coursework Mark 1", 'mark1', student.mark1, 20),
            ("Update Coursework Mark 2", 'mark2', student.mark2, 20),
            ("Update Coursework Mark 3", 'mark3', student.mark3, 20),
            ("Update Exam Mark", 'exam_mark', student.exam_mark, 100)
        ]
        
        for btn_text, field, current, max_val in buttons_info:
            btn = tk.Button(update_window, text=btn_text,
                           command=lambda f=field, c=current, m=max_val: update_field(f, c, m),
                           font=self.button_font,
                           bg=self.colors['accent_gold'],
                           fg=self.colors['text_dark'])
            btn.pack(fill=tk.X, padx=30, pady=6)
    
    # Lets the user select a student from a listbox
    def select_student_dialog(self, title):
        selection_window = tk.Toplevel(self.root)
        selection_window.title(title)
        selection_window.geometry("500x400")
        selection_window.configure(bg=self.colors['bg_main'])
        selection_window.transient(self.root)
        selection_window.grab_set()
        
        selected_student = [None]
        
        tk.Label(selection_window, text="Select a student:", 
                font=('Comic Sans MS', 12, 'bold'),
                bg=self.colors['bg_main'], 
                fg=self.colors['accent_cyan']).pack(pady=15)
        
        listbox = tk.Listbox(selection_window, width=50, height=12, 
                            font=self.label_font,
                            bg=self.colors['bg_sidebar'],
                            fg=self.colors['text_light'],
                            selectbackground=self.colors['accent_cyan'],
                            selectforeground=self.colors['text_dark'])
        listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Show "number - name" for each student
        for student in self.manager.students:
            listbox.insert(tk.END, f"{student.student_number} - {student.name}")
        
        # When user clicks select
        def on_select():
            selection = listbox.curselection()
            if selection:
                selected_student[0] = self.manager.students[selection[0]]
                selection_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a student.")
        
        self.create_dialog_button(selection_window, "Select", on_select)
        
        self.root.wait_window(selection_window)
        return selected_student[0]

# App launcher
def main():
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
