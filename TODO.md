# AMP API TODO

A small todo list local to the project.
Items carry a stable number (#3-N) for reference; `.local_data/plans/todo_index.md` tracks their type and status.
The `3-` marks the AMP3 index, so its numbers never meet the 5.x index's; AMP3 work began as #47, now #3-47.


## ampapi/session.py

---

- (#3-47.1) Confirm `PasskeyRequiredResponse` and `Session.second_factor` live; needs the panel on HTTPS, a passkey and recovery codes. *DONE*
- (#3-47.2) A SignalR hub client for live events, logging in with `Session.get_hub_token`.
- (#3-47.3) Confirm upstream report 01 (passkey registration needs `transports`) in a browser; trust vm3's Caddy root CA first.

## ampapi/panel.py

---

- (#3-47.14) Build the rest of the AMP3 library in the agreed layout: `ShardModule` with `Shard`, `SpireModule` with `Spire`, `TemplateModule`, the rest of `AccountModule`, `AnalyticsModule`, `TaskModule`, `CredentialModule`. *DONE*

## ampapi/platform.py

---

- (#3-47.10) Type the platform writes from the vm4 run (settings, https, bus, enrolments, networking, licence, monitoring, updates); most are still marked `# TODO:`.

## ampapi/shards.py

---

- (#3-47.7) Type the shard replies still marked `# TODO:`: moves between spires and imports with vm5, then disk, users, wake and the file ACL changes.

## ampapi/spires.py

---

- (#3-47.8) Type the enrolment approve and deny replies and a spire's import, now seen with vm5 joining vm4.

## Test VMs

---

- (#3-47.4) A second AMP3 VM (vm4, `amp3-beta2`) for parallel tests, built by `.scripts/amp3/build_vm.py`. *DONE*
- (#3-47.5) Teach the Refactor checkout's `.scripts/vms.py` about vm4, and move its login into that checkout's `local.ini`.
- (#3-47.15) vm5 (`amp3-spire`) joins vm4 as a second spire, for moving and cloning shards between spires and for gateways.
