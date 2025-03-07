# phpIPAM Integration for vRealize Automation 8.x
This integration allows vRealize Automation 8.x to use [phpIPAM](https://phpipam.net) for assigning static IP addresses to provisioned virtual machines. Built against vRA 8.2.0.12946 and phpIPAM 1.5.

Details on how I built this (as well as notes on how I configured phpIPAM to work correctly with this plugin) can be found here:
https://runtimeterror.dev/integrating-phpipam-with-vrealize-automation-8/

> [!IMPORTANT]
> This project is no longer being maintained. I'm sure it's quite out of date at this point. Feel free to fork it and use it as a starting point for your own work, but I don't have a vRA/Aria environment or the time/energy to update it anymore.

## Prerequisites

- phpIPAM 1.5 must be installed, configured, and available over HTTPS
  - Consult the [phpIPAM installation docs](https://phpipam.net/documents/installation/)
- Subnets [must be defined in phpIPAM](https://runtimeterror.dev/integrating-phpipam-with-vrealize-automation-8/#step-2-configuring-phpipam-subnets).
- (Optional) A [Custom Field](docs/custom_field.md) defined to identify subnets which should be available to vRA.
  - Note: I previously used the built-in `isPool` field, but this is not ideal with versions of phpIPAM 1.5 since a [change on April 4, 2022](https://github.com/phpipam/phpipam/commit/7de080b8) which made the subnet and broadcast addresses (`x.x.x.0` and `x.x.x.255`) assignable on networks with this field set. Use a [Custom Field](docs/custom_field.md) instead. 
- A trusted SSL certificate is not required; vRA will prompt to confirm the certificate when the connection is initially validated.

## Usage
### From the phpIPAM web interface:
1. **Administration > phpIPAM Settings > Feature Settings** and enable the **API** option.
2. **Administration > phpIPAM Settings > Users** and create a new user to be used by vRA.
3. **Administration > phpIPAM Settings > API** and create a new API key with *Read/Write* permissions and *SSL with User Token* security. Make a note of the selected *App ID* field (not the auto-generated *App Code*).

### In vRealize Automation:
1. Go to **Cloud Assembly > Infrastructure > Integrations** and **Add Integration**.
2. Select the **IPAM** integration type.
3. Give it a name, then click **Manage IPAM Providers > Import Provider Package**.
4. Upload `phpIPAM.zip` (get it [here](https://github.com/jbowdre/phpIPAM-for-vRA8/releases/latest)).
5. Back at the **New Integration** page, click the **Provider** dropdown and select *phpIPAM*.
6. Enter the **API App ID**, **Username**, **Password**, and **Hostname** of the phpIPAM server (fully-qualified name or IP address).
7. (Optional) [Configure the subnet filter](docs/custom_field.md#configure-integration).
7. Click **Validate** to verify the information. It may take a minute or two for the validation to complete.
8. Once validated, click **Add**.

You can then learn how to utilize the new IPAM integration [here](https://docs.vmware.com/en/vRealize-Automation/8.2/Using-and-Managing-Cloud-Assembly/GUID-9AE32BD7-2D1B-4FEE-881F-A0EDE5907D10.html)

See [VMware's IPAM SDK README](README_VMware.md) for information on how to adapt the code if needed.
