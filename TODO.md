# AMP API TODO

A small todo list local to the project.
Items carry a stable number (#N) for reference; `.local_data/plans/todo_index.md` tracks their type and status.


## ampapi/session.py

---

- (#47.1) Confirm `PasskeyRequiredResponse` and `Session.second_factor` live; needs the panel on HTTPS, a passkey and recovery codes. *DONE*
- (#47.2) A SignalR hub client for live events, logging in with `Session.get_hub_token`.
- (#47.3) Confirm upstream report 01 (passkey registration needs `transports`) in a browser; trust vm3's Caddy root CA first.
