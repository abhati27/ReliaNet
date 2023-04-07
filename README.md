# ReliaNet: TCP-Like Reliable Data Transfer

ReliaNet is a project that demonstrates the implementation of a reliable data transfer protocol similar to TCP, ensuring successful communication over an unreliable connection with packet loss and latency.

## Files

- `reliable_transfer.py`: The main file containing the implementation of the send and recv functions for the reliable data transfer protocol.
- `tester.py`: A script used to test the reliable_transfer.py under different conditions, such as varying packet loss rates and latencies.
- `sender.py`: A script simulating the sender side of the communication, which uses the send function from `reliable_transfer.py` to transmit data over the unreliable link.
- `receiver.py`: A script simulating the receiver side of the communication, which uses the recv function from `reliable_transfer.py` to receive and reconstruct the transmitted data.
- `server.py`: A script simulating the unreliable link between the sender and receiver, introducing packet loss and latency based on the parameters set in the `tester.py` script.

## `testing the implementation

1. Test your file using the `tester.py` script. For example:

  python3 tester.py --file test_data.txt --loss 0.05 --delay 0.1

  This command tests the reliable_transfer.py sending the `test_data.txt` file over an unreliable connection with a 5% packet loss rate and a 100ms delay.

  You can replace 'test_data.txt' with any other file you would like to send and test.

2. You can view the available options and parameters for the `tester.py` script by running:
  
  python3 tester.py --help
  

This will display a help message with information on the optional arguments and their usage.

## Requirements

- Python 3

Ensure that Python 3 is installed on your system to run the project.

