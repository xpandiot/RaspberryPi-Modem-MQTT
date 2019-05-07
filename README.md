# RaspberryPi-Modem-MQTT
Connecting Pi with Modem and publishing data to XPAND IoT Platform 

This repository provides How - To for sending sensor data from RaspberryPI to IoT Platform over MQTT using Modem connected on USB UART port on the Pi

# Devices used
1. Raspberry Pi 2015
2. Neoway N20 GPRS, NB-IoT Modem
3. USB UART for connecting PI with Modem
4. SIM Card from mobile operator

*Refer attached pics in the repo*

# 1. Installing The Paho Client

You can Install the MQTT client using PIP with the command:

``` 
pi@raspberrypi: pip install paho-mqtt
```
# 2. Install PPP, screen & elinks

``` 
pi@raspberrypi:sudo apt-get update

pi@raspberrypi:sudo apt-get install ppp screen elinks
```
# 3. Configure PPP

Create file named *gprs* in peers directory

``` 
pi@raspberrypi: cd /etc/ppp/peers/
pi@raspberrypi: touch gprs

```
Copy below code and paste it in gprs file. Make sure you update the COM port and APN for the Mobile operator you are using in the modem
```
# internet - is the apn for CELCOM Connection
connect "/usr/sbin/chat -v -f /etc/chatscripts/gprs -T internet"
 
# For Raspberry Pi3 use /dev/ttyS0(Update based on your com port) as the communication port:
/dev/ttyUSB0
 
# Baudrate 9600 115200 etc depending on your modem
115200

debug
nodetach
ipcp-accept-local
ipcp-accept-remote

 
# Assumes that your IP address is allocated dynamically by the ISP.
noipdefault
 
# Try to get the name server addresses from the ISP.
usepeerdns
 
# Use this connection as the default route to the internet.
defaultroute
 
# Makes PPPD "dial again" when the connection is lost.
persist
 
# Do not ask the remote to authenticate.
noauth
 
# No hardware flow control on the serial link with GSM Modem
nocrtscts
 
# No modem control lines with GSM Modem
local

```
# 4. Establish GPRS connection

Activate GPRS connection by running the command as below (gprs is the file name you provided in step #3 above)

```
pi@raspberrypi: sudo pon gprs 
(or) 
pi@raspberrypi: pppd call gprs

// Add & sign if want to run in background as given below
// sudo pon gprs & 
// pppd call gprs &

```

You can verify the log file by visiting 

```
cat /var/log/syslog | grep pppd 

If everything is correct your log will be showing something  similar

Jul  8 03:47:40 raspberrypi pppd[2321]: pppd 2.4.5 started by root, uid 0
Jul  8 03:47:40 raspberrypi pppd[2321]: Serial connection established.
Jul  8 03:47:40 raspberrypi pppd[2321]: Using interface ppp0
Jul  8 03:47:40 raspberrypi pppd[2321]: Connect: ppp0 <--> /dev/ttyAMA0
Jul  8 03:47:41 raspberrypi pppd[2321]: PAP authentication succeeded
Jul  8 03:47:42 raspberrypi pppd[2321]: Could not determine remote IP address: defaulting to 10.64.64.64
Jul  8 03:47:42 raspberrypi pppd[2321]: local  IP address 21.144.145.193
Jul  8 03:47:42 raspberrypi pppd[2321]: remote IP address 10.64.64.64
Jul  8 03:47:42 raspberrypi pppd[2321]: primary   DNS address 10.177.0.34
Jul  8 03:47:42 raspberrypi pppd[2321]: secondary DNS address 10.168.185.116
```
# 5. Check network status 
run ifconfig on the terminal to verify the gprs connection status. There should be a new interface called ppp0 with IP details. 
```
pi@raspberrypi: sudo ifconfig
ppp0      Link encap:Point-to-Point Protocol  
          inet addr:21.144.145.193  P-t-P:10.64.64.64  Mask:255.255.255.255
          UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1500  Metric:1
          RX packets:6 errors:0 dropped:0 overruns:0 frame:0
          TX packets:7 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:3 
          RX bytes:72 (72.0 B)  TX bytes:111 (111.0 B)
```
# 6. Verify Intenret accessibility

```
pi@raspberrypi:~/Desktop $ ping adafruit.com
PING adafruit.com (104.20.38.240) 56(84) bytes of data.
^C64 bytes from 104.20.38.240: icmp_seq=1 ttl=57 time=1138 ms
64 bytes from 104.20.38.240: icmp_seq=2 ttl=57 time=1525 ms

--- adafruit.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1022ms
rtt min/avg/max/mdev = 1138.779/1332.165/1525.551/193.386 ms, pipe 2
pi@raspberrypi:~/Desktop $ ping google.com
PING google.com (216.58.196.14) 56(84) bytes of data.
64 bytes from kul01s11-in-f14.1e100.net (216.58.196.14): icmp_seq=1 ttl=54 time=5958 ms
64 bytes from kul01s11-in-f14.1e100.net (216.58.196.14): icmp_seq=2 ttl=54 time=5131 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 8724ms
rtt min/avg/max/mdev = 348.909/2585.431/5958.540/2033.999 ms, pipe 6
pi@raspberrypi:
```

Now that internet is working, you can run python script to connect to MQTT and publish the data to IoT Platform

Considering your python file ( sample provided in the repo cpuTemp.py) is in desktop.

```
pi@raspberrypi:~/Desktop $ python cpuTemp.py 
  global connected
Connected to mqtt.iot.ideamart.io : 1883
CPU temp: 54.768
message published successfully
CPU temp: 54.768
message published successfully
CPU temp: 53.692
message published successfully
CPU temp: 56.382
```

