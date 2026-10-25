import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    create_database,
    save_record,
    get_records,
    delete_record
)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# VIEW BMI HISTORY
# ============================================================

def view_history():
    try:
        records = get_records()

        history_window = tk.Toplevel(window)
        history_window.title("BMI History")
        history_window.geometry("850x500")

        # Title
        history_label = tk.Label(
            history_window,
            text="BMI HISTORY",
            font=("Arial", 20, "bold")
        )
        history_label.pack(pady=15)

        # No records
        if not records:
            tk.Label(
                history_window,
                text="No records found.",
                font=("Arial", 13)
            ).pack(pady=30)

            return

        # Table frame
        table_frame = tk.Frame(history_window)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Table
        tree = ttk.Treeview(
            table_frame,
            columns=(
                "Name",
                "Weight",
                "Height",
                "BMI",
                "Category",
                "Date"
            ),
            show="headings",
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(
            command=tree.yview
        )

        # Headings
        tree.heading("Name", text="Name")
        tree.heading("Weight", text="Weight (kg)")
        tree.heading("Height", text="Height (m)")
        tree.heading("BMI", text="BMI")
        tree.heading("Category", text="Category")
        tree.heading("Date", text="Date")

        # Column widths
        tree.column("Name", width=130)
        tree.column("Weight", width=100)
        tree.column("Height", width=100)
        tree.column("BMI", width=80)
        tree.column("Category", width=120)
        tree.column("Date", width=180)

        # Insert records
        for record in records:

            record_id, name, weight, height, bmi, category, date = record

            tree.insert(
                "",
                "end",
                iid=str(record_id),
                values=(
                    name,
                    f"{weight:.1f}",
                    f"{height:.2f}",
                    f"{bmi:.2f}",
                    category,
                    date
                )
            )

        tree.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Delete selected record
        # ----------------------------------------------------

        def delete_selected():

            selected = tree.selection()

            if not selected:
                messagebox.showwarning(
                    "No Selection",
                    "Please select a record to delete."
                )
                return

            record_id = selected[0]

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this record?"
            )

            if not confirm:
                return

            success = delete_record(
                int(record_id)
            )

            if success:
                messagebox.showinfo(
                    "Deleted",
                    "BMI record deleted successfully."
                )

                history_window.destroy()
                view_history()

            else:
                messagebox.showerror(
                    "Database Error",
                    "Could not delete the BMI record."
                )

        # Delete button
        delete_button = tk.Button(
            history_window,
            text="Delete Selected",
            font=("Arial", 12, "bold"),
            command=delete_selected
        )

        delete_button.pack(
            pady=8
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Could not load BMI history.\n\n{error}"
        )


# ============================================================
# SHOW BMI GRAPH
# ============================================================

