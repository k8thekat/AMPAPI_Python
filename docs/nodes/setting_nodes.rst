.. role:: raw-html(raw)
	:format: html

Setting Nodes
==============
:raw-html:`<hr>`



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




Settings Branding Nodes
########################
:raw-html:`<hr>`


**Name**: Background image URL
	| Description: If left blank, the default AMP background will show
	| Node: `Core.Branding.BackgroundURL`

**Name**: Brand Logo URL
	| Description: Address for a logo to show throughout - 3:1 or 2:1 Aspect Ratio. If left blank, default AMP logo will show
	| Node: `Core.Branding.LogoURL`

**Name**: Brand Name
	| Description: Name of your company/organization
	| Node: `Core.Branding.CompanyName`

**Name**: Brand Support Text
	| Description: How to present the support URL, for example 'Open Ticket' or 'Get Help'
	| Node: `Core.Branding.SupportText`

**Name**: Brand Support URL
	| Description: The URL that users should be directed to for general support
	| Node: `Core.Branding.SupportURL`

**Name**: Brand URL
	| Description: Typically the home page for your business or organization
	| Node: `Core.Branding.URL`

**Name**: Branding Message
	| Description: Used in various places where branding is included to reference your organization
	| Node: `Core.Branding.BrandingMessage`

**Name**: Custom Page Title
	| Description: Alternate name to show in the browserse title bar
	| Node: `Core.Branding.PageTitle`

**Name**: Display Branding
	| Description: Whether or not branding is displayed globally
	| Node: `Core.Branding.DisplayBranding`

**Name**: Forgot password URL
	| Description: What URL the user should be taken to if they click the 'Forgot Login' prompt on the login screen
	| Node: `Core.Branding.ForgotPasswordURL`

**Name**: Short Brand Message
	| Description: Mostly used for world seeds/names
	| Node: `Core.Branding.ShortBrandingMessage`

**Name**: Splash screen frame URL
	| Description: A URL for a page to be shown in a frame on the Login screen
	| Node: `Core.Branding.SplashFrameURL`

**Name**: Submit Ticket URL
	| Description: If a separate ticketing system is in place, the URL users should be directed to.
	| Node: `Core.Branding.SubmitTicketURL`

**Name**: Welcome Message
	| Description: Message that should be shown to users on the login screen
	| Node: `Core.Branding.WelcomeMessage`

Settings External_Services Nodes
#################################
:raw-html:`<hr>`


**Name**: Email 'From' address
	| Description: The address used for outgoing emails.
	| Node: `EmailSenderPlugin.SMTP.EmailFrom`

**Name**: Pushbullet Access Token
	| Node: `WebRequestPlugin.WebhookLogins.PushbulletAccessToken`

**Name**: SMTP Password
	| Description: If you're using GMail - you will need to request an [application specific password](https://security.google.com/settings/security/apppasswords) to send emails via AMP.
	| Node: `EmailSenderPlugin.SMTP.Password`

**Name**: SMTP Server Address
	| Node: `EmailSenderPlugin.SMTP.Host`

**Name**: SMTP Server Port
	| Node: `EmailSenderPlugin.SMTP.Port`

**Name**: SMTP Username
	| Node: `EmailSenderPlugin.SMTP.Username`

**Name**: Use SSL for SMTP
	| Node: `EmailSenderPlugin.SMTP.UseSSL`

Settings File_Manager Nodes
############################
:raw-html:`<hr>`


**Name**: Enable SFTP
	| Description: Whether or not SFTP is enabled
	| Node: `FileManagerPlugin.SFTP.SFTPEnabled`

**Name**: Enable SFTP Compression
	| Description: Compression increases transfer speeds at the expense of higher CPU usage.
	| Node: `FileManagerPlugin.SFTP.EnableCompression`

**Name**: Enable Websocket Uploads (Experimental)
	| Description: Use websockets to perform file transfers. Faster, but may cause issues with certain reverse proxy setups.
	| Node: `FileManagerPlugin.SFTP.EnableWebsocketUploads`

