Find your actual network configuration by typing
```Bash
ifconfig
```
You should see something similar to

eth0 Link encap Ethernet HWaddr 00:00:00:00:00:00
inet addr:192.168.1.10 Bcast 192.168.1.255 Mask:255.255.255.0
Edit the networking config file by typing

```Bash
sudo nano /etc/network/interfaces
```
Inside it find the line

```bash
auto eth0
iface eth0 inet dhcp
```

and change it to

```Bash
auto eth0

iface eth0 inet static

address 192.168.1.115

netmask 255.255.255.0

gateway 192.168.1.1

dns-nameservers 8.8.8.8 192.168.1.1
```

Restart networking:
```Bash
systemctl restart networking
```

The actual change may need to be modified to something more specific for you. IE if you're routers IP is 10.0.0.1 then your gateway and dns-nameservers would need to be configured accordingly. I set the address to 192.168.1.115 because the odds of you getting enough connections to reach that IP and have any conflict from DHCP are slim to none. Let me know if this works for you.