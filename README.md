# IPAddressParser
Takes in a list of IP addresses and returns a list of subnets that contain at least a set threshold percent of the listed IP addresses, sorted in order of bigger subnets to smaller

The main use case would be if you have a list of IPs that need to be blacklisted, instead of individually blocking the IPs, play with the threshold to block higher level groups of IPs.

Example:

Given this list of IP addresses:

![image](https://github.com/AyushSat/IPAddressParser/assets/18633636/ec2f3f54-382f-4ce8-8131-b9c0bc4d9037)

Transform it into this:

![image](https://github.com/AyushSat/IPAddressParser/assets/18633636/5d9f5323-d993-4df8-8ea1-7c268be1a7e7)

