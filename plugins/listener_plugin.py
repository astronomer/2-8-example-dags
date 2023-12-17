from airflow.plugins_manager import AirflowPlugin
from plugins import listener_code


class MyListenerPlugin(AirflowPlugin):
    # A list of Listeners that plugin provides. Listeners can register to
    # listen to particular events that happen in Airflow, like
    # TaskInstance state changes. Listeners are python modules.
    name = "my_listener_plugin"
    listeners = [listener_code]
