## Version - 0.0.31a - [8dce4d6](https://github.com/k8thekat/AMPAPI_Python/commit/8dce4d668550a3dd2794c4040596d9f5077aba02)
#### Overall Changes -
- Update "DEBUG" prints to provide better information. 
- Added *ADS Only* requirements to specific end points to prevent failure. -
- Version bumped `__init__.py`

#### Setup.py
- Added `project_urls=`
    - Added *Github* and *Changelog* links for Pypi.

#### Core.py -
- Added `Core.add_datastore()`. 
- Added `Core.get_api_spec()` to access API information for an ADS or Instance.

#### Base.py -
- Moved `Base._on_connect()` into `Base._call_api()` to simply code. 
- Added docstring to `Base.parse_data()`
- Fixed camelcase issue with `Base.InstanceId` to `Base.InstanceID` to match Controller to Instance dataclass. 

#### Util.py -
- Added `APIUtil.parse_get_api_spec()` to create the `./docs/api_spec.md` 
- Fixed filepaths for `APIUtil` functions to point to `../docs/`

#### Instance.py -
- Added `AMPInstance` class to bring together API and Instance dataclass similar to `ADSInstance`

#### Minecraft.py -
- Added `minecraft.py` to house `MinecraftModule` API endpoints. (Still needs dataclasses/returns finished) 
