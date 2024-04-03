# AMPAPI_Python_wrapper
___
CubeCoders AMP API wrapper in Python. 

### Key Features
___

- Pythonic API wrapper using `async` and `await`.
- Data is in dataclasses for easier management and interaction.
    - Optional parameter per function or global to disable formatting of data.
- Parent classes `ADSInstance` and `AMPInstance` to group endpoints together and make handling of multiple Instances easier.
    - This will also limit Instance specific API endpoints (eg. Minecraft) to that Instance type only.

### Installing
___

*Python 3.9 or higher is required*

To install run the below command to install the required pip packages from [Requirements](./requirements.txt)

### Pypi 
-> https://pypi.org/project/cubecoders-amp-api-wrapper/
```bash
# Linux/macOS
pip install cubecoders-amp-api-wrapper

# Windows
pip install cubecoders-amp-api-wrapper
```


### Quick Example -

```py
# You can pull these values from an `.ini` or a `.env` file,
# then populate the NamedTuple APIparams from `types -> APIParams`
_params = APIParams(url="http://192.168.13.130:8080",
                    user="amp_username",
                    password="amp_password")

async def Sample_API():
    """
    Example API Function to call method Endpoints.
    """
    _bridge = Bridge(api_params=_params)
    ADS: ADSInstance = ADSInstance()
    # This would populate the ADS class property .AvailableInstances
    ADS.get_instances()
    # We can break out all our instances into their own attributes.
    arkinstance: AMPInstance | AMPMinecraftInstance = ADS.AvailableInstances[1]
    mcinstance: AMPInstance | AMPMinecraftInstance = ADS.AvailableInstances[2]

    # Pre populated from the dataclass and has the API methods too!
    # You can take a backup really easily.
    await arkinstance.take_backup(title="ARK1_backup", description="This is an ARK backup", sticky=True)

    # Then you can call instance type specific API methods.
    await mcinstance.mc_add_to_whitelist(user_or_uuid="k8_thekat")

    # You can also check attributes and other fields of the instance.
    mcinstance.InstanceName
    mcinstance.InstanceID

    # The State of the Instance. eg. Running, Offline, Restarting. See `types.py -> State_enum
    # This is NOT updated constantly. See about using `get_status()` to keep it current.
    if mcinstance.AppState == State_enum.Stopped:
        await mcinstance.start_instance()

    # You can also check Metrics of an Instance easily.
    mcinstance.Status.Metrics

    # Want to kick a random person? Here ya go~
    players: list[Players] = await mcinstance.get_user_list()
    await mcinstance.mc_kick_user_by_id(id=players[0].id)
```


### Controlling data formatting -
- All JSON data returned from the API endpoints is formatted into a Dataclass/Enum/etc if possible.
- Data formatting can be controlled globally or locally by changing the `format_data` parameter of the method to `False`.
    - When turning off the data formatting, typically you will get a `dictionary` back.

### Example -
```py
# By default all API calls will be formatted into Dataclasses if possible.
# You can toggle format_data off with ANY of the API classes that inherit Base().
ADS.format_data = False

# You can turn data formatting back on globally through any Instance object.
arkinstance.format_data = True

# You can turn off or on data formatting per function also.
await arkinstance.get_updates(format_data=False)
await arkinstance.get_role_data(format_data=True)

```