**Name**: Enable direct file transfers
	| Description: Bypasses the API for file transfers. A restart of AMP is required for this setting change to take effect.
	| Node: `FileManagerPlugin.FileManager.FastFileTransfers`

**Name**: File Manager Base Path
	| Node: `FileManagerPlugin.FileManager.BasePath`

**Name**: SFTP Port
	| Description: The port number the SFTP server listens on
	| Node: `FileManagerPlugin.SFTP.SFTPPortNumber`

**Name**: Virtual Directories
	| Description: Additional directories to show up as shortcuts inside the file manager
	| Node: `FileManagerPlugin.FileManager.AdditionalVirtualDirectories`

Settings Instance_Deployment Nodes
###################################
:raw-html:`<hr>`


**Name**: Application Port Ranges
	| Description: List of ports that can be used by AMP and application servers. Specify port ranges by separating the upper and lower bounds using a colon (e.g. 25565:25665). These ports must not be used by other services outside of AMP.
	| Node: `ADSModule.Network.AppPortInclusions`

**Name**: Automatically reactivate instances
	| Description: If an instance fails to start due to a licence failure, ADS will attempt to automatically reactivate it.
	| Node: `ADSModule.ADS.AutoReactivate`

**Name**: Autostart Instances
	| Description: When ADS starts, automatically start any instances that should be run on-boot if they're not already running.
	| Node: `ADSModule.ADS.AutostartInstances`

**Name**: Base URL
	| Description: The base URL that instances on this ADS installation should use when generating links to this host. This is used for things like the AMP web interface, SFTP and the AMP API.
	| Node: `ADSModule.Network.BaseURL`

**Name**: Configuration Repositories
	| Description: Sources of git repositories to fetch deployment templates from. Use of third party sources is unregulated and entirely at your own risk.
	| Node: `ADSModule.ADS.ConfigurationRepositories`

**Name**: Configure for Traefik
	| Description: Apply Traefik labels to docker instances. (Experimental!)
	| Node: `ADSModule.Network.UseTraefik`

**Name**: Create in Docker Containers
	| Description: Creates all new instances inside Docker containers transparently. 
	| Node: `ADSModule.Defaults.UseDocker`

**Name**: Create local instances
	| Description: If disabled, this ADS instance will only pass provision requests to other ADS instances and never create instances locally.
	| Node: `ADSModule.Limits.CreateLocalInstances`

**Name**: Create shared instances
	| Description: Created instances use shared AMP core data rather than individual copies.
	| Node: `ADSModule.Defaults.CreateAsShared`

**Name**: Default AMP IP Binding
	| Description: Which IP address new AMP instances should use by default.
	| Node: `ADSModule.Network.DefaultIPBinding`

**Name**: Default Application IP Binding
	| Description: Which IP address applications deployed by AMP should use by default.
	| Node: `ADSModule.Network.DefaultAppIPBinding`

**Name**: Default Community Discord
	| Description: A link to a Discord invite to join a community discord server if not specified for a given instance
	| Node: `ADSModule.Community.DiscordURL`

**Name**: Default Community Display Name
	| Description: The name to display for the community pages if not specified for a given instance
	| Node: `ADSModule.Community.CommunityDisplayName`

**Name**: Default Community URL
	| Description: The URL to use for the community pages if not specified for the instance
	| Node: `ADSModule.Community.CommunityURL`

**Name**: Default Mount Bindings
	| Description: Default container mount bindings to be applied to all new instances when using containers. Use templates {{InstanceName}} or {{InstanceId}} to insert the instance name or ID into the path. It is recommended that the host and container path are the same where possible. The 'amp' user must have full read/write access to these paths on the host system.
	| Node: `ADSModule.Defaults.DefaultMountBindings`

**Name**: Default Settings
	| Description: Default settings to be applied to all new instances. You can find the Node for any given setting by turning on the [Show development information](setting:Core.Monitoring.ShowDevInfo) setting.
	| Node: `ADSModule.Defaults.DefaultSettings`

**Name**: Default auth server
	| Description: The URL of the authentication server to be used by new instances
	| Node: `ADSModule.Defaults.DefaultAuthServerURL`

