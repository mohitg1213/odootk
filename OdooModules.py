#!/usr/bin/python
# -*- coding: utf-8 -*-
import Tkinter
import ttk
import json
import tkMessageBox
import ScrolledText
from upload_module_on_webkul_store import WkModules
from tk_ac_widget import AutocompleteCombobox

class odoo_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.odoo_version_r = False
		self.module_r = False
		self.module_rt = False
		self.parent = parent
		self.initiate_class()
		# self.initialize()


	def initiate_class(self):
		self.CONFIG_DATA = self.get_config_data()
		if not self.CONFIG_DATA[1]:
			print "CONFIG_DATA NOT FOUND !!!"
			self.OnSettingClick()
		else:
			self.classInstance = WkModules(self.CONFIG_DATA[1])
			self.options = self.classInstance.get_module_lists()
			self.initialize()

	def initialize(self):
		setting_button = Tkinter.Button(self,text="Settings", command=self.OnSettingClick)
		setting_button.grid(row=0,column=1)

		newapps_button = Tkinter.Button(self,text="New Apps", command=self.OnNewAppsClick)
		newapps_button.grid(row=0,column=2)

		self.odooVersionVariable = Tkinter.StringVar()
		self.odooVersionVariable.set('Choose Odoo Version')

		# self.odooModuleVariable = Tkinter.StringVar()
		# self.odooModuleVariable.set('Choose Module...')		

		self.OdooVersionCombo = ttk.Combobox(self, textvariable=self.odooVersionVariable, values=self.options.keys())
		self.OdooVersionCombo.bind('<<ComboboxSelected>>',self.UpdateModuleList)
		Tkinter.Label(text="Select Odoo Version").grid(row=1,column=1,padx=20,pady=20)
		self.OdooVersionCombo.grid(row=1,column=2,pady=20)
		# self.OdooVersionCombo.pack(side='top', padx=10, pady=10)

		self.ModuleCombo = AutocompleteCombobox(self)
		self.ModuleCombo.bind('<<ComboboxSelected>>',self.DownloadModule)
		Tkinter.Label(text="Select Module").grid(row=4,column=1,padx=20,pady=10)
		self.ModuleCombo.grid(row=4,column=2,pady=10)

		# self.ModuleCombo.pack(side='top', padx=10, pady=10)

		button = Tkinter.Button(self,text=u"Download !!!", command=self.OnButtonClick)
		button.grid(row=6,column=2)

		quit_button = Tkinter.Button(self, text="Quit", command=self.destroy)
		quit_button.grid(row=6,column=1)
		# button.pack(side='left', padx=200, pady=20)


	def UpdateModuleList(self, event):
		self.odoo_version_r = self.OdooVersionCombo.get()
		self.ModuleCombo.set_completion_list(self.options[self.odoo_version_r].values())

	def DownloadModule(self, event):
		self.module_r = self.ModuleCombo.get()
		for m in self.options[self.odoo_version_r]:
			if self.module_r == self.options[self.odoo_version_r][m]:
				print self.options[self.odoo_version_r][m]
				self.module_rt = m

	def get_config_data(self):
		data_d = {}
		try:
			with open('app_config.json','r+') as myfile:
				data = json.load(myfile)
				for i in data:
					if i=='d_path':
						data_d[i] = str(data[i])
						continue
					data_d[i] = str(data[i]).split(",")
				for itm in data_d:
					if itm == 'd_path':
						if not data_d[itm].endswith('/'):
							data_d[itm] = data_d[itm]+"/"
					else:
						data_d[itm] = [x.endswith('/') and x or x+"/" for x in data_d[itm]]
				return [data, data_d]
		except:
			pass
		return [{}, False]

	def select_e10(self, event):
		self.e10.tag_add(Tkinter.SEL, "1.0", Tkinter.END)
		self.e10.mark_set(Tkinter.INSERT, "1.0")
		self.e10.see(Tkinter.INSERT)
		return 'break'

	def select_e9(self, event):
		self.e9.tag_add(Tkinter.SEL, "1.0", Tkinter.END)
		self.e9.mark_set(Tkinter.INSERT, "1.0")
		self.e9.see(Tkinter.INSERT)
		return 'break'

	def select_e8(self, event):
		self.e8.tag_add(Tkinter.SEL, "1.0", Tkinter.END)
		self.e8.mark_set(Tkinter.INSERT, "1.0")
		self.e8.see(Tkinter.INSERT)
		return 'break'

	def select_d_path(self, event):
		self.d_path.tag_add(Tkinter.SEL, "1.0", Tkinter.END)
		self.d_path.mark_set(Tkinter.INSERT, "1.0")
		self.d_path.see(Tkinter.INSERT)
		return 'break'

	def OnNewAppsClick(self):
		try:
			self.classInstance.GetNewModules()
			tkMessageBox.showinfo("Success :D", "DONE !!!")
		except Exception,e:
			print e
			tkMessageBox.showerror("Failed :(", "Some error has been occurred, plz contact admin or retry.")
		return True


	def OnSettingClick(self):
		data = self.CONFIG_DATA[0]
		self.toplevel = Tkinter.Toplevel()
		Tkinter.Label(self.toplevel, text="Set/Update Path for Odoo Modules:").grid(row=0,column=0,padx=5)
		Tkinter.Label(self.toplevel, text="For Odoo Version 10 :-").grid(row=1,column=0)
		self.e10 = ScrolledText.ScrolledText(self.toplevel, height=3, width=30)
		self.e10.grid(row=1,column=2,padx=5,pady=3)
		self.e10.insert(Tkinter.END, data.get('10.0',""))
		self.e10.bind("<Control-Key-a>", self.select_e10)
		
		self.e10.focus()

		Tkinter.Label(self.toplevel, text="For Odoo Version 9 :-").grid(row=2,column=0)
		self.e9 = ScrolledText.ScrolledText(self.toplevel, height=3, width=30)
		self.e9.grid(row=2,column=2,padx=5,pady=3)
		self.e9.insert(Tkinter.END, data.get('9.0',""))
		self.e9.bind("<Control-Key-a>", self.select_e9)

		Tkinter.Label(self.toplevel, text="For Odoo Version 8 :-").grid(row=3,column=0)
		self.e8 = ScrolledText.ScrolledText(self.toplevel, height=3, width=30)
		self.e8.grid(row=3,column=2,padx=5,pady=3)
		self.e8.insert(Tkinter.END, data.get('8.0',""))
		self.e8.bind("<Control-Key-a>", self.select_e8)
		
		Tkinter.Label(self.toplevel, text="Set/Update Path for Download:").grid(row=4,column=0)
		self.d_path = ScrolledText.ScrolledText(self.toplevel, height=3, width=50)
		self.d_path.grid(row=5,column=0,padx=5,pady=3, columnspan=3)
		self.d_path.insert(Tkinter.END, data.get('d_path',""))
		self.d_path.bind("<Control-Key-a>", self.select_d_path)

		save_button = Tkinter.Button(self.toplevel,text="SAVE", command=self.OnSaveClick)
		save_button.grid(row=7,column=1)

	def OnSaveClick(self):
		temp = {}
		temp['d_path'] = (self.d_path.get(1.0, Tkinter.END)).strip()
		temp['8.0'] = (self.e8.get(1.0, Tkinter.END)).strip()
		temp['9.0'] = (self.e9.get(1.0, Tkinter.END)).strip()
		temp['10.0'] = (self.e10.get(1.0, Tkinter.END)).strip()
		if not (temp['d_path'] and temp['8.0'] and temp['9.0'] and temp['10.0']):
			tkMessageBox.showwarning("Warning :|", "All Fields are mandatory !!!")
			return False
		print temp
		json.dump(temp, open("app_config.json",'w+'))
		# with open('app_config.py','w+') as myfile:
		# 	myfile.writelines(temp)
		if not self.CONFIG_DATA[1]:
			self.destroy()
		else:
			self.toplevel.destroy()

	def OnButtonClick(self):
		if not self.odoo_version_r:
			tkMessageBox.showwarning("Warning :|", "Select Odoo Version first.")
			return False
		if not self.module_r:
			tkMessageBox.showwarning("Warning :|", "Select Module you want to Download.")
			return False
		try:
			self.classInstance.main(self.module_rt, self.odoo_version_r)
			tkMessageBox.showinfo("Success :D", "DONE !!!")
		except Exception,e:
			print e
			tkMessageBox.showerror("Failed :(", "Some error has been occurred, plz contact admin or retry.")
		return True


if __name__ == "__main__":
	# print get_module_lists()
	import sys
	app = odoo_tk(None)
	app.title('Download Odoo Module')
	if sys.platform == "linux2":
		app.iconbitmap('@icon.xbm')
	else:
		app.iconbitmap('@icon.ico')
	app.geometry("%dx%d+%d+%d" % (380, 180, 200, 150))
	app.mainloop()
	# print dir(tkMessageBox)