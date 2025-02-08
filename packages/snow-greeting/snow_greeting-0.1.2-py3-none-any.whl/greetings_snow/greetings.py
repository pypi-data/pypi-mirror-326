import platform

def print_hello_message():
    # Get the operating system information
    system_info = platform.system()

    # Check whether the system is Windows or Linux
    if system_info == "Windows":
        print("Hello, message from Snow. Your system is Windows.")
    elif system_info == "Linux":
        print("Hello, message from Snow. Your system is Linux.")
    else:
        print(f"Hello, message from Snow. Your system is {system_info}.")
