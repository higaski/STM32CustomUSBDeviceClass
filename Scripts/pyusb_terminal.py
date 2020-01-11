import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=1155, idProduct=42)

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

ep_out = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
    == usb.util.ENDPOINT_OUT,
)

ep_in = usb.util.find_descriptor(
    intf,
    # match the first IN endpoint
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
    == usb.util.ENDPOINT_IN,
)

assert ep_out is not None
assert ep_in is not None

while True:
    str_tx = input("TX: ")
    if str_tx == "exit":
        print("exiting...")
        break
    ep_out.write(str_tx + "\n")
    raw_rx = ep_in.read(len(str_tx) + 1, 1000)
    str_rx = str(raw_rx, "utf-8")
    print("RX: " + str_rx)
