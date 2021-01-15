Sample IPAM Integration
============

A reference implementation of an IPAM integration plugin for vRA(C) 8.x

Use this documentation as a step by step guide for creating your own IPAM plugin.

For more information about the IPAM integration see: [vRA IPAM plugin reference documentation]

[vRA IPAM plugin reference documentation]: https://docs.vmware.com/en/VMware-Cloud-services/1.0/ipam_integration_contract_reqs.pdf

Prerequisites
===============

The following software should be installed and configured in order to use this plugin:

1. **Java 8**

2. **Maven 3** (Used for packaging the IPAM zip)

3. **Python 3** (The IPAM plugin is based on Python)

4. **Docker** (Docker is used to collect Python dependency libs that are needed by the IPAM plugin)

5. **Internet access** (The IPAM SDK relies on Maven Central, Docker HUB & PIP during packaging time. **Internet access is not required during runtime.** More details below)

Note: You can use a higher version of the above software as long as it is backward compatible.

Guide for creating the IPAM package
===============

Step 1: Package the scripts
----------------

Maven & Docker are used during build time to package the Python scripts into IPAM.zip distribution.
Maven enables the building of the IPAM package to be platform independent. This allows integrators to develop their IPAM integration solution under any Java-enabled OS - Windows, Unix, Mac, etc...

Docker is used during build time to start up a Photon OS container. All 3rd party libraries that the IPAM plugin depends on are downloaded during build time, using PIP, from within the Photon OS docker container. This guarantees that all Python lib binaries will be compiled exactly for Photon OS which is the OS of the Running Environment that is going to be executing the IPAM Python actions.

The first thing you can do is build the package by following the instructions below:

1. Open the `pom.xml` and modify the following properties:

    `<provider.name>SampleIPAM</provider.name>`
    `<provider.description>Sample IPAM integration for vRA</provider.description>`
    `<provider.version>0.1</provider.version>`

    Replace these property values with the name, description & version of your choice.
    The provider.name will be used as a display name in vRA(C) when you deploy the plugin zip, along with the description & version.
    
    Note: 
    Use the src/main/resources/CHANGELOG.md file to document any bug fixes, features and additions to the plugin over the course of time when a new plugin version is released. The file is included in the final plugin zip distribution so that vRA end-customers would know what is new in the plugin.

2. Update the logo.png file with the logo icon of your company (advisable)

    The vRA(C) UI uses the logo.png file located in ./src/main/resources when displaying the IPAM endpoints you create using this package.
     
3. (Optional) Change the IPAM Integration endpoint custom form.

    This is done by modifying the endpoint-schema.json file located in ./src/main/resources. It contains the custom form definition that renders the IPAM provider's specific fields
during IPAM endpoint registration. You can change it however you like except that **it is required that this file contains entries for privateKey and privateKeyId fields.**

    Note: In ./src/main/resources you can also see the registration.yaml file. It contains meta information about the contents of the package.
**Don't change anything in this file.**

4. Run `mvn package -PcollectDependencies`

    **This produces a SampleIPAM.zip file under ./target.**
    **The zip should be ready for deployment into vRA(C).**

    Notice that the first time you run this command, it could take up to several minutes to complete packaging the IPAM zip.
    The reason for that is because the first time the script runs it attempts to collect any 3rd party Python libs that
    the plugin depends on - such as **requests**, **pyopenssh** & others.

    Next consecutive runs of `mvn package` **will not** trigger another collection of 3rd party libs because this is time consuming and most often unnecessary.
    In order to re-trigger collection of dependencies (could be needed in case you introduced a new 3rd party Python lib) you must provide the `-PcollectDependencies` option again.

    Note:
    If you are building the package on Linux you must add one additional parameter to the build: `-Duser.id=${UID}` 
    (`mvn package -PcollectDependencies -Duser.id=${UID}`)

Now the IPAM package is ready to use.
We advise you to test whether it works by uploading it in vRA(C) and then checking that the actions are triggered when they should be and executed successfully.
For example, create a new IPAM endpoint and choose the package you uploaded in the **Provider** dropdown, enter an arbitrary username and password, enter **httpbin.org** as a **Hostname** and click on `Validate`.
You should see the **Validate Endpoint** action is triggered in the **Extensibility** tab. It should complete successfully.

