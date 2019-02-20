import os

# change to the root directory of this project for an example.
os.chdir(os.path.basename(os.getcwd()))

# Import the main python script.
import pihole_stat_rainbow_hat

# We're going to define library as the script.
# Initialize the main class PiholeStatRainbowHat()
# Provide Parameters via the constructor

library = pihole_stat_rainbow_hat.PiholeStatRainbowHat(
    server="192.168.0.1",  # Your server address
    password="randomness",  # Password to your PiHole Administration Interface
    update_frequency=10,  # How often your HAT should update.
)

# When you are ready, you can run the worker.
# Consider running this in a thread for your application.
library.work()

# When you want to stop it, signal that the work method should stop.
library.stop()