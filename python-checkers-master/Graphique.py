import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
class Graphics:
    def __init__(self, rewards, color_up):
        self.Rewards = rewards
        self.Essai = []
        for i in range(len(self.Rewards)):
            self.Essai.append(i)
        self.color_up = color_up
        self.plot_type_var = None
        self.plot_frame = None
        self.root = None

    def plot_essai_reward(self,Essai, Rewards, plot_type='line'):
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
        color = ""
        if self.color_up == 'W':
            color = 'Blanc'
        else:
            color = 'Noir'
        ax.set_xlabel('Nombre d\'essai')
        ax.set_ylabel('Reward (R)')
        ax.set_title('Essai vs Reward pour '+color)
        ax.grid(True)
        
        return fig

    def save_plot_as_image(self,plot_type='line', filename='plot.png'):
        """
        Function to plot the number of trials (Essai) on the x-axis and the rewards (Rewards) on the y-axis,
        and save the plot as an image file.
        
        Parameters:
        Essai (list): List of trial numbers.
        Rewards (list): List of reward values corresponding to each trial.
        plot_type (str): Type of plot ('line', 'bar', 'scatter').
        filename (str): The name of the file to save the plot image.
        """
        # Check if Essai and Rewards are lists and have the same length
        if not isinstance(self.Essai, list):
            raise ValueError("self.Essai must be a list.")
        if not isinstance(self.Rewards, list):
            raise ValueError("self.Rewards must be a list.")
        if len(self.Essai) != len(self.Rewards):
            raise ValueError("self.Essai and self.Rewards must have the same length.")
        
        # Create the figure and axis
        fig, ax = plt.subplots()
        
        # Plot the data based on the plot_type
        if plot_type == 'line':
            ax.plot(self.Essai, self.Rewards, marker='o', linestyle='-')
        elif plot_type == 'bar':
            ax.bar(self.Essai, self.Rewards)
        elif plot_type == 'scatter':
            ax.scatter(self.Essai, self.Rewards)
        else:
            raise ValueError("Invalid plot_type. Choose from 'line', 'bar', or 'scatter'.")
        
        color = "Blanc" if self.color_up == 'W' else "Noir"
        ax.set_xlabel('Nombre d\'essai')
        ax.set_ylabel('Reward (R)')
        ax.set_title('Essai vs Reward pour ' + color)
        ax.grid(True)
        
        # Save the plot as an image file
        fig.savefig(filename)
        plt.close(fig)

    def on_plot_button_click(self):
        plot_type = self.plot_type_var.get()
        fig = self.plot_essai_reward(self.Essai, self.Rewards, plot_type)
        
        # Clear the previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Display the new plot
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def on_closing(self):
        self.root.quit()
        self.root.destroy()

    def show_plot(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Choose Plot Type")

        # Bind the window close event to the on_closing function
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create a frame for the plot
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a frame for the controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a label
        label = tk.Label(control_frame, text="Choose the type of plot:")
        label.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a combobox for plot type selection
        self.plot_type_var = tk.StringVar(value='line')
        plot_type_combobox = ttk.Combobox(control_frame, textvariable=self.plot_type_var, values=['line', 'bar', 'scatter'])
        plot_type_combobox.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a button to plot
        plot_button = tk.Button(control_frame, text="Plot", command=self.on_plot_button_click)
        plot_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Initial plot
        self.on_plot_button_click()

        # Run the GUI event loop
        self.root.mainloop()

