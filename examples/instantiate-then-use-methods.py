import os

# change to the root directory of this project for an example.
os.chdir(os.path.basename(os.getcwd()))

# Import the main python script.
import pihole_stat_rainbow_hat

# We're going to define library as the script.
# Initialize the main class PiholeStatRainbowHat()
library = pihole_stat_rainbow_hat.PiholeStatRainbowHat()

# Give the library information via methods

# Set the server IP Address
library.set_server("192.168.0.1")  # Your server address

# Set the password to the Pi-Hole administration panel.
library.set_password("randomness")

# Set the frequency of how often the display should update with a new percentage in seconds.
library.set_update_frequency(10)

# When you are ready, you can run the worker.
# Consider running this in a thread for your application.
library.work()

# When you want to stop it, signal that the work method should stop.
library.stop()
