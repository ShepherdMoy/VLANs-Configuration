This is a python 3 script which utilises the telnet library and the getpass library .
The script prompts the user for username and password and then opens a file (myswitches)
The myswitches file contains the IP addresses of the switches that will be accessed and configured .
The script will access each switch in a top down fashion ,configure the vlans defined in the range and then telnet into the next IP address in the myswitches file 
The script will then write the changes to memory 

SWVLANs--------script
myswitches------contains the inventory IP addresses 
