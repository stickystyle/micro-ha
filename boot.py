# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import gc

def do_connect():
    import network
    try:
        from config import ssid, psk
    except ImportError:
        pass
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, psk)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
#do_connect()
gc.collect()
