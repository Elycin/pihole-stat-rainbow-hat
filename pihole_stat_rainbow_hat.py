#!/usr/bin/env python3

# Import Modules
import time
import rainbowhat
import pihole
import sys
import configuration


# The main class of the project.
class PiholeStatRainbowHat:
    def __init__(self, server=None, password=None, update_frequency=10):
        self.__update_frequency = update_frequency
        self.__running = None
        self.__request_stop = False
        self.__pihole_interface = None

        # Check if initialized variables
        if server is not None and password is not None:
            self.set_server(server=server)
            self.set_password(password=password)

    # Set the server where the PiHole panel is.
    def set_server(self, server):
        if self.__running:
            print("Please stop the script before running.")
        else:
            try:
                self.__pihole_interface = pihole.PiHole(server)
                print("Instantiated new instance of Pi-hole API.")
            except:
                sys.stderr.print("There was a problem while attempting to connect to the specified Pi-hole server.")

    # Set the administration password for the PiHole Interface so this script can use it.
    def set_password(self, password):
        if self.__running:
            print("Please stop the script before running.")
        else:
            try:
                self.__pihole_interface.authenticate(password)
                print("Authentication succeeded.")
            except:
                sys.stderr.print("Invalid password while attempting to authenticate with Pi-hole API.")

    # Set the frequency in seconds of when the display should be updated.
    def set_update_frequency(self, frequency_in_seconds):
        # Run safety checks to make sure it's within valid ranges.
        if frequency_in_seconds < 0:
            print("A invalid update interval of %d was given, it will be defaulted to 10 seconds.")
            frequency_in_seconds = 10
        elif frequency_in_seconds > 3600:
            print("Please specify an interval less than one hour, it will be defaulted to 3600 seconds.")
            frequency_in_seconds = 3600

        # Update the class variable
        self.__update_frequency = frequency_in_seconds

    # Get the frequency of how often the display should update in seconds - API
    def get_update_frequency(self):
        return self.__update_frequency

    # Calculates the value from the pihole interface.
    def get_percentage(self):
        # Get the latest data
        self.__pihole_interface.refresh()

        # Add to variables for easy access.
        total = self.__pihole_interface.queries.replace(",", "")
        blocked = self.__pihole_interface.blocked.replace(",", "")

        # Print to the console
        print("Update received!")
        print("Total Queries: " + total)
        print("Blocked: " + blocked)

        # Return
        return (int(blocked) / int(total)) * 100

    # Send a stop signal for the work loop.
    def stop(self):
        print("The script is preparing to safely shut down.")
        print("When the loop runs for the next time, this script will exit.")
        self.__request_stop = True

    # The method that does the work.
    def work(self):
        self.__running = True

        while not self.__request_stop:
            try:
                # Get the raw percentage
                raw_percentage = self.get_percentage()

                # Determine the number of decimals we should use.
                if int(raw_percentage) < 10:
                    precision = 3
                else:
                    precision = 2

                # Format the percentage based on the precision
                formatted_percentage = round(raw_percentage, precision)

                # Update the rainbow hat
                rainbowhat.display.clear()
                rainbowhat.display.print_float(formatted_percentage)
                rainbowhat.display.show()

                # Print to the console.
                print("Rainbow HAT has been updated successfully: %s%% of DNS requests have been blocked."
                      % formatted_percentage)
                print()
            except:
                rainbowhat.display.clear()
                rainbowhat.display.print_str('ERR')
                rainbowhat.display.show()

            # Wait for the next run
            time.sleep(self.__update_frequency)

        # Update the running variable to mark that we have stopped.
        self.__running = False


# If the script is not invoked from another class, we're running it directly.
if __name__ == "__main__":

    # Please see the examples for multiple methods of utilizing this script.
    app = PiholeStatRainbowHat(
        server=configuration.server_ip,
        password=configuration.server_password,
        update_frequency=configuration.update_frequency
    )
    app.work()
