# AMP API Python

---

CubeCoders AMP 3 API wrapper in Python.

<div align="left">
    <a href="https://discord.gg/BtNyU8DFtt"><img src='https://img.shields.io/discord/705500489248145459?color=blue&label=Discord&logo=Discord%20Server&logoColor=green' alt='Discord Server'></a>
</div>

![Version](https://img.shields.io/pypi/v/cc-ampapi?label=PyPI&include_prereleases)

> **This is the AMP 3 beta, `6.0.0b5`.** It is built against AMP 3's preview builds, tested on AMP 3.0.0, 3.0.1 and 3.0.2, and only talks to AMP 3.
> For AMP 2, use the 5.x releases, which keep supporting it. A plain `pip install cc-ampapi` never picks up this beta.
>
> A version named in the docs, eg. "AMP 3.0.0", is AMP's version. The library's own version is `ampapi.__version__`.

### AMP 3

---

- **AMP 3's API is not published.** Every call here was worked out from the web panel, so any of them can change between AMP builds.
- AMP 3 renamed some of AMP's terms, and the library uses AMP 3's terms:
  - An Instance is a **shard** (`Shard`).
  - An ADS or a Target is a **spire** (`Spire`).
  - A game definition is a **template**, eg. `minecraft-java` or `teeworlds`.
- Coming from 5.x, `Session` takes the place of `Bridge` and `Panel` takes the place of `Controller`.

### Key Features

---

- Pythonic API wrapper using `async` and `await`, built on `aiohttp`.
- `Session` handles the login: it renews the token before it runs out, logs in again when AMP ends the session, waits out a short AMP outage the way the web panel does, and takes a recovery code when the account needs a second factor. Calls waiting on a login that fails all raise its error, rather than each trying again.
- `Panel` groups every API area (accounts, analytics, audit, credentials, enrolments, networking, platform, shards, spires, tasks and templates) in one object.
- Taking an invite needs no account yet: make a `Session` with any username, eg. `""`, and the password you want, then call `session.accept_invite(...)`. It logs in as the new account.
- `Shard` and `Spire` objects carry the calls that act on them, eg. `await shard.start()`.
- Typed replies: `TypedDict`s for most calls, and small objects for live data such as `ShardStatus`, `ConsoleLine` and `RunningTask`. The package ships `py.typed`.
- File downloads and uploads, including AMP's chunked upload for big files.
- Every request and AMP's reply can be saved as redacted JSON files, see [Capturing replies](#capturing-replies).
<!-- The hubs are set aside for now (#3-50.1).
- Live events from AMP's hubs, through decorators on your own `Shard`, `Spire` and `Panel` subclasses, or plain functions.
-->

### Docs

---

- There are no hosted docs for the 6.0 beta yet. The docstrings carry them, so your editor's hover is the place to look.
- The 5.x docs are at https://ampapi-python.readthedocs.io/en/latest/

### Installing

---

_Python 3.12 or higher is required_

### PyPi

---

-> Visit the package on [Pypi](https://pypi.org/project/cc-ampapi/)

The beta is a pre-release, so pip only picks it up with `--pre`. This works once the beta is published to PyPI:

```bash
# Linux/macOS/Windows
pip install --pre cc-ampapi
```

Until then, install it from this branch on GitHub:

```bash
pip install git+https://github.com/k8thekat/AMPAPI_Python@AMP3-beta
```

### Basic Usage

---

In your IDE Python file. -> `import ampapi`.

1. Make a `Session` with the panel's URL and a login. It logs in on the first call that needs it.
2. Hand it to a `Panel`, which has the API calls. Logging in and taking an invite are on the `Session` itself.
   - Leaving an `async with` block, or `await panel.clean_up()`, logs out and closes the session.
3. A call on the `Panel` takes IDs, eg. `panel.start_shard(shard_id=...)`. The same call on a `Shard` drops the ID, eg. `shard.start()`.

```py
import asyncio

from ampapi import Panel, Session, Shard, ShardState, ShardStatus


async def main() -> None:
    # You can pull these values from an `.ini` or a `.env` file.
    session = Session(url="http://192.168.1.10:8443", username="amp_username", password="amp_password")

    async with Panel(session=session) as panel:
        shards: list[Shard] = await panel.get_shards()
        for shard in shards:
            state: ShardStatus = await shard.get_state()
            print(shard.display_name, state.status, state.is_running)

            # AMP answers a start before the game is up, so check `get_state()` again to see it running.
            if shard.display_name == "Minecraft" and state.status == ShardState.stopped:
                await shard.start()


asyncio.run(main())
```

See [samples](./samples) for scripts you can run against your own panel. Each one reads the panel's URL and login from `AMP_URL`, `AMP_USER` and `AMP_PASSWORD`. `shard_control.py` and `files.py` also take the shard's ID from `AMP_SHARD`.

- `basic.py`: log in, list the spires and shards, and read a shard's state.
- `shard_control.py`: start a shard, send a console command, read the console back and stop it.
- `files.py`: list, upload, read, download and delete a shard's files.
<!-- The hubs are set aside for now (#3-50.1), so these two samples are commented out.
- `live_events.py`: class-level and instance-level listeners, until Ctrl+C.
- `discord_cog.py`: a discord.py cog that posts shard state changes to a channel.
-->

<!-- The hubs are set aside for now (#3-50.1).
### Live events

---

AMP 3 pushes live events through its hubs. The library keeps the sockets up, connects again after a drop, and hands each event to your listeners as an object.

A listener is a method on your own `Shard`, `Spire` or `Panel` subclass, marked with `@ShardHub.listener(...)`, `@SpireHub.listener(...)` or `@PanelHub.listener(...)`. Each one gets its own queue, so it keeps its order and a slow one doesn't hold up the rest.

```py
import asyncio

from ampapi import ConsoleLine, Panel, Session, Shard, ShardHub


class MyShard(Shard):
    @ShardHub.listener(name="console")
    async def on_console(self, data: ConsoleLine) -> None:
        print(f"[{self.display_name}] {data.text}")


async def main() -> None:
    session = Session(url="http://192.168.1.10:8443", username="amp_username", password="amp_password")

    # `get_shard` and `get_shards` hand back `MyShard` objects now.
    async with Panel(session=session, shard_class=MyShard) as panel:
        # The panel only holds its shards weakly, so keep your own reference.
        shard: Shard = await panel.get_shard(shard_id="your shard ID")
        await panel.start_listening()
        await asyncio.sleep(300)
```

Or add a plain function to one object, eg. for a script or a discord.py cog. It gets the object first, then the event's data:

```py
from ampapi import Panel, ShardStatus

# Inside an `async with Panel(session=session) as panel:` block.


@panel.listen("state")
async def on_state(panel: Panel, data: ShardStatus) -> None:
    print(data.shard_id, data.status)


# The panel hears the shards and spires it subscribes. With no list, that's every one it can see, new ones included.
await panel.add_subscribers()
await panel.start_listening()
```

- Listeners hear nothing until `panel.start_listening()`, and `panel.stop_listening()` (or `clean_up()`) stops them.
- `panel.add_subscribers(...)` takes shards, spires and their IDs, mixed. `spire.add_subscribers(...)` does the same for the shards a spire's listeners hear, and with no list it takes every shard on that spire. An empty list raises `ValueError`.
- `remove_subscribers(...)` takes the same. Removing a few while the panel subscribes everything leaves it subscribing the rest, and `add_subscribers()` turns everything back on.
- **`console`**: AMP's console lines don't say which shard they came from. A `console` listener on a `Shard` opens that shard's own socket, so it only hears that shard. On a `Panel` or a `Spire`, the lines arrive without saying whose they are.
- **`auto_state`**: a `Shard` or `Spire` with `auto_state` on keeps its `state` attribute current from AMP's state events, with no listener and no `start_listening()`. It's off by default, so nothing opens a socket unless you ask. `Panel(session=session, auto_state=True)` turns it on for every shard and spire the panel hands out, and `auto_state=True` on `get_shard(...)`, `get_shards(...)`, `get_spire(...)`, `get_spires(...)` or a `Shard` / `Spire` you make yourself turns it on for those.

The events, and where you can listen for them:

- On a shard, a spire or the panel: `console`, `state`, `lifecycle`, `metrics`, `players`, `player_joined`, `player_left`, `migration`, `snapshot`, `schedule_run` and `task`. A shard gets its own tasks, a spire its own and its subscribed shards' tasks, and the panel every task.
- On a spire or the panel: `spire_state`.
- On the panel only: `spire_presence` and `network_status`.
-->

### Capturing replies

---

A `Session` can save every request it sends, and AMP's reply, as a JSON file. It's handy for a bug report, or for seeing what AMP really sent when a reply doesn't match its type.

- `Session(..., capture_dir=Path("captures"))` captures the whole run.
- `with session.capture(Path("captures")):` captures only the calls made inside the block.
- Every call is captured, logins, renewals and error replies included. Each file is named from the method and the path, with each ID as `{id}`, then the UTC time to the microsecond, eg. `GET_api_shards_{id}_state_2026-11-13_21-52-07.123456.json`, so a route's files sort in time order. A file already in the folder is never written over.
- Inside a `capture` block, a `capture_dir` the session was made with still gets every reply too.
- Each file holds the request (method, path, query parameters, headers and body) and the reply (status, the useful headers and body). A download or any other binary reply is kept as its content type and length only.
- Captures are redacted by default: tokens, passwords, keys, recovery codes and the `Authorization` header become `<redacted str len=N>`, a game's sign-in code is blanked, and public IP addresses become `<public ip>`. Private addresses are kept. `redact=False` writes them as sent, so keep those files to yourself.
- A capture that fails to write, eg. to a read-only folder, is logged as a warning and the call carries on.

```py
from pathlib import Path

from ampapi import Panel, Session

# Inside an `async with Panel(session=session) as panel:` block.
with session.capture(Path("captures")):
    await panel.get_shards()
```

### Errors

---

The errors from AMP are all `AMPAPIError`s. When AMP answers a call with an error, you get an `AMPAPIRequestError` carrying whatever AMP sent:

- `.status`: the HTTP status code.
- `.code`: AMP's dotted error key, eg. `shards.error.eulaRequired`, when it sends one.
- `.message`: AMP's message, when it sends one.
- `.errors`: the validation errors, eg. for a password the policy refuses, when it sends any.
- `.data`: the whole body: the decoded JSON, or the text of a reply that isn't JSON, eg. a proxy's error page.

```py
from ampapi import AMPAPIRequestError

try:
    await shard.start()
except AMPAPIRequestError as error:
    if error.code == "shards.error.eulaRequired":
        await shard.accept_eula()
    else:
        print(error.status, error.code, error.message)
```

A login that can't finish raises its own:

- `AMPAPILoginError` for a wrong username or password.
- `AMPAPIPasskeyRequiredError` when the account needs a second factor. Send one of its recovery codes to `session.second_factor(code=...)`.
- `AMPAPIPasswordChangeRequiredError` when AMP wants a new password first. `session.change_expired_password(new_password=...)` sets it and logs in.
