.. role:: raw-html(raw)
	:format: html

Trigger Events
===============
:raw-html:`<hr>`

Testing....

Events Information
#####################
:raw-html:`<hr>`

.. note::
	All of these triggers will have a unique ID field that is generated from :meth:`~Core.get_triggers` due to uniqueness.



***PLACE HOLDER TEXT***


:raw-html:`<hr>`
**Trigger Description**: A backup finishes restoring.

- Emits: Reason | Id | Filename | WasCreatedAutomatically

:raw-html:`<hr>`
**Trigger Description**: A backup has failed.

- Emits: Reason | Id | Filename | WasCreatedAutomatically

:raw-html:`<hr>`
**Trigger Description**: A backup has started.

- Emits: Reason | Id | Filename | WasCreatedAutomatically

:raw-html:`<hr>`
**Trigger Description**: A player achieves an advancement

- Emits: User | Advancement

:raw-html:`<hr>`
**Trigger Description**: A player commits suicide

- Emits: User | Method

:raw-html:`<hr>`
**Trigger Description**: A player gets an achievement

- Emits: User | Achievement

:raw-html:`<hr>`
**Trigger Description**: A player is killed by an NPC

- Emits: Victim | Attacker | Method

:raw-html:`<hr>`
**Trigger Description**: A player is killed by another player

- Emits: Victim | Attacker | Method

:raw-html:`<hr>`
**Trigger Description**: A player joins the server

- Emits: User | UserID

:raw-html:`<hr>`
**Trigger Description**: A player joins the server for the first time

- Emits: User | UserID

:raw-html:`<hr>`
**Trigger Description**: A player joins the server while it was empty

- Emits: User | UserID

:raw-html:`<hr>`
**Trigger Description**: A player leaves the server

- Emits: User | UserID

:raw-html:`<hr>`
**Trigger Description**: A player sends a chat message

- Emits: User | UserID | Message

:raw-html:`<hr>`
**Trigger Description**: A player tries to join the server while it's sleeping


:raw-html:`<hr>`
**Trigger Description**: A player who has previously visited rejoins the server

- Emits: User | UserID

:raw-html:`<hr>`
**Trigger Description**: A scheduled backup finishes archiving.

- Emits: Reason | Id | Filename | WasCreatedAutomatically

:raw-html:`<hr>`
**Trigger Description**: The application state changes

- Emits: PreviousState | NextState

:raw-html:`<hr>`
**Trigger Description**: The last player leaves the server

- Emits: User | UserID

:raw-html:`<hr>`
**Trigger Description**: The Minecraft server is unable to keep up

- Emits: MillisecondsBehind | TicksSkipped

:raw-html:`<hr>`
**Trigger Description**: The Minecraft server repeatedly fails to start

- Emits: Time

:raw-html:`<hr>`
**Trigger Description**: The Minecraft Server watchdog forced a shutdown (server unresponsive)

- Emits: Time

:raw-html:`<hr>`
**Trigger Description**: The server enters sleep mode


:raw-html:`<hr>`
**Trigger Description**: The server wakes up from sleep mode due to player connect

