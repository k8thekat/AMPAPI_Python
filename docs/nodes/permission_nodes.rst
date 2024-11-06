.. role:: raw-html(raw)
	:format: html

Permission Nodes
=================
:raw-html:`<hr>`

Filler test for the luls.. HI UMBRA~

.. note::
	Any node with a '*' at the end of it is a wild card and using that will make all permissions nodes in that section equal to the value set, treat it like parent inheritance.



.. note::
    To access lets say `Privacy.AllowAnalytics` of :ref:`Privacy Nodes` we would use "Settings.Core.Privacy.AllowAnalytics" as a string. See the Example below.


.. code-block:: python
    :linenos:

    # We are going to access Privacy.AllowAnalytics.
    # ... assume we created our Bridge object and API Params to login.
    import ampapi
    node = "Settings.Core.Privacy.AllowAnalytics"
    res = ADSModule.set_instance_config(instance_name="AMPInstance01", setting_node= node, value= True)
    print(res) # This should be an ActionResult class which we can see the results via its `__repr__` definition.


.. note::
    Here's another example.. lets say we want `InstanceManagement.StopInstances` of :ref:`InstanceManagement Nodes` we would use "ADS.InstanceManagement.StopInstances" as a string. See the Example below.



.. code-block:: python
    :linenos:

    # We are going to access InstanceManagement.StopInstances.
    # ... assume we created our Bridge object and API Params to login.
    import ampapi
    node = "ADS.InstanceManagement.StopInstances"
    res = ADSModule.set_instance_config(instance_name="AMPInstance01", setting_node= node, value= True)
    print(res) # This should be an ActionResult class which we can see the results via its `__repr__` definition.




Settings Permission Nodes
##########################
:raw-html:`<hr>`

Description: Which Settings users in this role have permission to change the value of

.. note::
	All nodes in this section will be prefixed with "Settings.", see examples :ref:`Permission Nodes`


- Settings.*

Core Nodes
~~~~~~~~~~~
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "Core.", see examples :ref:`Permission Nodes`


- Core.*

Security Nodes
^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Security.*
- Security.EnablePassthruAuth
- Security.RateLimitLogins
- Security.AuthFailureTimeWindow
- Security.AuthFailureAttemptsInWindow
- Security.TwoFactorMode
- Security.RequireSessionIPStickiness
- Security.AllowUserPasswords
- Security.IncludeExceptionDataInAPI

Webserver Nodes
^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Webserver.*
- Webserver.APIRateLimit
- Webserver.AllowGETForAPIEndpoints
- Webserver.UsingReverseProxy
- Webserver.ReverseProxyHosts
- Webserver.CORSOrigin
- Webserver.DisableCompression

Login Nodes
^^^^^^^^^^^^
:raw-html:`<hr>`

- Login.*
- Login.UseAuthServer
- Login.AuthServerURL

Branding Nodes
^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Branding.*
- Branding.DisplayBranding
- Branding.PageTitle
- Branding.CompanyName
- Branding.WelcomeMessage
- Branding.BrandingMessage
- Branding.ShortBrandingMessage
- Branding.URL
- Branding.SupportURL
- Branding.SupportText
- Branding.SubmitTicketURL
- Branding.LogoURL
- Branding.BackgroundURL
- Branding.SplashFrameURL
- Branding.ForgotPasswordURL

AMP Nodes
^^^^^^^^^^
:raw-html:`<hr>`

- AMP.*
- AMP.ScheduleOffsetSeconds
- AMP.AppStartupMode
- AMP.FirstStart
- AMP.MapAllPluginStores
- AMP.Theme
- AMP.ShowHelpOnStatus
- AMP.SchedulerTimezoneId

Monitoring Nodes
^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Monitoring.*
- Monitoring.UseMulticoreCPUCalc
- Monitoring.IgnoreSMTCores
- Monitoring.ConsoleScrollback
- Monitoring.LogLevel
- Monitoring.FullMetricsGathering
- Monitoring.ReportPhysicalMemoryAsTotal
- Monitoring.MetricsPollInterval
- Monitoring.MetricsReportingInterval
- Monitoring.ShowDevInfo

