from colorama import Fore, Style, init
import os
import re
import logging
import sys
import time
# Initialize Colorama
init()


class Utils:
    """Utility class for common functions used in the Byte Scanner project."""
    @staticmethod

    def print_banner():
        banner = f"""
{Fore.GREEN}
                      :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:sᴏᴜғɪᴀɴᴇ!$WX??#MRRMMM!
               ~?WuxiW*`   `'#$ᴉɹᴉɥɐꓕ!!??!!!
             :X- M$$$$       `'T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~''##*'
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `'~:    :
#'~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u '$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo('*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu('**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~'##*$$$$M~ 


 ▄▄▄▄ ▓██   ██▓▄▄▄█████▓▓█████      ██████  ▄████▄   ▄▄▄       ███▄    █  ███▄    █ ▓█████  ██▀███  
▓█████▄▒██  ██▒▓  ██▒ ▓▒▓█   ▀    ▒██    ▒ ▒██▀ ▀█  ▒████▄     ██ ▀█   █  ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒
▒██▒ ▄██▒██ ██░▒ ▓██░ ▒░▒███      ░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██  ▀█ ██▒▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒
▒██░█▀  ░ ▐██▓░░ ▓██▓ ░ ▒▓█  ▄      ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄  
░▓█  ▀█▓░ ██▒▓░  ▒██▒ ░ ░▒████▒   ▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒▒██░   ▓██░▒██░   ▓██░░▒████▒░██▓ ▒██▒
░▒▓███▀▒ ██▒▒▒   ▒ ░░   ░░ ▒░ ░   ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
▒░▒   ░▓██ ░▒░     ░     ░ ░  ░   ░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░░ ░░   ░ ▒░░ ░░   ░ ▒░ ░ ░  ░  ░▒ ░ ▒░
 ░    ░▒ ▒ ░░    ░         ░      ░  ░  ░  ░          ░   ▒      ░   ░ ░    ░   ░ ░    ░     ░░   ░ 
 ░     ░ ░                 ░  ░         ░  ░ ░            ░  ░         ░          ░    ░  ░   ░     
      ░░ ░                                 ░                                                        
                                
                                    A N D  H A C K E R S  R E A L I T Y

{Style.RESET_ALL}

    """
        Utils.clear_screen()
        # print(banner)
        Utils.typewriter_effect(banner)

    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For macOS and Linux
            os.system('clear')

    @staticmethod
    def validate_ip(ip):
        """Validate the given IP address."""
        pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
        if pattern.match(ip):
            return True
        else:
            print(f"{Fore.RED}Invalid IP address: {ip}{Style.RESET_ALL}")
            return False

    @staticmethod
    def setup_logging(log_file='scanner.log'):
        """Set up logging to a file."""
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    def log_message(message, level='info'):
        """Log a message at the specified level."""
        if level == 'info':
            logging.info(message)
        elif level == 'warning':
            logging.warning(message)
        elif level == 'error':
            logging.error(message)

    @staticmethod
    def show_progress(iteration, total, prefix='', length=50, fill='█'):
        """Display a progress bar in the console."""
        percent = (iteration / total)
        filled_length = int(length * percent)
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write('\r' + ' ' * (len(prefix) + length + 10) + '\r')  # Clear previous line
        sys.stdout.write(f'\r{prefix} |{bar}| {percent:.1%}')
        sys.stdout.flush()

    @staticmethod
    def get_user_input(prompt):
        """Safely get user input."""
        try:
            return input(prompt)
        except EOFError:
            print(f"{Fore.RED}Input was terminated.{Style.RESET_ALL}")
            return None
        except KeyboardInterrupt:
            print(f"{Fore.RED}Input was interrupted.{Style.RESET_ALL}")
            return None
    @staticmethod
    def typewriter_effect(text, speed=0.00009):
        for char in text:
            # if char == 'A':
            #     speed = 0.05
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()  # Move to the next line after finishing

if __name__ == "__main__":
    
    Utils.print_banner()
    for i in range(0, 100):
        Utils.show_progress(i, 100)
        time.sleep(0.2)
