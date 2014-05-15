from kivy.properties import StringProperty, ObjectProperty
from kivy.event import EventDispatcher

class Task(EventDispatcher):
	unique_id = StringProperty("None")
	name = StringProperty("None")
	date = StringProperty("None")
	value = StringProperty("None")
	attributes = StringProperty("")
	task_board = ObjectProperty(None)
	screen_manager = ObjectProperty(None)
	task_parent = ObjectProperty(None)

	def load_fullscreen_task(self, task):
		self.task_board.origin_screen = self.screen_manager.current

		self.screen_manager.current = 'FullScreen'
		self.task_board.full_screen.unique_id = task.unique_id
		self.task_board.full_screen.name = task.name
		self.task_board.full_screen.date = task.date
		self.task_board.full_screen.value = task.value
		self.task_board.full_screen.attributes = task.attributes