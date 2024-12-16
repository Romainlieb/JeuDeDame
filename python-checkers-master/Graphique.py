import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

def plot_essai_reward(Essai, Rewards, plot_type='line'):
    """
    Function to plot the number of trials (Essai) on the x-axis and the rewards (Rewards) on the y-axis.
    
    Parameters:
    Essai (list): List of trial numbers.
    Rewards (list): List of reward values corresponding to each trial.
    plot_type (str): Type of plot ('line', 'bar', 'scatter').
    """
    # Check if Essai and Rewards are lists and have the same length
    if not isinstance(Essai, list):
        raise ValueError("Essai must be a list.")
    if not isinstance(Rewards, list):
        raise ValueError("Rewards must be a list.")
    if len(Essai) != len(Rewards):
        raise ValueError("Essai and Rewards must have the same length.")
    
    # Create the figure and axis
    fig, ax = plt.subplots()
    
    # Plot the data based on the plot_type
    if plot_type == 'line':
        ax.plot(Essai, Rewards, marker='o', linestyle='-')
    elif plot_type == 'bar':
        ax.bar(Essai, Rewards)
    elif plot_type == 'scatter':
        ax.scatter(Essai, Rewards)
    else:
        raise ValueError("Invalid plot_type. Choose from 'line', 'bar', or 'scatter'.")
    
    ax.set_xlabel('Nombre d\'essai')
    ax.set_ylabel('Reward (R)')
    ax.set_title('Essai vs Reward')
    ax.grid(True)
    
    return fig

def on_plot_button_click():
    plot_type = plot_type_var.get()
    fig = plot_essai_reward(Essai, Rewards, plot_type)
    
    # Clear the previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    # Display the new plot
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def on_closing():
    root.quit()
    root.destroy()

# Example usage
Essai = [1, 2, 3, 4, 5]
Rewards = [2.0, 5.0, 3.5, 4.0, 6.0]

# Create the main window
root = tk.Tk()
root.title("Choose Plot Type")

# Bind the window close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create a frame for the plot
plot_frame = tk.Frame(root)
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a frame for the controls
control_frame = tk.Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create a label
label = tk.Label(control_frame, text="Choose the type of plot:")
label.pack(side=tk.LEFT, padx=10, pady=10)

# Create a combobox for plot type selection
plot_type_var = tk.StringVar(value='line')
plot_type_combobox = ttk.Combobox(control_frame, textvariable=plot_type_var, values=['line', 'bar', 'scatter'])
plot_type_combobox.pack(side=tk.LEFT, padx=10, pady=10)

# Create a button to plot
plot_button = tk.Button(control_frame, text="Plot", command=on_plot_button_click)
plot_button.pack(side=tk.LEFT, padx=10, pady=10)

# Initial plot
on_plot_button_click()

# Run the GUI event loop
root.mainloop()