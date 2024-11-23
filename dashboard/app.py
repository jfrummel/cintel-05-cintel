from shiny import reactive, render
from shiny.express import ui
from shinywidgets import render_widget
from shinyswatch import theme

# Imports from Python Standard Library to simulate live data
import random
from datetime import datetime
from faicons import icon_svg
from collections import deque

# Import pandas for working with data
import pandas as pd
import plotly.express as px
from scipy import stats

# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------
UPDATE_INTERVAL_SECS: int = 1
# --------------------------------------------

DEQUE_SIZE: int = 6
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))


# Initialize a REACTIVE CALC that our display components can call
# to get the latest data and display it.
# The calculation is invalidated every UPDATE_INTERVAL_SECS
# to trigger updates.


@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic
    temp = round(random.uniform(-20, -10), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"Temperature": temp, "Time Stamp": timestamp}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry


ui.page_opts(
    title="Jeremy's PyShiny Express: Live Data (Basic)",
    fillable=True,
    theme=theme.pulse,
    style="background-color: grey",
)


with ui.sidebar(open="open"):
    ui.h2("Antarctic Explorer", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )
    ui.hr()
    ui.h5("Links:", class_="text-center")
    ui.a(
        "GitHub Source",
        href="https://github.com/jfrummel/cintel-05-cintel",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")


with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("snowflake"),
        theme=ui.value_box_theme(fg="white", bg="purple"),
    ):

        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['Temperature']} C"

        "warmer than usual"

    with ui.value_box(
        showcase=icon_svg("clock"),
        theme=ui.value_box_theme(fg="white", bg="purple"),
    ):
        "Current Date and Time"

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['Time Stamp']}"


with ui.card(fill=True):
    ui.card_header("Currrent Data")

    @render.data_frame
    def table():
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

        return render.DataGrid(df, width="100%")


with ui.card():
    ui.card_header("Trending Temperature Readings")

    @render_widget
    def plot():
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        # Ensure the DataFrame is not empty before plotting
        if not df.empty:
            # Convert the 'timestamp' column to datetime for better plotting
            df["Time Stamp"] = pd.to_datetime(df["Time Stamp"])

            # Create scatter plot for readings
            # pass in the df, the name of the x column, the name of the y column,
            # and more

            fig = px.scatter(
                df,
                x="Time Stamp",
                y="Temperature",
                title="Temperature Readings with Regression Line",
                labels={"Temperature": "Temperature (°C)", "Time Stamp": "Time"},
                color_discrete_sequence=["blue"],
            )

            # Linear regression - we need to get a list of the
            # Independent variable x values (time) and the
            # Dependent variable y values (temp)
            # then, it's pretty easy using scipy.stats.linregress()

            # For x let's generate a sequence of integers from 0 to len(df)
            sequence = range(len(df))
            x_vals = list(sequence)
            y_vals = df["Temperature"]

            slope, intercept, r_value, p_value, std_err = stats.linregress(
                x_vals, y_vals
            )
            df["best_fit_line"] = [slope * x + intercept for x in x_vals]

            # Add the regression line to the figure
            fig.add_scatter(
                x=df["Time Stamp"],
                y=df["best_fit_line"],
                mode="lines",
                name="Regression Line",
            )

            # Update layout as needed to customize further
            fig.update_layout(xaxis_title="Time", yaxis_title="Temperature (°C)")

        return fig