**Name**: Default post-create action
	| Description: What should the application do by default in newly created instances.
	| Node: `ADSModule.Defaults.DefaultPostCreate`

**Name**: Default release stream
	| Description: Which release stream to use by default when creating or updating instances
	| Node: `ADSModule.Defaults.DefaultReleaseStream`

**Name**: Docker External IP
	| Description: Which IP AMP should report for instances created within Docker when no specific IP is specified
	| Node: `ADSModule.Network.DockerExternalIPBinding`

**Name**: Download Mirror
	| Description: Which source to use to download AMP data. Using a mirror close to you may result in faster speeds.
	| Node: `ADSModule.ADS.DownloadMirror`

**Name**: Enable Community Pages
	| Description: Whether or not to enable the community pages feature. This allows users to share their instances with others.
	| Node: `ADSModule.Community.EnableCommunityPages`

**Name**: Exclude new instances from firewall
	| Description: If enabled, new instances will not have their required ports added to the system firewall by default.
	| Node: `ADSModule.Defaults.ExcludeFromFirewall`

**Name**: Geographic Location
	| Description: The geographic location of this ADS instance. Only used for display purposes
	| Node: `ADSModule.Community.GeographicLocation`

**Name**: Ignore Version Compatibility
	| Description: When enabled, ADS will not verify that the instance and ADS are the same version. This will frequently cause compatibility issues.
	| Node: `ADSModule.ADS.IgnoreCompatibility`

**Name**: Instance Hostname
	| Description: The hostname that instances on this ADS installation should use displaying a hostname for applications inside instances
	| Node: `ADSModule.Network.InstanceHostname`

**Name**: Instance Start Delay
	| Description: When bulk starting instances, how many milliseconds delay should be inserted between each instance start?
	| Node: `ADSModule.ADS.InstanceStartDelay`

**Name**: Licence Key
	| Description: The licence key to use for newly created instances
	| Node: `ADSModule.Defaults.NewInstanceKey`

**Name**: Match ADS Version
	| Description: Newly created instances match the same version as this ADS instance when created.
	| Node: `ADSModule.Defaults.MatchVersion`

**Name**: Metrics Server Port
	| Description: The port used by ADS to receive metrics data from instances
	| Node: `ADSModule.Network.MetricsServerPort`

**Name**: Mode
	| Description: Mode
	| Node: `ADSModule.ADS.Mode`

**Name**: Overlay Path
	| Description: The directory ADS will search for instance overlays. It will search for both overlay-common.zip and overlay-{MODULE}.zip where MODULE is the module being deployed such as minecraft, ark, srcds. E.g. overlay-srcds.zip
	| Node: `ADSModule.Defaults.OverlayPath`

**Name**: Propagate auth server to targets
	| Description: If enabled, the Default Auth Server URL will be copied to all targets when they are added to ADS
	| Node: `ADSModule.Defaults.PropagateAuthServer`

**Name**: Propagate repositories
	| Description: If enabled, the list of app repositories will be copied to all targets
	| Node: `ADSModule.Defaults.PropogateRepos`

