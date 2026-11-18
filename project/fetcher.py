import network
import time
from secrets import WIFI_SSID, WIFI_PASSWORD, API_KEY
import requests # urequests for micropython
import json
import re
from data import TransportMode, DepartureInfo, datetime
from debug_log import log
TYPE_CHECKING=False
if TYPE_CHECKING:
    from typing import Callable

class Fetcher:
    net_tranport_mode_to_transport_mode={
        'BOAT':TransportMode('Ferry'),
        'BUS':TransportMode('Bus'),
        'TRAIN':TransportMode('Train'),
    }

    date_pattern=re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):\d\d')

    class NetworkStatus:
        last_fetch: int
        active: bool
        def __init__(self, last_fetch:int, active:bool):
            self.last_fetch=last_fetch
            self.active=active

    def __init__(self,get_current_stop:Callable,on_refetch:Callable):
        self.last_fetch={}
        self.get_current_stop=get_current_stop
        self.on_refetch=on_refetch
        self.station = network.WLAN(network.STA_IF)

    def connect(self):
        self.station.active(True)
        self.station.connect(WIFI_SSID, WIFI_PASSWORD)
        started = time.ticks_ms()
        while (not self.station.isconnected() and time.ticks_diff(time.ticks_ms(), started) < 15_000):
            time.sleep_ms(100)
        log("Wi-Fi connected" if self.station.isconnected() else "Wi-Fi could not connect (timeout)")

    def status(self) -> NetworkStatus:
        return self.NetworkStatus(self.last_fetch.get(self.get_current_stop(),-1),self.station.isconnected())

    def refetch(self):
        stop=self.get_current_stop()
        if stop is None or not self.station.isconnected():
            return
        out=requests.get(url='https://realtime-api.trafiklab.se/v1/departures/%s?key=%s'%(stop,API_KEY)).text
        out=json.loads(out)
        if 'errorCode' in out:
            log('request error: %s'%(out['errorDetail']))
            return
        self.last_fetch[stop]=time.ticks_ms()
        self.on_refetch(stop,tuple((DepartureInfo(
            (lambda match: datetime(*(int(match.group(j+1)) for j in range(5))))(self.date_pattern.match(i['realtime'])),
            i['route']['designation'],
            i['route']['destination']['name'],
            self.net_tranport_mode_to_transport_mode[i['route']['transport_mode']],
            'Canceled' if i['canceled'] else 'Delayed' if i['delay']>60 else 'On time',
            ) for i in out['departures'])))

    def need_refetch(self):
        stop=self.get_current_stop()
        return (stop not in self.last_fetch
                or (time.ticks_ms()-self.last_fetch[stop])>=60_000)
