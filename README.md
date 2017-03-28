Part of the observatory software for the Warwick one-meter telescope.

vaisalad recieves data from a Vaisala WXT520 weather station attached via a USB-RS232 adaptor and
makes the latest measurement available for other services via Pyro.

vaisala is a commandline utility that prints the latest measurement in a human-readable form.

#### Setup

The Vaisala unit should be configured with 4800 8N1 with no flow control.

The message parsing expects the general status message 0R0 to include Dm,Sm,Ta,Ua,Pa,Rc,Ri,Th,Vh parameters in metric units.
This can be set if necessary by sending the following command:
```
0RU,R=11111100&10100000,I=60,U=M,S=M,M=R,Z=M
```

The `vaisalad` service will be automatically started when the USB-Serial converter with serial number `FTYQH2HQ` is plugged in to the machine.
If this ever changes then the udev rule in 10-onemetre-vaisala.rules should be updated to match.

If the `onemetre-vaisala-server` package is (re-)installed after the device is attached then it may be manually started using
```
sudo systemctl vaisalad start
```

The `vaisala-reset-rain` service must be enabled after installation using
```
sudo systemctl enable vaisala-reset-rain.timer
sudo systemctl start vaisala-reset-rain.timer
```
