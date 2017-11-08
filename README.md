## W1m Vaisala weather station daemon [![Travis CI build status](https://travis-ci.org/warwick-one-metre/vaisalad.svg?branch=master)](https://travis-ci.org/warwick-one-metre/vaisalad)

Part of the observatory software for the Warwick La Palma telescopes.

`vaisalad` wraps a Vaisala WXT520/WXT530 weather station attached via a USB-RS232 adaptor and
makes the latest measurement available for other services via Pyro.

`vaisala` is a commandline utility that prints the latest measurements in a human-readable form.

An additional `vaisala-reset-rain` service runs on gotoserver and resets the accumulated rain count each day at 12:00.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software Setup (W1m)

The `vaisalad` service will be automatically started when the USB-Serial converter with serial number `FTYQH2HQ` is plugged in to the machine.
If this ever changes then the udev rule in `10-onemetre-vaisala.rules` should be updated to match.

If the `onemetre-vaisala-server` package is (re-)installed after the device is attached then it may be manually started using
```
sudo systemctl start vaisalad
```

Finally, open a port in the firewall so that other machines on the network can access the daemon:
```
sudo firewall-cmd --zone=public --add-port=9001/tcp --permanent
sudo firewall-cmd --reload
```

Note that the `vaisala-reset-rain` service runs on gotoserver and is covered under the GOTO instructions.

### Software Setup (GOTO)

The `vaisalad` service will be automatically started when the USB-Serial converter with serial number `FTB3L8SI` is plugged in to the machine.
If this ever changes then the udev rule in `10-goto-vaisala.rules` should be updated to match.

If the `goto-vaisala-server` package is (re-)installed after the device is attached then it may be manually started using
```
sudo systemctl start goto-vaisalad
```

The `vaisala-reset-rain` service must be enabled after installation using
```
sudo systemctl enable vaisala-reset-rain.timer
sudo systemctl start vaisala-reset-rain.timer
```

Finally, open a port in the firewall so that other machines on the network can access the daemon:
```
sudo firewall-cmd --zone=public --add-port=9022/tcp --permanent
sudo firewall-cmd --reload
```


### Hardware Setup

The Vaisala unit should be configured with 4800 8N1 with no flow control. Set this by sending:
```
0XU,A=0,M=A,C=2,I=5,B=4800,D=8,P=N,S=1,L=25<cr><lf>
```
through minicom (write this to a file, replacing &lt;cr&gt; with 0x0D and &lt;lf&gt; with 0x0A and then use the send file command)

The default parameters are almost correct, but need to modify the rain sensor to add Ri (rain intensity) and remove Rd (rain duration) to/from the composite message:
```
0RU,R=&10100000<cr><lf>
```

and change the wind speed unit from m/s to km/h:
```
0WU,U=K<cr><lf>
```
