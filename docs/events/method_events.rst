.. role:: raw-html(raw)
	:format: html

Method Events
==============
:raw-html:`<hr>`


Method Information
#####################
:raw-html:`<hr>`





BanUser
~~~~~~~~
:raw-html:`<hr>`
Ban a user from the server

- ``Event.MinecraftModule.BanUser``

Consumes these values:
	* Reason: type(String)
	* User: type(SimpleUser)

BanUserIP
~~~~~~~~~~
:raw-html:`<hr>`
Ban a user from the server by their IP address

- ``Event.MinecraftModule.BanUserIP``

Consumes these values:
	* Reason: type(String)
	* User: type(SimpleUser)

CheckForUpdates
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Check for available updates via SteamCMD

- ``Event.steamcmdplugin.CheckForUpdates``


CheckForUpdates - MinecraftModule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Check for Minecraft server updates

- ``Event.MinecraftModule.CheckForUpdates``


CommandWithWarnings
~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Run a command in one hour, with warnings (non-blocking)

- ``Event.CommonCorePlugin.CommandWithWarnings``

Consumes these values:
	* Command: type(String)
	* FiveMins: type(String)
	* FiveSecs: type(String)
	* OneHour: type(String)
	* OneMin: type(String)
	* ThirtyMins: type(String)
	* ThirtySecs: type(String)

DiscordMessage
~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Post a message on Discord

- ``Event.WebRequestPlugin.DiscordMessage``

Consumes these values:
	* Contents: type(String)
	* DisplayUsername: type(String)
	* WebhookURL: type(String)

Fabulous
~~~~~~~~~
:raw-html:`<hr>`
Make a player fabulous

- ``Event.MinecraftModule.Fabulous``

Consumes these values:
	* User: type(SimpleUser)

GiveXP
~~~~~~~
:raw-html:`<hr>`
Give XP to a player

- ``Event.MinecraftModule.GiveXP``

Consumes these values:
	* Quantity: type(Int32)
	* User: type(SimpleUser)

IfCondition
~~~~~~~~~~~~
:raw-html:`<hr>`
If condition is met

- ``Event.CommonCorePlugin.IfCondition``

Consumes these values:
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
	* ValueToCheck: type(String)
	* ValueToCompare: type(String)

KickUser
~~~~~~~~~
:raw-html:`<hr>`
Kick a user from the server

- ``Event.MinecraftModule.KickUser``

Consumes these values:
	* Reason: type(String)
	* User: type(SimpleUser)

KillPlayer
~~~~~~~~~~~
:raw-html:`<hr>`
Kill a player

- ``Event.MinecraftModule.KillPlayer``

Consumes these values:
	* User: type(SimpleUser)

MakeGETRequest
~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Make a GET request to a URI.

- ``Event.WebRequestPlugin.MakeGETRequest``

Consumes these values:
	* URI: type(String)

MakePOSTRequest
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Make a POST request to a URI.

- ``Event.WebRequestPlugin.MakePOSTRequest``

Consumes these values:
	* ContentType: type(String)
	* Payload: type(String)
	* URI: type(String)

PushMessage
~~~~~~~~~~~~
:raw-html:`<hr>`
Push a message via PushBullet

- ``Event.WebRequestPlugin.PushMessage``

Consumes these values:
	* body: type(String)
	* title: type(String)

PushMessageChannel
~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Push a message via PushBullet to a specific channel

- ``Event.WebRequestPlugin.PushMessageChannel``

Consumes these values:
	* body: type(String)
	* channel: type(String)
	* title: type(String)

Restart
~~~~~~~~
:raw-html:`<hr>`
Restart the Minecraft server

- ``Event.MinecraftModule.Restart``


RestartIfEmpty
~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Restart the application server, but only if it is empty

- ``Event.CommonCorePlugin.RestartIfEmpty``


RestoreBackup
~~~~~~~~~~~~~~
:raw-html:`<hr>`
Restore a backup

- ``Event.LocalFileBackupPlugin.RestoreBackup``

Consumes these values:
	* BackupId: type(String)

SaveChanges
~~~~~~~~~~~~
:raw-html:`<hr>`
Write unsaved world data to disk (save-all)

- ``Event.MinecraftModule.SaveChanges``


ScheduleEmptyUpdate
~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Schedule an update and restart once the last user leaves, or immediately if empty.

- ``Event.CommonCorePlugin.ScheduleEmptyUpdate``


SendConsole
~~~~~~~~~~~~
:raw-html:`<hr>`
Send console input to the Minecraft server

