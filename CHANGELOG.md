## Version - 1.0.1 - [448e6ee](https://github.com/k8thekat/AMPAPI_Python/commit/448e6ee)
#### Changelog.md
- Version info from `1.0.0` added.
#### __init__.py
- Version bump to `1.0.1`

#### Overall
- Version bump v`1.0.1`
- Finished numpy docstring conversion throughout codebase.
	- implemented a different numpy-template for better Sphinx autodoc support and layout.
- Began conversion of data returns from Dataclasses to something simpler like TypedDicts and class definitions.
- Developed functions to generate .rst and API docs.
- Changed parameters of multiple functions for similarity and ease of understanding.
- updated docstring numpy format.
- added .rst files for Trigger events.
- added .rst files for Method events.
- added `types_.py` to further define JSON response data.

## Version - 1.0.0 - [922a08b](https://github.com/k8thekat/AMPAPI_Python/commit/922a08b)
#### Changelog.md
- Version info from `0.3.0` added.
#### __init__.py
- Version bump to `1.0.0`

#### Overall
- Implementation of Sphinx documentation.
- Added `gitHub` actions to handle changelog building.
- Switched to `pyproject.toml` and `ruff`.
	- Changed docStrings to `numpy`.
- Added LICENSES for MIT for borrowed libraries.
- Restructured dataclass file layout and enums.
- Auto-generator for Setting Nodes/Permission Node rst files.

## Version - 0.3.0 - [68556f7](https://github.com/k8thekat/AMPAPI_Python/commit/68556f7)
#### Changelog.md
- Version info from `0.2.0` added.
#### __init__.py
- Version bump to `0.3.0`

#### Overall
- Fixed script patths
- Updated to `2.5.1.4` | Build: `20240731.1`

#### __init__.py
- Version bump `0.3.0`.

#### ads.py
- Updated docstring to better communicate the point/usage of the `class ADSInstance()`.
- Updated function docstring's to a better format.
- Changed `AvailableInstances()` to a set.
- Changed
- Updated `property AvailableInstances()` docstring to give better information/understanding of what it returns.
	- Improved logic to include the `ADSInstance()` class to our `AMPMinecraftInstance()` and `AMPInstance()` inits.
- Added `AppState` property.

#### adsmodule.py
- Added `ADSonly` decorator to every function to validate the Module is correct before making the API call.
- Updated function docstring's to a better format.
- Changed logic handling for passed in dataclass's for multiple methods.
- Added type hinting throughout.

#### analytics.py
- Implementation of `class AnalyticsPlugin()`.
	- Added a `get_analytics_summary()` function which supports a `period_days`, `start_date` and `filters`.

#### base.py
- Updated function docstring's to a better format.
- Added `ADSonly()` decorator to validate the Module is of `ADS`.
- Added `online()` decorator to check if the Instance is `Running`.
- Added a length check to the `token` parameter of the Bridge.
- Added type hinting throughout.
- Added debug prints to `_call_api()`
- Added a `_no_data` parameter to `_call_api()` to support endpoints without data returns.

#### bridge.py
- Updated function docstring's to a better format.

#### core.py
- Updated function docstring's to a better format.
- Made `start_instance()`, `stop_instance()`, `restart_instance()` and `kill_instance()` deprecated.
	- Replaced with `start_application()`, `stop_application()`, `restart_application()` and `kill_application()`.
- Added `run_security_check()` - UNK data return, waiting on info.
- Made `update_amp_instance()`, `restart_amp()` and `upgrade_amp()` ADS only methods as that is their intention.

#### emailsender.py
- Updated function docstring's to a better format.

#### filebackup.py
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### filemanager.py
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### instance.py
- Added a `debug` print to the `__init__()`.
- Fixed attribute access issues and added docstring's to commonly used properties for better clarification.
- Added `start()`, `stop()`, `restart()` and `update()` functions to control the Instance from inside the Instance.
- Added `online()` decorators to validate an instance is `Running`.
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### minecraft.py
- Added a `MConly()` decorator to check the instance Module is `Minecraft`.
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### types.py
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### util.py
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### docs/
- Updated ADS API Spec
- Updated Minecraft API Spec
- Version info from `0.2.0` added.

## Version - 0.2.0 - [4b70f0d](https://github.com/k8thekat/AMPAPI_Python/commit/4b70f0d)
#### Changelog.md
- Version info from `0.1.11` added.
#### __init__.py
- Version bump to `0.2.0`

#### Readme.md
- Updated naming of methods in Quick Example.
	- Added a Sample_Analytics_API() method.
- Added a section called Basic Usage to help people understand how to setup the Bridge and API Params.

#### __init__.py
- Version bump `0.2.0` release.

#### ads.py
- Removed `LocalFileBackupPlugin` from ADSInstance class inheritance as the ADS no longer has backup functionality.
- Removed un-used imports.

#### analytics.py
- New API class to support AMP `2.5.1.0` Update which introduces Analytics!
- Added `get_analytics_summary()` method to retrieve the Instance Analytics Summary.

