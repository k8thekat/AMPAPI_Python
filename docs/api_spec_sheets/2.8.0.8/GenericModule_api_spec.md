INSTANCE TYPE: GenericModule
APP VERSION: 2.8.0.8
BUILD: 27/09/2026 01:11

____________________________________________________
analytics_plugin:
	get_analytics_summary:
		description: None
		is_complex_type: False
		parameters: [{'name': 'PeriodDays', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'StartDate', 'type_name': 'Nullable<DateTime>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'Filters', 'type_name': 'Dictionary<String, String>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'PlayerCount', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Analytics.Analytics.AccessAnalytics']
		return_type_name: Object
		returns: None
	get_user_details:
		description: None
		is_complex_type: False
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Analytics.Analytics.AccessUserDetails']
		return_type_name: Object
		returns: None
____________________________________________________
common_core_plugin:
____________________________________________________
core:
	acknowledge_amp_update:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: []
		return_type_name: Void
		returns: None
	activate_amp_licence:
		description: None
		is_complex_type: True
		parameters: [{'name': 'LicenceKey', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'QueryOnly', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Core.Special.QueryLicenceInformation', 'Core.Special.ActivateAMP']
		return_type_name: ActionResult<JObject>
		returns: None
	add_event_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'triggerId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.CreateTrigger']
		return_type_name: ActionResult
		returns: None
	add_interval_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'months', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'days', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'hours', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'minutes', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'daysOfMonth', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'description', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.CreateTrigger']
		return_type_name: ActionResult
		returns: None
	add_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'MethodID', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'ParameterMapping', 'type_name': 'Dictionary<String, String>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.CreateTask']
		return_type_name: ActionResult
		returns: None
	async_test:
		description: DEV: Async test method
		is_complex_type: False
		parameters: []
		required_permissions: ['Core.Special.UseDevMethods']
		return_type_name: String
		returns: 
	cancel_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TaskId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: ActionResult
		returns: None
	change_task_order:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'TaskID', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewOrder', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.EditTask']
		return_type_name: ActionResult
		returns: None
	change_user_password:
		description: For a user to change their own password, requires knowing the old password
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'OldPassword', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewPassword', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'TwoFactorPIN', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: ActionResult
		returns: 
	confirm_two_factor_setup:
		description: Completes two-factor setup by supplying a valid two factor code based on the secret provided by EnableTwoFactor
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'TwoFactorCode', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: ActionResult
		returns: 
	convert_user_to_oidc:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'OIDCSub', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.UpdateUserInfo']
		return_type_name: ActionResult
		returns: None
	create_role:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Name', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'AsCommonRole', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Core.RoleManagement.CreateRole']
		return_type_name: ActionResult<Guid>
		returns: None
	create_test_task:
		description: DEV: Creates a non-ending task with 50% progress for testing purposes
		is_complex_type: False
		parameters: []
		required_permissions: ['Core.Special.UseDevMethods']
		return_type_name: Void
		returns: 
	create_user:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'IsOIDCUser', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'OIDCSub', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.CreateNewUser']
		return_type_name: ActionResult<Guid>
		returns: None
	current_session_has_permission:
		description: None
		is_complex_type: False
		parameters: [{'name': 'PermissionNode', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: Boolean
		returns: None
	delete_instance_users:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.DeleteUser']
		return_type_name: ActionResult
		returns: None
	delete_role:
		description: None
		is_complex_type: True
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.RoleManagement.DeleteRoles']
		return_type_name: ActionResult
		returns: None
	delete_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'TaskID', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.DeleteTask']
		return_type_name: ActionResult
		returns: None
	delete_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.DeleteTask', 'Core.Scheduler.DeleteTrigger']
		return_type_name: ActionResult
		returns: None
	delete_user:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.DeleteUser']
		return_type_name: ActionResult
		returns: None
	disable_two_factor:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Password', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'TwoFactorCode', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.UpdateOwnAccount']
		return_type_name: ActionResult
		returns: None
	dismiss_all_tasks:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: ActionResult
		returns: None
	dismiss_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TaskId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: ActionResult
		returns: None
	edit_interval_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'months', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'days', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'hours', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'minutes', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'daysOfMonth', 'type_name': 'Int32[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'description', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.EditTrigger']
		return_type_name: ActionResult
		returns: None
	edit_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'TaskID', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'ParameterMapping', 'type_name': 'Dictionary<String, String>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.EditTask']
		return_type_name: ActionResult
		returns: None
	enable_two_factor:
		description: Sets up two-factor authentication for the given user. ConfirmTwoFactorSetup must be invoked to complete setup.
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Password', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: ActionResult<TwoFactorSetupInfo>
		returns: Data container the URI for a QR code that should be scanned by a mobile authenticator.
	end_user_session:
		description: None
		is_complex_type: False
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.EndUserSessions']
		return_type_name: Void
		returns: None
	get_active_amp_sessions:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.UserManagement.ViewActiveSessions']
		return_type_name: IEnumerable<JObject>
		returns: None
	get_all_amp_user_info:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.UserManagement.ViewUserInfo']
		return_type_name: IEnumerable<UserInfo>
		returns: None
	get_amp_role_permissions:
		description: None
		is_complex_type: False
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.RoleManagement.ViewRoles']
		return_type_name: IEnumerable<String>
		returns: None
	get_amp_user_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.ViewUserInfo']
		return_type_name: UserInfo
		returns: None
	get_amp_users_summary:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.UserManagement.ViewUserInfo']
		return_type_name: IEnumerable<UserInfoSummary>
		returns: None
	get_api_spec:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: Dictionary<String, Dictionary<String, JObject>>
		returns: None
	get_audit_log_entries:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Before', 'type_name': 'Nullable<DateTime>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Count', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.AuditLog.ViewAuditLog']
		return_type_name: IEnumerable<IAuditLogEntry>
		returns: None
	get_authentication_requirements:
		description: None
		is_complex_type: True
		parameters: [{'name': 'username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: IEnumerable<AuthenticationRequirement>
		returns: None
	get_config:
		description: None
		is_complex_type: True
		parameters: [{'name': 'node', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: JObject
		returns: None
	get_configs:
		description: None
		is_complex_type: True
		parameters: [{'name': 'nodes', 'type_name': 'String[]', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: IEnumerable<JObject>
		returns: None
	get_diagnostics_info:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['Core.Special.Diagnostics']
		return_type_name: Dictionary<String, String>
		returns: None
	get_module_info:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: JObject
		returns: None
	get_new_guid:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: []
		return_type_name: Guid
		returns: None
	get_oidc_login_url:
		description: None
		is_complex_type: False
		parameters: [{'name': 'redirect_uri', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: String
		returns: None
	get_oidc_logout_url:
		description: None
		is_complex_type: False
		parameters: [{'name': 'redirect_uri', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: String
		returns: None
	get_permissions_spec:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: IList<IPermissionsTreeNode>
		returns: None
	get_port_summaries:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: IEnumerable<ListeningPortSummary>
		returns: None
	get_provision_spec:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: List<JObject>
		returns: None
	get_remote_login_token:
		description: None
		is_complex_type: False
		parameters: [{'name': 'Description', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'IsTemporary', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: String
		returns: None
	get_role:
		description: None
		is_complex_type: True
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.RoleManagement.ViewRoles']
		return_type_name: AuthRoleSummary
		returns: None
	get_role_data:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.RoleManagement.ViewRoles']
		return_type_name: IEnumerable<AuthRoleSummary>
		returns: None
	get_role_ids:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['Core.RoleManagement.ViewRoles']
		return_type_name: IDictionary<Guid, String>
		returns: None
	get_schedule_data:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.Scheduler.ViewSchedule']
		return_type_name: JObject
		returns: None
	get_setting_values:
		description: None
		is_complex_type: False
		parameters: [{'name': 'SettingNode', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'WithRefresh', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: IDictionary<String, String>
		returns: None
	get_settings_spec:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: Dictionary<String, IEnumerable<JObject>>
		returns: None
	get_status:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: JObject
		returns: None
	get_structured_diagnostics:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['Core.Special.Diagnostics']
		return_type_name: Dictionary<String, Object>
		returns: None
	get_tasks:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: IEnumerable<RunningTask>
		returns: None
	get_time_interval_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.ViewSchedule']
		return_type_name: JObject
		returns: None
	get_update_info:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.Special.UpdateAMPInstance']
		return_type_name: JObject
		returns: None
	get_updates:
		description: Gets changes to the server status, in addition to any notifications or console output that have occurred since the last time GetUpdates() was called by the current session.
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: JObject
		returns: 
	get_user_actions_spec:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: []
		return_type_name: Object
		returns: None
	get_user_info:
		description: Provides information about a given in-application user (as opposed to AMP system users)
		is_complex_type: True
		parameters: [{'name': 'UID', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: SimpleUser
		returns: 
	get_user_list:
		description: Returns a list of in-application users
		is_complex_type: False
		parameters: []
		required_permissions: []
		return_type_name: Dictionary<String, String>
		returns: 
	get_webauthn_challenge:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: ActionResult<String>
		returns: None
	get_webauthn_credential_ids:
		description: None
		is_complex_type: True
		parameters: [{'name': 'username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: JObject
		returns: None
	get_webauthn_credential_summaries:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.UserManagement.UpdateOwnAccount']
		return_type_name: IEnumerable<WebauthnCredentialSummary>
		returns: None
	kill:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['Core.AppManagement.StopApplication']
		return_type_name: Void
		returns: None
	login:
		description: None
		is_complex_type: True
		parameters: [{'name': 'username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'password', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'token', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'rememberMe', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: JObject
		returns: None
	logout:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: []
		return_type_name: Void
		returns: None
	oidc_login:
		description: None
		is_complex_type: True
		parameters: [{'name': 'code', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'state', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'redirect_uri', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'serverId', 'type_name': 'Nullable<Guid>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: JObject
		returns: None
	refresh_setting_value_list:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Node', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: ActionResult
		returns: None
	refresh_settings_source_cache:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: []
		return_type_name: Void
		returns: None
	rename_role:
		description: None
		is_complex_type: True
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.RoleManagement.EditRoleInfo']
		return_type_name: ActionResult
		returns: None
	reset_user_password:
		description: For administrative users to alter the password of another user
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewPassword', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.ResetUserPassword']
		return_type_name: ActionResult
		returns: 
	restart:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.AppManagement.RestartApplication']
		return_type_name: ActionResult
		returns: None
	restart_amp:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.Special.RestartAMP']
		return_type_name: ActionResult
		returns: None
	resume:
		description: Allows the service to be re-started after previously being suspended.
		is_complex_type: False
		parameters: []
		required_permissions: []
		return_type_name: Void
		returns: 
	revert_user_from_oidc:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.UpdateUserInfo']
		return_type_name: ActionResult
		returns: None
	revoke_webauthn_credential:
		description: None
		is_complex_type: True
		parameters: [{'name': 'ID', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.UpdateOwnAccount']
		return_type_name: ActionResult
		returns: None
	run_event_trigger_immediately:
		description: None
		is_complex_type: True
		parameters: [{'name': 'triggerId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.CreateTrigger']
		return_type_name: ActionResult
		returns: None
	run_security_check:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.Special.RunSecurityCheck']
		return_type_name: IEnumerable<JObject>
		returns: None
	send_console_message:
		description: None
		is_complex_type: False
		parameters: [{'name': 'message', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.AppManagement.SendConsoleInput']
		return_type_name: Void
		returns: None
	set_amp_role_permission:
		description: None
		is_complex_type: True
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'PermissionNode', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Enabled', 'type_name': 'Nullable<Boolean>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.RoleManagement.EditRolePermissions']
		return_type_name: ActionResult
		returns: None
	set_amp_user_role_membership:
		description: None
		is_complex_type: True
		parameters: [{'name': 'UserId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'IsMember', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.ChangeRoleMembership']
		return_type_name: ActionResult
		returns: None
	set_config:
		description: None
		is_complex_type: True
		parameters: [{'name': 'node', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'value', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: ActionResult
		returns: None
	set_configs:
		description: None
		is_complex_type: False
		parameters: [{'name': 'data', 'type_name': 'Dictionary<String, String>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: Boolean
		returns: None
	set_trigger_enabled:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Enabled', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.Scheduler.EditTrigger']
		return_type_name: ActionResult
		returns: None
	sleep:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.AppManagement.StopApplication']
		return_type_name: ActionResult
		returns: None
	start:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.AppManagement.StartApplication']
		return_type_name: ActionResult
		returns: None
	stop:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['Core.AppManagement.StopApplication']
		return_type_name: Void
		returns: None
	suspend:
		description: Prevents the current instance from being started, and stops it if it's currently running.
		is_complex_type: False
		parameters: []
		required_permissions: []
		return_type_name: Void
		returns: 
	update_account_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'EmailAddress', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'TwoFactorPIN', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.UpdateOwnAccount']
		return_type_name: ActionResult
		returns: None
	update_amp_instance:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.Special.UpdateAMPInstance']
		return_type_name: ActionResult
		returns: None
	update_application:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.AppManagement.UpdateApplication']
		return_type_name: ActionResult
		returns: None
	update_oidc_sub:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'OIDCSub', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.UpdateUserInfo']
		return_type_name: ActionResult
		returns: None
	update_public_key:
		description: None
		is_complex_type: True
		parameters: [{'name': 'PubKey', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.UpdateOwnAccount']
		return_type_name: ActionResult
		returns: None
	update_tools:
		description: Updates the AMP system tools (ampinstmgr) to the latest release.
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.Special.UpgradeAMP']
		return_type_name: ActionResult<String>
		returns: 
	update_user_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Disabled', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'PasswordExpires', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'CannotChangePassword', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'MustChangePassword', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'EmailAddress', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.UpdateUserInfo']
		return_type_name: ActionResult
		returns: None
	upgrade_amp:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Core.Special.UpgradeAMP']
		return_type_name: ActionResult
		returns: None
	webauthn_register:
		description: None
		is_complex_type: True
		parameters: [{'name': 'attestationObject', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'clientDataJSON', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'description', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Core.UserManagement.UpdateOwnAccount']
		return_type_name: ActionResult
		returns: None
____________________________________________________
email_sender_plugin:
	test_smtp_settings:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: []
		return_type_name: ActionResult
		returns: None
____________________________________________________
file_manager_plugin:
	append_file_chunk:
		description: None
		is_complex_type: False
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Data', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Delete', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.UploadFiles']
		return_type_name: Void
		returns: None
	calculate_file_md5_sum:
		description: None
		is_complex_type: True
		parameters: [{'name': 'FilePath', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.DownloadFiles']
		return_type_name: ActionResult<String>
		returns: None
	change_exclusion:
		description: None
		is_complex_type: True
		parameters: [{'name': 'ModifyPath', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'AsDirectory', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Exclude', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.ChangeBackupExclusions']
		return_type_name: ActionResult
		returns: None
	copy_file:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Origin', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'TargetDirectory', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.CopyFiles']
		return_type_name: ActionResult
		returns: None
	create_archive:
		description: None
		is_complex_type: True
		parameters: [{'name': 'PathToArchive', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'OverwriteExisting', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.CreateArchive']
		return_type_name: ActionResult
		returns: None
	create_directory:
		description: Creates a new directory. The parent directory must already exist.
		is_complex_type: True
		parameters: [{'name': 'NewPath', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.CreateDirectory']
		return_type_name: ActionResult
		returns: 
	download_file_from_url:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Source', 'type_name': 'Uri', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'TargetDirectory', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.DownloadFromURL']
		return_type_name: ActionResult
		returns: None
	download_folder_as_zip:
		description: Download an entire folder as a zip archive
		is_complex_type: True
		parameters: [{'name': 'DirectoryPath', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.DownloadFiles']
		return_type_name: ActionResult<String>
		returns: 
	dummy:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['FileManager.FileManager.ConnectViaSFTP']
		return_type_name: Void
		returns: None
	empty_trash:
		description: Empties a trash bin
		is_complex_type: True
		parameters: [{'name': 'TrashDirectoryName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.EmptyTrash']
		return_type_name: ActionResult
		returns: 
	extract_archive:
		description: None
		is_complex_type: True
		parameters: [{'name': 'ArchivePath', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'DestinationPath', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.ExtractArchive']
		return_type_name: ActionResult
		returns: None
	get_directory_listing:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Dir', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.BrowseFiles']
		return_type_name: IEnumerable<JObject>
		returns: None
	get_file_chunk:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Position', 'type_name': 'Int64', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Length', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.DownloadFiles']
		return_type_name: JObject
		returns: None
	read_file_chunk:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Offset', 'type_name': 'Int64', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'ChunkSize', 'type_name': 'Int64', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.DownloadFiles']
		return_type_name: ActionResult<String>
		returns: None
	release_file_upload_lock:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.UploadFiles']
		return_type_name: ActionResult
		returns: None
	rename_directory:
		description: Renames a directory
		is_complex_type: True
		parameters: [{'name': 'oldDirectory', 'type_name': 'String', 'description': 'The full path to the old directory', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewDirectoryName', 'type_name': 'String', 'description': 'The name component of the new directory (not the full path)', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.RenameDirectories']
		return_type_name: ActionResult
		returns: 
	rename_file:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewFilename', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.RenameFiles']
		return_type_name: ActionResult
		returns: None
	trash_directory:
		description: Moves a directory to trash, files must be trashed before they can be deleted.
		is_complex_type: True
		parameters: [{'name': 'DirectoryName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.TrashDirectories']
		return_type_name: ActionResult
		returns: 
	trash_file:
		description: Moves a file to trash, files must be trashed before they can be deleted.
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.TrashFiles']
		return_type_name: ActionResult
		returns: 
	upload_folder:
		description: Upload an entire folder as a set of files with relative paths
		is_complex_type: True
		parameters: [{'name': 'TargetDirectory', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Files', 'type_name': 'List<FolderUploadFile>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.UploadFiles']
		return_type_name: ActionResult
		returns: 
	write_file_chunk:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Data', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Offset', 'type_name': 'Int64', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'FinalChunk', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['FileManager.FileManager.UploadFiles']
		return_type_name: ActionResult
		returns: None
____________________________________________________
generic_module:
	import_config:
		description: None
		is_complex_type: True
		parameters: [{'name': 'filename', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Generic.GenericConfig.ImportConfig']
		return_type_name: JObject
		returns: None
	refresh_remote_options:
		description: None
		is_complex_type: True
		parameters: [{'name': 'fieldName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: ActionResult
		returns: None
	refresh_tool_discovery:
		description: None
		is_complex_type: True
		parameters: [{'name': 'fieldName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: ActionResult
		returns: None
	reload_generic_config:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['Generic.GenericConfig.ReloadGenericConfig']
		return_type_name: Void
		returns: None
	request_server_info:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: []
		return_type_name: Void
		returns: None
____________________________________________________
local_file_backup_plugin:
	backup_will_stop_server:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['LocalFileBackup.Backup.ViewBackupsList']
		return_type_name: Boolean
		returns: None
	delete_from_s3:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['LocalFileBackup.Backup.DeleteBackup']
		return_type_name: ActionResult
		returns: None
	delete_local_backup:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['LocalFileBackup.Backup.DeleteBackup']
		return_type_name: ActionResult
		returns: None
	download_from_s3:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['LocalFileBackup.Backup.TransferBackup']
		return_type_name: RunningTask
		returns: None
	get_backups:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['LocalFileBackup.Backup.ViewBackupsList']
		return_type_name: IEnumerable<JObject>
		returns: None
	refresh_backup_list:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['LocalFileBackup.Backup.ViewBackupsList']
		return_type_name: Void
		returns: None
	restore_backup:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'DeleteExistingData', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['LocalFileBackup.Backup.RestoreBackup']
		return_type_name: ActionResult
		returns: None
	set_backup_sticky:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Sticky', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['LocalFileBackup.Backup.ToggleStickiness']
		return_type_name: ActionResult
		returns: None
	take_backup:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Title', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Description', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Sticky', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Local', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'S3', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'WasCreatedAutomatically', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'DirtyOnly', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'BackupWhileRunning', 'type_name': 'Nullable<Boolean>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['LocalFileBackup.Backup.CreateBackup']
		return_type_name: ActionResult
		returns: None
	upload_to_s3:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['LocalFileBackup.Backup.TransferBackup']
		return_type_name: RunningTask
		returns: None
____________________________________________________
rcon_plugin:
	dummy:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['RCON.RCONPassthru.Connect']
		return_type_name: Void
		returns: None
____________________________________________________
steamcmdplugin:
	cancel_steam_guard:
		description: None
		is_complex_type: False
		parameters: []
		required_permissions: ['Core.AppManagement.UpdateApplication']
		return_type_name: Void
		returns: None
	steam_guard_code:
		description: None
		is_complex_type: False
		parameters: [{'name': 'code', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.AppManagement.UpdateApplication']
		return_type_name: Void
		returns: None
	steam_username_password:
		description: None
		is_complex_type: False
		parameters: [{'name': 'username', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'password', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Core.AppManagement.UpdateApplication']
		return_type_name: Void
		returns: None
____________________________________________________
store_plugin:
	clear_store_data:
		description: None
		is_complex_type: True
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.InstallStoreEntries']
		return_type_name: ActionResult
		returns: None
	get_available_stores:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Store.Store.BrowseStores']
		return_type_name: IEnumerable<JObject>
		returns: None
	get_store_categories:
		description: None
		is_complex_type: True
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.BrowseStores']
		return_type_name: IEnumerable<JObject>
		returns: None
	get_store_entries_for_category:
		description: None
		is_complex_type: True
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'CategoryId', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'CategoryType', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'page', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'pageSize', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Store.Store.BrowseStores']
		return_type_name: PagedRecords<JObject>
		returns: None
	get_store_entry:
		description: None
		is_complex_type: True
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'EntryId', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.InstallStoreEntries']
		return_type_name: JObject
		returns: None
	get_store_filter_keys:
		description: None
		is_complex_type: False
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.BrowseStores']
		return_type_name: IEnumerable<String>
		returns: None
	get_store_filter_selections:
		description: None
		is_complex_type: False
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.BrowseStores']
		return_type_name: Dictionary<String, String>
		returns: None
	get_store_filter_values:
		description: None
		is_complex_type: False
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'FilterKey', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.BrowseStores']
		return_type_name: IEnumerable<String>
		returns: None
	install_store_entry:
		description: None
		is_complex_type: True
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'EntryId', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.InstallStoreEntries']
		return_type_name: RunningTask
		returns: None
	search_store:
		description: None
		is_complex_type: True
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'SearchQuery', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'page', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'pageSize', 'type_name': 'Int32', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: ['Store.Store.BrowseStores']
		return_type_name: PagedRecords<JObject>
		returns: None
	set_store_entry_auto_update:
		description: None
		is_complex_type: False
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'EntryId', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'AutoUpdate', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.InstallStoreEntries']
		return_type_name: Task
		returns: None
	set_store_entry_disabled:
		description: None
		is_complex_type: False
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'EntryId', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Disabled', 'type_name': 'Boolean', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.InstallStoreEntries']
		return_type_name: Task
		returns: None
	set_store_filter_selections:
		description: None
		is_complex_type: False
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'Filters', 'type_name': 'Dictionary<String, String>', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.BrowseStores']
		return_type_name: Void
		returns: None
	uninstall_store_entry:
		description: None
		is_complex_type: True
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'EntryId', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.InstallStoreEntries']
		return_type_name: ActionResult
		returns: None
	update_everything:
		description: None
		is_complex_type: True
		parameters: []
		required_permissions: ['Store.Store.UpdateStoreEntries']
		return_type_name: RunningTask
		returns: None
	update_store_entries:
		description: None
		is_complex_type: True
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.UpdateStoreEntries']
		return_type_name: RunningTask
		returns: None
	update_store_entry:
		description: None
		is_complex_type: True
		parameters: [{'name': 'StoreName', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}, {'name': 'EntryId', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': False, 'param_enum_values': None}]
		required_permissions: ['Store.Store.UpdateStoreEntries']
		return_type_name: RunningTask
		returns: None
____________________________________________________
webhook_plugin:
	trigger_webhook_event:
		description: None
		is_complex_type: False
		parameters: [{'name': 'payload', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}, {'name': 'data', 'type_name': 'String', 'description': '', 'placeholder': '', 'suffix': '', 'optional': True, 'param_enum_values': None}]
		required_permissions: []
		return_type_name: Void
		returns: None
