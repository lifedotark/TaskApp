from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton
from kivy.event import EventDispatcher
from task import Task
import uuid
import math
import data
import time

class AccordionTask(AccordionItem, Task):
	pass

class FullScreenLayout(GridLayout):
	unique_id = StringProperty("");
	name = StringProperty("");
	date = StringProperty("");
	value = StringProperty("");
	attributes = StringProperty("");

class ListTask(ListItemButton, Task):
	selected_color = ListProperty()
	deselected_color = ListProperty()

class TaskBoard(GridLayout):
	last_tasks = ObjectProperty(None)
	task_open_list = ObjectProperty(None)
	task_finished_list = ObjectProperty(None)
	options_manager = ObjectProperty(None)
	screen_manager = ObjectProperty(None)
	title_input = ObjectProperty(None)
	value_input = ObjectProperty(None)
	full_screen = ObjectProperty(None)
	origin_screen = StringProperty("")
	current_task_uuid = StringProperty("")
	text = "There's no tasks here =/\n Go and add some Tasks!"
	
	def update_tasks(self):
		self.registros = data.retrieve_data(size=5,attr='opened')

	def load_task_list(self, attribute,task_list,selected_color, deselected_color, empty_message="There's no tasks here =/"):
		dados = data.retrieve_data(attr=attribute)
		if len(dados) == 0:
			task_list.add_widget(Label(text=empty_message))
		else:
			for c in task_list.children:
				 if type(c).__name__ == 'Label':
				 	task_list.remove_widget(c)
			

		item_args_converter = lambda row_index, obj:{'name':'[b][size=16]' + obj.name + '[/size][/b]',
										'date': '[i]' + obj.date + '[/i]',
										'value': obj.value[:60] + '...',
										'selected_color' : selected_color,
										'deselected_color' : deselected_color,
										'size_hint_y': None,
										'screen_manager': self.screen_manager,
										'task_board':self,
										'task_parent': obj,
										'height':150,
										'is_selected':False,
										'markup':True}

		list_adapter = ListAdapter(data=dados,
									args_converter = item_args_converter,
									selection_mode = 'single',
									propagate_selection_to_data=False,
									allow_empty_selection=False,
									cls=ListTask)
		task_list.adapter = list_adapter

	def load_open_tasks_page(self):
		self.load_task_list('opened',self.task_open_list,[.2,.4,.6, 1], [.9, 1, 0, 1], self.text)

	def load_finished_task_page(self):
		self.load_task_list('closed',self.task_finished_list, [.66,.67,.1, 1], [.65, .49, .24, 1])		

	def load_last_tasks_page(self):
		dados = data.retrieve_data(size=5,attr='opened')
		self.last_tasks.clear_widgets()

		if len(dados) == 0:
			self.last_tasks.parent.add_widget(Label(text=self.text))

		for r in dados[0:5]:
			task = AccordionTask()
			task.task_parent = r
			task.unique_id = r.unique_id
			task.name = r.name
			task.date = r.date
			task.value = r.value
			task.attributes = r.attributes
			task.screen_manager = self.screen_manager
			task.full_screen = self.full_screen
			task.task_board = self
			self.last_tasks.add_widget(task)

	def go_home(self):
		self.screen_manager.current = 'Last Tasks'
		self.update_tasks()
		self.load_last_tasks_page()

	def go_back_screen(self, task_list=None):
		self.clear_create()
		self.screen_manager.current = self.origin_screen

	def clear_create(self):
		self.value_input.focus = False
		self.value_input.text = ""
		self.title_input.focus = False
		self.title_input.text = ""
		self.current_task_uuid = ""

	def save_task(self, uuid_value=None, attr='opened', go_back_screen=False):
		if uuid_value != None:
			self.current_task_uuid = uuid_value
			task = data.retrieve_data(uuid_value)
			value = task.value
			title = task.name
		else:
			value = self.value_input.text.strip()
			title = self.title_input.text.strip()		

		if len(value) <= 0:
			return;

		if len(title) <= 0:
			title = value[0:30] + "..."

		if self.current_task_uuid == "":
			self.current_task_uuid = str(uuid.uuid4())

		data.create_data(self.current_task_uuid,title,time.strftime("%H:%M:%S %d/%m/%Y"),value,attr)
		
		self.clear_create()

		if go_back_screen:
			self.go_back_screen()
		else:
			self.go_home()

	def go_edit_task(self, uuid_value):
		self.screen_manager.current = 'Add New'
		task = data.retrieve_data(uuid_value)
		self.title_input.text = task.name
		self.value_input.text = task.value
		self.current_task_uuid = uuid_value

	def go_delete_task(self,uuid_value):
		data.delete_data(uuid_value)
		self.update_tasks()
		self.go_home()

class TaskApp(App):
    def build(self):
    	t = TaskBoard()
    	t.update_tasks()
    	t.load_last_tasks_page();
    	return t

TaskApp().run()