# Install python dependencies
# This is horrible, but it seems to be the only way that actually works!
pip3 install pyserial Pyro4

# Enable the service so that it starts immediately
systemctl enable vaisalad.service
systemctl start vaisalad.service