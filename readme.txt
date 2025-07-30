run using:

python3 main.py

Accepts information for driver. Assumes driver is active upon registration.

First calculates driver with euclidean distance.

If I had more time, I would select driver this way:
    1. Calculate euclidean distance between rider and drivers, select 5 closest drivers within 5 ticks.
    2. If closest driver has had > 2 * (second closest driver rides), select second closest driver.
    3. Make same check for selected driver and 3rd closest driver.
