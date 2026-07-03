from ncclient import manager
import xml.dom.minidom

HOST = '192.168.56.102'
PORT = 830
USER = 'cisco'
PASS = 'cisco123!'

def change_hostname(hostname):
    payload = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>{hostname}</hostname>
      </native>
    </config>
    """
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS,
                         hostkey_verify=False, device_params={'name': 'csr'}) as m:
        response = m.edit_config(target='running', config=payload)
        print(xml.dom.minidom.parseString(response.xml).toprettyxml())

def create_loopback():
    payload = """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>11</name>
            <ip>
              <address>
                <primary>
                  <address>11.11.11.11</address>
                  <mask>255.255.255.255</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
      </native>
    </config>
    """
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS,
                         hostkey_verify=False, device_params={'name': 'csr'}) as m:
        response = m.edit_config(target='running', config=payload)
        print(xml.dom.minidom.parseString(response.xml).toprettyxml())

if __name__ == '__main__':
    change_hostname("Router-Valdes-Bernilla")
    create_loopback()