def show_bmi_graph():

    try:
        records = get_records()

        if not records:
            messagebox.showinfo(
                "BMI Trend",
                "No BMI records available."
            )
            return

        # Get current user's name
        selected_name = name_entry.get().strip()

        # If a name is entered, show only that user's records
        if selected_name:

            user_records = [
                record
                for record in records
                if record[1].lower() == selected_name.lower()
            ]

        else:

            messagebox.showwarning(
                "Name Required",
                "Please enter a name to view that user's BMI trend."
            )
            return

        if not user_records:

            messagebox.showinfo(
                "BMI Trend",
                f"No BMI records found for {selected_name}."
            )
            return

        # Reverse because get_records() returns newest first
        user_records = list(reversed(user_records))

        dates = []
        bmi_values = []

        for record in user_records:

            record_id, name, weight, height, bmi, category, date = record

            dates.append(date)
            bmi_values.append(bmi)

        # Create graph window
        graph_window = tk.Toplevel(window)

        graph_window.title(
            f"BMI Trend - {selected_name}"
        )

        graph_window.geometry(
            "850x550"
        )

        # Create figure
        figure = plt.Figure(
            figsize=(8, 5),
            dpi=100
        )

        axis = figure.add_subplot(111)

        # Plot BMI
        axis.plot(
            dates,
            bmi_values,
            marker="o",
            linewidth=2
        )

        # Title
        axis.set_title(
            f"BMI Trend - {selected_name}",
            fontsize=16,
            fontweight="bold"
        )

        axis.set_xlabel(
            "Date"
        )

        axis.set_ylabel(
            "BMI"
        )

        # BMI reference lines
        axis.axhline(
            18.5,
            linestyle="--",
            label="Underweight Limit"
        )

        axis.axhline(
            25,
            linestyle="--",
            label="Normal Limit"
        )

        axis.axhline(
            30,
            linestyle="--",
            label="Obese Limit"
        )

        # Grid
        axis.grid(
            True,
            alpha=0.3
        )

        # Legend
        axis.legend()

        # Rotate dates
        figure.autofmt_xdate()

        # Add graph to Tkinter
        canvas = FigureCanvasTkAgg(
            figure,
            master=graph_window
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    except Exception as error:

        messagebox.showerror(
            "Graph Error",
            f"Could not display BMI graph.\n\n{error}"
        )


# ============================================================
# CALCULATE BMI
# ============================================================

def calculate_bmi():

    try:

        # ----------------------------------------------------
        # Get input values
        # ----------------------------------------------------

        name = name_entry.get().strip()

        weight_text = weight_entry.get().strip()

        height_text = height_entry.get().strip()

        # ----------------------------------------------------
        # Validate name
        # ----------------------------------------------------

        if not name:

            result_label.config(
                text="Error: Please enter your name.",
                fg="red"
            )

            return

        # ----------------------------------------------------
        # Validate empty fields
        # ----------------------------------------------------

        if not weight_text:

            result_label.config(
                text="Error: Please enter your weight.",
                fg="red"
            )

            return

        if not height_text:

            result_label.config(
                text="Error: Please enter your height.",
                fg="red"
            )

            return

        # ----------------------------------------------------
        # Convert input to numbers
        # ----------------------------------------------------

        weight = float(weight_text)

        height = float(height_text)

        # ----------------------------------------------------
        # Validate weight
        # ----------------------------------------------------

        if weight <= 0:

            result_label.config(
                text="Error: Weight must be greater than zero.",
                fg="red"
            )

            return

        # ----------------------------------------------------
        # Validate height
        # ----------------------------------------------------

        if height <= 0:

            result_label.config(
                text="Error: Height must be greater than zero.",
                fg="red"
            )

            return

        # ----------------------------------------------------
        # Convert height
        #
        # Example:
        # 5.4 = 5 feet 4 inches
        # 5.7 = 5 feet 7 inches
        # ----------------------------------------------------

        feet = int(height)

        inches = round(
            (height - feet) * 10
        )

        # ----------------------------------------------------
        # Handle rounding such as 5.99
        # ----------------------------------------------------

        if inches >= 12:

            feet += inches // 12

            inches = inches % 12

        # ----------------------------------------------------
        # Validate height range
        # ----------------------------------------------------

        if feet < 3 or feet > 8:

            result_label.config(
                text="Error: Height must be between 3 and 8 feet.",
                fg="red"
            )

            return

        # ----------------------------------------------------
        # Validate inches
        # ----------------------------------------------------

        if inches < 0 or inches > 11:

            result_label.config(
                text="Error: Inches must be between 0 and 11.",
                fg="red"
            )

            return

        # ----------------------------------------------------
        # Convert feet/inches to meters
        # ----------------------------------------------------

        total_inches = (
            feet * 12
        ) + inches

        height_meters = (
            total_inches * 0.0254
        )

        # ----------------------------------------------------
        # Calculate BMI
        # ----------------------------------------------------

        bmi = (
            weight /
            (height_meters ** 2)
        )

        # ----------------------------------------------------
        # Determine BMI category
        # ----------------------------------------------------

        if bmi < 18.5:

            category = "Underweight"

            display_color = "orange"

        elif bmi < 25:

            category = "Normal"

            display_color = "green"

        elif bmi < 30:

            category = "Overweight"

            display_color = "orange"

        else:

            category = "Obese"

            display_color = "red"

        # ----------------------------------------------------
        # Save record to SQLite database
        # ----------------------------------------------------

        success = save_record(
            name,
            weight,
            height_meters,
            bmi,
            category
        )

        if not success:

            result_label.config(
                text="Error: Could not save BMI record.",
                fg="red"
            )

            return

        # ----------------------------------------------------
        # Display result
        # ----------------------------------------------------

        result_label.config(
            text=(
                f"Name: {name}\n"
                f"Height: {feet} ft {inches} in\n"
                f"Height: {height_meters:.2f} m\n"
                f"BMI: {bmi:.2f}\n"
                f"Category: {category}"
            ),
            fg=display_color
        )

    except ValueError:

        result_label.config(
            text="Error: Please enter numbers only.",
            fg="red"
        )

    except Exception as error:

        result_label.config(
            text=f"Unexpected error: {error}",
            fg="red"
        )


# ============================================================
# CLEAR INPUT
# ============================================================

def clear_fields():

    name_entry.delete(
        0,
        tk.END
    )

    weight_entry.delete(
        0,
        tk.END
    )

    height_entry.delete(
        0,
        tk.END
    )

    result_label.config(
        text="Enter your details and click Calculate BMI",
        fg="black"
    )

    name_entry.focus()


# ============================================================
# CREATE DATABASE
# ============================================================

if not create_database():

    messagebox.showerror(
        "Database Error",
        "Could not create or open the BMI database."
    )


# ============================================================
# CREATE MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title(
    "BMI Calculator"
)

