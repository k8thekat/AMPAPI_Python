INSTANCE TYPE: Minecraft
APP VERSION: 2.6.0.4 | None
BUILD: 06/11/2024 22:37

____________________________________________________
analytics_plugin:
	get_analytics_summary:
		description: None
		is_complex_type: False
		parameters: [{'name': 'PeriodDays', 'type_name': 'Int32', 'description': '', 'optional': True, 'param_enum_values': None}, {'name': 'StartDate', 'type_name': 'Nullable<DateTime>', 'description': '', 'optional': True, 'param_enum_values': None}, {'name': 'Filters', 'type_name': 'Dictionary<String, String>', 'description': '', 'optional': True, 'param_enum_values': None}]
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
		return_type_name: Void
		returns: None
	activate_amp_licence:
		description: None
		is_complex_type: True
		parameters: [{'name': 'LicenceKey', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'QueryOnly', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult<JObject>
		returns: None
	add_event_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'triggerId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	add_interval_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'months', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'days', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'hours', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'minutes', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'daysOfMonth', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'description', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	add_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'MethodID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'ParameterMapping', 'type_name': 'Dictionary<String, String>', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	async_test:
		description: DEV: Async test method
		is_complex_type: False
		parameters: []
		return_type_name: String
		returns: 
	cancel_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TaskId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	change_task_order:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TaskID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewOrder', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	change_user_password:
		description: For a user to change their own password, requires knowing the old password
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'OldPassword', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewPassword', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TwoFactorPIN', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: 
	confirm_two_factor_setup:
		description: Completes two-factor setup by supplying a valid two factor code based on the secret provided by EnableTwoFactor
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TwoFactorCode', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: 
	create_role:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Name', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'AsCommonRole', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult<Guid>
		returns: None
	create_test_task:
		description: DEV: Creates a non-ending task with 50% progress for testing purposes
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: 
	create_user:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult<Guid>
		returns: None
	current_session_has_permission:
		description: None
		is_complex_type: False
		parameters: [{'name': 'PermissionNode', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Boolean
		returns: None
	delete_instance_users:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	delete_role:
		description: None
		is_complex_type: True
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	delete_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TaskID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	delete_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	delete_user:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	disable_two_factor:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Password', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TwoFactorCode', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	dismiss_all_tasks:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: ActionResult
		returns: None
	dismiss_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TaskId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	edit_interval_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'months', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'days', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'hours', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'minutes', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'daysOfMonth', 'type_name': 'Int32[]', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'description', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	edit_task:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TriggerID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TaskID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'ParameterMapping', 'type_name': 'Dictionary<String, String>', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	enable_two_factor:
		description: Sets up two-factor authentication for the given user. ConfirmTwoFactorSetup must be invoked to complete setup.
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Password', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult<TwoFactorSetupInfo>
		returns: Data container the URI for a QR code that should be scanned by a mobile authenticator.
	end_user_session:
		description: None
		is_complex_type: False
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	get_active_amp_sessions:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	get_all_amp_user_info:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<UserInfo>
		returns: None
	get_amp_role_permissions:
		description: None
		is_complex_type: False
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: IEnumerable<String>
		returns: None
	get_amp_user_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: UserInfo
		returns: None
	get_amp_users_summary:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<UserInfoSummary>
		returns: None
	get_api_spec:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: Dictionary<String, Dictionary<String, JObject>>
		returns: None
	get_audit_log_entries:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Before', 'type_name': 'Nullable<DateTime>', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Count', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: IEnumerable<IAuditLogEntry>
		returns: None
	get_authentication_requirements:
		description: None
		is_complex_type: True
		parameters: [{'name': 'username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: IEnumerable<AuthenticationRequirement>
		returns: None
	get_config:
		description: None
		is_complex_type: True
		parameters: [{'name': 'node', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JObject
		returns: None
	get_configs:
		description: None
		is_complex_type: True
		parameters: [{'name': 'nodes', 'type_name': 'String[]', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: IEnumerable<JObject>
		returns: None
	get_diagnostics_info:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Dictionary<String, String>
		returns: None
	get_module_info:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JObject
		returns: None
	get_new_guid:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Guid
		returns: None
	get_permissions_spec:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IList<IPermissionsTreeNode>
		returns: None
	get_port_summaries:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<ListeningPortSummary>
		returns: None
	get_provision_spec:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: List<JObject>
		returns: None
	get_remote_login_token:
		description: None
		is_complex_type: False
		parameters: [{'name': 'Description', 'type_name': 'String', 'description': '', 'optional': True, 'param_enum_values': None}, {'name': 'IsTemporary', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: String
		returns: None
	get_role:
		description: None
		is_complex_type: True
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: AuthRoleSummary
		returns: None
	get_role_data:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<AuthRoleSummary>
		returns: None
	get_role_ids:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: IDictionary<Guid, String>
		returns: None
	get_schedule_data:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JObject
		returns: None
	get_setting_values:
		description: None
		is_complex_type: False
		parameters: [{'name': 'SettingNode', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'WithRefresh', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: IDictionary<String, String>
		returns: None
	get_settings_spec:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: Dictionary<String, IEnumerable<JObject>>
		returns: None
	get_status:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JObject
		returns: None
	get_tasks:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<RunningTask>
		returns: None
	get_time_interval_trigger:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JObject
		returns: None
	get_update_info:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JObject
		returns: None
	get_updates:
		description: Gets changes to the server status, in addition to any notifications or console output that have occurred since the last time GetUpdates() was called by the current session.
		is_complex_type: True
		parameters: []
		return_type_name: JObject
		returns: 
	get_user_actions_spec:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Object
		returns: None
	get_user_info:
		description: Provides information about a given in-application user (as opposed to AMP system users)
		is_complex_type: True
		parameters: [{'name': 'UID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: SimpleUser
		returns: 
	get_user_list:
		description: Returns a list of in-application users
		is_complex_type: False
		parameters: []
		return_type_name: Dictionary<String, String>
		returns: 
	get_webauthn_challenge:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: ActionResult<String>
		returns: None
	get_webauthn_credential_i_ds:
		description: None
		is_complex_type: True
		parameters: [{'name': 'username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JObject
		returns: None
	get_webauthn_credential_summaries:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<WebauthnCredentialSummary>
		returns: None
	kill:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	login:
		description: None
		is_complex_type: True
		parameters: [{'name': 'username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'password', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'token', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'rememberMe', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JObject
		returns: None
	logout:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	refresh_setting_value_list:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Node', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	refresh_settings_source_cache:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	rename_role:
		description: None
		is_complex_type: True
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	reset_user_password:
		description: For administrative users to alter the password of another user
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewPassword', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: 
	restart:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: ActionResult
		returns: None
	restart_amp:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	resume:
		description: Allows the service to be re-started after previously being suspended.
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: 
	revoke_webauthn_credential:
		description: None
		is_complex_type: True
		parameters: [{'name': 'ID', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	run_event_trigger_immediately:
		description: None
		is_complex_type: True
		parameters: [{'name': 'triggerId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	run_security_check:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	send_console_message:
		description: None
		is_complex_type: False
		parameters: [{'name': 'message', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	set_amp_role_permission:
		description: None
		is_complex_type: True
		parameters: [{'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PermissionNode', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Enabled', 'type_name': 'Nullable<Boolean>', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	set_amp_user_role_membership:
		description: None
		is_complex_type: True
		parameters: [{'name': 'UserId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'RoleId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'IsMember', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	set_config:
		description: None
		is_complex_type: True
		parameters: [{'name': 'node', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'value', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	set_configs:
		description: None
		is_complex_type: False
		parameters: [{'name': 'data', 'type_name': 'Dictionary<String, String>', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Boolean
		returns: None
	set_trigger_enabled:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Enabled', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	sleep:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: ActionResult
		returns: None
	start:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: ActionResult
		returns: None
	stop:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	suspend:
		description: Prevents the current instance from being started, and stops it if it's currently running.
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: 
	update_account_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'EmailAddress', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TwoFactorPIN', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	update_amp_instance:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	update_application:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: ActionResult
		returns: None
	update_user_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Disabled', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PasswordExpires', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'CannotChangePassword', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'MustChangePassword', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'EmailAddress', 'type_name': 'String', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	upgrade_amp:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	webauthn_register:
		description: None
		is_complex_type: True
		parameters: [{'name': 'attestationObject', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'clientDataJSON', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'description', 'type_name': 'String', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
____________________________________________________
email_sender_plugin:
	test_smtp_settings:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: ActionResult
		returns: None
____________________________________________________
file_manager_plugin:
	append_file_chunk:
		description: None
		is_complex_type: False
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Data', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Delete', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	calculate_file_md5_sum:
		description: None
		is_complex_type: True
		parameters: [{'name': 'FilePath', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult<String>
		returns: None
	change_exclusion:
		description: None
		is_complex_type: True
		parameters: [{'name': 'ModifyPath', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'AsDirectory', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Exclude', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	copy_file:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Origin', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TargetDirectory', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	create_archive:
		description: None
		is_complex_type: True
		parameters: [{'name': 'PathToArchive', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	create_directory:
		description: Creates a new directory. The parent directory must already exist.
		is_complex_type: True
		parameters: [{'name': 'NewPath', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: 
	download_file_from_url:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Source', 'type_name': 'Uri', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TargetDirectory', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	dummy:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	empty_trash:
		description: Empties a trash bin
		is_complex_type: True
		parameters: [{'name': 'TrashDirectoryName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: 
	extract_archive:
		description: None
		is_complex_type: True
		parameters: [{'name': 'ArchivePath', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'DestinationPath', 'type_name': 'String', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	get_directory_listing:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Dir', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: IEnumerable<JObject>
		returns: None
	get_file_chunk:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Position', 'type_name': 'Int64', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Length', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JObject
		returns: None
	read_file_chunk:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Offset', 'type_name': 'Int64', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'ChunkSize', 'type_name': 'Int64', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult<String>
		returns: None
	release_file_upload_lock:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	rename_directory:
		description: Renames a directory
		is_complex_type: True
		parameters: [{'name': 'oldDirectory', 'type_name': 'String', 'description': 'The full path to the old directory', 'optional': False, 'param_enum_values': None}, {'name': 'NewDirectoryName', 'type_name': 'String', 'description': 'The name component of the new directory (not the full path)', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: 
	rename_file:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewFilename', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	trash_directory:
		description: Moves a directory to trash, files must be trashed before they can be deleted.
		is_complex_type: True
		parameters: [{'name': 'DirectoryName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: 
	trash_file:
		description: Moves a file to trash, files must be trashed before they can be deleted.
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: 
	write_file_chunk:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Filename', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Data', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Offset', 'type_name': 'Int64', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'FinalChunk', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
____________________________________________________
local_file_backup_plugin:
	delete_from_s3:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	delete_local_backup:
		description: None
		is_complex_type: False
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	download_from_s3:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: RunningTask
		returns: None
	get_backups:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	refresh_backup_list:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	restore_backup:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'DeleteExistingData', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	set_backup_sticky:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Sticky', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	take_backup:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Title', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Description', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Sticky', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'WasCreatedAutomatically', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	upload_to_s3:
		description: None
		is_complex_type: True
		parameters: [{'name': 'BackupId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: RunningTask
		returns: None
____________________________________________________
minecraft_module:
	accept_eula:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Boolean
		returns: None
	add_op_entry:
		description: None
		is_complex_type: True
		parameters: [{'name': 'UserOrUUID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	add_to_whitelist:
		description: None
		is_complex_type: True
		parameters: [{'name': 'UserOrUUID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	ban_user_by_id:
		description: None
		is_complex_type: False
		parameters: [{'name': 'ID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	buk_get_categories:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JSONRawResponse
		returns: None
	buk_get_install_update_plugin:
		description: None
		is_complex_type: True
		parameters: [{'name': 'pluginId', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: RunningTask
		returns: None
	buk_get_installed_plugins:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JSONRawResponse
		returns: None
	buk_get_plugin_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'PluginId', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JSONRawResponse
		returns: None
	buk_get_plugins_for_category:
		description: None
		is_complex_type: True
		parameters: [{'name': 'CategoryId', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PageNumber', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PageSize', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JSONRawResponse
		returns: None
	buk_get_popular_plugins:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JSONRawResponse
		returns: None
	buk_get_remove_plugin:
		description: None
		is_complex_type: False
		parameters: [{'name': 'PluginId', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	buk_get_search:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Query', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PageNumber', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PageSize', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JSONRawResponse
		returns: None
	clear_inventory_by_id:
		description: None
		is_complex_type: False
		parameters: [{'name': 'ID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	get_failure_reason:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: String
		returns: None
	get_head_by_uuid:
		description: Get a skin as a base64 string
		is_complex_type: False
		parameters: [{'name': 'id', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: String
		returns: 
	get_op_whitelist:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JObject
		returns: None
	get_whitelist:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	kick_user_by_id:
		description: None
		is_complex_type: False
		parameters: [{'name': 'ID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	kill_by_id:
		description: None
		is_complex_type: False
		parameters: [{'name': 'ID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	load_op_list:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	remove_op_entry:
		description: None
		is_complex_type: False
		parameters: [{'name': 'UserOrUUID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	remove_whitelist_entry:
		description: None
		is_complex_type: False
		parameters: [{'name': 'UserOrUUID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	smite_by_id:
		description: Strike a player with lightning
		is_complex_type: False
		parameters: [{'name': 'ID', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: 
