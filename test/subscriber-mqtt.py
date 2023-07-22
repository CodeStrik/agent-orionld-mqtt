import paho.mqtt.client as mqtt
import argparse

def suscription(topic):
    # MQTT client configuration
    broker_address = "localhost"  
    client = mqtt.Client("Subscriber")  

    # Username and password configuration for the connection
    username = "admin"  
    password = "strik"  
    client.username_pw_set(username, password)

    # Definition of a function to process received messages
    def on_message(client, userdata, message):
        print("Message received on the topic: ", message.topic)
        print("Message content: ", message.payload.decode())

    # Configuration of the message reception function
    client.on_message = on_message

    # Connecting to the broker
    client.connect(broker_address)

    # Subscription to a specific topic
    #topic = "urn:ngsi-ld:PruebaDispositivo:003"     # Each topic will have the name of the device's URN within Orion-LD
    client.subscribe(topic)

    # Keeping the client listening for incoming messages
    client.loop_forever()

def main():
    parser = argparse.ArgumentParser(description="Script to subscribe to an MQTT topic")
    parser.add_argument("-t", "--topic", required=True, help="MQTT topic name (Device URN), example: urn:ngsi-ld:Device:001")
    parser.add_argument("-u", "--user", required=True, help="User to access the MQTT broker, example: user1")
    parser.add_argument("-pw", "--password", required=True, help="Password to access the MQTT broker, example: 1234")
    args = parser.parse_args()

    # We call the function, passing the argument received from the terminal
    suscription(args.topic)

if __name__ == '__main__':
    main()