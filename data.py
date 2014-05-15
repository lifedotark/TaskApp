from kivy.storage.jsonstore import JsonStore
from task import Task
import json

file_name = "tasks.json"

store = JsonStore(file_name)

def retrieve_data(uuid_value=None, attr=None, size=0):
	if uuid_value != None:
		reg = store.get(uuid_value);
		if reg == None:
			return None
		task = Task()
		task.unique_id = uuid_value
		task.name = reg["name"]
		task.date = reg["date"]
		task.value = reg["value"]
		task.attributes = reg["attributes"]
		return task
	else:
		registros = []
		counter = 0
		for key in store:
			reg = store.get(key)
			if attr != None and reg["attributes"] != attr:
				continue
			task = Task()
			task.unique_id = key
			task.name = reg["name"]
			task.date = reg["date"]
			task.value = reg["value"]
			task.attributes = reg["attributes"]
			registros.append(task)
			if size != 0 and counter >= 5:
				break;
			counter+=1

		registros.reverse()
		return registros

def delete_data(uuid_key):
	store.delete(uuid_key)

def create_data(uuid_key, name, date, value, attributes):
	if store.exists(uuid_key):
		delete_data(uuid_key)
	store.put(uuid_key, name=name, date=date, value=value, attributes=attributes)

