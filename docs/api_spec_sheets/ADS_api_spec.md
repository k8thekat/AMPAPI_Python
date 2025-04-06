INSTANCE TYPE: ADS
APP VERSION: 2.6.0.12 | None
BUILD: 24/02/2025 17:12

____________________________________________________
ads_module:
	add_datastore:
		description: None
		is_complex_type: True
		parameters: [{'name': 'newDatastore', 'type_name': 'InstanceDatastore', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	apply_instance_configuration:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Args', 'type_name': 'Dictionary<String, String>', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'RebuildConfiguration', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	apply_template:
		description: Overlays an existing template on an existing instance. Used to perform package reconfigurations. Do not use this to 'transform' an existing application into another. The instance should be deleted and re-created in that situation.
		is_complex_type: True
		parameters: [{'name': 'InstanceID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TemplateID', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewFriendlyName', 'type_name': 'String', 'description': '', 'optional': True, 'param_enum_values': None}, {'name': 'Secret', 'type_name': 'String', 'description': '', 'optional': True, 'param_enum_values': None}, {'name': 'RestartIfPreviouslyRunning', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: 
	attach_ads:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Friendly', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'IsHTTPS', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Host', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Port', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'InstanceID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	clone_template:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	create_deployment_template:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Name', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	create_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TargetADSInstance', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'NewInstanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Module', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'InstanceName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'FriendlyName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'IPBinding', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PortNumber', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'AdminUsername', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'AdminPassword', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'ProvisionSettings', 'type_name': 'Dictionary<String, String>', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'AutoConfigure', 'type_name': 'Boolean', 'description': 'When enabled, all settings other than the Module, Target and FriendlyName are ignored and replaced with automatically generated values.', 'optional': True, 'param_enum_values': None}, {'name': 'PostCreate', 'type_name': 'PostCreateAppActions', 'description': '', 'optional': True, 'param_enum_values': {'do_nothing': 0, 'update_once': 1, 'update_always': 2, 'update_and_start_once': 3, 'update_and_start_always': 4, 'start_always': 5}}, {'name': 'StartOnBoot', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}, {'name': 'DisplayImageSource', 'type_name': 'String', 'description': '', 'optional': True, 'param_enum_values': None}, {'name': 'TargetDatastore', 'type_name': 'Int32', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	create_instance_from_spec:
		description: None
		is_complex_type: True
		parameters: [{'name': 'SpecId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'TargetADSInstance', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'FriendlyName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PostCreate', 'type_name': 'PostCreateAppActions', 'description': '', 'optional': True, 'param_enum_values': {'do_nothing': 0, 'update_once': 1, 'update_always': 2, 'update_and_start_once': 3, 'update_and_start_always': 4, 'start_always': 5}}, {'name': 'StartOnBoot', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}, {'name': 'TargetDatastore', 'type_name': 'Int32', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	create_local_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Instance', 'type_name': 'LocalAMPInstance', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PostCreate', 'type_name': 'PostCreateAppActions', 'description': '', 'optional': True, 'param_enum_values': {'do_nothing': 0, 'update_once': 1, 'update_always': 2, 'update_and_start_once': 3, 'update_and_start_always': 4, 'start_always': 5}}]
		return_type_name: ActionResult
		returns: None
	delete_datastore:
		description: None
		is_complex_type: True
		parameters: [{'name': 'id', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	delete_deployment_template:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	delete_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: RunningTask
		returns: None
	delete_instance_users:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	deploy_template:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TemplateID', 'type_name': 'Int32', 'description': 'The ID of the template to be deployed, as per the Template Management UI in AMP itself.', 'optional': False, 'param_enum_values': None}, {'name': 'NewUsername', 'type_name': 'String', 'description': 'If specified, AMP will create a new user with this name for this instance. Must be unique. If this user already exists, this will be ignored but the new instance will be assigned to this user.', 'optional': True, 'param_enum_values': None}, {'name': 'NewPassword', 'type_name': 'String', 'description': "If 'NewUsername' is specified and the user doesn't already exist, the password that will be assigned to this user.", 'optional': True, 'param_enum_values': None}, {'name': 'NewEmail', 'type_name': 'String', 'description': "If 'NewUsername' is specified and the user doesn't already exist, the email address that will be assigned to this user.", 'optional': True, 'param_enum_values': None}, {'name': 'RequiredTags', 'type_name': 'List<String>', 'description': "If specified, AMP will only deploy this template to targets that have every single 'tag' specified in their target configuration. You can adjust this via the controller by clicking 'Edit' on the target settings.", 'optional': True, 'param_enum_values': None}, {'name': 'Tag', 'type_name': 'String', 'description': "Unrelated to RequiredTags. This is to uniquely identify this instance to your own systems. It may be something like an order ID or service ID so you can find the associated instance again at a later time. If 'UseTagAsInstanceName' is enabled, then this will also be used as the instance name for the created instance - but it must be unique.", 'optional': True, 'param_enum_values': None}, {'name': 'FriendlyName', 'type_name': 'String', 'description': 'A friendly name for this instance. If left blank, AMP will generate one for you.', 'optional': True, 'param_enum_values': None}, {'name': 'Secret', 'type_name': 'String', 'description': 'Must be a non-empty strong in order to get a callback on deployment state change. This secret will be passed back to you in the callback so you can verify the request.', 'optional': True, 'param_enum_values': None}, {'name': 'PostCreate', 'type_name': 'PostCreateAppActions', 'description': '0: Do Nothing, 1: Update Once, 2: Update Always, 3: Update and Start Once, 4: Update and Start Always, 5. Start Always', 'optional': True, 'param_enum_values': {'do_nothing': 0, 'update_once': 1, 'update_always': 2, 'update_and_start_once': 3, 'update_and_start_always': 4, 'start_always': 5}}, {'name': 'ExtraProvisionSettings', 'type_name': 'Dictionary<String, String>', 'description': 'A dictionary of setting nodes and values to create the new instance with. Identical in function to the provisioning arguments in the template itself.', 'optional': True, 'param_enum_values': None}]
		return_type_name: RunningTask
		returns: None
	detach_target:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	extract_everywhere:
		description: None
		is_complex_type: True
		parameters: [{'name': 'SourceArchive', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	get_application_endpoints:
		description: None
		is_complex_type: True
		parameters: [{'name': 'instanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: IEnumerable<JObject>
		returns: None
	get_datastore:
		description: None
		is_complex_type: True
		parameters: [{'name': 'id', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JObject
		returns: None
	get_datastore_instances:
		description: None
		is_complex_type: True
		parameters: [{'name': 'datastoreId', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: IEnumerable<JObject>
		returns: None
	get_datastores:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	get_deployment_templates:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	get_group:
		description: None
		is_complex_type: True
		parameters: [{'name': 'GroupId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JObject
		returns: None
	get_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JObject
		returns: None
	get_instance_network_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: IEnumerable<JObject>
		returns: None
	get_instance_statuses:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	get_instances:
		description: None
		is_complex_type: True
		parameters: [{'name': 'ForceIncludeSelf', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: IEnumerable<JObject>
		returns: None
	get_local_instances:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	get_provision_arguments:
		description: None
		is_complex_type: True
		parameters: [{'name': 'ModuleName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: IEnumerable<ProvisionSettingInfo>
		returns: None
	get_provision_fitness:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JObject
		returns: None
	get_supported_app_summaries:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	get_supported_applications:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: IEnumerable<JObject>
		returns: None
	get_target_info:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: JObject
		returns: None
	handout_instance_configs:
		description: None
		is_complex_type: True
		parameters: [{'name': 'ForModule', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'SettingNode', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Values', 'type_name': 'List<String>', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	manage_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult<String>
		returns: None
	modify_custom_firewall_rule:
		description: None
		is_complex_type: True
		parameters: [{'name': 'instanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PortNumber', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Range', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Protocol', 'type_name': 'PortProtocol', 'description': '', 'optional': False, 'param_enum_values': {'tcp': 0, 'udp': 1, 'both': 2}}, {'name': 'Description', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Open', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	move_instance_datastore:
		description: None
		is_complex_type: True
		parameters: [{'name': 'instanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'datastoreId', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: RunningTask
		returns: None
	reactivate_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'instanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: RunningTask
		returns: None
	reactivate_local_instances:
		description: None
		is_complex_type: True
		parameters: []
		return_type_name: RunningTask
		returns: None
	refresh_app_cache:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: Void
		returns: None
	refresh_group:
		description: None
		is_complex_type: True
		parameters: [{'name': 'GroupId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	refresh_instance_config:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceId', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	refresh_remote_config_stores:
		description: None
		is_complex_type: False
		parameters: [{'name': 'force', 'type_name': 'Boolean', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	register_target:
		description: None
		is_complex_type: True
		parameters: [{'name': 'controllerUrl', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'myUrl', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'password', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'twoFactorToken', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'friendlyName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	repair_datastore:
		description: None
		is_complex_type: True
		parameters: [{'name': 'id', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: RunningTask
		returns: None
	request_datastore_size_calculation:
		description: None
		is_complex_type: True
		parameters: [{'name': 'datastoreId', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: RunningTask
		returns: None
	restart_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	servers:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Data', 'type_name': 'JObject', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'RealIP', 'type_name': 'IPAddress', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: JSONRawResponse
		returns: None
	set_instance_config:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'SettingNode', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Value', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	set_instance_network_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceId', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'PortMappings', 'type_name': 'Dictionary<String, Int32>', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	set_instance_suspended:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Suspended', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	start_all_instances:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TargetADSInstance', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	start_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	stop_all_instances:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TargetADSInstance', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	stop_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	test_ads_login_details:
		description: None
		is_complex_type: True
		parameters: [{'name': 'url', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'username', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'password', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'twoFactorToken', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	update_datastore:
		description: None
		is_complex_type: True
		parameters: [{'name': 'updatedDatastore', 'type_name': 'InstanceDatastore', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	update_deployment_template:
		description: None
		is_complex_type: True
		parameters: [{'name': 'templateToUpdate', 'type_name': 'DeploymentTemplate', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	update_instance_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceId', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'FriendlyName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Description', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'StartOnBoot', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Suspended', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'ExcludeFromFirewall', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'RunInContainer', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'ContainerMemory', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'ContainerSwap', 'type_name': 'Int32', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'MemoryPolicy', 'type_name': 'ContainerMemoryPolicy', 'description': '', 'optional': False, 'param_enum_values': {'not_specified': 0, 'reserve': 100, 'restrict': 200}}, {'name': 'ContainerMaxCPU', 'type_name': 'Single', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'ContainerImage', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'WelcomeMessage', 'type_name': 'String', 'description': '', 'optional': True, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	update_target:
		description: None
		is_complex_type: False
		parameters: [{'name': 'TargetID', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: Void
		returns: None
	update_target_info:
		description: None
		is_complex_type: True
		parameters: [{'name': 'Id', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'FriendlyName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Url', 'type_name': 'Uri', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Description', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'Tags', 'type_name': 'List<String>', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	upgrade_all_instances:
		description: None
		is_complex_type: True
		parameters: [{'name': 'TargetADSInstance', 'type_name': 'Guid', 'description': '', 'optional': False, 'param_enum_values': None}, {'name': 'RestartRunning', 'type_name': 'Boolean', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
		returns: None
	upgrade_instance:
		description: None
		is_complex_type: True
		parameters: [{'name': 'InstanceName', 'type_name': 'String', 'description': '', 'optional': False, 'param_enum_values': None}]
		return_type_name: ActionResult
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
	get_oidc_login_url:
		description: None
		is_complex_type: False
		parameters: []
		return_type_name: String
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
