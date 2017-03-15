import sys
import os
import Tkinter
import ttk

class AutocompleteCombobox(ttk.Combobox):
	
	def set_completion_list(self, completion_list):
		self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
		self._hits = []
		self._hit_index = 0
		self.position = 0
		self.bind('<KeyRelease>', self.handle_keyrelease)
		self.bind("<Control-Key-a>", self.select_all)
		self['values'] = self._completion_list  # Setup our popup menu

	def select_all(self, event):
		self.select_range(0, Tkinter.END)
		return 'break'

	def autocomplete(self, delta=0):
		if delta:
			self.delete(self.position, Tkinter.END)
		else:
			self.position = len(self.get())
		_hits = []
		for element in self._completion_list:
			if element.lower().startswith(self.get().lower()): # Match case insensitively
				_hits.append(element)
		if _hits != self._hits:
			self._hit_index = 0
			self._hits=_hits
		if _hits == self._hits and self._hits:
			self._hit_index = (self._hit_index + delta) % len(self._hits)
		if self._hits:
			self.delete(0,Tkinter.END)
			self.insert(0,self._hits[self._hit_index])
			self.select_range(self.position,Tkinter.END)

	def handle_keyrelease(self, event):
		if event.keysym == "BackSpace":
			self.delete(self.index(Tkinter.INSERT), Tkinter.END)
			self.position = self.index(Tkinter.END)
		if event.keysym == "Left":
			if self.position < self.index(Tkinter.END): # delete the selection
				self.delete(self.position, Tkinter.END)
			else:
				self.position = self.position-1 # delete one character
				self.delete(self.position, Tkinter.END)
		if event.keysym == "Right":
			self.position = self.index(Tkinter.END) # go to end (no selection)
		if len(event.keysym) == 1:
			self.autocomplete()