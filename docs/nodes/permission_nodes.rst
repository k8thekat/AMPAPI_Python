.. role:: raw-html(raw)
	:format: html

Permission Nodes
=================
:raw-html:`<hr>`



.. note::
	Any node with a '*' at the end of it is a wild card and using that will make all permissions nodes in that section equal to the value set, treat it like parent inheritance.





ADS Permission Nodes
#####################
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "ADS.", see examples :ref:`Permission Nodes`


- ADS.*

DatastoreManagement Nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- DatastoreManagement.*
- DatastoreManagement.ManageDatastores

InstanceManagement Nodes
~~~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- InstanceManagement.*
- InstanceManagement.AttachRemoteADSInstance
- InstanceManagement.CreateInstance
- InstanceManagement.DeleteInstances
- InstanceManagement.EditRemoteTargets
- InstanceManagement.ManageSuspendedInstances
- InstanceManagement.Reconfigure
- InstanceManagement.RefreshConfiguration
- InstanceManagement.RefreshRemoteConfigStores
- InstanceManagement.RegisterToController
- InstanceManagement.RemoveRemoteADSInstance
- InstanceManagement.RestartInstances
- InstanceManagement.StartInstances
- InstanceManagement.StopInstances
- InstanceManagement.SuspendInstances
- InstanceManagement.UpgradeInstances

TemplateManagement Nodes
~~~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- TemplateManagement.*
- TemplateManagement.ManageTemplates

Core Permission Nodes
######################
:raw-html:`<hr>`

Description: Core functionality built into AMP itself

.. note::
	All nodes in this section will be prefixed with "Core.", see examples :ref:`Permission Nodes`


- Core.*

AppManagement Nodes
~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

Description: Actions that allow the user to control the running application

- AppManagement.*
- AppManagement.ReadConsole
- AppManagement.RestartApplication
- AppManagement.SendConsoleInput
- AppManagement.StartApplication
- AppManagement.StopApplication
- AppManagement.UpdateApplication

AuditLog Nodes
~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- AuditLog.*
- AuditLog.ViewAuditLog

RoleManagement Nodes
~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- RoleManagement.*
- RoleManagement.CreateCommonRoles
- RoleManagement.CreateRole
- RoleManagement.DeleteRoles
- RoleManagement.EditRoleInfo
- RoleManagement.EditRolePermissions
- RoleManagement.ViewRoles

Scheduler Nodes
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

Description: Permissions required to manage AMPs scheduler

- Scheduler.*
- Scheduler.CreateTask
- Scheduler.CreateTrigger
- Scheduler.DeleteTask
- Scheduler.DeleteTrigger
- Scheduler.EditOtherUsersTasks
- Scheduler.EditTask
- Scheduler.EditTrigger
- Scheduler.ViewSchedule

Special Nodes
~~~~~~~~~~~~~~
:raw-html:`<hr>`

- Special.*
- Special.ActivateAMP
- Special.BypassSettingValueLimits
- Special.CancelOtherUsersTasks
- Special.Diagnostics
- Special.QueryLicenceInformation
- Special.RestartAMP
- Special.RunSecurityCheck
- Special.UpdateAMPInstance
- Special.UpgradeAMP
- Special.UseDevMethods
- Special.ViewOtherUsersTasks

UserManagement Nodes
~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

Description: Permissions that control the management of other AMP users, should be used with care so as not to allow users to increase their own permissions

- UserManagement.*
- UserManagement.AccessExternalPermissions
- UserManagement.ChangeRoleMembership
- UserManagement.CreateNewUser
- UserManagement.DeleteUser
- UserManagement.EndUserSessions
- UserManagement.ResetUserPassword
- UserManagement.UpdateOwnAccount
- UserManagement.UpdateUserInfo
- UserManagement.ViewActiveSessions
- UserManagement.ViewOtherUsersSessions
- UserManagement.ViewUserInfo

FileManager Permission Nodes
#############################
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "FileManager.", see examples :ref:`Permission Nodes`


- FileManager.*

FileManager Nodes
~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- FileManager.*
- FileManager.BrowseFiles
- FileManager.ChangeBackupExclusions
- FileManager.ChangeFileExtension
- FileManager.ConnectViaSFTP
- FileManager.CopyFiles
- FileManager.CreateArchive
- FileManager.CreateDirectory
- FileManager.DownloadFiles
- FileManager.DownloadFromURL
- FileManager.EmptyTrash
- FileManager.ExtractArchive
- FileManager.ModifyAMPConfigFiles
- FileManager.RenameDirectories
- FileManager.RenameFiles
- FileManager.TrashDirectories
- FileManager.TrashFiles
- FileManager.UploadFiles

Instances Permission Nodes
###########################
:raw-html:`<hr>`

.. note::
	Replace ``instance-id`` with the something like the :py:class:`~Instance.instance_id` value.

- Instances.*
- Instances.`instance-id`.Manage
- Instances.`instance-id`.Restart
- Instances.`instance-id`.Start
- Instances.`instance-id`.Stop
- Instances.`instance-id`.Update

Settings Permission Nodes
##########################
:raw-html:`<hr>`

Description: Which Settings users in this role have permission to change the value of

.. note::
	All nodes in this section will be prefixed with "Settings.", see examples :ref:`Permission Nodes`


- Settings.*

ADSModule Nodes
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "ADSModule.", see examples :ref:`Permission Nodes`


- ADSModule.*

ADS Nodes
^^^^^^^^^^
:raw-html:`<hr>`

- ADS.*
- ADS.AutoReactivate
- ADS.AutostartInstances
- ADS.ConfigurationRepositories
- ADS.InstanceStartDelay
- ADS.Mode
- ADS.ShowDeprecated

