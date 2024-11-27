example_note = """
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


"""
