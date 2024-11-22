from shiny import reactive, render
from shiny.express import ui

# Imports from Python Standard Library to simulate live data
import random
from datetime import datetime
from faicons import icon_svg


# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------
UPDATE_INTERVAL_SECS: int = 1
# --------------------------------------------

# Initialize a REACTIVE CALC that our display components can call
# to get the latest data and display it.
# The calculation is invalidated every UPDATE_INTERVAL_SECS
# to trigger updates.

@reactive.calc()
def reactive_calc_combined():

    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic. Get random between -18 and -16 C, rounded to 1 decimal place
    temp = round(random.uniform(-18, -16), 1)

    # Get a timestamp for "now" and use string format strftime() method to format it
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    latest_dictionary_entry = {"temp": temp, "timestamp": timestamp}

    # Return everything we need
    return latest_dictionary_entry


ui.page_opts(title="PyShiny Express: Live Data (Basic)", fillable=True)


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


ui.h2("Current Temperature")

@render.text
def display_temp():
    latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['temp']} C"

ui.p("warmer than usual")

icon_svg("sun")

ui.hr()

ui.h2("Current Date and Time")

@render.text
def display_time():
    """Get the latest reading and return a timestamp string"""
    latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['timestamp']}"

with ui.card():  
    ui.card_header("Currrent Data")

with ui.card():  
    ui.card_header("Current Chart")
