import logging
import asyncio

from config import ConfigurationReader

class SensorsController():
	_events_initialized = False
	_loop = None

	
	def __init__(self, message_manager_f):
		self._message_manager = message_manager_f
		self.enable_sensors()


	def enable_sensors(self):
		try:
			import RPi.GPIO as gpio
			if self._events_initialized == False :
				self._events_initialized = True
				#Define raspberry gpio input/output
				gpio.setmode(gpio.BCM)
				if int(ConfigurationReader._infrared_sensor_pin) > 0 :
					gpio.setup(ConfigurationReader._infrared_sensor_pin, gpio.IN)
					gpio.add_event_detect(ConfigurationReader._infrared_sensor_pin, gpio.RISING, callback=self.motion_detection_event, bouncetime=500)
				if ConfigurationReader._sound_sensor_pin > 0 :
					gpio.setup(ConfigurationReader._sound_sensor_pin, gpio.IN)
					gpio.add_event_detect(ConfigurationReader._sound_sensor_pin, gpio.RISING, callback=self.sound_detection_event, bouncetime=500)
				logging.info("Sensors enabled!")
				asyncio.async(self._message_manager("Started..."))
				# run the event loop
				self._loop = asyncio.get_event_loop()
				self._loop.run_forever()
				self._loop.close()
		except ImportError:
			logging.error("No GPIO library found! Sensors are not enabled!")
			self.sensor_error(message_manager_f, "🚫 No GPIO library found! Sensors are not enabled! 🚫")


	def motion_detection_event(self, channel):
		print("Motion")
		if self._loop is None:
			print(":(")
			return
		# this enqueues a call to message_manager_f() 
		self._loop.call_soon_threadsafe(self._message_manager("🚨Motion detected in '" + ConfigurationReader._alias + "'!  "))
		print("---")


	def sound_detection_event(self, channel):
		print("Sound!")
		if self._loop is None:
			print(":(")
			return
		# this enqueues a call to message_manager_f() 
		self._loop.call_soon_threadsafe(self._message_manager("🚨Motion detected in '" + ConfigurationReader._alias+  "'!  "))
		print("---")

			
	def motion_sensor(self):
		print("Motion")
		event_loop = asyncio.get_event_loop()
		try:
			event_loop.run_until_complete(self._message_manager("🚨Motion detected in '" + ConfigurationReader._alias + "'!  "))
		finally:
			event_loop.close()
		#asyncio.async(self._message_manager("🚨Motion detected in '" + ConfigurationReader._alias + "'! 🚨"))
		print("---")


	def sound_sensor(self):
		print("Sound!")
		event_loop = asyncio.get_event_loop()
		try:
			event_loop.run_until_complete(self._message_manager("🚨Motion detected in '" + ConfigurationReader._alias + "'!   "))
		finally:
			event_loop.close()
		#asyncio.async(self._message_manager("📢 Sound detected in '" + ConfigurationReader._alias + "'! 📢"))
		print("---")

		
	def sensor_started(self):
		asyncio.async(self._message_manager("Enabling node '" + ConfigurationReader._alias + "' 🏁"))

		
	def sensor_error(self, message):
		asyncio.async(self._message_manager(message))
