# AutoWateringPi
Using a Raspberry Pi in conjunction with moisture sensors to automatically water plants.
Currently can read analog moisture data and submit it to a MySQL Server the user defines with the percentage of moisture and the datetime it was recorded.
It is designed to run as a cronjob and periodically decide if the moisture level in the soil is low enough to water a plant.

Long-Term Plans(In No Specific Order):
Add detailed instructions on the hardware side.
Draw diagrams for those looking into the project to better understand.
Allow functionality to run a 3v DC motor for a predetermined period of time for watering.

Lofty Goals:
Apply machine learning in conjunction with data analytics to determine the period of time in which to water dynamically over time to maximize growth.
 
