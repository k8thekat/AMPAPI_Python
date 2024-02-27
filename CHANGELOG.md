## Version - 0.0.32a - [a3973cc](https://github.com/k8thekat/AMPAPI_Python/commit/a3973cc)
#### __init__.py
- Version bump to `0.0.32a`.
- Version bump `0.0.31a`

#### Changelog.md
- Fixed layout of Version line.

#### ads.py
- Added logic to check `Instance.Module` attribute to create `AMPMinecraftInstance`.
- Updated `ADSInstance.AvailableInstances` return types to include `AMPMinecraftInstance`.

#### adsmodule.py
- Added docstring to `add_datastore()`.
- Added `await self._connect()` to all methods.

#### base.py
- Added `MINECRAFT_ONLY` attribute for logic checks.
- Removed `await self._connect()` from `_call_api()`.

#### core.py
- Added `await self._connect()` to all methods.

#### filebackup.py
- Added `await self._connect()` to all methods.

#### filemanager.py
- Added `await self._connect()` to all methods.
- Added comments for remaining filemanager methods.

#### instance.py
- Updated `__init__()` print debug for better naming conventions.
- Added `__all__` property to include `AMPInstance` and `AMPMinecraftInstance`.
- Added `AMPMinecraftInstance` class.

#### minecraft.py
- Creation of all Minecraft specific API endpoints and methods pertaining to them.
- Partial completion of dataclasses, docstrings and return types.
- Implemented logic to check `.Module` != `Minecraft` on all calls to prevent failure outside of the Instance class.
- Prefixed all methods with `mc_`.

#### types.py
- Added `BukkitPlugin()` dataclass.
"
"# Changelog.md
- Creation of Changelog.md and added `0.0.30a` under `0.0.31a`

#### Setup.py
- Added `project_urls` to `setup()`
	- Github and Changelog links

#### Base.py
- Added `TYPE_CHECKING` to fix `Self` import at runtime error.

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
