# v1.0.9
Improve documentation on subnet filter usage

# v1.0.8
Fix gateway check logic

# v1.0.7
Enable optional custom subnet filter

# v1.0.6
Fix for [an error](https://github.com/jbowdre/phpIPAM-for-vRA8/issues/3) when a subnet doesn't have a defined gateway.

Adds new option on integration configuration screen for whether or not vRA should only retrieve subnets marked as IP Pools in phpIPAM.

# v1.0.5
vRA 8.6.1 fixed the bug introduced in 8.6 where the `resource` property had dropped the `owner` field, causing `allocate_ip` to fail.

v1.0.4 was created to work around that bug by removing the field entirely.

v1.0.5 restores the field in a way which shouldn't break on existing 8.6 installs.

# v1.0.4
Fix for [an issue with vRA 8.6](https://github.com/jbowdre/phpIPAM-for-vRA8/issues/2)

# v1.0.3
Minor code cleanup; dynamically compute IP version in `allocate_ip` action.

# v1.0.2
Updated to allocate from the entire range of usable IPs; previously we started at x.x.x.10.

