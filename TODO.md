# AMP API TODO

A small todo list local to the project.
Items carry a stable number (#3-N) for reference; `.local_data/plans/todo_index.md` tracks their type and status.
The `3-` marks the AMP3 index, so its numbers never meet the 5.x index's; AMP3 work began as #47, now #3-47.


## ampapi/session.py

---

- (#3-47.1) Confirm `PasskeyRequiredResponse` and `Session.second_factor` live; needs the panel on HTTPS, a passkey and recovery codes. *DONE*
- (#3-47.2) A SignalR hub client for live events, logging in with `Session.get_hub_token`. *DONE* to Kat's design (`hubs.py`, `objects.py`), now set aside while Kat reworks it (#3-50.1); left: an `auto_state` setter (waits for Kat), `UserLeft` (never arrived when Kat left her world, U18f), `Lifecycle` kinds 4 and 6.
- (#3-47.3) Confirm upstream report 01 (passkey registration needs `transports`) in a browser; trust vm3's Caddy root CA first.
- (#3-69) Raise `AMPAPIPanelVersionError` when the URL is an AMP 2 panel, pointing to `cc-ampapi~=5.0`. *DONE* (the AMP 2 line's own check is 5.x #47)

## Releases

---

- (#3-70) Publish the 6.0.0 betas to PyPI as pre-releases from AMP3-beta, then 6.0.0 when AMP 3 is out (steps in NOTES.md, "Releases").

## README.md and samples/

---

- (#3-49) A README for the 6.0 beta and runnable samples. *DONE*

## ampapi/

---

- (#3-48) A structure pass: lower-case routes and an Endpoint line on every call, docstrings without test-run context, request TypedDicts, body spacing. *DONE*
- (#3-51) Fix the code analysis findings (`.local_data/plans/code_analysis/summary.md`).
    - Group A, the `Session` paths. *DONE*
    - Group B, stale objects and the registry. *DONE* (#3-51.6)
    - Group C, writes that lose data. *DONE* (#3-51.7)
    - Group G, structure. *DONE* (#3-51.8)
    - Group D, uncatchable errors. *DONE* (#3-51.9)
    - Groups E (names), F (types) and H (docs). *DONE* (#3-51.10)
- (#3-51.11) Shard infra and preferences as `AMPSettings` objects, built from keywords or read from AMP, where the update calls send only the fields set. *DONE*
- (#3-51.10f) Request TypedDicts: `NotRequired` for keys the library leaves out, `Optional` only for keys sent as null.
- (#3-56) Match the library to AMP's own OpenAPI document (`.local_data/plans/openapi_compare/plan.md`).
    - The shards area. *DONE* (#3-56.6)
    - Spires and platform. *DONE* (#3-56.7)
    - Accounts and session. *DONE* (#3-56.8)
    - First-run setup. *DONE* (#3-56.9)
- (#3-65) Bring the library up to AMP 3.0.2 "Neptune": diff its OpenAPI against 3.0.1's, recheck the U reports its release notes touch, and reword the docs that still name 3.0.1. *DONE*
- (#3-67) `Preferences.default()`: a `Preferences` holding the web panel's default for each preference, to reset them through `update_preferences`. *DONE*
- (#3-68) Docstrings: one meaning per word (CODING_STYLE.md §20), the 8 `param-as-noun` and 30 repeated-word sentences `land_check.py` found. *DONE*

## ampapi/panel.py

---

- (#3-47.14) Build the rest of the AMP3 library in the agreed layout: `ShardModule` with `Shard`, `SpireModule` with `Spire`, `TemplateModule`, the rest of `AccountModule`, `AnalyticsModule`, `TaskModule`, `CredentialModule`. *DONE*
- (#3-50) Module layout by what a call acts on: collections and lookups on `Panel`, shards under their spire, the hubs set aside, then `NetworkModule` (#3-50.5), `AuditModule` (#3-50.6), invites onto `Session` (#3-50.7) and `EnrollmentModule` with the message bus calls (#3-50.8). *DONE*
- (#3-50b) Look at what `create_shard` drops from AMP's reply (`infraSettings`, `appConfig`, `ports`, `portOutcomes`, `overLicenceLimit`) and decide what to hand back. *DONE* in #3-50.11: read-only properties on the `Shard`.
- (#3-50.11d) Type `ShardPortOutcome.reason` once we know what its numbers mean; only 0 has been seen. *DONE* from AMP's own docs (#3-54).
- (#3-50.1) Bring the hubs back: `hubs.py` out of pyright's exclude list, `Panel`/`Shard`/`Spire` on the hub classes again, `auto_state`, the samples and the README's live events section, and the `# TODO:` markers on `AMPAPIHubError`, `LifecycleEvent` and `NetworkStatus`.
- (#3-52.1q) When the hubs come back, the README's live events section and `samples/live_events.py` say the panel holds its shards weakly; it keeps them in a plain dict now.
- (#3-47.7) Type `Panel.get_shards_awaiting_action`'s items; needs a game waiting for input. *DONE* with a `hytale` shard waiting for sign-in (#3-54).

## ampapi/platform.py

---

- (#3-47.10) Type the platform writes from the vm4 run (settings, https, licence, monitoring, updates; the bus, enrolment and networking ones are now in `enrollments.py` and `networking.py`). *DONE* except the replies only ever seen refused, still `# TODO:`: HTTPS setup and removal (needs a public domain), applying an update (no newer release), licence terms (needs a key with terms). Platform warnings *DONE* (#3-54).

## ampapi/analytics.py

---

- (#3-47.11) Type `get_analytics_connected_users`' reply and confirm `get_analytics_skin`'s image; both need a player online on a shard with `userSpecificData` on. *DONE* with Kat online in "Kat MC World" (#3-54).
- (#3-54) Type a Steam profile (`AnalyticsProfilesResponse.steam`), and the `steam`, `othersAtAddress`, `recoveredAddress` and `otherUsers` fields only ever seen `None`; they need a Steam player, or two players at one address.
- (#3-54) Type `AnalyticsAddressSearchResponse.addresses` once a search finds an address.

## ampapi/shards.py

---

- (#3-47.7) Type the shard replies still marked `# TODO:`: users (need players), wake (needs a template that can sleep: `minecraft-java` is the only one that claims it and was refused for its slow start, then U18b). The shards awaiting action are `Panel.get_shards_awaiting_action`, under `ampapi/panel.py`.

## ampapi/enrollments.py

---

- (#3-47.8) Type the enrolment deny reply (needs a machine waiting to join); approve is done. *DONE* live on vm4 + vm5 (#3-53).

## ampapi/spires.py

---

- (#3-47.8) Type a spire's import, import preflight, update and delete replies. *DONE* live on vm4 + vm5 (#3-53), except the update's success: no older AMP 3 release exists to put a spire behind the panel.
- (#3-53) Type the import fields only ever seen empty: `liveness`, `unavailable`, `alreadyImportedAs`, `truncatedRoots`, `unreadableDirectories`, and the import record's lists.

## Test VMs

---

- (#3-47.4) A second AMP3 VM (vm4, `amp3-beta2`) for parallel tests, built by `.scripts/amp3/build_vm.py`. *DONE*
- (#3-47.5) Teach the Refactor checkout's `.scripts/vms.py` about vm4, and move its login into that checkout's `local.ini`.
- (#3-47.15) vm5 (`amp3-spire`) joins vm4 as a second spire, for moving and cloning shards between spires and for gateways. *DONE*
