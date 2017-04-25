# Use systemd to trigger the feeder over HTTP

> git clone https://github.com/Spredzy/feeders
> cd feeders/systemd
> checkmodule -M -m -o allow-http-access.mod allow-http-access.te
> semodule_package -o allow-http-access.pp -m allow-http-access.mod
> sudo semodule -i allow-http-access.pp
> sudo cp dci-rdo-feeder.service /etc/systemd/system
> sudo cp dci-rdo-feeder.socket /etc/systemd/system
> sudo systemctl enable dci-rdo-feeder.socket
> sudo systemctl enable dci-rdo-feeder
> sudo systemctl start dci-rdo-feeder.socket