Privacy Nodes
^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Privacy.*
- Privacy.PrivacySettingsSet
- Privacy.SessionTimeout
- Privacy.AutoReportFatalExceptions
- Privacy.AllowAnalytics
- Privacy.EnhancedLicenceReporting

ADSModule Nodes
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "ADSModule.", see examples :ref:`Permission Nodes`


- ADSModule.*

Limits Nodes
^^^^^^^^^^^^^
:raw-html:`<hr>`

- Limits.*
- Limits.InstanceLimit
- Limits.CreateLocalInstances

Defaults Nodes
^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Defaults.*
- Defaults.NewInstanceKey
- Defaults.DefaultAuthServerURL
- Defaults.DefaultSettings
- Defaults.DefaultMountBindings
- Defaults.DefaultReleaseStream
- Defaults.UseDocker
- Defaults.PropagateAuthServer
- Defaults.PropogateRepos
- Defaults.UseOverlays
- Defaults.MatchVersion
- Defaults.DefaultPostCreate
- Defaults.ExcludeFromFirewall

ADS Nodes
^^^^^^^^^^
:raw-html:`<hr>`

- ADS.*
- ADS.AutoReactivate
- ADS.Mode
- ADS.AutostartInstances
- ADS.InstanceStartDelay
- ADS.ConfigurationRepositories
- ADS.ShowDeprecated
- ADS.DownloadMirror

Network Nodes
^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Network.*
- Network.DefaultIPBinding
- Network.DefaultAppIPBinding
- Network.DockerExternalIPBinding
- Network.AppPortInclusions
- Network.MetricsServerPort
- Network.UseDockerHostNetwork
- Network.UseTraefik
- Network.TraefikNetworkName
- Network.TraefikDomainWildcard
- Network.AccessMode
- Network.BaseURL
- Network.InstanceHostname

Community Nodes
^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Community.*
- Community.EnableCommunityPages
- Community.CommunityDisplayName
- Community.CommunityURL
- Community.DiscordURL
- Community.GeographicLocation

FileManagerPlugin Nodes
~~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

.. note::
	All nodes in this section will be prefixed with "FileManagerPlugin.", see examples :ref:`Permission Nodes`


- FileManagerPlugin.*

FMP Security Nodes
^^^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- Security.*
- Security.RestrictUploadExtensions
- Security.RestrictDownloadExtensions
- Security.DownloadableExtensions
- Security.UploadableExtensions
- Security.AllowExtensionChange
- Security.AllowArchiveOperations
- Security.OnlyExtractUploadableExtensionsFromArchives
- Security.HoneypotSFTPLogins

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
- SMTP.UseSSL
- SMTP.Host
- SMTP.Port
- SMTP.Username
- SMTP.Password
- SMTP.EmailFrom

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

SteamWorkshop Nodes
^^^^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- SteamWorkshop.*
- SteamWorkshop.WorkshopItemIDs

SteamUpdateSettings Nodes
^^^^^^^^^^^^^^^^^^^^^^^^^^
:raw-html:`<hr>`

- SteamUpdateSettings.*
- SteamUpdateSettings.AutomaticallyRetryOnFailure
- SteamUpdateSettings.AutomaticRetryLimit
- SteamUpdateSettings.UpdateCheckMethod
- SteamUpdateSettings.SteamCMDBetaPassword
- SteamUpdateSettings.ThrottleDownloadSpeed
- SteamUpdateSettings.KeepSteamCMDScripts
- SteamUpdateSettings.ShowDownloadSpeedInBits

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

TemplateManagement Nodes
~~~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- TemplateManagement.*
- TemplateManagement.ManageTemplates

