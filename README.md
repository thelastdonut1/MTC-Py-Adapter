# MTC-Py-Adapter
## Description:
MTConnect Adapter written in python with the purpose of continuously looping and changing data items to be recorded by an MTC Agent. Adapter creates a "virtual device" that continually shuffles its ouptut and samples the device at a defined interval. Adapter also creates a socket server fro clients (MTC Agent) to connect to and as data is collected by the adapter, it is arranged into SHDR format (per the MTConnect Standard) and distributed to all of the clients connected to the server.

## Goal: 
To make a standalone adapter that can flip inputs and outputs, which can then be paired with a standalone agent for an all encompassing MTConnect demo.

## To-Do:
1. Replace the printing to terminal functionality with a logger. The logger needs to be able to recieve statements from the server, adapter, and other objects in order to have an all-encompassing detailed description of events in the adapter log file. The logger will have different levels of logging status and each message will be assigned to one of these levels, the most complex of which will give full-detailed descriptions of events as they happen, and the most basic of which will only report critical errors. The user should be able to configure their adapter logging settings in an adapter settings file.
2. Create a GUI that users can use to interact with the adapter as it is running, as well as view and manage the connected "virtual devices".
3. Refactor code so that everything can be exectuted by simply calling the adapter.run() method.
4. See other TODO items in code...