# menu.py
from utils import Utils  # Import the Utils class from utils.py
from colorama import Fore, Style
import sys
from port_scanner import *
class Menu:
    """Menu class to handle tool selection in the Byte Scanner project."""
    
    @staticmethod
    def display_menu():
        Utils.print_banner()
        """Display a menu of available tools."""
        menu = f"""
        {Fore.CYAN}
    ========================================
                                            ||
            Welcome to Byte Scanner Toolkit ||
                                            ||
    ========================================||
                                            ||
            1. Port Scanner                 ||
                                            ||
            2. Validate IP Address          ||
            3. Show Banner                  ||
            4. Exit                         ||
                                            ||
    ========================================
        {Style.RESET_ALL}
        """
        print(menu)

    @staticmethod
    def display_port_scanner_menu():
        """Display the sub-options for the Port Scanner."""
        menu = f"""
        {Fore.CYAN}
    ========================================
            Port Scanner Options            ||
    ========================================||
                                            ||
            1. Provide range of ports       ||
            2. Custom port scanner          ||
            3. Common port scanner          ||
            4. Back to Main Menu            ||
                                            ||
    ========================================
        {Style.RESET_ALL}
        """
        print(menu)

    @staticmethod
    def get_user_choice():
        """Get user input for selecting a tool."""
        choice = Utils.get_user_input(f"{Fore.YELLOW}Enter your choice (1-4): {Style.RESET_ALL}")
        return choice
    @staticmethod
    def port_scanner():
        scanner = PortScanner(input("Enter target ip: "))
        while True:
            Menu.display_port_scanner_menu()
            choice = Menu.get_user_choice()
            if choice == '1':
                # Call the function to scan a range of ports

                
                print(f"{Fore.GREEN}Provide range of ports...{Style.RESET_ALL}")
                scanner.start_scan()  # Will ask the user for a port range
                scanner.display_open_ports()
                input("Press any key to continue...")
            elif choice == '2':
                print(f"{Fore.GREEN}Custom Port Scanner...{Style.RESET_ALL}")
                # Function to scan user-specified custom ports
                scanner.scan_custom_ports()  # Function to scan specific ports provided by the user
                scanner.display_open_ports()
                input("Press any key to continue...")
            elif choice == '3':
                print(f"{Fore.GREEN}Common Port Scanner...{Style.RESET_ALL}")
                # Function to scan commonly used ports
                scanner.scan_common_ports()  # Function to scan a predefined list of common ports
                scanner.display_open_ports()
                input("Press any key to continue...")
            elif choice == '4':
                break  # Return to main menu
            else:
                print(f"{Fore.RED}Invalid choice! Please enter a valid option.{Style.RESET_ALL}")
    @staticmethod
    def handle_choice():
        while True:
            Menu.display_menu()
            choice = Menu.get_user_choice()
            if choice == '1':
                Menu.port_scanner()
            else:
                break
        
            
