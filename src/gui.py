#!/usr/bin/env python3
"""
Graphical User Interface for the Base Converter utility.
Built with tkinter for cross-platform compatibility.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Dict, List, Optional

from src.converter import BaseConverter
from src.validation import InputValidator, ValidationError


class BaseConverterGUI:
    """Main GUI application for base conversion."""

    def __init__(self):
        """Initialize the GUI application."""
        self.converter = BaseConverter()
        self.validator = InputValidator()
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.setup_bindings()

        # Variables for tracking state
        self.history = []
        self.current_theme = "default"

    def setup_window(self):
        """Configure the main window."""
        self.root.title("Base Converter v1.0")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Configure icon if available
        try:
            # You would add an icon file here
            # self.root.iconbitmap("icon.ico")
            pass
        except:
            pass

        # Configure style
        style = ttk.Style()
        style.theme_use("clam")  # Modern cross-platform theme

    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        self.create_input_section(main_frame)
        self.create_conversion_section(main_frame)
        self.create_results_section(main_frame)
        self.create_tools_section(main_frame)
        self.create_status_bar()
        self.create_menu_bar()

    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_command(label="Load Batch", command=self.load_batch_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear All", command=self.clear_all)
        edit_menu.add_command(label="Copy Result", command=self.copy_result)
        edit_menu.add_command(label="Clear History", command=self.clear_history)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(
            label="Base Information", command=self.show_base_info_dialog
        )
        tools_menu.add_command(
            label="Arithmetic Calculator", command=self.show_arithmetic_dialog
        )
        tools_menu.add_command(label="Batch Converter", command=self.show_batch_dialog)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)

    def create_input_section(self, parent):
        """Create the input section of the GUI."""
        # Input frame
        input_frame = ttk.LabelFrame(parent, text="Input", padding="10")
        input_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        input_frame.columnconfigure(1, weight=1)

        # Number input
        ttk.Label(input_frame, text="Number:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )
        self.number_var = tk.StringVar()
        self.number_entry = ttk.Entry(
            input_frame, textvariable=self.number_var, font=("Consolas", 11)
        )
        self.number_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))

        # Detect base button
        self.detect_button = ttk.Button(
            input_frame, text="Detect Base", command=self.detect_base
        )
        self.detect_button.grid(row=0, column=2, padx=(5, 0))

        # Source base
        ttk.Label(input_frame, text="From Base:").grid(
            row=1, column=0, sticky=tk.W, pady=(10, 0), padx=(0, 5)
        )
        self.from_base_var = tk.StringVar(value="10")
        self.from_base_combo = ttk.Combobox(
            input_frame, textvariable=self.from_base_var, width=15
        )
        self.from_base_combo["values"] = [str(i) for i in range(2, 37)]
        self.from_base_combo.grid(
            row=1, column=1, sticky=tk.W, pady=(10, 0), padx=(0, 5)
        )

        # Common base buttons for input
        base_frame = ttk.Frame(input_frame)
        base_frame.grid(row=1, column=2, pady=(10, 0), padx=(5, 0))

        ttk.Button(
            base_frame, text="Bin", width=5, command=lambda: self.set_base("from", 2)
        ).grid(row=0, column=0, padx=1)
        ttk.Button(
            base_frame, text="Oct", width=5, command=lambda: self.set_base("from", 8)
        ).grid(row=0, column=1, padx=1)
        ttk.Button(
            base_frame, text="Dec", width=5, command=lambda: self.set_base("from", 10)
        ).grid(row=0, column=2, padx=1)
        ttk.Button(
            base_frame, text="Hex", width=5, command=lambda: self.set_base("from", 16)
        ).grid(row=0, column=3, padx=1)

    def create_conversion_section(self, parent):
        """Create the conversion controls section."""
        convert_frame = ttk.LabelFrame(parent, text="Convert To", padding="10")
        convert_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        convert_frame.columnconfigure(1, weight=1)

        # Target base
        ttk.Label(convert_frame, text="To Base:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )
        self.to_base_var = tk.StringVar(value="2")
        self.to_base_combo = ttk.Combobox(
            convert_frame, textvariable=self.to_base_var, width=15
        )
        self.to_base_combo["values"] = [str(i) for i in range(2, 37)]
        self.to_base_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 5))

        # Convert button
        self.convert_button = ttk.Button(
            convert_frame, text="Convert", command=self.convert_number
        )
        self.convert_button.grid(row=0, column=2, padx=(10, 5))

        # Common base buttons for output
        out_base_frame = ttk.Frame(convert_frame)
        out_base_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        ttk.Button(
            out_base_frame, text="Binary", command=lambda: self.quick_convert(2)
        ).grid(row=0, column=0, padx=2)
        ttk.Button(
            out_base_frame, text="Octal", command=lambda: self.quick_convert(8)
        ).grid(row=0, column=1, padx=2)
        ttk.Button(
            out_base_frame, text="Decimal", command=lambda: self.quick_convert(10)
        ).grid(row=0, column=2, padx=2)
        ttk.Button(
            out_base_frame, text="Hexadecimal", command=lambda: self.quick_convert(16)
        ).grid(row=0, column=3, padx=2)
        ttk.Button(
            out_base_frame, text="Show Table", command=self.show_conversion_table
        ).grid(row=0, column=4, padx=2)

    def create_results_section(self, parent):
        """Create the results display section."""
        results_frame = ttk.LabelFrame(parent, text="Results", padding="10")
        results_frame.grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)

        # Result display with larger font
        self.result_var = tk.StringVar()
        result_label = ttk.Label(
            results_frame,
            textvariable=self.result_var,
            font=("Consolas", 14, "bold"),
            foreground="darkgreen",
            background="lightgray",
            padding="5",
        )
        result_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # History text area
        history_label = ttk.Label(results_frame, text="Conversion History:")
        history_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))

        self.history_text = scrolledtext.ScrolledText(
            results_frame, height=8, width=70, font=("Consolas", 9), state=tk.DISABLED
        )
        self.history_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_tools_section(self, parent):
        """Create the tools and options section."""
        tools_frame = ttk.LabelFrame(parent, text="Options", padding="5")
        tools_frame.grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5)
        )

        # Formatting options
        self.add_prefix_var = tk.BooleanVar()
        self.format_separators_var = tk.BooleanVar()
        self.uppercase_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            tools_frame, text="Add prefix (0x, 0b, 0o)", variable=self.add_prefix_var
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Checkbutton(
            tools_frame,
            text="Format with separators",
            variable=self.format_separators_var,
        ).grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        ttk.Checkbutton(
            tools_frame, text="Uppercase letters", variable=self.uppercase_var
        ).grid(row=0, column=2, sticky=tk.W)

    def create_status_bar(self):
        """Create the status bar."""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root, textvariable=self.status_var, relief=tk.SUNKEN, padding="5"
        )
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def setup_bindings(self):
        """Setup keyboard bindings and events."""
        # Enter key converts
        self.number_entry.bind("<Return>", lambda e: self.convert_number())

        # Auto-conversion on input change (with delay)
        self.number_var.trace("w", self.on_input_change)
        self.from_base_var.trace("w", self.on_base_change)
        self.to_base_var.trace("w", self.on_base_change)

        # Copy result on double-click
        self.result_var.trace("w", lambda *args: self.setup_result_click())

    def setup_result_click(self):
        """Setup click-to-copy on result."""
        # This is called when result changes to setup the click binding
        pass

    def on_input_change(self, *args):
        """Handle input change events."""
        # Clear any previous error status
        self.status_var.set("Ready")

    def on_base_change(self, *args):
        """Handle base change events."""
        # Auto-convert if there's input
        if self.number_var.get().strip():
            self.convert_number()

    def set_base(self, base_type: str, base: int):
        """Set the from or to base."""
        if base_type == "from":
            self.from_base_var.set(str(base))
        else:
            self.to_base_var.set(str(base))

    def detect_base(self):
        """Detect the base of the input number."""
        number = self.number_var.get().strip()
        if not number:
            messagebox.showwarning("Warning", "Please enter a number first.")
            return

        try:
            detected = self.converter.detect_base(number)
            if detected:
                self.from_base_var.set(str(detected))
                self.status_var.set(f"Detected base: {detected}")
            else:
                self.status_var.set("Could not detect base automatically")
        except Exception as e:
            messagebox.showerror("Error", f"Error detecting base: {e}")

    def convert_number(self):
        """Perform the base conversion."""
        try:
            # Get input values
            number = self.number_var.get().strip()
            from_base = int(self.from_base_var.get())
            to_base = int(self.to_base_var.get())

            if not number:
                self.status_var.set("Please enter a number")
                return

            # Validate input
            validated_number, _ = self.validator.validate_number_for_base(
                number, from_base
            )

            # Perform conversion
            result = self.converter.convert_base(validated_number, from_base, to_base)

            # Apply formatting options
            formatted_result = self.format_result(result, to_base)

            # Display result
            self.result_var.set(formatted_result)

            # Add to history
            history_entry = (
                f"{number} (base {from_base}) → {formatted_result} (base {to_base})"
            )
            self.add_to_history(history_entry)

            self.status_var.set("Conversion successful")

        except ValidationError as e:
            self.result_var.set("Invalid Input")
            self.status_var.set(f"Validation error: {e}")
        except Exception as e:
            self.result_var.set("Error")
            self.status_var.set(f"Error: {e}")

    def format_result(self, result: str, base: int) -> str:
        """Apply formatting options to the result."""
        formatted = result

        # Apply case conversion
        if self.uppercase_var.get():
            formatted = formatted.upper()
        else:
            formatted = formatted.lower()

        # Add separators
        if self.format_separators_var.get():
            formatted = self.converter.format_number_with_separators(formatted, base)

        # Add prefix
        if self.add_prefix_var.get():
            prefixes = {2: "0b", 8: "0o", 16: "0x"}
            prefix = prefixes.get(base, "")
            if prefix and not formatted.lower().startswith(prefix):
                is_negative = formatted.startswith("-")
                if is_negative:
                    formatted = "-" + prefix + formatted[1:]
                else:
                    formatted = prefix + formatted

        return formatted

    def quick_convert(self, target_base: int):
        """Quick conversion to a specific base."""
        self.to_base_var.set(str(target_base))
        self.convert_number()

    def show_conversion_table(self):
        """Show conversion table in a popup window."""
        number = self.number_var.get().strip()
        if not number:
            messagebox.showwarning("Warning", "Please enter a number first.")
            return

        try:
            from_base = int(self.from_base_var.get())
            table = self.converter.get_conversion_table(number, from_base)

            # Create popup window
            table_window = tk.Toplevel(self.root)
            table_window.title("Conversion Table")
            table_window.geometry("400x300")
            table_window.resizable(False, False)

            # Create table
            frame = ttk.Frame(table_window, padding="10")
            frame.pack(fill=tk.BOTH, expand=True)

            ttk.Label(
                frame,
                text=f"Conversion table for '{number}' (base {from_base})",
                font=("Arial", 12, "bold"),
            ).pack(pady=(0, 10))

            # Table headers
            headers_frame = ttk.Frame(frame)
            headers_frame.pack(fill=tk.X, pady=(0, 5))

            ttk.Label(
                headers_frame, text="Base", font=("Arial", 10, "bold"), width=8
            ).pack(side=tk.LEFT)
            ttk.Label(
                headers_frame, text="Name", font=("Arial", 10, "bold"), width=15
            ).pack(side=tk.LEFT)
            ttk.Label(headers_frame, text="Value", font=("Arial", 10, "bold")).pack(
                side=tk.LEFT
            )

            # Separator
            ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

            # Table content
            base_names = {2: "Binary", 8: "Octal", 10: "Decimal", 16: "Hexadecimal"}

            for base in [2, 8, 10, 16]:
                row_frame = ttk.Frame(frame)
                row_frame.pack(fill=tk.X, pady=2)

                ttk.Label(
                    row_frame, text=str(base), width=8, font=("Consolas", 9)
                ).pack(side=tk.LEFT)
                ttk.Label(
                    row_frame, text=base_names[base], width=15, font=("Arial", 9)
                ).pack(side=tk.LEFT)
                ttk.Label(
                    row_frame, text=table[base], font=("Consolas", 9, "bold")
                ).pack(side=tk.LEFT)

        except Exception as e:
            messagebox.showerror("Error", f"Error generating table: {e}")

    def add_to_history(self, entry: str):
        """Add an entry to the conversion history."""
        self.history.append(entry)

        # Update history display
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)

        # Limit history size
        if len(self.history) > 100:
            self.history.pop(0)
            # Remove oldest line from display
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete("1.0", "2.0")
            self.history_text.config(state=tk.DISABLED)

    def clear_all(self):
        """Clear all input and results."""
        self.number_var.set("")
        self.result_var.set("")
        self.status_var.set("Cleared")

    def clear_history(self):
        """Clear the conversion history."""
        self.history.clear()
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        self.history_text.config(state=tk.DISABLED)
        self.status_var.set("History cleared")

    def copy_result(self):
        """Copy the result to clipboard."""
        result = self.result_var.get()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_var.set("Result copied to clipboard")
        else:
            self.status_var.set("No result to copy")

    def save_results(self):
        """Save conversion history to a file."""
        if not self.history:
            messagebox.showinfo("Info", "No history to save.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if filename:
            try:
                with open(filename, "w") as f:
                    f.write("Base Converter - Conversion History\n")
                    f.write("=" * 40 + "\n\n")
                    for entry in self.history:
                        f.write(entry + "\n")
                self.status_var.set(f"History saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {e}")

    def load_batch_file(self):
        """Load numbers from a file for batch conversion."""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            self.show_batch_dialog(filename)

    def show_base_info_dialog(self):
        """Show dialog with information about bases."""
        info_window = tk.Toplevel(self.root)
        info_window.title("Base Information")
        info_window.geometry("500x400")

        frame = ttk.Frame(info_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Supported Number Bases", font=("Arial", 14, "bold")
        ).pack(pady=(0, 10))

        # Create scrollable text widget
        text_widget = scrolledtext.ScrolledText(
            frame, height=20, width=60, font=("Consolas", 9)
        )
        text_widget.pack(fill=tk.BOTH, expand=True)

        # Add base information
        info_text = "Common Bases:\n\n"
        common_bases = [2, 8, 10, 16, 36]

        for base in common_bases:
            info = self.converter.get_base_info(base)
            info_text += f"Base {base} - {info['name']}\n"
            info_text += (
                f"  Digits: {', '.join(info['digits'][:min(10, len(info['digits']))])}"
            )
            if len(info["digits"]) > 10:
                info_text += "..."
            info_text += f"\n  Range: 0 to {info['max_digit']}\n"
            if info["common_prefixes"]:
                info_text += f"  Prefixes: {', '.join(info['common_prefixes'])}\n"
            info_text += "\n"

        info_text += "All bases from 2 to 36 are supported.\n"
        info_text += "Digits used: 0-9, A-Z"

        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)

    def show_arithmetic_dialog(self):
        """Show arithmetic calculator dialog."""
        calc_window = tk.Toplevel(self.root)
        calc_window.title("Arithmetic Calculator")
        calc_window.geometry("400x300")
        calc_window.resizable(False, False)

        frame = ttk.Frame(calc_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Input fields
        ttk.Label(frame, text="First Number:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        num1_var = tk.StringVar()
        ttk.Entry(frame, textvariable=num1_var, width=20).grid(
            row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5
        )

        ttk.Label(frame, text="Second Number:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        num2_var = tk.StringVar()
        ttk.Entry(frame, textvariable=num2_var, width=20).grid(
            row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5
        )

        ttk.Label(frame, text="Base:").grid(row=2, column=0, sticky=tk.W, pady=5)
        base_var = tk.StringVar(value="10")
        ttk.Combobox(
            frame,
            textvariable=base_var,
            values=[str(i) for i in range(2, 37)],
            width=10,
        ).grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(frame, text="Operation:").grid(row=3, column=0, sticky=tk.W, pady=5)
        op_var = tk.StringVar(value="+")
        ttk.Combobox(
            frame, textvariable=op_var, values=["+", "-", "*", "/", "%", "**"], width=10
        ).grid(row=3, column=1, sticky=tk.W, pady=5)

        # Result
        ttk.Label(frame, text="Result:").grid(row=4, column=0, sticky=tk.W, pady=5)
        result_var = tk.StringVar()
        ttk.Label(
            frame,
            textvariable=result_var,
            font=("Consolas", 10, "bold"),
            foreground="darkgreen",
        ).grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        def calculate():
            try:
                num1 = num1_var.get().strip()
                num2 = num2_var.get().strip()
                base = int(base_var.get())
                operation = op_var.get()

                if not num1 or not num2:
                    messagebox.showwarning("Warning", "Please enter both numbers.")
                    return

                # Validate numbers
                self.validator.validate_number_for_base(num1, base)
                self.validator.validate_number_for_base(num2, base)

                # Convert to decimal for calculation
                dec1 = self.converter.base_to_decimal(num1, base)
                dec2 = self.converter.base_to_decimal(num2, base)

                # Perform operation
                if operation == "+":
                    result = dec1 + dec2
                elif operation == "-":
                    result = dec1 - dec2
                elif operation == "*":
                    result = dec1 * dec2
                elif operation == "/":
                    if dec2 == 0:
                        raise ValueError("Division by zero")
                    result = dec1 // dec2
                elif operation == "%":
                    if dec2 == 0:
                        raise ValueError("Division by zero")
                    result = dec1 % dec2
                elif operation == "**":
                    result = dec1**dec2

                # Convert back to original base
                final_result = self.converter.decimal_to_base(result, base)
                result_var.set(final_result)

            except Exception as e:
                messagebox.showerror("Error", f"Calculation error: {e}")

        ttk.Button(frame, text="Calculate", command=calculate).grid(
            row=5, column=1, pady=10
        )

    def show_batch_dialog(self, filename: Optional[str] = None):
        """Show batch conversion dialog."""
        batch_window = tk.Toplevel(self.root)
        batch_window.title("Batch Converter")
        batch_window.geometry("600x500")

        frame = ttk.Frame(batch_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Batch Conversion", font=("Arial", 12, "bold")).pack(
            pady=(0, 10)
        )

        # Input area
        input_frame = ttk.LabelFrame(frame, text="Numbers (one per line)", padding="5")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        input_text = scrolledtext.ScrolledText(
            input_frame, height=10, width=70, font=("Consolas", 9)
        )
        input_text.pack(fill=tk.BOTH, expand=True)

        if filename:
            try:
                with open(filename, "r") as f:
                    input_text.insert(tk.END, f.read())
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file: {e}")

        # Controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_frame, text="From Base:").pack(side=tk.LEFT, padx=(0, 5))
        from_base_var = tk.StringVar(value="10")
        ttk.Combobox(
            control_frame,
            textvariable=from_base_var,
            values=[str(i) for i in range(2, 37)],
            width=5,
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(control_frame, text="To Base:").pack(side=tk.LEFT, padx=(0, 5))
        to_base_var = tk.StringVar(value="2")
        ttk.Combobox(
            control_frame,
            textvariable=to_base_var,
            values=[str(i) for i in range(2, 37)],
            width=5,
        ).pack(side=tk.LEFT, padx=(0, 10))

        def process_batch():
            try:
                numbers = [
                    line.strip()
                    for line in input_text.get("1.0", tk.END).splitlines()
                    if line.strip()
                ]
                if not numbers:
                    messagebox.showwarning("Warning", "Please enter some numbers.")
                    return

                from_base = int(from_base_var.get())
                to_base = int(to_base_var.get())

                results = []
                for number in numbers:
                    try:
                        result = self.converter.convert_base(number, from_base, to_base)
                        results.append(f"{number} -> {result}")
                    except Exception as e:
                        results.append(f"{number} -> Error: {e}")

                # Show results
                result_window = tk.Toplevel(batch_window)
                result_window.title("Batch Results")
                result_window.geometry("500x400")

                result_frame = ttk.Frame(result_window, padding="10")
                result_frame.pack(fill=tk.BOTH, expand=True)

                result_text = scrolledtext.ScrolledText(
                    result_frame, font=("Consolas", 9)
                )
                result_text.pack(fill=tk.BOTH, expand=True)

                result_text.insert(tk.END, "\n".join(results))
                result_text.config(state=tk.DISABLED)

            except Exception as e:
                messagebox.showerror("Error", f"Error processing batch: {e}")

        ttk.Button(control_frame, text="Convert All", command=process_batch).pack(
            side=tk.RIGHT
        )

    def show_help(self):
        """Show help dialog."""
        help_window = tk.Toplevel(self.root)
        help_window.title("Base Converter - Help")
        help_window.geometry("600x500")

        frame = ttk.Frame(help_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        help_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Arial", 9))
        help_text.pack(fill=tk.BOTH, expand=True)

        help_content = """Base Converter - User Guide