Step 2: Get familiar with the IPAM operations and their skeleton implementations
----------------

After checking that the packaging of the sample IPAM scripts works, you can start exploring the code.
Under ./src/main/python you'd find separate directory for each IPAM specific operation that the plugin supports.

| Operation name              | Description                                                                                                                               | Script                                          | Required |
| ----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------|:---------|
| Allocate IP                 | Allocates the next available IP for a VM                                                                                                  | ./src/main/python/allocate_ip/source.py         | Yes      |
| Deallocate IP               | Deallocates an already allocated IP                                                                                                       | ./src/main/python/deallocate_ip/source.py       | Yes      |
| Get IP Ranges               | Data collects IP ranges & networks from the IPAM provider                                                                                 | ./src/main/python/get_ip_ranges/source.py       | Yes      |
| Update Record               | Updates the created host record. Could be used to update MAC address of VM after it has been provisioned                                  | ./src/main/python/update_record/source.py       | No       |
| Validate Endpoint           | Validates that the IPAM endpoint credentials are valid and that a connection to the external IPAM system can be established successfully  | ./src/main/python/validate_endpoint/source.py   | Yes      |
| Allocate IP Range           | Creates network inside some of the specified IP blocks                                                                                    | ./src/main/python/allocate_ip_range/source.py   | No       |
| Deallocate IP Range         | Deletes an already allocated network                                                                                                      | ./src/main/python/deallocate_ip_range/source.py | No       |
| Get IP Blocks               | Data collects IP blocks                                                                                                                   | ./src/main/python/get_ip_blocks/source.py       | No       |

The ./src/main/python/\*\*/source.py scripts contain the Python source code that would be used by vRA(C) to perform the respective IPAM operation.

Each script defines a `def handler(context, inputs):` function that is the entry point into the IPAM operation. vRA(C)'s IPAM framework calls the respective operation's `handler` function, passing request specific inputs in the form of Python dictionary along with the context object that can be used to securely connect to vRA(C) and call its services.

Step 3: Implement the IPAM operations
----------------

Integrators can choose to implement the `def handler(context, inputs):` function of each IPAM operation's source.py script from scratch, as long as they conform to the contract defined in the [vRA IPAM plugin reference documentation]

---
**We advise against implementing the operations from scratch.**
Instead, integrators can utilize the `vra_ipam_utils` library located in ./src/main/python/commons/vra_ipam_utils which contains utility functions and classes that will help with the `def handler(context, inputs):` implementation.

The source.py code already makes use of the `vra_ipam_utils` lib so you can look at it as reference:

```python
def handler(context, inputs):

    ipam = IPAM(context, inputs)
    IPAM.do_validate_endpoint = do_validate_endpoint

    return ipam.validate_endpoint()

def do_validate_endpoint(self, auth_credentials, cert):
    # Your implemention goes here
    ...
```
All you need to do in order to implement an operation is add your specific logic in the places indicated by the comments in the corresponding source.py file.
**Tip: It is a good idea to build the package, upload it in vRA(C) and test it after implementing each operation.**

We advise integrators to implement the IPAM operations one by one in the following order:

    1. Validate Endpoint
    2. Get IP Ranges
    3. Get IP Blocks (Optionally)
    4. Allocate IP
    5. Allocate IP Range (Optionally)
    6. Deallocate IP
    7. Deallocate IP Range (Optionally)
    8. Update Record (Optionally)

----

**Tip: How to call vRA(C) REST endpoints from within the IPAM operation**\
You can execute REST calls against vRA from within the Python scripts.
This is done by using the ```context``` object in your ```handler```

```python
context.request(link='/iaas/api/machines', operation='GET', body='')
```
The ```context``` is configured to handle authentication, authorization and proxying of your requests.

Step 4: Define 3rd party libraries (in case you use some)
----------------

In order to use 3rd party Python libs in the source.py scripts, you need to define them in the `requirements.txt` file that is located next to each IPAM operation's source.py.

The plugin build script takes care of downloading the dependency libs defined in `requirements.txt` and package them in the correct format within the IPAM zip.

