.. role:: raw-html(raw)
	:format: html

Method Events
==============
:raw-html:`<hr>`
Testing......

Method Information
#####################
:raw-html:`<hr>`

.. note::
	 Place holder text....



***PLACEHOLDER TEXT**


BanUser
~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.BanUser``

Ban a user from the server

Consumes these values:
	* User: type(SimpleUser)
	* Reason: type(String)

BanUserIP
~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.BanUserIP``

Ban a user from the server by their IP address

Consumes these values:
	* User: type(SimpleUser)
	* Reason: type(String)

CheckForUpdates
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.CheckForUpdates``

Check for Minecraft server updates

Consumes these values:

GiveXP
~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.GiveXP``

Give XP to a player

Consumes these values:
	* User: type(SimpleUser)
	* Quantity: type(Int32)

IfCondition
~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.CommonCorePlugin.IfCondition``

If condition is met

Consumes these values:
	* ValueToCheck: type(String)
	* Operation: type(IfOperators)
		* 0 - Equals
		* 1 - NotEquals
		* 2 - Contains
		* 3 - DoesNotContain
		* 4 - GreaterThan
		* 5 - LessThan
		* 6 - GreaterThanOrEqual
		* 7 - LessThanOrEqual
		* 8 - RegexMatch
	* ValueToCompare: type(String)

KickUser
~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.KickUser``

Kick a user from the server

Consumes these values:
	* User: type(SimpleUser)
	* Reason: type(String)

KillPlayer
~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.KillPlayer``

Kill a player

Consumes these values:
	* User: type(SimpleUser)

MakeGETRequest
~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.WebRequestPlugin.MakeGETRequest``

Make a GET request to a URI.

Consumes these values:
	* URI: type(String)

Fabulous
~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.Fabulous``

Make a player fabulous

Consumes these values:
	* User: type(SimpleUser)

MakePOSTRequest
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.WebRequestPlugin.MakePOSTRequest``

Make a POST request to a URI.

Consumes these values:
	* URI: type(String)
	* Payload: type(String)
	* ContentType: type(String)

DiscordMessage
~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.WebRequestPlugin.DiscordMessage``

Post a message on Discord

Consumes these values:
	* WebhookURL: type(String)
	* Contents: type(String)
	* DisplayUsername: type(String)

SlackMessage
~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.WebRequestPlugin.SlackMessage``

Post a message on Slack

Consumes these values:
	* WebhookURL: type(String)
	* Contents: type(String)

PushMessage
~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.WebRequestPlugin.PushMessage``

Push a message via PushBullet

Consumes these values:
	* title: type(String)
	* body: type(String)

PushMessageChannel
~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.WebRequestPlugin.PushMessageChannel``

Push a message via PushBullet to a specific channel

Consumes these values:
	* channel: type(String)
	* title: type(String)
	* body: type(String)

Sleep
~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.Sleep``

Put the server to sleep (Players can still connect)

Consumes these values:

RestartIfEmpty
~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.CommonCorePlugin.RestartIfEmpty``

Restart the application server, but only if it is empty

Consumes these values:

Restart
~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.Restart``

Restart the Minecraft server

Consumes these values:

RestoreBackup
~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.LocalFileBackupPlugin.RestoreBackup``

Restore a backup

Consumes these values:
	* BackupId: type(String)

CommandWithWarnings
~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.CommonCorePlugin.CommandWithWarnings``

Run a command in one hour, with warnings (non-blocking)

Consumes these values:
	* OneHour: type(String)
	* ThirtyMins: type(String)
	* FiveMins: type(String)
	* OneMin: type(String)
	* ThirtySecs: type(String)
	* FiveSecs: type(String)
	* Command: type(String)

ScheduleEmptyUpdate
~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.CommonCorePlugin.ScheduleEmptyUpdate``

Schedule an update and restart once the last user leaves, or immediately if empty.

Consumes these values:

SendGlobalTitle
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SendGlobalTitle``

Send a global title message

Consumes these values:
	* Title: type(String)
	* Subtitle: type(String)

SendUserMessage
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SendUserMessage``

Send a message to a specific player

Consumes these values:
	* Player: type(SimpleUser)
	* Message: type(String)

SendServerMessage
~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SendServerMessage``

Send a message to everyone on the server

Consumes these values:
	* Message: type(String)

SendTitle
~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SendTitle``

Send a title message to a specific player

Consumes these values:
	* User: type(SimpleUser)
	* Title: type(String)
	* Subtitle: type(String)

SendWakeOnLan
~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.CommonCorePlugin.SendWakeOnLan``

Send a Wake-On-LAN packet

Consumes these values:
	* MACAddress: type(String)

SendConsoleAdv
~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SendConsoleAdv``

Send advanced console input to the Minecraft server (Supports escaped characters)

Consumes these values:
	* Input: type(String)

SendMail
~~~~~~~~~
:raw-html:`<hr>`
- ``Event.EmailSenderPlugin.SendMail``

Send an email

Consumes these values:
	* To: type(String)
	* Subject: type(String)
	* Message: type(String)
	* Priority: type(MailPriority)
		* 0 - Normal
		* 1 - Low
		* 2 - High

SendConsole
~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SendConsole``

Send console input to the Minecraft server

Consumes these values:
	* Input: type(String)

SendMultipleConsole
~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SendMultipleConsole``

Send multiple lines of input to the Minecraft server

Consumes these values:
	* Input: type(String)

SetGameTime
~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SetGameTime``

Set the game time to a given real-world time

Consumes these values:
	* When: type(DateTime)

Start
~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.Start``

Start the Minecraft Server

Consumes these values:

StopIfEmpty
~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.CommonCorePlugin.StopIfEmpty``

Stop the application server, but only if it is empty

Consumes these values:

Stop
~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.Stop``

Stop the Minecraft Server

Consumes these values:

SmitePlayer
~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SmitePlayer``

Strike a player with lightning

Consumes these values:
	* User: type(SimpleUser)

TakeBackup
~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.LocalFileBackupPlugin.TakeBackup``

Take a backup

Consumes these values:

TakeStickyBackup
~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.LocalFileBackupPlugin.TakeStickyBackup``

Take a sticky backup

Consumes these values:

TeleportToCoords
~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.TeleportToCoords``

Teleport a player to a set of coordinates

Consumes these values:
	* User: type(SimpleUser)
	* X: type(Single)
	* Y: type(Single)
	* Z: type(Single)
	* YAngle: type(Single)
	* ZAngle: type(Single)

TeleportToPlayer
~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.TeleportToPlayer``

Teleport a player to another player

Consumes these values:
	* User: type(SimpleUser)
	* Target: type(SimpleUser)

UpdateAndRestart
~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.CommonCorePlugin.UpdateAndRestart``

Update the application and restart it if it was previously running

Consumes these values:

Wait
~~~~~
:raw-html:`<hr>`
- ``Event.CommonCorePlugin.Wait``

Wait

Consumes these values:
	* Seconds: type(Double)

Weaken
~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.Weaken``

Weaken a player

Consumes these values:
	* User: type(SimpleUser)

SaveChanges
~~~~~~~~~~~~
:raw-html:`<hr>`
- ``Event.MinecraftModule.SaveChanges``

Write unsaved world data to disk (save-all)

Consumes these values:
