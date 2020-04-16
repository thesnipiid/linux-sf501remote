Thanks a lot to Arjen Klaverstijn to have done the most important job : understand the protocol. it's a painfull job, so thank to you to have done this and to have share it as an opensource project.
If you want the more advanced arduino library, clone this : https://github.com/arjhun/arduino-sf501remote.git.

# Raspberry Pi sf-501 python library by Timothée Surgis (Adaptation of the work of Arjen Klaverstijn)

A python library to control SF-501 RF switches by Flamingo (Smartwares.eu) . Theoratically you can control 65,536 remotes with each 15 sockets/ button pairs (on/ off).

>NOTE: THIS IS NOT A LIBRARY FOR THE SF-501SHC!!! The SHC version is a smart controller with app, that commuicates with a cloud api and is able to control the standard 'dumb' sf-501 rf sockets.

To start using the library import it and create a new SF501R object

```python
import sf501-remote

myObject = SF501R(pin,id)
```
  - **pin:** The pin number that is connected to the transmit/ data pin of a 433.9 mhz transmitter. i make it work with a cheap **FS1000A**.
  - **id:** a 16 bit unsigned integer 0 - 65535 that will be used as the remote id.

#### 2.  How to send data

```python
myObject.send_ommand(onoff, channel, repeat=8);
```
- **onOff:** 0 is off button 1 is on button.
- **channel:** a 4 bit value (1 - 15) discribing the button number (the remotes I have, have only 4 buttons).
- **repeat:** *(Optional)* the number of packages to send each transmit the remotes send them 8 times. *(default: 8)*

```python
myObject.switch_all(onOff,repeat = 8);
```
This is a helper function to switch all sockets at once.

- **onOff:** 0 is off button 1 is on button.
- **Repeat:** *(Optional)* the number of packages to send each transmit the vendor's remotes send them 8 times. *(default: 8)*

### Protocol explained

A frame consists of 8 bytes of data and a preamble/end of frame :
Preamble - Data (8 bytes) - End (1 pulse)

Data section format:
32 bits LSB data section

32 - 18: 16 bit remote id, 65535 different remotes on this system.
9 - 17: 8 bits are empty on all remotes.
5 - 8: 4 bits a decimal value of 1 is switch **ON** a 0 is switch **OFF**.
1 - 4: maximum of 15 buttons/channels per remote.

Pulses are around 200µS.

|¯¯¯|_______________________________________
preamble = 1 pulse high 14 pulses low

|¯¯¯|
end = 1 pulse high

a one or a zero bit is represented by a succession of pulses like this :

|¯¯¯|______|¯¯¯|_____________________
data 0 = 1 pulse high & 2 pulses low, 1 pulses high & 7 pulses low

|¯¯¯|_____________________|¯¯¯|______
data 1 = 1 pulse high & 7 pulses low, 1 pulse high & 2 pulses low

