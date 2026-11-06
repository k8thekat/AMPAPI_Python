# AMP API Notes

Developer context for the AMP 3 (6.0.0b0) branch. AMP 2 support stays on `Refactor`/`developer` (5.x).

## Test panel (vm3)

- `vm3` (`amp3-beta`) runs AMP `3.0.0` from the `preview` channel, installed 2026-11-06 with `getamp3.sh -y`
  (rootless Podman, panel on `:8443`, no HTTPS). Its login is `[VM_AMP3]` in `local.ini`, its licence `[LICENSE] amp3`.
- The licence is the "Beta Preview" grade, 50 Instances, valid to 2027-02-04. The preview build itself runs out
  2026-12-07 (`HealthStatusResponse.preview`).
- Captures live in `_responses/3.0.0/auth/` (gitignored), one file per call: the request (secrets redacted), status,
  kept headers and body.
- There is no OpenAPI document. `/openapi/v1.json` is 401 without a token and 404 with one, so the types come from
  captures plus the web panel's own JS (`main-*.js` and its `chunk-*.js`).

## AMP 3 API shape

- REST under `/api/`, JSON bodies, camelCase keys. AMP 2's `POST /API/Module/Method` is gone.
- An Instance is a **shard** (`/api/shards/{id}/...`) and an ADS/Target is a **spire** (`/api/spires/{id}/...`).
- Path casing is mixed (`/api/Auth/login` and `/api/auth/logout`); both casings answer, we send the panel's own.

## Sessions (#47)

- Login is `POST /api/Auth/login` with `{username, password, rememberMe}`, answered with `{token, expiration}`.
  The token is an HS256 JWT sent as `Authorization: Bearer`. Its claims carry the user ID, name, email and a `sid`.
- A token lasts **8 hours**, or **28 days** with `rememberMe`.
- `POST /api/Auth/renew` swaps the token for a new one in the same session (same `sid`). The old token keeps working
  until the session ends. The web panel renews at 75% of the lifetime, and `Session` does the same.
- A session is one login. `POST /api/auth/logout` ends it: every token it was given gets 401 with
  `WWW-Authenticate: Bearer error="invalid_token"`. Other logins of the same user carry on.
  An admin's `POST /api/users/{id}/logout` ends all of that user's sessions the same way.
- A login can answer 200 without a token:
    - `{passwordChangeRequired: true, reason: "forced"}` for a user made with `requirePasswordChange`.
      `POST /api/Auth/change-expired-password` with `{username, currentPassword, newPassword}` logs in.
      AMP took the old password again as the new one, so there's no reuse check.
    - `{passkeyRequired: true}` (from the panel's JS, not seen live). `POST /api/Auth/login/second-factor` takes
      `{username, password, code, rememberMe}` where `code` is a recovery code. There's no TOTP in AMP 3.
      Passkeys show `NotConfigured` on vm3, likely because the panel isn't on HTTPS.
- `POST /api/auth/reauth` with `{password}` answers 204; AMP asks for it ("reproof") before sensitive changes.
- `POST /api/auth/hub-token` gives a 60 second token for the SignalR hub (WebSockets), which is where live events
  come from.
- A wrong password and an unknown user get the same 401 `{message: "Invalid username or password."}`.
  One wrong attempt of each did not lock the admin out; lockout wasn't tested further.

## Error shapes

AMP 3 answers errors in five shapes, so `AMPAPIRequestError` reads whichever keys are there:
- `{code, params, message}`, AMP's own: `code` is a dotted translation key, eg. `auth.error.reproofRejected`.
- `{errors: [str]}`, eg. a password the policy refuses.
- `{message}`, only for a refused login.
- ASP.NET ProblemDetails `{type, title, status, errors: {Field: [str]}, traceId}` for a malformed body.
- No body at all: 401 (with `WWW-Authenticate`) and 403 (no permission).

## First-run setup

Done through the API on vm3, with the setup code from `/opt/cubecoders/amp3/data/setup-token.txt` sent as
`X-Setup-Token`: `GET /api/Auth/setup/code`, `POST /api/Auth/setup/database/provision` (AMP sets up its own database,
done in seconds), `POST /api/Auth/setup/admin` (returns the first token), then `POST /api/licence` with
`{key, terms}`. `POST /api/licence/query` checks a key without using it. The privacy, network and HTTPS steps are
browser-only and optional; `GET /api/health/status` read `ready` after the licence.