- ``Event.MinecraftModule.SendConsole``

Consumes these values:
	* Input: type(String)

SendConsoleAdv
~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Send advanced console input to the Minecraft server (Supports escaped characters)

- ``Event.MinecraftModule.SendConsoleAdv``

Consumes these values:
	* Input: type(String)

SendGlobalTitle
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Send a global title message

- ``Event.MinecraftModule.SendGlobalTitle``

Consumes these values:
	* Subtitle: type(String)
	* Title: type(String)

SendMail
~~~~~~~~~
:raw-html:`<hr>`
Send an email

- ``Event.EmailSenderPlugin.SendMail``

Consumes these values:
	* Message: type(String)
	* Priority: type(MailPriority)
		* 0 - Normal
		* 1 - Low
		* 2 - High
	* Subject: type(String)
	* To: type(String)

SendMultipleConsole
~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Send multiple lines of input to the Minecraft server

- ``Event.MinecraftModule.SendMultipleConsole``

Consumes these values:
	* Input: type(String)

SendServerMessage
~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Send a message to everyone on the server

- ``Event.MinecraftModule.SendServerMessage``

Consumes these values:
	* Message: type(String)

SendTitle
~~~~~~~~~~
:raw-html:`<hr>`
Send a title message to a specific player

- ``Event.MinecraftModule.SendTitle``

Consumes these values:
	* Subtitle: type(String)
	* Title: type(String)
	* User: type(SimpleUser)

SendUserMessage
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Send a message to a specific player

- ``Event.MinecraftModule.SendUserMessage``

Consumes these values:
	* Message: type(String)
	* Player: type(SimpleUser)

SendWakeOnLan
~~~~~~~~~~~~~~
:raw-html:`<hr>`
Send a Wake-On-LAN packet

- ``Event.CommonCorePlugin.SendWakeOnLan``

Consumes these values:
	* MACAddress: type(String)

SetGameTime
~~~~~~~~~~~~
:raw-html:`<hr>`
Set the game time to a given real-world time

- ``Event.MinecraftModule.SetGameTime``

Consumes these values:
	* When: type(DateTime)

SlackMessage
~~~~~~~~~~~~~
:raw-html:`<hr>`
Post a message on Slack

- ``Event.WebRequestPlugin.SlackMessage``

Consumes these values:
	* Contents: type(String)
	* WebhookURL: type(String)

Sleep
~~~~~~
:raw-html:`<hr>`
Put the server to sleep (Players can still connect)

- ``Event.MinecraftModule.Sleep``


SmitePlayer
~~~~~~~~~~~~
:raw-html:`<hr>`
Strike a player with lightning

- ``Event.MinecraftModule.SmitePlayer``

Consumes these values:
	* User: type(SimpleUser)

Start
~~~~~~
:raw-html:`<hr>`
Start the Minecraft Server

- ``Event.MinecraftModule.Start``


Stop
~~~~~
:raw-html:`<hr>`
Stop the Minecraft Server

- ``Event.MinecraftModule.Stop``


StopIfEmpty
~~~~~~~~~~~~
:raw-html:`<hr>`
Stop the application server, but only if it is empty

- ``Event.CommonCorePlugin.StopIfEmpty``


TakeBackup
~~~~~~~~~~~
:raw-html:`<hr>`
Take a backup

- ``Event.LocalFileBackupPlugin.TakeBackup``


TakeStickyBackup
~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Take a sticky backup

- ``Event.LocalFileBackupPlugin.TakeStickyBackup``


TeleportToCoords
~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Teleport a player to a set of coordinates

- ``Event.MinecraftModule.TeleportToCoords``

Consumes these values:
	* User: type(SimpleUser)
	* X: type(Single)
	* Y: type(Single)
	* YAngle: type(Single)
	* Z: type(Single)
	* ZAngle: type(Single)

TeleportToPlayer
~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Teleport a player to another player

- ``Event.MinecraftModule.TeleportToPlayer``

Consumes these values:
	* Target: type(SimpleUser)
	* User: type(SimpleUser)

UpdateAndRestart
~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`
Update the application and restart it if it was previously running

- ``Event.CommonCorePlugin.UpdateAndRestart``


Wait
~~~~~
:raw-html:`<hr>`
Wait

- ``Event.CommonCorePlugin.Wait``

Consumes these values:
	* Seconds: type(Double)

Weaken
~~~~~~~
:raw-html:`<hr>`
Weaken a player

- ``Event.MinecraftModule.Weaken``

Consumes these values:
	* User: type(SimpleUser)
