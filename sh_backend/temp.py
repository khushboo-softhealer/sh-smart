import websocket

print("\n\n\n websocket connect code start----->")
ws = websocket.create_connection("wss://www.cloudposintegration.io/nexouat1")
print("\n\n\n websocket connected------>")
status = ws.getstatus()
print("\n\n\nwebsocket connection status------->", status)