InstanceManagement Nodes
~~~~~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- InstanceManagement.*
- InstanceManagement.RegisterToController
- InstanceManagement.CreateInstance
- InstanceManagement.SuspendInstances
- InstanceManagement.UpgradeInstances
- InstanceManagement.StopInstances
- InstanceManagement.DeleteInstances
- InstanceManagement.StartInstances
- InstanceManagement.AttachRemoteADSInstance
- InstanceManagement.RemoveRemoteADSInstance
- InstanceManagement.EditRemoteTargets
- InstanceManagement.Reconfigure
- InstanceManagement.RestartInstances
- InstanceManagement.RefreshConfiguration
- InstanceManagement.RefreshRemoteConfigStores
- InstanceManagement.ManageSuspendedInstances

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
- FileManager.CreateArchive
- FileManager.ExtractArchive
- FileManager.BrowseFiles
- FileManager.DownloadFiles
- FileManager.UploadFiles
- FileManager.RenameFiles
- FileManager.ChangeFileExtension
- FileManager.CopyFiles
- FileManager.TrashFiles
- FileManager.TrashDirectories
- FileManager.EmptyTrash
- FileManager.CreateDirectory
- FileManager.RenameDirectories
- FileManager.ChangeBackupExclusions
- FileManager.DownloadFromURL
- FileManager.ModifyAMPConfigFiles
- FileManager.ConnectViaSFTP

Core Permission Nodes
######################
:raw-html:`<hr>`

Description: Core functionality built into AMP itself

.. note::
	All nodes in this section will be prefixed with "Core.", see examples :ref:`Permission Nodes`


- Core.*

AuditLog Nodes
~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- AuditLog.*
- AuditLog.ViewAuditLog

Special Nodes
~~~~~~~~~~~~~~
:raw-html:`<hr>`

- Special.*
- Special.CancelOtherUsersTasks
- Special.ViewOtherUsersTasks
- Special.UpdateAMPInstance
- Special.UseDevMethods
- Special.RestartAMP
- Special.Diagnostics
- Special.UpgradeAMP
- Special.BypassSettingValueLimits
- Special.QueryLicenceInformation
- Special.ActivateAMP
- Special.RunSecurityCheck

RoleManagement Nodes
~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

- RoleManagement.*
- RoleManagement.ViewRoles
- RoleManagement.CreateRole
- RoleManagement.DeleteRoles
- RoleManagement.EditRoleInfo
- RoleManagement.EditRolePermissions
- RoleManagement.CreateCommonRoles

Scheduler Nodes
~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

Description: Permissions required to manage AMPs scheduler

- Scheduler.*
- Scheduler.ViewSchedule
- Scheduler.CreateTrigger
- Scheduler.EditTrigger
- Scheduler.CreateTask
- Scheduler.DeleteTask
- Scheduler.DeleteTrigger
- Scheduler.EditTask
- Scheduler.EditOtherUsersTasks

UserManagement Nodes
~~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

Description: Permissions that control the management of other AMP users, should be used with care so as not to allow users to increase their own permissions

- UserManagement.*
- UserManagement.ChangeRoleMembership
- UserManagement.UpdateUserInfo
- UserManagement.UpdateOwnAccount
- UserManagement.DeleteUser
- UserManagement.ResetUserPassword
- UserManagement.CreateNewUser
- UserManagement.ViewActiveSessions
- UserManagement.ViewOtherUsersSessions
- UserManagement.EndUserSessions
- UserManagement.ViewUserInfo
- UserManagement.AccessExternalPermissions

AppManagement Nodes
~~~~~~~~~~~~~~~~~~~~
:raw-html:`<hr>`

Description: Actions that allow the user to control the running application

- AppManagement.*
- AppManagement.StartApplication
- AppManagement.StopApplication
- AppManagement.RestartApplication
- AppManagement.UpdateApplication
- AppManagement.SendConsoleInput
- AppManagement.ReadConsole

Instances Permission Nodes
###########################
:raw-html:`<hr>`

.. note::
	Replace ``instance-id`` with the something like the :py:class:`~Instance.instance_id` value.

- Instances.*
- Instances.`instance-id`.Start
- Instances.`instance-id`.Stop
- Instances.`instance-id`.Restart
- Instances.`instance-id`.Update
- Instances.`instance-id`.Manage
