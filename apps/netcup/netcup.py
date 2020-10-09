import appdaemon.plugins.hass.hassapi as hass
import globals
import datetime
import math
from suds.client import Client

class Netcup(hass.Hass):
    def initialize(self):
        self.scp_user = globals.get_arg(self.args, "scp_user")
        self.scp_api_passw = globals.get_arg(self.args, "scp_api_passw")
        self.timer = globals.get_arg(self.args, "timer")
        self.server = None
        url = 'https://www.servercontrolpanel.de:443/WSEndUser?wsdl'
        self.client = Client(url)
        self.run_every(self.getvalues, "now", self.timer * 60)

    def getvalues(self, kwargs):

        # get list with all servers 
        serversExists = False
        try: 
            result = self.client.service.getVServers(self.scp_user, self.scp_api_passw)
            self.set_state("sensor.netcup_vserver",state=result)
            servers = list(result)
            serversExists = True 
        except:
            self.log("Couldnt get Server list, check configuration")
        if(serversExists == True):
            count = 0
            for i in servers:
                self.server = servers[count]
                self.log("Create/Update Server: "+ format(self.server))
                self.createServers(self)
                count = count + 1

    def createServers(self, kwargs):
        serverstate = None
        try: 
            serverstate = self.client.service.getVServerState(self.scp_user, self.scp_api_passw, self.server)
            self.log("Server "+ format(self.server) + " " + format(serverstate))
        except: 
            self.log("Couldnt get State for "+ format(self.server))

        nickname = None
        try: 
            nickname = self.client.service.getVServerNickname(self.scp_user, self.scp_api_passw, self.server)
            self.log("Server "+ format(self.server) + " " + format(nickname))
        except: 
            self.log("Couldnt get Nickname for "+ format(self.server))
            
        ips = None
        try: 
            ips = self.client.service.getVServerIPs(self.scp_user, self.scp_api_passw, self.server)
            self.log("Server "+ format(self.server) + " " + format(ips[0]))
            self.log("Server "+ format(self.server) + " " + format(ips[1]))
        except: 
            self.log("Couldnt get IP Adresses for "+ format(self.server))
        
        uptime = None
        try: 
            uptime = self.client.service.getVServerUptime(self.scp_user, self.scp_api_passw, self.server)
            self.log("Server "+ format(self.server) + " " + format(uptime))
        except: 
            self.log("Couldnt get Uptime for "+ format(self.server))
        
        infor = None
        try: 
            infor = self.client.service.getVServerInformation(self.scp_user, self.scp_api_passw, self.server)
            self.log("Server "+ format(self.server) + " Additional Information")
        except: 
            self.log("Couldnt get Additional Information for "+ format(self.server))

        listee = infor[8]
        sensorserver = "sensor.netcup_vserver_"+ format(self.server)
        try: 
            self.set_state(sensorserver,state=serverstate.capitalize(),attributes={"friendly_name": nickname, "IPv4": ips[0], "IPv6": ips[1], "Uptime": uptime, "Cores": infor[0], "Memory": infor[3], "Reboot recommended": infor[4], "HDD Size": listee[0][0], "HDD Used": listee[0][5], "Optimization Recommended": listee[0][3], "Optimization Message": listee[0][4]})
            self.log("Created / Updated sensor for "+ format(self.server))
        except:
            self.log("Couldnt create / update sensor for " + format(self.server) + " Please check configuration")