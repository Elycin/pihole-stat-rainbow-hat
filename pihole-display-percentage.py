#!/usr/bin/env python3

# Import Modules
import time
import rainbowhat
import pihole


# Class
class DisplayPercentage:
    def __init__(self, server=None, password=None):
        self.__server = server
        self.__update_interval = None
        self.__running = None
        self.__request_stop = False

        # Check if initialized variables
        if self.__server is not None and password is not None:
            self.__pihole_interface = pihole.PiHole(self.__server)
            self.__pihole_interface.authenticate(password)

    def set_server(self, server):
        if self.__running:
            print("Please stop the script before running.")
        else:
            self.__server = server
            self.__pihole_interface = pihole.PiHole(self.__server)

    def get_server(self):
        return self.__server

    def set_password(self, password):
        if not self.__server:
            print("Please specify a server before providing a password.")
        else:
            self.__pihole_interface.authenticate(password)

    def set_update_interval(self, interval):
        # Run safety checks to make sure it's within valid ranges.
        if interval < 0:
            print("A invalid update interval of %d was given, it will be defaulted to 10 seconds.")
            interval = 10
        elif interval > 3600:
            print("Please specify an interval less than one hour, it will be defaulted to 3600 seconds.")
            interval = 3600

        # Update the class variable
        self.__update_interval = interval

    def get_update_interval(self):
        return self.__update_interval

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

    def stop(self):
        print("The script is preparing to safely shut down.")
        print("When the loop runs for the next time, this script will exit.")
        self.__request_stop = True

    def work(self):
        self.__running = True

        while not self.__request_stop:
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

            # Wait for the next run
            time.sleep(self.__update_interval)

        # Update the running variable to mark that we have stopped.
        self.__running = True


if __name__ == "__main__":
    # Instantiate the class - You can also provide the server and password via the constructor
    script = DisplayPercentage(
        server="127.0.0.1",
        password="your_password_here"
    )

    # Optionally, you can also provide the server and password separately.
    # script.set_server("127.0.0.1")
    # script.set_password("your_password_here")

    # Set the update frequency
    script.set_update_interval(10)

    # Start the work.
    script.work()