**Name**: Remote Instance Access Mode
	| Description: Which [access mode](https://discourse.cubecoders.com/docs?topic=2268&utm_source=ampsettings&utm_content=accessmode) ADS should use when managing remote instances.
	| Node: `ADSModule.Network.AccessMode`

**Name**: Service Limit
	| Description: The maximum number of instances that may exist within this ADS target
	| Node: `ADSModule.Limits.InstanceLimit`

**Name**: Show deprecated applications
	| Description: If enabled, it will be possible to create new instances with legacy or deprecated configurations.
	| Node: `ADSModule.ADS.ShowDeprecated`

**Name**: Traefik domain name
	| Description: The wildcard domain to be used to access Traefik managed instances. Must take the format of .domain.tld
	| Node: `ADSModule.Network.TraefikDomainWildcard`

**Name**: Traefik network name
	| Description: The docker network to be used for Traefik managed instances.
	| Node: `ADSModule.Network.TraefikNetworkName`

**Name**: Use Host Networking for new Containers
	| Description: Binds docker containers directly to the host network adapter by default. Changing this option requires additional configuration changes for new AMP instances to function correctly.
	| Node: `ADSModule.Network.UseDockerHostNetwork`

**Name**: Use Overlays
	| Description: Whether or not to apply overlays to newly created instances on this target
	| Node: `ADSModule.Defaults.UseOverlays`

Settings Login Nodes
#####################
:raw-html:`<hr>`


**Name**: 
	| Node: `Core.Login.UseAuthServer`

**Name**: 
	| Node: `Core.Login.AuthServerURL`

Settings Security_And_Privacy Nodes
####################################
:raw-html:`<hr>`


**Name**: 
	| Node: `Core.Security.EnablePassthruAuth`

**Name**: 
	| Node: `Core.Privacy.PrivacySettingsSet`

**Name**: Allow Browser Analytics
	| Description: Allows analytics to be included in the AMP frontend. Analytics are hosted by CubeCoders and no data is sent to third parties. [Privacy Policy](https://cubecoders.com/PrivacyPolicy)
	| Node: `Core.Privacy.AllowAnalytics`

**Name**: Allow archive operations
	| Description: Allow folders to be archived, and archives to be extracted
	| Node: `FileManagerPlugin.Security.AllowArchiveOperations`

**Name**: Allow extension changes
	| Description: Allowing extension changes could let a user upload a file as one type, and change it later
	| Node: `FileManagerPlugin.Security.AllowExtensionChange`

**Name**: Allow user-defined passwords
	| Description: For password fields, allow the use of user-defined passwords rather than being limited to randomly generated ones only. Passwords will be subject to strength requirements and should not be shared amongst other services.
	| Node: `Core.Security.AllowUserPasswords`

**Name**: Auto-report errors
	| Description: Automatically sends anonymous error report to CubeCoders if AMP encounters an error from which it can't recover.
	| Node: `Core.Privacy.AutoReportFatalExceptions`

**Name**: Downloadable Extensions
	| Description: Which file extensions can be downloaded via the file manager or via SFTP
	| Node: `FileManagerPlugin.Security.DownloadableExtensions`

**Name**: Enhanced Licence Reporting
	| Description: If enabled, AMP will include instance names and other information in licence reports. This is useful for providers who wish to track usage of their licences.
	| Node: `Core.Privacy.EnhancedLicenceReporting`

**Name**: Honeypot SFTP Login Attempts
	| Description: Automatically bans IP addresses from SFTP logins if they try to login as [common usernames](https://discourse.cubecoders.com/t/honeypot-usernames/2296?utm_source=ampsettings&utm_content=honeypot). Make sure you're not using any of these names as an AMP username to login.
	| Node: `FileManagerPlugin.Security.HoneypotSFTPLogins`

**Name**: Include exception data in API calls
	| Description: If enabled, AMP will include exception data in API responses. This is useful for debugging but may expose sensitive information.
	| Node: `Core.Security.IncludeExceptionDataInAPI`

**Name**: Login rate-limit attempts
	| Description: If more than this number attempts occurs within the rate-limit time window, the IP address will be unable to make further login requests
	| Node: `Core.Security.AuthFailureAttemptsInWindow`

**Name**: Login rate-limit time window
	| Description: How many minutes the sliding window should be to check for authentication failures.
	| Node: `Core.Security.AuthFailureTimeWindow`

**Name**: Rate-limit Logins
	| Description: If enabled - login attempts will be rate limited after too many failures. If you're using external tools such as reverse proxies to handle rate limiting you may wish to disable this from within AMP
	| Node: `Core.Security.RateLimitLogins`

**Name**: Require Session IP Stickiness
	| Description: When enabled, web sessions are tied to the IP address that initiated them. This improves security, but can cause problems with fast changing/dynamic routing IPs (often found on cheaper ISPs or Campuses)
	| Node: `Core.Security.RequireSessionIPStickiness`

**Name**: Restrict Archive Extractions
	| Description: Only allow extensions in the approved 'upload' list to be extracted from archives
	| Node: `FileManagerPlugin.Security.OnlyExtractUploadableExtensionsFromArchives`

**Name**: Restrict downloadable extensions
	| Description: Whether or not the types of files that can be downloaded should be restricted
	| Node: `FileManagerPlugin.Security.RestrictDownloadExtensions`

**Name**: Restrict uploadable extensions
	| Description: Whether or not the types of files that can be uploaded should be restricted
	| Node: `FileManagerPlugin.Security.RestrictUploadExtensions`

**Name**: Session Timeout
	| Description: Sessions will timeout after this length of inactivity.
	| Node: `Core.Privacy.SessionTimeout`

**Name**: Two Factor Authentication
	| Description: Server-wide two-factor policy
	| Node: `Core.Security.TwoFactorMode`

**Name**: Uploadable Extensions
	| Description: Which file extensions can be Uploaded via the file manager or via SFTP
	| Node: `FileManagerPlugin.Security.UploadableExtensions`

Settings System_Settings Nodes
###############################
:raw-html:`<hr>`


**Name**: 
	| Node: `Core.AMP.MapAllPluginStores`

**Name**: AMP Theme
	| Description: Affects all users - change AMPs visual appearance with different themes.
	| Node: `Core.AMP.Theme`

**Name**: API rate limit
	| Description: The number of requests per second to allow the webserver to respond to (AMP must be restarted for changes to this setting to apply)
	| Node: `Core.Webserver.APIRateLimit`

**Name**: Allow GET method for API
	| Description: Allows the GET method to be used for API requests. Useful for debugging and development but should not be used in production (AMP must be restarted for changes to this setting to apply)
	| Node: `Core.Webserver.AllowGETForAPIEndpoints`

**Name**: Approved Reverse Proxy Hosts
	| Description: IP addresses of authorized reverse proxies for which the X-Forwarded-For header will be honoured.
	| Node: `Core.Webserver.ReverseProxyHosts`

**Name**: CORS Origin
	| Description: The origin domain to allow CORS requests from. Should be the URL of your controller in controller/target setups. See [MDN CORS Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
	| Node: `Core.Webserver.CORSOrigin`

**Name**: Console Scrollback Period
	| Description: How many minutes into the past should the console show when a user logs in. (Affects all users)
	| Node: `Core.Monitoring.ConsoleScrollback`

**Name**: Disable Compression
	| Description: Disable compression of responses from the webserver. (AMP must be restarted for changes to this setting to apply)
	| Node: `Core.Webserver.DisableCompression`

**Name**: Enable Fetch/Post Endpoints
	| Node: `Core.Webserver.EnableFetchPostEndpoints`

**Name**: Enable Websockets
	| Node: `Core.Webserver.EnableWebSockets`

**Name**: First Start
	| Node: `Core.AMP.FirstStart`

**Name**: Full process metrics
	| Description: Gathers extended information for running AMP processes
	| Node: `Core.Monitoring.FullMetricsGathering`

**Name**: Ignore SMT Cores
	| Description: If enabled, SMT cores (Hyperthreading, etc) are ignored when calculating CPU usage of processes. E.g. when disabled a quad core with hyperthreading is treated like an 8 core system, when enabled it's treated like a 4 core system.
	| Node: `Core.Monitoring.IgnoreSMTCores`

**Name**: Last Special Notice ID
	| Node: `Core.AMP.LastSpecialNoticeID`

**Name**: Logging Level
	| Description: What level of logging should be used by AMP. The selected log level and all higher levels will be logged.
	| Node: `Core.Monitoring.LogLevel`

**Name**: Metrics polling interval
	| Description: How frequently AMP should push metrics data to connected sessions
	| Node: `Core.Monitoring.MetricsPollInterval`

**Name**: Metrics reporting interval
	| Description: How frequently AMP should report metrics data to the controller
	| Node: `Core.Monitoring.MetricsReportingInterval`

**Name**: Multicore CPU usage calculation
	| Description: If enabled, AMP takes into account the number of CPU cores when calculating total CPU usage, otherwise it calculates assuming one core. A restart is required after changing this setting for it to take effect.
	| Node: `Core.Monitoring.UseMulticoreCPUCalc`

**Name**: Previous Version Installed
	| Node: `Core.AMP.PreviousVersion`

**Name**: Safe Mode
	| Node: `Core.AMP.SafeMode`

**Name**: Schedule Offset
	| Description: Offset in seconds to advance or delay execution of scheduled tasks that use time-based triggers.
	| Node: `Core.AMP.ScheduleOffsetSeconds`

**Name**: Scheduler Timezone
	| Description: Which time zone to use for the scheduler. Does not affect other AMP components
	| Node: `Core.AMP.SchedulerTimezoneId`

**Name**: Show development information
	| Description: When enabled, the node names for settings will be visible under each setting. Useful for configuration templates. Applies to all users.
	| Node: `Core.Monitoring.ShowDevInfo`

**Name**: Show support on status
	| Description: Affects all users - whether or not the Status tab should show the 'Help' button
	| Node: `Core.AMP.ShowHelpOnStatus`

**Name**: Shut down properly
	| Node: `Core.AMP.ShutdownProperly`

**Name**: Startup Mode
	| Description: What AMP should do when it starts
	| Node: `Core.AMP.AppStartupMode`

**Name**: Store IPs as MACs
	| Description: Map selected IP addresses to their associated MAC addresses when saving configuration files. Handles dynamic/varying IP address situations.
	| Node: `Core.AMP.StoreIPAddressesAsMACAddresses`

**Name**: User Friendly process metrics
	| Description: Reports memory usage only as physical RAM usage, ignoring swap usage. Doesn't apply when full process metrics is enabled.
	| Node: `Core.Monitoring.ReportPhysicalMemoryAsTotal`

**Name**: Using Reverse Proxy
	| Description: Whether or not AMP is configured to be run behind a reverse proxy
	| Node: `Core.Webserver.UsingReverseProxy`

Settings Updates Nodes
#######################
:raw-html:`<hr>`


**Name**: Automatic retry count
	| Description: How many times AMP should attempt to automatically retry failed updates if 'Automatically retry on failure' is enabled.
	| Node: `steamcmdplugin.SteamUpdateSettings.AutomaticRetryLimit`

**Name**: Automatically retry on failure
	| Description: Some applications require multiple attempts at an update to actually update correctly (notably those that use App ID 90). If enabled AMP will retry updates on certain error conditions that would normally indicate failure.
	| Node: `steamcmdplugin.SteamUpdateSettings.AutomaticallyRetryOnFailure`

**Name**: Beta Password
	| Description: The password to be used for participating in betas via SteamCMD if required.
	| Node: `steamcmdplugin.SteamUpdateSettings.SteamCMDBetaPassword`

**Name**: Keep SteamCMD scripts
	| Description: If enabled, AMP will keep the SteamCMD scripts it uses to update applications. This can be useful for debugging purposes.
	| Node: `steamcmdplugin.SteamUpdateSettings.KeepSteamCMDScripts`

**Name**: Show download speed in bits
	| Description: If enabled, download speeds will be shown in bits per second instead of bytes.
	| Node: `steamcmdplugin.SteamUpdateSettings.ShowDownloadSpeedInBits`

**Name**: Steam workshop items
	| Description: Item IDs for steam workshop items that should be downloaded/updated when the main application is updated
	| Node: `steamcmdplugin.SteamWorkshop.WorkshopItemIDs`

**Name**: Throttle Downloads
	| Description: Limits downloads to a given speed (In megabits/sec) to avoid disrupting other applications. 0 for unlimited.
	| Node: `steamcmdplugin.SteamUpdateSettings.ThrottleDownloadSpeed`

**Name**: Update check method
	| Description: Which method AMP should use to check for application updates, by either comparing the build timestamps, or by comparing the build ID from the application manifest.
	| Node: `steamcmdplugin.SteamUpdateSettings.UpdateCheckMethod`
