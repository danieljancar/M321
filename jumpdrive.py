from opcua import Client, ua


client = Client("opc.tcp://10.255.255.254:2035/")

def connect_to_opcua():
    try:
        client.connect()
        print("Verbunden mit OPC UA Server")

        node = client.get_node("ns=0;i=20001")
        print(f"Node Name: {node.get_browse_name()}")
    except Exception as e:
        print(f"Fehler bei der Verbindung zum OPC UA Server: {e}")


def jump_to(x, y):
    try:
        node = client.get_node("ns=0;i=20001")
        result = node.call_method("0:JumpTo", ua.Variant(x, ua.VariantType.Int32), ua.Variant(y, ua.VariantType.Int32))
        print(f"Ergebnis von JumpTo: {result}")
        client.disconnect()

    except Exception as e:
        print(f"Fehler bei JumpTo: {e}")

"""
- nuclear reactor muss laufen und uran verbennen
- wenn jumpdrive aufgeladen ist dann ausführen
- kann nur 20000 springen (x und y zusammen)

Beispiel:
Wenn ich (-50000; -40000) bin, muss ich zu (-40000; -30000) springen
Dann bewege ich mich 10000 in X-Richtung und in Y-Richtung. Das gibt zusammen das Limit 20000
"""
connect_to_opcua()
jump_to(0, 0)
