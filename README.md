Voodoo Privacy
==============

Protect your computer from unsecure environment with a very strict firewall and a strong VPN through Amazon EC2.

## The firewall

Voodoo privacy firewall gives you absolute control over your computer firewall so that you can control very precisely what is allowed in your computer, but also what is allowed out of your computer. This is very useful to protect your privacy, because it will allow you to block all broadcast packets that your computer might send when you turn it on.

The firewall rules are defined in `voodoo-pf.conf`, feel free to edit them. You need to at least define the interface that you will use to connect to an unsecure network. The other interfaces will be blocked.

When you run `sudo ./voodoo.sh hostile`, the rules in voodoo-pf.conf will be loaded and will replace all default rules of your Mac (including Network sharing, Application firewall, etc).

To get back to Apple default settings, run `sudo ./voodoo.sh safe`.

To see what packets get blocked, run `sudo ./voodoo.sh log`.

To find more information about how to write firewall rules for Open BSD packet-filter, run `man pf.conf`

For more information, read the introduction article: http://www.sarfata.org/posts/secure-your-mac.md

## The VPN

Voodoo privacy also makes it very easy to set up a secure VPN gateway on Amazon EC2.

### Setting up the VPN gateway

* Create a new security group (EC2 Management interface -> Security groups) 
** Allow traffic to TCP port 500, and UDP ports 500 and 4500. 
** It might be helpful to add a rule to allow SSH but you dont really need it. I like to limit SSH login from my home/office IP but if you are really brave you can let everyone find your SSH.
* Change the default value for the three variables `IPSEC_PSK`, `VPN_USER` and `VPN_PASSWORD` at the top of launch script and copy everything into your clipboard.
* In amazon console Click on Instances -> Launch Instance -> Classic Wizard -> Ubuntu 12.04 -> 1 micro instance.
** In the user data field, past the launch script you have just adapted.
** Select your keypair
** Select the security group you created earlier
** Give the machine a name
* Click launch

And that's it! Your server is now ready to accept connection from your mac. Get the public DNS name of your new server and resolve it to an IP address. You will need it in the next step.

### Configure the VPN on your Mac

This should also work on other types of OS but I have not tried yet.

* Open your network settings
* Click on the "+" button in the top-left corner of the interfaces list
* Select a VPN interface, with 'IPSec L2TP' and give it a name
* In the address field, put the public IP of your server (you can get from the amazon console)
* In the account name field, put the value of the `VPN_USER` variable that you defined earlier.
* Click on auth settings, fill your `VPN_PASSWORD` in the first field and your `IPSEC_PSK` in the second box. Click Ok
* Click on Advanced Settings, select "Send all traffic" and click ok.
* If you are also using voodoo firewall, update the VPN server address at the top of the script and re-run it to allow VPN traffic to go through to your server.
* Click Connect, it should take a few seconds and you should be online.
* Ask google about your IP address: https://www.google.com/search?q=what+is+my+ip+address, you should see the IP address of your Amazon EC2 box

### For more information

For more explaination and help debugging, read my initial blog post about this: http://www.sarfata.org/posts/setting-up-an-amazon-vpn-server.md

## License

Copyright Thomas Sarlandie 2012

This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 
Unported License: http://creativecommons.org/licenses/by-sa/3.0/

Attribution required: please include my name in any derivative and let me know how you have improved it!

## About Voodoo Privacy

Voodoo Privacy was born during Defcon XX to protect my very own privacy. The name comes from the rooftop bar of the Rio hotel where the conference was held.



