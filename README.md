# AppdaemonNetcupAPI
Appdaemon App which connects to the Netcup ServerControlPanel API and generates for every VServer an entity with basic stats. 

The app creates a single sensor with all active servers in a single array. 

For each entity in the array, the app creates an sensor with the "Online/Offline" as the state. If available additional data like free space or ip addresses are stored in the attributes of each entity. 

![Preview](https://github.com/dolphinxjd/AppdaemonNetcupAPI/blob/master/HomeAssistant.png?raw=true)


you need to change the scp_user and scp_api_passw to your ServerControlPanel user and api password. If you dont have an api-password, you can request it in your ServerControlPanel.

The timer defines time beteween each update in minutes. Default value is every hour.

### "suds-community" python-package in Appdaemon required!
## only works with appdaemon 4.0.4 or later !!!