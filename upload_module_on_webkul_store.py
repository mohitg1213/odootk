import os
import ast
from sys import exit
from zipme import zip_folder
SKIP_MODULES 	= ['.git']
DUMMY_URLS		= ['https://store.webkul.com/Odoo.html']

CHECK			= ["", "https://store.webkul.com", "http://www.webkul.com"]

class WkModules():
	def __init__(self, c_data):
		self.generate_here 	= c_data.pop('d_path')
		self.modules_dir 	= c_data

	def get_module_lists(self):
		odoo_modules   = {'8.0':{}, '9.0':{}, '10.0':{}}
		for odoo_version in odoo_modules.keys():
			for md in self.modules_dir[odoo_version]:
				for root, dirs, files in os.walk(md):
					for module in dirs:
						if module in SKIP_MODULES:
								continue
						if os.path.exists(root+os.sep+module+'/__openerp__.py'):
								file_path = root+os.sep+module+'/__openerp__.py'
						elif os.path.exists(root+os.sep+module+'/__manifest__.py'):
							file_path = root+os.sep+module+'/__manifest__.py'
						with open(file_path, "r") as myfile:
							module_data = ast.literal_eval(myfile.read())
							odoo_modules[odoo_version][module] = module_data['name']
					break
		return odoo_modules

	def get_webkul_modules(self, odoo_version):
		temp_list = []
		for md in self.modules_dir[odoo_version]:
			for root, dirs, files in os.walk(md):
				for module in dirs:
					if module in SKIP_MODULES:
							continue
					temp_list.append(module)
				break
		return temp_list

	def get_result(self, mDownload, odoo_version):
		WEBKUL_MODULES 	= self.get_webkul_modules(odoo_version)
		TAR_NAME	   	= "__Extract-Me__%s_for_odoo_v%s.zip"%(mDownload, odoo_version.split(".")[0])
		result = {'module_to_zip':[],'module_dependency':[],'paid_modules':[]}
		result['tar_name'] = TAR_NAME
		for md in self.modules_dir[odoo_version]:
			for root, dirs, files in os.walk(md):
				for module in dirs:
					if module in SKIP_MODULES:
							continue
					if module == mDownload:
						flag = True
						if os.path.exists(root+os.sep+module+'/__openerp__.py'):
							file_path = root+os.sep+module+'/__openerp__.py'
						elif os.path.exists(root+os.sep+module+'/__manifest__.py'):
							file_path = root+os.sep+module+'/__manifest__.py'
						with open(file_path, "r") as myfile:
							module_data = ast.literal_eval(myfile.read())
							result['module'] = module
							result['module_name'] = module_data["name"]
							result['module_price'] = module_data.get("price")
							result['blog_link'] = module_data.get("description")
							if module_data.get("depends"):
								result['module_dependency'] = list(set(module_data["depends"]).intersection(WEBKUL_MODULES))
						result['module_to_zip'].append(root+os.sep+module)
				break
		return result

	def main(self, MODULE_TO_DOWNLOAD, VERSION):
		RESULT = self.get_result(MODULE_TO_DOWNLOAD, VERSION)
		if not RESULT:
			print "Module(%s) not found for Odoo version(%s) in Given Directories."%(MODULE_TO_DOWNLOAD, VERSION)
			exit(1)
		if RESULT.has_key('module_dependency') and len(RESULT['module_dependency']):
			module_dependency = RESULT['module_dependency']
			while(module_dependency):
				temp = []
				for dependency in module_dependency:
					response = self.get_result(dependency, VERSION)
					if not response:
						print "Module(%s) not found for Odoo version(%s) in Given Directories."%(dependency, VERSION)
						exit(1)
					if not response.has_key('module_price') or not response['module_price']:
						RESULT['module_to_zip'].extend(response['module_to_zip'])
						temp.extend(response['module_dependency'])
					else:
						RESULT['paid_modules'].append(response['module_name']+"("+response['module']+")")
				module_dependency = temp
		zip_folder(RESULT['module_to_zip'] , self.generate_here+RESULT['tar_name'])
		print "DONE"

		with open(self.generate_here+RESULT['module']+".txt", "w+") as myfile:
			myfile.write("Product Name\t:-\t%s"%RESULT["module_name"])
			myfile.write("\n")
			myfile.write("Price\t\t\t:-\t%s $"%RESULT["module_price"])
			myfile.write("\n")
			myfile.write("Blog Link\t\t:-\t%s"%RESULT["blog_link"])
			myfile.write("\n")
			myfile.write("Store Link\t\t:-\t")
			myfile.write("\n")
			myfile.write("Screenshots\t\t:-\tPFA")
			myfile.write("\n")
			myfile.write("Thumbnail\t\t:-\tPFA")
			myfile.write("\n")
			myfile.write("Module Zip\t\t:-\tPFA")
			myfile.write("\n")
			myfile.write("Category\t\t:-\t")
			myfile.write("\n")
			myfile.write("Odoo Version\t:-\t%s"%VERSION)
			myfile.write("\n")
			if RESULT["paid_modules"]:
				myfile.write("Add Note\t\t:-\tNote: Module is dependent on %s."%RESULT["paid_modules"])
				myfile.write("\n")
			myfile.write("Features\t\t:-")
			myfile.write("\n\n\n\n")
			myfile.write("Description\t\t:-")
			myfile.write("\n\n\n\n")
		return RESULT

	def GetNewModules(self):
		DATA 			= ['Module Name, Supported Versions, Store Link, Blog Link, Demo Link, Price, Module Technical Name, Category, Module Version']
		ALL_NEW_MODULES = {}
		for odoo_version in ['10.0', '9.0']:
			for md in self.modules_dir[odoo_version]:
				for root, dirs, files in os.walk(md):
					for module in dirs:
						if module in SKIP_MODULES:
								continue
						if os.path.exists(root+os.sep+module+'/__openerp__.py'):
							file_path = root+os.sep+module+'/__openerp__.py'
						elif os.path.exists(root+os.sep+module+'/__manifest__.py'):
							file_path = root+os.sep+module+'/__manifest__.py'
						with open(file_path, "r") as myfile:
							module_data = ast.literal_eval(myfile.read())
							store_url = module_data.get('website','')
							if store_url not in CHECK or store_url in DUMMY_URLS:
								continue
							if not ALL_NEW_MODULES.has_key(module):
								ALL_NEW_MODULES[module] = {
									'module_tech_name': module,
									'module_name': module_data.get("name"),
									'odoo_version': [odoo_version],
									'module_version': module_data.get("version"),
									'store_link': module_data.get("website"),
									'blog_link': module_data.get("description"),
									'demo_link': module_data.get("live_test_url"),
									'odoo_price': module_data.get("price"),
									'category': module_data.get("category"),
								}
							else:
								ALL_NEW_MODULES[module]['odoo_version'].append(odoo_version)
					break
		for key,item in ALL_NEW_MODULES.items():
			mod_str = ""
			mod_str += ', '.join([str(i) for i in [item.get('module_name',''), \
					" & ".join(item.get('odoo_version',[])), item.get('store_link',''), item.get('blog_link',''), \
					item.get('demo_link',''), item.get('odoo_price',''), \
					item.get('module_tech_name',''), item.get('category',''), item.get('module_version',''), ]])
			DATA.append(mod_str)
		with open(self.generate_here+'ODOO_NEW_APPS'+".ods", "w+") as myfile:
			for row in DATA:
				myfile.write(row)
				myfile.write("\n")
		return True

if __name__=="__main__":
	from myconfig import CONFIG_DATA
	MODULE_TO_DOWNLOAD 	= 'amazon_odoo_bridge'
	VERSION				= "10.0"
	Class_obj = WkModules(CONFIG_DATA)
	Class_obj.GetNewModules()
	# RESULT = Class_obj.main(MODULE_TO_DOWNLOAD, VERSION)
	# print RESULT