#### core.py
- Added `get_authentication_requirements()` method to retrieve a users Auth requirements.

#### emailsender.py
- Added `test_SMTP_settings()` method to validate SMTP settings for an Instance.

#### filebackup.py
- Added `refresh_backup_list()` method to refresh the list of backups an Instance has.

#### instance.py
- Added `AnalyticsPlugin()` API class to `AMPInstance` class inheritance for the new Analytics feature from `2.5.1.0`.

#### base.py
- Fixed typo in `parse_data()` docstring.

#### types.py
- Added dataclasses for Analytics.
	- Added `Analytics_Filter()` to assist with filtering Analytics API call.
	- Added `Analytics_Summary()` to handle the data from `get_analytics_summary()` method call.
	- Added `Analytics_Country_data()`, `Analytics_Stats()` and `Analytics_Top_Players()`  to assist attributes of `Analytics_Summary()`.

#### util.py
- Added an `AMP_to_API_update()` method to wrap over `parse_get_api_spec()`. *No current usage at this time*
- Changed `parse_get_api_spec()` to a staticmethod.
- Fixed typo in version syntax.

#### Changelog.md
- Version info from `0.1.11`.

## Version - 0.1.11 - [4b8c37a](https://github.com/k8thekat/AMPAPI_Python/commit/4b8c37a)
#### requirements.txt
- Changed all version checks to be equal to or greater than the package version.

#### Changelog.md
- Version info from `0.1.1`.

#### __init__.py
- Version bump `0.1.11`

#### Overall
- Added `ADS_api_spec.md` document.

## Version - 0.1.1 - [0cf953e](https://github.com/k8thekat/AMPAPI_Python/commit/0cf953e)
#### __init__.py
- Version bump `0.1.1`
- Changed formatting of releaseLevel and `__version__` to match *PEP440*

#### changelog.md
- Version info from `0.0.42b` and `0.1.0r`

## Version - 0.1.0r - [ac16314](https://github.com/k8thekat/AMPAPI_Python/commit/ac16314)
#### __init__.py
- Version bump to `0.1.0r`
- Changed `releaseLevel` to "release"
- Version bump `0.1.0r`

#### setup.py
- Changed classifiers from "Alpha" to "Production/Stable"

#### ads.py
- Added `_AvailableInstances` as an attribute to better handle population of `AvailableInstances` attribute.
- Added `_Controller_exists` as an attribute to catch attribute errors for the Controller dataclass that ADSInstance inherits from when accessed prior to class creation/population.

#### adsmodule.py
- Updated `detatch_target` to `detach_target` to align with the `v2.5.0.12` AMP Update.
- Updated the API endpoint for `detach_target` to align with the `v2.5.0.12` AMP Update.

#### base.py
- Added parameter declaration to the `fields()` method.

#### core.py
- Formatting change on one line.
- Updated return type for `get_api_spec()`

#### types.py
- Added `to_str()` method to the `AMP_Version()` dataclass to be used for future plans.
- Removed an un-needed `# type:ignore`

#### util.py
- Formatting changes on multiple lines.
- Re-wrote logic for `parse_get_api_spec()`
	- Added the `@classmethod` decorator for usage prior to `APIUtil` class generation.
	- Added Instance Type, Version and Build strings to the output document to better compare API changes between versions.
	-- Improved formatting of data output from API parsing.

## Version - 0.0.42b - [2bf7996](https://github.com/k8thekat/AMPAPI_Python/commit/2bf7996)
#### Changelog.md
- Version info from `0.0.41b`

#### __init__.py
- Version bump `0.0.42b`

#### README.md
- Added missing `await` in Quick Example - Sample_API().

#### ads.py
- Changed some prints to `_logger.debug()`.
- Type-hinted `ads_list` inside `get_instances()` method.
- Added logic check to `get_instances()` when not formatting data to prevent error.

#### base.py
- Removed `type:ignore` from `__init__()`.
- Added return value to `format_data` setter.
- Added `_logger.debug()` for monitoring data formatting.
- Fixed logic when formatting data causing return failure using the `ADSInstance` class.
- Improved readability of format logic of `_call_api()`.

#### bridge.py
- Added logging.
- Changed `apiparams` to `api_params`.
- Added type-hinting to `__new__()`.
- Added `_logger.debug()` to `__init__()`.

#### minecraft.py
- Removed unused imports.

#### types.py
- added `repr = False` to the `Controller()` dataclass.

