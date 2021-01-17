# homeassistant-xiaomi-water-purifier-yunmi
Yunmi Xiaomi Water Purifier component for Homeassistant.
Based on https://github.com/bit3725/homeassistant-mi-water-purifier

![Screenshot1](https://github.com/dollop80/homeassistant-xiaomi-water-purifier-yunmi/blob/master/images/screen1.PNG?raw=true)

## Installation
1. Copy *custom_components/water_purifier_yunmi/sensor.py* to **.homeassistant/custom_components/water_purifier_yunmi**.
2. Determine the IP-addres of your sensor.
3. Follow [Retrieving the Access Token](https://home-assistant.io/components/vacuum.xiaomi_miio/#retrieving-the-access-token) guide to get the token of your water purifier

## Configuration
put the following lines in your configuration.yaml
```yaml
sensor:
  - platform: water_purifier_yunmi
    host: YOUR_SENSOR_IP
    token: YOUR_SENSOR_TOKEN
    name: YOUT_SENSOR_NAME
```

put the following lines in your groups.yaml
```yaml
water_purifier:
  name: Xiaomi Water Purifier
  icon: mdi:water
  entities:
    - sensor.run_status
    - sensor.tds_in
    - sensor.tds_out
    - sensor.ppc_filter
    - sensor.ro_filter
    - sensor.cb_filter
    - sensor.temperature
    - sensor.rinse
    - sensor.water_used
    - sensor.water_purified
```

Some screen shots...
![Screenshot2](https://github.com/dollop80/homeassistant-xiaomi-water-purifier-yunmi/blob/master/images/screen2.PNG?raw=true)
![Screenshot3](https://github.com/dollop80/homeassistant-xiaomi-water-purifier-yunmi/blob/master/images/screen3.PNG?raw=true)
![Screenshot4](https://github.com/dollop80/homeassistant-xiaomi-water-purifier-yunmi/blob/master/images/screen4.PNG?raw=true)
![Screenshot5](https://github.com/dollop80/homeassistant-xiaomi-water-purifier-yunmi/blob/master/images/screen5.PNG?raw=true)