BASIC USAGE:
1. Enter a number in the "Number" field
2. Select the source base ("From Base")
3. Select the target base ("To Base")
4. Click "Convert" or press Enter

QUICK CONVERSION:
- Use the Binary, Octal, Decimal, Hexadecimal buttons for quick conversion
- Click "Detect Base" to automatically detect the input base

INPUT FORMATS:
- Regular numbers: 123, ABC, 1010
- With prefixes: 0x1A (hex), 0b1010 (binary), 0o777 (octal)
- Negative numbers: -123, -0xFF

FEATURES:
- Conversion Table: Shows the number in all common bases
- Arithmetic Calculator: Perform calculations in any base
- Batch Converter: Convert multiple numbers at once
- History: Track all conversions
- Export: Save results to file

SUPPORTED BASES:
- Base 2 (Binary): Uses digits 0, 1
- Base 8 (Octal): Uses digits 0-7
- Base 10 (Decimal): Uses digits 0-9
- Base 16 (Hexadecimal): Uses digits 0-9, A-F
- All bases from 2 to 36 are supported

KEYBOARD SHORTCUTS:
- Enter: Convert number
- Ctrl+C: Copy result (when result is selected)

OPTIONS:
- Add Prefix: Adds 0x, 0b, 0o prefixes to results
- Format with Separators: Adds underscores for readability
- Uppercase Letters: Controls letter case in results

For more information, visit the project repository."""

        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)

    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            "Base Converter v1.0\n\n"
            "A comprehensive cross-platform base conversion utility\n\n"
            "Features:\n"
            "• Convert between bases 2-36\n"
            "• GUI and command-line interfaces\n"
            "• Arithmetic operations\n"
            "• Batch processing\n"
            "• Input validation\n\n"
            "Built with Python and Tkinter",
        )

    def run(self):
        """Start the GUI application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass


def main():
    """Entry point for the GUI application."""
    app = BaseConverterGUI()
    app.run()


if __name__ == "__main__":
    main()
