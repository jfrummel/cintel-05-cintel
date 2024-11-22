from shiny import reactive, render
from shiny.express import ui

# Imports from Python Standard Library to simulate live data
import random
from datetime import datetime
from faicons import icon_svg
from collections import deque

# Import pandas for working with data
import pandas as pd


# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------
UPDATE_INTERVAL_SECS: int = 2
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
    new_dictionary_entry = {"temp":temp, "timestamp":timestamp}

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



ui.page_opts(title="Jeremy's PyShiny Express: Live Data (Basic)", fillable=True)


with ui.sidebar(open="open"):
    ui.h2("Antarctic Explorer", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )
    ui.hr()
    ui.h5("Links:", class_="text-center")
    ui.a("GitHub Source", href="https://github.com/jfrummel/cintel-05-cintel", target="_blank")
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")


with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("snowflake"),
        theme=ui.value_box_theme(
                fg="white",
                bg="purple"),
    ):
    
    

        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} C"

        "warmer than usual"

  

    with ui.card(full_screen=True):
        ui.card_header("Current Date and Time")

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

with ui.card():  
    ui.card_header("Currrent Data")

with ui.card():  
    ui.card_header("Current Chart")
