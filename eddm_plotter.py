import subprocess

def run_orca_plot():
    # Ask the user for the .gbw file name
    gbw_filename = input("Enter the filename of the .gbw file (with extension): ").strip()
    
    # Ensure the filename has the correct extension
    if not gbw_filename.endswith('.gbw'):
        print("Error: The file must have a .gbw extension.")
        return
    
    # Command to invoke orca_plot with the specified file
    command = f"orca_plot {gbw_filename} -i"
    print(f"Running command: {command}")
    
    # Open the subprocess and interact with it
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        # Send answers to the prompts sequentially
        responses = [
            "4\n",              # Enter number: 4 (Set NGRID)
            "250\n",            # Enter NGRID: 250
            "5\n",              # Enter number: 5 (Set file format)
            "7\n",              # Enter Format: 7 (Gaussian cube)
            "6\n",              # Enter number: 6 (CIS/TD-DFT difference densities)
            "y\n",              # Default CIS file confirmation
            "1 5 12 26\n"       # States to compute densities for
        ]
        
        # Feed the responses into the process
        for response in responses:
            print(f"Sending response: {response.strip()}")
            process.stdin.write(response)
            process.stdin.flush()

        # Close stdin after all responses are sent
        process.stdin.close()
        
        # Capture and print the process output
        stdout, stderr = process.communicate()
        print("\n=== ORCA_PLOT OUTPUT ===\n")
        print(stdout)
        
        if stderr:
            print("\n=== ORCA_PLOT ERRORS ===\n")
            print(stderr)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        process.kill()
    finally:
        process.wait()

if __name__ == "__main__":
    run_orca_plot()
