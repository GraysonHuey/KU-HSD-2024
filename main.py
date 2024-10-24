from tkinter import Label, Button, Tk, filedialog, messagebox
from tkinter.ttk import Combobox
from matplotlib import pyplot as plt
from statistics import mean
from typing import List, Dict

# ******IF QUERYING A SINGLE VALUE, YOU CAN PUT ANYTHING IN FOR THE END DATE, BUT THERE MUST BE******
# ******SOME VALUE THERE. YOU WILL NOT RECIEVE RESULTS IF THERE IS NOTHING IN THE BOX.*******

# Sample Weather Data
###############################################################################
# date: 2024-04-24 2024-04-25 2024-04-26 2024-04-27 2024-04-28 2024-04-29     #
# weather_code: 3.0 61.0 3.0 55.0 3.0 63.0                                    #
# temperature_max: 54.9464 52.6064 61.9664 52.2464 52.6064 48.4664            #
# temperature_min: 44.2364 47.1164 48.6464 47.9264 42.796402 40.0064          #
# precipitation_sum: 0.0 0.22440945 0.0 0.1456693 0.0 0.2952756               #
# wind_speed_max: 9.309791 10.116089 8.249648 10.711936 13.588738 7.4495792   #
# precipitation_probability_max: 45.0 100.0 100.0 100.0 97.0 100.0            #
###############################################################################

global weatherData
global resultEntry
global resultEntry2
global root


def loadData() -> Dict[str, List[float]]:
    data = {}
    try:
        # Opens a file dialog to let the user choose a file
        filePath = filedialog.askopenfilename(title="Select Data File", filetypes=[("Text files", "*.txt")])
        with open(filePath, 'r') as file:
            # Reads the first line of dates and assigns them to the dictionary
            dates = file.readline().strip().split()
            data["dates"] = dates
            for line in file:
                # Splits each line into a data label and its associated values
                dataPoint, *values = line.strip().split()
                # Converts the values into floats and adds them to the dictionary
                data[dataPoint.rstrip(":")] = [float(value) for value in values]

        ##print(f"\x1b[1;30;44m{data}")  # Debug print to view loaded data
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")
    histogram(data)
    return data


def histogram(data: Dict[str, List[float]]) -> None:
    # List of data categories to plot
    data_points = [
        "weather_code",
        "temperature_max",
        "temperature_min",
        "precipitation_sum",
        "wind_speed_max",
        "precipitation_probability_max"
    ]

    # Creates a 2x3 grid for the histograms
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Weather Data Histograms')  # Title for the entire figure

    # Flatten the axis array to easily loop through each subplot
    axs_flat = axs.flatten()

    # Dictionary specifying the number of bins for each data point
    bin_counts = {
        "weather_code": 15,
        "temperature_max": 20,
        "temperature_min": 20,
        "precipitation_sum": 12,
        "wind_speed_max": 15,
        "precipitation_probability_max": 20
    }

    # Loop through each data category and create a histogram
    for idx, data_point in enumerate(data_points):
        ax = axs_flat[idx]
        values = data[data_point]

        # Plotting the histogram for the current data category
        ax.hist(values, bins=bin_counts[data_point], edgecolor='black', alpha=0.7)
        ax.set_title(data_point.replace('_', ' ').title())  # Titles for each subplot
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)  # Grid lines with transparency for better readability
        ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better spacing

    plt.tight_layout()  # Adjust subplots to fit into the figure area
    plt.show()  # Display the histograms


def runQuery(queryType: str, dataPoint: str, start: int, end: int, type: str | None = None) -> int | None:
    global root
    global resultEntry

    # Convert the data point name into a format matching the data keys
    dataPoint = dataPoint.lower().replace(' ', '_')

    # Perform different operations based on the selected query type
    match queryType:
        case "max":
            result = max(weatherData[dataPoint][start:end + 1])
        case "min":
            result = min(weatherData[dataPoint][start:end + 1])
        case "average":
            result = mean(weatherData[dataPoint][start:end + 1])
        case "single":
            result = weatherData[dataPoint][start]
    
    if type == "compare":
        return result

    # Display the result in the resultEntry label
    resultEntry.config(text=f"Result: {result}", font=("Arial", 14, "bold"), fg="blue")