The only important thing to remember here is to always re-run `mvn package -PcollectDependencies`  every time you add or remove new dependency from the `requirements.txt`

The `requirements.txt` format is defined [here](https://pip.readthedocs.io/en/1.1/requirements.html)

Step 5: Change specific properties in the `pom.xml` (if needed)
----------------

**Implementing the optional Update Record operation**\
Integrators can choose to optionally implement the Update Record operation.
This operation is used by the vRA(C) IPAM service to notify the external IPAM system that a VM has been successfully provisioned and to propagate the VM's MAC address to the IPAM system.

Support of this optional operation is controlled by the following property in the `pom.xml`:
`<provider.supportsUpdateRecord>true</provider.supportsUpdateRecord>`

Changing this to `false` will force the build to exclude the Update Operation from the IPAM.zip package.

**Note**: If you ever change the property value from `false` to `true`, you'd have to re-run the build with `mvn package -PcollectDependencies` since the dependencies for the Update Operation would need to be re-collected.

----
**Implementing the optional 'Get IP Blocks', 'Allocate IP Range' and 'Deallocate IP Range' operations**\
The three operations are part of the extended IPAM plugin specification for vRA 8.X. They enable the plugin to support provisioning of on-demand networks from vRA.
Every time a vRA user requests to provision an on-demand network on i.e. NSX-T, a CIDR for that network will be allocated from the plugin along with other network settings such as default gateway.

The support for this operations is controlled by the following property in the `pom.xml`:
`<provider.supportsOnDemandNetworks>false</provider.supportsOnDemandNetworks>`

Changing this to `true` will force the build to include the `get_ip_blocks`, `allocate_ip_range` and `deallocate_ip_range` operations inside the IPAM.zip package.

**Note**: The same as with the Update operation, changing the `provider.supportsOnDemandNetworks` property from `false` to `true` must be followed by re-run of the `mvn package -PcollectDependencies` command in order to collect the required dependencies.

----
**Supporting address spaces**\
External IPAM networks & ranges can be organized into logical groups with overlapping address spaces, serving a single routing domain.
By default, the **SampleIPAM.zip** that this SDK produces is configured to not support address spaces. If your IPAM system does have the notion of an address space, you can choose to enable support for address spaces. This is done by changing the following property in the `pom.xml`:
`<provider.supportsAddressSpaces>true</provider.supportsAddressSpaces>`

Step 6: Build the package with the implemented IPAM operations (actually, it is advisable to do so after implementing each operation)
----------------
It is a good idea to deploy the package to vRA(C) and test the operations after implementing each IPAM operation.
When you're ready with your implementation, you can build the package by running `mvn package` (or `mvn package -PcollectDependencies` if needed) again.
After you implement all of the required operations (and some optional ones, if you choose to do so), the IPAM package is ready to be distributed and used.

Troubleshooting
===============

The following list contains the most common errors that might occur during build time:
1. `mvn package` build fails with:

    > [ERROR] Plugin org.apache.maven.plugins:maven-resources-plugin:3.1.0 or one of its dependencies could not be resolved: Failed to read artifact descriptor for org.apache.maven.plugins:maven-resources-plugin:jar:3.1.0: Could not transfer artifact org.apache.maven.plugins:maven-resources-plugin:pom:3.1.0 from/to central (https://repo.maven.apache.org/maven2): repo.maven.apache.org: Unknown host repo.maven.apache.org -> [Help 1]

    **Resolution**:
    Sometimes establishing connections to Maven Central fails. Retry again after couple of minutes. If the issue persists - check your internet connection.

2. `mvn package -PcollectDependencies` build fail with:
    >[ERROR] DOCKER> Unable to pull 'vmware/photon2:20180424' : error pulling image configuration: Get https://production.cloudflare.docker.com/registry-v2/docker/registry/v2/blobs/sha256/12/1204ad97f071063bea855f351348e15e9cc03610cbfc8df46ab96b42d7cafa9f/data?verify=1578042999-Nu9yKJgKQcuFU0Y9hAQe%2BKEOKGo%3D: dial tcp: lookup production.cloudflare.docker.com on XXX:53: read udp XXX:57798->XXX:53: i/o timeout

    **Resolution**:
    Sometimes establishing connections to the Docker Registry times out. Retry again after couple of minutes. If the issue persists - check your internet connection

3. `mvn package -PcollectDependencies` build on `Windows` fails with:
    > [ERROR] Failed to execute goal io.fabric8:docker-maven-plugin:0.31.0:start (start-container) on project sample-ipam: I/O Error: Unable to create container for [ipam-dependency-collector:latest] : Drive has not been shared (Internal Server Error: 500)

    **Resolution**:
     The build script uses Docker to collect the Python dependencies that are needed by the plugin. In order for Docker to operate correctly, it needs to have access to the Windows Drive that the build script resides in.
     You need to allow Docker access to the respective drive: [Configure shared volume on Docker for Windows](https://blogs.msdn.microsoft.com/stevelasker/2016/06/14/configuring-docker-for-windows-volumes/)
4. `mvn package -PcollectDependencies` build fails with:
    > [INFO] --- docker-maven-plugin:0.31.0:start (start-container) @ sample-ipam ---
[ERROR] DOCKER> Error occurred during container startup, shutting down...
[ERROR] DOCKER> I/O Error [Unable to create container for [ipam-dependency-collector:latest] : {"message":"Conflict. The container name \"/ipam-dependency-collector-1\" is already in use by container \"2bfb215381514cd6496ecd5d0103da0a4d94034c5691b25bdf27b16bd2236022\". You have to remove (or rename) that container to be able to reuse that name."} (Conflict: 409)]

    **Resolution**:
    Run `docker ps -a `
The output should look similar to this:
    | CONTAINER ID | IMAGE | COMMAND | CREATED | STATUS | PORTS | NAMES
    | ------------ | ----- | ------- | ------- | ------ | ----- | ---- |
    | 2bfb21538151 | d886e9bba96e | "/bin/sh -c 'yes \| c…" | 3 minutes ago |      Exited (0) 3 minutes ago | | ipam-dependency-collector-1

    Locate the container with name `ipam-dependency-collector-*` and purge it:
    Run `docker rm -f 2bfb21538151`
5. `mvn package -PcollectDependencies` build fails with:
    > [INFO] --- docker-maven-plugin:0.31.0:build (build-image) @ sample-ipam ---
    > [INFO] Building tar: ...\sample-abx-integration\target\docker\ipam-dependency-collector\latest\tmp\docker-build.tar
    > [INFO] DOCKER> [ipam-dependency-collector:latest]: Created docker-build.tar in 214 milliseconds
    > [ERROR] DOCKER> Unable to build image [ipam-dependency-collector:latest] : "The command '/bin/sh -c tdnf install -y python3-3.6.5-1.ph2 python3-pip-3.6.5-1.ph2 shadow &&     pip3 install --upgrade pip setuptools &&     pip3 install certifi' returned a non-zero code: 127"  ["The command '/bin/sh -c tdnf install -y python3-3.6.5-1.ph2 python3-pip-3.6.5-1.ph2 shadow &&     pip3 install --upgrade pip setuptools &&     pip3 install certifi' returned a non-zero code: 127" ]

    **Resolution**:
    Sometimes the **tdnf** Photon OS package manager fails to install Python3 due to connectivity errors.
    In case this happens, please wait for 1 min and retrigger the build.
    If the issue persists, check your internet connectivity.

Changelog
============

## IPAM SDK 1.1.0:
**Features:**
- IPAM actions are now packaged for Python 3.7.5 runtime. User's 3rd party libraries that contain binaries (defined in requirements.txt and gathered during build time when -PcollectDependencies is supplied) are now compiled against Python 3.7.5 runtime (as opposed to Python 3.6).
If you upgrade from SDK 1.0.0, you'd have to recompile with -PcollectDependencies so that new libs for Python 3.7.5 are gathered.
- This version adds a new CHANGELOG.md file in src/main/resources to allow IPAM SDK users to keep track of bug fixes, features and additions to the plugin over the course of time when a new plugin version is released.

**Bug fixes:**
- As part of this release, a known permission issue for Linux users is fixed by adding the `-Duser.id` parameter.
