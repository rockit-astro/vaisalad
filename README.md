## Vaisala weather station daemon

`vaisalad` wraps a Vaisala WXT520/WXT530 weather station attached via an RS232-USB or RS232-ethernet adaptor and
makes the latest measurement available for other services via Pyro.

`vaisala` is a commandline utility that reports the latest weather data.

### Configuration

Configuration is read from json files that are installed by default to `/etc/vaisalad`.
A configuration file is specified when launching the server, and the `vaisala` frontend will search this location when launched.

```python
{
  "daemon": "onemetre_vaisala", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "vaisalad", # The name to use when writing messages to the observatory log.
  "control_machines": ["OneMetreDome", "OneMetreTCS", "CLASPTCS", "GOTOServer", "SWASPTCS"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `rockit.common.IP`.
  "serial_port": "/dev/vaisala", # Serial FIFO for communicating with the vaisala
  "serial_baud": 4800, # Serial baud rate
  "serial_timeout": 5, # Serial comms timeout
  "rain_reset_time": "12:00:00" # Time of day to reset the accumulated rain counter
}
```

The FIFO device names are defined in the .rules files installed through the `rockit-vaisala-data-*` rpm packages.
If the physical serial port or USB adaptors change these should be updated to match.

### Initial Installation

The automated packaging scripts will push 4 RPM packages to the observatory package repository:

| Package                     | Description                                                                    |
|-----------------------------|--------------------------------------------------------------------------------|
| rockit-vaisala-server       | Contains the `vaisalad` server and systemd service file.                       |
| rockit-vaisala-client       | Contains the `vaisala` commandline utility for controlling the vaisala server. |
| rockit-vaisala-data-lapalma | Contains the json configuration and udev rules for the La Palma stations.      |
| python3-rockit-vaisala      | Contains the python module with shared code.                                   |

Alternatively, perform a local installation using `sudo make install`.

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable --now vaisalad@<config>
```

where `config` is the name of the json file for the appropriate unit.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `rockit.common.daemons` for the daemon specified in the vaisala config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl restart vaisalad@<config>
```

### Testing Locally

The vaisala server and client can be run directly from a git clone:
```
./vaisalad ./config/onemetre.json
VAISALAD_CONFIG_PATH=./config/onemetre.json ./vaisala status
```

### Hardware Setup

When setting up a new vaisala station the baud rate and measurement outputs must be configured to the expected format.
Set this by sending:
```
0XU,A=0,M=A,C=2,I=5,B=4800,D=8,P=N,S=1,L=25\r\n
```
through minicom or python.

Change the wind and rain measurements by sending:
```
0WU,R=1111110001011100,G=3,A=30,U=K\r\n
```