Community Nodes
^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Community.*
- Community.CommunityDisplayName
- Community.CommunityURL
- Community.DiscordURL
- Community.EnableCommunityPages
- Community.GeographicLocation

Defaults Nodes
^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Defaults.*
- Defaults.DefaultAuthServerURL
- Defaults.DefaultMountBindings
- Defaults.DefaultPostCreate
- Defaults.DefaultReleaseStream
- Defaults.DefaultSettings
- Defaults.ExcludeFromFirewall
- Defaults.NewInstanceKey
- Defaults.PropagateAuthServer
- Defaults.PropogateRepos
- Defaults.UseDocker

Limits Nodes
^^^^^^^^^^^^^
:raw-html:`<hr>`

- Limits.*
- Limits.CreateLocalInstances
- Limits.InstanceLimit

Network Nodes
^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Network.*
- Network.AccessMode
- Network.AppPortInclusions
- Network.BaseURL
- Network.DefaultAppIPBinding
- Network.DefaultIPBinding
- Network.DockerExternalIPBinding
- Network.IPAddressList
- Network.InstanceHostname
- Network.MetricsServerPort
- Network.TraefikDomainWildcard
- Network.TraefikNetworkName
- Network.UseDockerHostNetwork
- Network.UseTraefik

Core Nodes
~~~~~~~~~~~
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "Core.", see examples :ref:`Permission Nodes`


- Core.*

AMP Nodes
^^^^^^^^^^
:raw-html:`<hr>`

- AMP.*
- AMP.AppStartupMode
- AMP.FirstStart
- AMP.MapAllPluginStores
- AMP.ScheduleOffsetSeconds
- AMP.SchedulerTimezoneId
- AMP.ShowHelpOnStatus
- AMP.Theme

Login Nodes
^^^^^^^^^^^^
:raw-html:`<hr>`

- Login.*
- Login.AuthServerURL
- Login.UseAuthServer

Monitoring Nodes
^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Monitoring.*
- Monitoring.ConsoleScrollback
- Monitoring.FullMetricsGathering
- Monitoring.IgnoreSMTCores
- Monitoring.LogLevel
- Monitoring.MetricsPollInterval
- Monitoring.MetricsReportingInterval
- Monitoring.ReportPhysicalMemoryAsTotal
- Monitoring.ShowDevInfo
- Monitoring.UseMulticoreCPUCalc

Privacy Nodes
^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Privacy.*
- Privacy.AllowAnalytics
- Privacy.AutoReportFatalExceptions
- Privacy.EnhancedLicenceReporting
- Privacy.PrivacySettingsSet
- Privacy.SessionTimeout

Security Nodes
^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Security.*
- Security.AllowUserPasswords
- Security.AuthFailureAttemptsInWindow
- Security.AuthFailureTimeWindow
- Security.EnablePassthruAuth
- Security.IncludeExceptionDataInAPI
- Security.RateLimitLogins
- Security.RequireSessionIPStickiness
- Security.RequireTokenIPStickiness
- Security.TwoFactorMode

Webserver Nodes
^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Webserver.*
- Webserver.APIRateLimit
- Webserver.AllowGETForAPIEndpoints
- Webserver.CORSOrigin
- Webserver.DisableCompression
- Webserver.ReverseProxyHosts
- Webserver.UsingReverseProxy

EmailSenderPlugin Nodes
~~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "EmailSenderPlugin.", see examples :ref:`Permission Nodes`


- EmailSenderPlugin.*

SMTP Nodes
^^^^^^^^^^^
:raw-html:`<hr>`

- SMTP.*
- SMTP.EmailFrom
- SMTP.Host
- SMTP.Password
- SMTP.Port
- SMTP.UseSSL
- SMTP.Username

FileManagerPlugin Nodes
~~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "FileManagerPlugin.", see examples :ref:`Permission Nodes`


- FileManagerPlugin.*

FMP FileManager Nodes
^^^^^^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- FileManager.*
- FileManager.AdditionalVirtualDirectories
- FileManager.FastFileTransfers

FMP SFTP Nodes
^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- SFTP.*
- SFTP.EnableCompression
- SFTP.EnableWebsocketUploads

FMP Security Nodes
^^^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Security.*
- Security.AllowArchiveOperations
- Security.AllowExtensionChange
- Security.DownloadableExtensions
- Security.HoneypotSFTPLogins
- Security.OnlyExtractUploadableExtensionsFromArchives
- Security.PublicKeyOnly
- Security.RestrictDownloadExtensions
- Security.RestrictUploadExtensions
- Security.UploadableExtensions

WebRequestPlugin Nodes
~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "WebRequestPlugin.", see examples :ref:`Permission Nodes`


- WebRequestPlugin.*

WebhookLogins Nodes
^^^^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- WebhookLogins.*
- WebhookLogins.PushbulletAccessToken

steamcmdplugin Nodes
~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "steamcmdplugin.", see examples :ref:`Permission Nodes`


- steamcmdplugin.*

SteamUpdateSettings Nodes
^^^^^^^^^^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- SteamUpdateSettings.*
- SteamUpdateSettings.AutomaticRetryLimit
- SteamUpdateSettings.AutomaticallyRetryOnFailure
- SteamUpdateSettings.KeepSteamCMDScripts
- SteamUpdateSettings.ShowDownloadSpeedInBits
- SteamUpdateSettings.SteamCMDBetaPassword
- SteamUpdateSettings.SteamCMDValidateDownloads
- SteamUpdateSettings.ThrottleDownloadSpeed
- SteamUpdateSettings.UpdateCheckMethod

SteamWorkshop Nodes
^^^^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- SteamWorkshop.*
- SteamWorkshop.WorkshopItemIDs