## Version - 0.0.41b - [5b0aed8](https://github.com/k8thekat/AMPAPI_Python/commit/5b0aed8)
#### __init__.py
- Version bump `0.0.41b

#### types.py
- Added `LastExecuteError` and `LastErrorReason` to `Triggers()` dataclass.

#### base.py
- Removed un-used code.

#### Changelog.md
- Version log - `0.0.40b`

## Version - 0.0.40b - [b055fb3](https://github.com/k8thekat/AMPAPI_Python/commit/b055fb3)
#### Readme.md
- Changed TestPypi to Pypi
	- Updated bash commands for installing package.

#### init.py
- Version bump `0.0.40b`

#### Overall
- `isort` imports

## Version - 0.0.39b - [778bb87](https://github.com/k8thekat/AMPAPI_Python/commit/778bb87)
#### __init__.py
- Version bump `0.0.39b`
- Added `MANIFEST.in`

#### setup.py
- Re-added requirements.txt

## Version - 0.0.38b - [970db4b](https://github.com/k8thekat/AMPAPI_Python/commit/970db4b)
#### setup.py
- Changed `install_requires` to a list instead of a prepopulated list.

#### __init__.py
- Version bump `0.0.38b`

## Version - 0.0.37b - [63121cc](https://github.com/k8thekat/AMPAPI_Python/commit/63121cc)
#### __init__.py
- Version bump `0.0.37b`

#### requirements.txt
- Removed `setuptools`

## Version - 0.0.36b - [c9417a3](https://github.com/k8thekat/AMPAPI_Python/commit/c9417a3)
#### __init__.py
- Version bump `0.0.36b`

#### Changelog.md
- Fixed typos.

## Version - 0.0.35b - [585ecf3](https://github.com/k8thekat/AMPAPI_Python/commit/585ecf3)
#### __init__.py
- Version bump `0.0.35b`

#### README.md
- Updated description and key features.
- Added coding examples.

#### requirements.txt
- Added `setuptools` to requirements.

#### ads.py
- Removed unused methods.

#### base.py
- Changed type check of `parse_data()` data parameter.

#### core.py
- Changed return type `Status` to `AppStatus`.

#### types.py
- Changed `Status` to `AppStatus`.

#### instance.py
- Added `State` property to return `AppState`
- Added `AppStatus` and `Updates` to class inheritance.
- Added `.get_status()` methods to AMPInstance to set self class attributes.
- Added `get_updates()` methods to AMPInstance to set self class attributes.

## Version - 0.0.34b - [9ac1e3c](https://github.com/k8thekat/AMPAPI_Python/commit/9ac1e3c)
#### __init__.py
- Switched from `ALPHA` to `BETA`
- Version bump `0.0.34b`

#### Readme.md
- Updated documentation.
- Referenced the package as a wrapper now.

#### setup.py
- Updated name and description to properly represent the package as a wrapper.

#### ads.py
- Removed prints from development.
- Updated doc strings and methods for `format_data` parameter.
- Added logic for when there is no instances from `get_instances()`

#### adsmodule.py
- Added all endpoints for "API/ADSModule/".
- Formatted `get_instance()` to pep8.

#### base.py
- Added global var `FORMAT_DATA`
- Added time to live value for sessions. See `session_ttl`, default 240 seconds.
- Added `FAILED_API` for exception raising.
- Added `format_data` property to access the global `FORMAT_DATA`
- Added `camel_case_data()` method to camel case keys of a dictionary.
- Added `dataclass_to_dict()` to unpack a dataclass into a dictionary.
- Added `json_to_dataclass()` to format the JSON response from API calls into dataclasses.
- Refactored `_call_api()` and added support for `FORMAT_DATA`.
	- Moved data formatting into `json_to_dataclass()` method.
- Refactored `_connect()` and improved session handling.

#### bridge.py
- Removed commented out code and commented out print statements.
- Revered `Self` change due to import error.

#### core.py
- Added remaining `API/Core` endpoints and added `format_data` functionality.
- Updated doc strings.

#### filebackup.py
- Updated method functionality to support `format_data`.
	- Updated doc strings to match.
- Finished remaining API endpoints.
	- TODO - Finish return types.

#### filemanager.py
- Updated method functionality to support `format_data`.
	- Updated doc strings to match.
- Finished remaining API endpoints.
	- TODO - Finish return types.

#### instance.py
- Commented out print statements.

#### minecraft.py
- Updated method functionality to support `format_data`.
	- Updated doc strings to match.

#### types.py
- Added multiple dataclasses to support added Endpoints.
- Added `APIParams()` to better assist users with connection setup.
- Added `APISession()` to better handle session TTL values.
- Updated multiple dataclasses to better handle data formatting.

# Overall
- Removed `api_spec.md` and created Instance Module specific documents.

#### utils.py
- Added `instance_type` parameter to `parse_get_api_spec()` to differentiate API endpoint specs in files.

# setup.py
- Added `CHANGELOG.md` to packages.

#### Changelog.md
- Version bump `0.0.33a`.

## Version - 0.0.33a - [4df55fa](https://github.com/k8thekat/AMPAPI_Python/commit/4df55fa)
#### __init__.py
- Version bump `0.0.33a`.

#### Changelog.md
- Version bump `0.0.33a`.

#### ads.py
- Added `if TYPE_CHECKING` for Self

#### bridge.py
- Added `if TYPE_CHECKING` for Self

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

# Changelog.md
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