def compare(value1: int, value2: int) -> None:
    global resultEntry2
    if value1 > value2:
        resultEntry2.config(text=f"Result: Data value 1 is greater than data value 2", font=("Arial", 14, "bold"), fg="blue")
    else:
        resultEntry2.config(text=f"Result: Data value 2 is greater than data value 1", font=("Arial", 14, "bold"), fg="blue")


def setupGUI() -> None:
    global weatherData
    global resultEntry
    global resultEntry2

    root.configure(bg="#b6faee")  # Set background color of the main window

    # Button to load new weather data
    dataButton = Button(root, text="Load New Data", command=loadData, font=("Arial", 12, "bold"))
    dataButton.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Dropdown for selecting the type of query (max, min, average, or single)
    queryTypeLabel = Label(root, text="Query Type:", font=("Arial", 12, "bold"), bg="#b6faee")
    queryTypeLabel.grid(row=1, column=0, padx=10, pady=10)

    queryTypeEntry = Combobox(root, values=["max", "min", "average", "single"], width=25, font=("Arial", 12))
    queryTypeEntry.grid(row=1, column=1, padx=10, pady=10)

    # Dropdown for selecting which weather data point to query
    dataPointLabel = Label(root, text="Data Point:", font=("Arial", 12, "bold"), bg="#b6faee")
    dataPointLabel.grid(row=2, column=0, padx=10, pady=10)

    dataPointEntry = Combobox(root, values=["Weather Code", "Temperature Max", "Temperature Min", "Precipitation Sum",
                                            "Wind Speed Max", "Precipitation Probability Max"], width=25,
                              font=("Arial", 12))
    dataPointEntry.grid(row=2, column=1, padx=10, pady=10)

    # Dropdown for selecting the start date index for the query
    startLabel = Label(root, text="Start Date:", font=("Arial", 12, "bold"), bg="#b6faee")
    startLabel.grid(row=3, column=0, padx=10, pady=10)

    startEntry = Combobox(root, values=list(range(len(weatherData["dates"]) - 1)), width=25, font=("Arial", 12))
    startEntry.grid(row=3, column=1, padx=10, pady=10)

    # Dropdown for selecting the end date index for the query
    endLabel = Label(root, text="End Date:", font=("Arial", 12, "bold"), bg="#b6faee")
    endLabel.grid(row=4, column=0, padx=10, pady=10)

    endEntry = Combobox(root, values=list(range(len(weatherData["dates"]) - 1)), width=25, font=("Arial", 12))
    endEntry.grid(row=4, column=1, padx=10, pady=10)

    # Button to run the query based on user input
    queryButton = Button(root, text="Run Query", font=("Arial", 12, "bold"),
                        command=lambda: runQuery(queryTypeEntry.get(), dataPointEntry.get(),
                                                int(startEntry.get()), int(endEntry.get())))

    queryButton.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Label to display the results of the query
    resultLabel = Label(root, text="Results:", font=("Arial", 12, "bold"), bg="#b6faee")
    resultLabel.grid(row=6, column=0, padx=10, pady=10)

    # Label widget where the query result will be shown
    resultEntry = Label(root, text="Results will be displayed here", font=("Arial", 12, "italic"), bg="#ffffff",
                        borderwidth=2, relief="solid", width=40)
    resultEntry.grid(row=6, column=1, padx=10, pady=10)

    typeLabel1 = Label(root, text="Query type 1:", font=("Arial", 12, "bold"), bg="#b6faee")
    typeLabel1.grid(row=7, column=0, padx=10, pady=10)

    typeEntry1 = Combobox(root, values=["max", "min", "average", "single"], width=25, font=("Arial", 12))
    typeEntry1.grid(row=7, column=1, padx=10, pady=10)

    dataPointLabel1 = Label(root, text="Data Point:", font=("Arial", 12, "bold"), bg="#b6faee")
    dataPointLabel1.grid(row=8, column=0, padx=10, pady=10)

    dataPointEntry1 = Combobox(root, values=["Weather Code", "Temperature Max", "Temperature Min", "Precipitation Sum",
                                            "Wind Speed Max", "Precipitation Probability Max"], width=25,
                              font=("Arial", 12))
    dataPointEntry1.grid(row=8, column=1, padx=10, pady=10)

    startLabel1 = Label(root, text="Start Date:", font=("Arial", 12, "bold"), bg="#b6faee")
    startLabel1.grid(row=9, column=0, padx=10, pady=10)

    startEntry1 = Combobox(root, values=list(range(len(weatherData["dates"]) - 1)), width=25, font=("Arial", 12))
    startEntry1.grid(row=9, column=1, padx=10, pady=10)

    # Dropdown for selecting the end date index for the query
    endLabel1 = Label(root, text="End Date:", font=("Arial", 12, "bold"), bg="#b6faee")
    endLabel1.grid(row=10, column=0, padx=10, pady=10)

    endEntry1 = Combobox(root, values=list(range(len(weatherData["dates"]) - 1)), width=25, font=("Arial", 12))
    endEntry1.grid(row=10, column=1, padx=10, pady=10)

    typeLabel2 = Label(root, text="Query type 2:", font=("Arial", 12, "bold"), bg="#b6faee")
    typeLabel2.grid(row=7, column=3, padx=10, pady=10)

    typeEntry2 = Combobox(root, values=["max", "min", "average", "single"], width=25, font=("Arial", 12))
    typeEntry2.grid(row=7, column=4, padx=10, pady=10)

    dataPointLabel2 = Label(root, text="Data Point:", font=("Arial", 12, "bold"), bg="#b6faee")
    dataPointLabel2.grid(row=8, column=3, padx=10, pady=10)

    dataPointEntry2 = Combobox(root, values=["Weather Code", "Temperature Max", "Temperature Min", "Precipitation Sum",
                                            "Wind Speed Max", "Precipitation Probability Max"], width=25,
                              font=("Arial", 12))
    dataPointEntry2.grid(row=8, column=4, padx=10, pady=10)

    startLabel2 = Label(root, text="Start Date:", font=("Arial", 12, "bold"), bg="#b6faee")
    startLabel2.grid(row=9, column=3, padx=10, pady=10)

    startEntry2 = Combobox(root, values=list(range(len(weatherData["dates"]) - 1)), width=25, font=("Arial", 12))
    startEntry2.grid(row=9, column=4, padx=10, pady=10)

    # Dropdown for selecting the end date index for the query
    endLabel2 = Label(root, text="End Date:", font=("Arial", 12, "bold"), bg="#b6faee")
    endLabel2.grid(row=10, column=3, padx=10, pady=10)

    endEntry2 = Combobox(root, values=list(range(len(weatherData["dates"]) - 1)), width=25, font=("Arial", 12))
    endEntry2.grid(row=10, column=4, padx=10, pady=10)

    compareButton = Button(root, text="Compare Values", font=("Arial", 12, "bold"), command=lambda: compare(runQuery(typeEntry1.get(), dataPointEntry1.get(),
                                                int(startEntry1.get()), int(endEntry1.get()), type="compare"), runQuery(typeEntry2.get(), dataPointEntry2.get(),
                                                int(startEntry2.get()), int(endEntry2.get()), type="compare")))
    compareButton.grid(row=11, column=0, columnspan=2, padx=10, pady=10)


    resultLabel = Label(root, text="Results:", font=("Arial", 12, "bold"), bg="#b6faee")
    resultLabel.grid(row=12, column=0, padx=10, pady=10)


    resultEntry2 = Label(root, text="Results will be displayed here", font=("Arial", 12, "italic"), bg="#ffffff",
                        borderwidth=2, relief="solid", width=40)
    resultEntry2.grid(row=12, column=1, padx=10, pady=10)



def main() -> None:
    global weatherData
    global root

    root = Tk()
    root.title("Weather Data Viewer")
    root.geometry("1200x1000")

    weatherData = loadData()
    setupGUI()

    root.mainloop()  # Start the Tkinter event loop


if __name__ == '__main__':
    main()
