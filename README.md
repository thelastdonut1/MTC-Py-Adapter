# MTC-Py-Adapter
## Description:
MTConnect Adapter written in python with the purpose of continuously looping and changing data items to be recorded by an MTC Agent

## Goal: 
To make a standalone adapter that can flip inputs and outputs, which can then be paired with a standalone agent for an all encompassing MTConnect demo.

## Progress:
1. Learning how to use core GIT functionalities to make acessing files and sharing project information with other developers easier.
2. Successfully pushed both a new and modified file into the repository
3. Changed the git config file to show my full name and changed the email from "momoore@mazakcorp.com" to "thelastdonut1@gmail.com". Not sure how this affects the users ability to push files to the repository. When using the initial email "momoore@mazakcorp.com", had to enter the command "$ git remote set-url origin git@github.com:thelastdonut1/MTC-Py-Adapter.git". Not quite sure what this did but it seems to be working and I will continue to test by pushing commits.
4. Created an adapter.py and device.py file to begin testing with the communication between the adapter and device. Set up device object to randomly shuffle one of its outputs, every rand(1,5) seconds. Set up the adapter object to be connected to a device object when creted and to read the device outputs. Need to work on continuously looping both the shuffling of the inputs and the reading of the outputs
5. Integrated multi-threading in the playground.py file to allow both the device to run continuously and the adapter to read continuously. Need to do further research on multi-threading, and research whether it would be better to use multi-threading or multi-processing for this project.

## To-Do:
Create the device.xml file that will map the outputs of the virtual device to data items. Use a Mazak device file for reference.

## Notes:
1/11/23: From conversation with Lem, it sounds like most MTConnect Adapter use multithreading to continuously run processes simultaneously, typically one for reading and one for sending the data. In this case there would be three, including the virtual device that is being simulated. Also, can consider adding functionality to the adapter to filter to find only the updated values every time that the adapter reads the device. This can be done in the device file or through the agent as well, but it is a good exercise.