window.geometry(
    "500x650"
)

window.resizable(
    False,
    False
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    window,
    text="BMI CALCULATOR",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=25
)


# ============================================================
# NAME
# ============================================================

name_label = tk.Label(
    window,
    text="Name:",
    font=("Arial", 13)
)

name_label.pack()


name_entry = tk.Entry(
    window,
    font=("Arial", 13),
    width=28
)

name_entry.pack(
    pady=8
)


# ============================================================
# WEIGHT
# ============================================================

weight_label = tk.Label(
    window,
    text="Weight (kg):",
    font=("Arial", 13)
)

weight_label.pack()


weight_entry = tk.Entry(
    window,
    font=("Arial", 13),
    width=28
)

weight_entry.pack(
    pady=8
)


# ============================================================
# HEIGHT
# ============================================================

height_label = tk.Label(
    window,
    text="Height (ft.in):",
    font=("Arial", 13)
)

height_label.pack()


height_entry = tk.Entry(
    window,
    font=("Arial", 13),
    width=28
)

height_entry.pack(
    pady=8
)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    window
)

button_frame.pack(
    pady=20
)


# ============================================================
# CALCULATE BUTTON
# ============================================================

calculate_button = tk.Button(
    button_frame,
    text="Calculate BMI",
    font=("Arial", 12, "bold"),
    width=16,
    command=calculate_bmi
)

calculate_button.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


# ============================================================
# CLEAR BUTTON
# ============================================================

clear_button = tk.Button(
    button_frame,
    text="Clear",
    font=("Arial", 12, "bold"),
    width=10,
    command=clear_fields
)

clear_button.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# ============================================================
# HISTORY BUTTON
# ============================================================

history_button = tk.Button(
    button_frame,
    text="View History",
    font=("Arial", 12, "bold"),
    width=16,
    command=view_history
)

history_button.grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


# ============================================================
# GRAPH BUTTON
# ============================================================

graph_button = tk.Button(
    button_frame,
    text="BMI Trend Graph",
    font=("Arial", 12, "bold"),
    width=16,
    command=show_bmi_graph
)

graph_button.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# ============================================================
# RESULT LABEL
# ============================================================

result_label = tk.Label(
    window,
    text="Enter your details and click Calculate BMI",
    font=("Arial", 13),
    justify="center",
    wraplength=450
)

result_label.pack(
    pady=25
)


# ============================================================
# FOOTER
# ============================================================

footer_label = tk.Label(
    window,
    text="OASIS INFOBYTE - Python Programming",
    font=("Arial", 9)
)

footer_label.pack(
    side="bottom",
    pady=10
)


# ============================================================
# START APPLICATION
# ============================================================

window.mainloop()