# AMP API TODO

A small todo list local to the project.
Items carry a stable number (#N) for reference; `.local_data/plans/todo_index.md` tracks their type and status.


## ampapi/session.py

---

- (#47.1) Confirm `PasskeyRequiredResponse` and `Session.second_factor` live; needs the panel on HTTPS, a passkey and recovery codes. *DONE*
- (#47.2) A SignalR hub client for live events, logging in with `Session.get_hub_token`.
- (#47.3) Confirm upstream report 01 (passkey registration needs `transports`) in a browser; trust vm3's Caddy root CA first.

## ampapi/panel.py

---

- (#47.14) Build the rest of the AMP3 library in the agreed layout: `ShardModule` with `Shard`, `SpireModule` with `Spire`, `TemplateModule`, the rest of `AccountModule`, `AnalyticsModule`, `TaskModule`, `CredentialModule`.

## Test VMs

---

- (#47.4) A second AMP3 VM (vm4, `amp3-beta2`) for parallel tests, built by `.scripts/amp3/build_vm.py`. *DONE*
- (#47.5) Teach the Refactor checkout's `.scripts/vms.py` about vm4, and move its login into that checkout's `local.ini`.
