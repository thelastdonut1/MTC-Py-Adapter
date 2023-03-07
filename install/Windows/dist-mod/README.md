# MTConnect Python Adapter
___
The purpose of this project is to use Python to create an MTConnect adapter that is capable of reading a simple, nominal device (a virtual device, RaspberryPi I/O) and communicating this data to an MTConnect Agent to be displayed in the browser. The project is not intended for production use and is merely a demonstration of:

- The simplicity of creating a MTC Adapter
- The function of the adapter
- The abiltity to create an adapter using Python

This adapter will be used to provide students attending future MTConnect training courses an all-encompassing experience of using the MTC Adapter, and MTC Agent on a standalone PC, without the need for an available machine tool with an MTConnect Adapter installed.

Future versions of this adapter may be distributed and the source code, shared once the adapter has reached a more complete state, however, for now this will only be used for demonstrations during Mazak MTConnect training events.


## Installing the Adapter
The installer can be found in the `install\Windows` folder of the directory. Simply download the installer and run it.

## Setting Up
The adapter comes ready to use after install, however, in order to get the correct agent output, the `device.xml` file from the install folder will need to be read by the MTC Agent. The suggested method would be, copying this file and pasting it in the local MTC Agent install folder, and updating the `agent.cfg` file in this directory to read the `device.xml` file. An example of this is shown below.

```agent-cfg
Devices = device.xml   # Change this value to reflect device file name
.....
```

The `Host` paramter in the `agent.cfg` file will also need to be updated to match your current IP Address on the network. An example of this can be seen below:

```
Adapters {

 AdapterName {
    FilterDuplicates = yes
    Device = DeviceName
    Host = 172.87.90.100 # Change this value to reflect your IP Address
    Port = 7878
  }
}
```

If you do not know how to find your IP Address, follow this [link for instructions](https://www.avast.com/c-how-to-find-ip-address).

>📘 A current bug prevents the user from being able to use `127.0.0.1` or `localhost` for the host address in the `agent.cfg` file. Use the machine network IP Address here instead.

Once both of these changes have been made, save the `agent.cfg` file and, if your agent is running, restart the agent. The adapter is now ready to be used.

## Using the Adapter
Navigate to the install folder and find the `MTConnect-Test-Adapter.exe` file. When you are ready to run the adapter, double-click this file. A terminal window will open and display the adapter logging information, as well as the communications between the adapter and agent. An example of the output can be seen below:

```Log
[STARTING] Creating virtual device...
[STARTING] Server is starting...
[STARTING] Starting adapter...
[LISTENING] Server is listening on 172.87.90.100
[172.87.90.100:56123]->[SERVER]: * PING

[NEW CONNECTION] MTC Agent at 172.87.90.100 connected.
[ACTIVE CONNECTIONS] 1
[SERVER]->[172.87.90.100:56123]: * PONG 10000
```

To view the agent output, open a browser and navigate to:
- {Your-Local-IP-Address} : {Agent Port}
- localhost : {Agent Port}

The default address would then be `localhost:5000` or, following the example above, `172.87.90.100:5000`.

Once you have navigated to this page, you should now see the MTC Agent output.