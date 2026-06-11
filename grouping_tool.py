import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from PIL import Image, ImageTk



# ---------- Globals ----------


root = tk.Tk()
root.title("Stormworks Vehicle Grouping Tool")
root.geometry("850x550")
if Path("stormworks_grouping_tool.ico").exists():
	root.iconbitmap("stormworks_grouping_tool.ico")

SAVE_PATH = ""
SHOP_PATH = ""
dir,savexml,vlist,vimages,vlistcheck,vlistselectall,vlistgroup,glist = None,None,[],[],[],None,{},[]
selectedGroup = tk.StringVar(value="Default")
filteredgroup = None
vehicleZone, groupZone = None,None



# ---------- Functions ----------



def sequence(methods):
	def doAllOf(m): 
		for i in m: i()
	
	return lambda:doAllOf(methods)

def runwith(method,param):
	return lambda: method(param)

def createScrollable(master,width,height,color=None):
	container = tk.Frame(master,width=width,height=height,bg=color)

	canvas = tk.Canvas(container,bg=color,width=width,height=height)

	canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event:canvas.yview_scroll(int(-event.delta / 120), "units")))
	canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


	scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
	scrollbar.pack(side="right", fill="y")

	scrollable_frame = tk.Frame(canvas,bg=color)
	scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

	canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
	canvas.configure(yscrollcommand=scrollbar.set)
	canvas.pack(anchor="nw")

	return container, scrollable_frame, canvas, scrollbar

def resetRoot():
	for widget in root.winfo_children(): 
		widget.destroy()



def assignButtonBehavior():
	value = selectedGroup.get()
	if value=="Default": value=None
	for i in range(len(vlist)):
		if vlistcheck[i].get() and testWithFilter(i): vlistgroup[i]=value
	displayVehicles(vehicleZone)

def filterButtonBehavior():
	global filteredgroup
	filteredgroup = selectedGroup.get()
	displayVehicles(vehicleZone)

def defilterButtonBehavior():
	global filteredgroup
	filteredgroup = None
	displayVehicles(vehicleZone)

def writeGroupingToSaveFiles():
	groupingData = ""
	for g in glist:
		groupingData+=f"\t\t\t<g name=\"{g}\">\n\t\t\t\t<filenames>\n"
		for i in range(len(vlist)):
			if vlistgroup.get(i,None)==g:
				if vlist[i].is_file():
					groupingData+=f"\t\t\t\t\t<f value=\"{vlist[i].name[:-4]}\"/>\n"
				else:
					groupingData+=f"\t\t\t\t\t<f value=\"{vlist[i].name}\"/>\n"

		groupingData+="\t\t\t\t</filenames>\n\t\t\t</g>\n"
	text = savexml.read_text()
	savexml.write_text(text[:(text.index("<vehicle_groups>")+17)]+groupingData+text[(text.index("</vehicle_groups>")-2):])

def commandSelectAll():
	for i in range(len(vlist)): vlistcheck[i].set(vlistselectall.get() and testWithFilter(i))

def testWithFilter(i):
	if filteredgroup!=None and filteredgroup!=vlistgroup.get(i,"Default"): return False

	return True

def displayVehicles(zone):
	for i in zone.winfo_children(): i.destroy()
	for i in range(len(vlist)):
		if not testWithFilter(i):continue
		if vlist[i].is_file():
			tk.Checkbutton(zone, text=vlist[i].name[:-4], variable=vlistcheck[i]).grid(row=i, column=1, sticky="w")
			tk.Button(zone,text=" 🖉 ",command=runwith(renameVehicle,i)).grid(row=i, column=2, sticky="w")
		else:
			tk.Checkbutton(zone, text=vlist[i].name, variable=vlistcheck[i]).grid(row=i, column=1, sticky="w")

		if vlistgroup.get(i,None) != None:
			tk.Label(zone,text=vlistgroup.get(i," ")).grid(row=i,column=3, sticky="w")



def groupBumpUp(name):
	try: i = glist.index(name)
	except: return
	if i<1: return

	temp = glist[i-1]
	glist[i-1] = glist[i]
	glist[i] = temp
	displayGroups(groupZone)

def groupMergeUp(name):
	try: i = glist.index(name)
	except: return
	if i<1: return

	for k,v in vlistgroup.items():
		if v==name: vlistgroup[k]=glist[i-1]
	
	glist.remove(name)
	displayGroups(groupZone)
	displayVehicles(vehicleZone)

def groupBumpDown(name):
	try: i = glist.index(name)
	except: return
	if i>=len(glist)-1: return

	temp = glist[i+1]
	glist[i+1] = glist[i]
	glist[i] = temp
	displayGroups(groupZone)

def groupRename(name):
	popup = tk.Toplevel(root)
	popup.title(f"Rename \"{name}\"")
	popup.geometry("350x80")
	renametextvar = tk.StringVar(value=str(name))
	error = tk.Label(popup,text="")
	tk.Button(popup,text="Cancel",command=lambda:popup.destroy()).pack(side="right")
	tk.Button(popup,text="Rename",command=runwith(finishRenamingGroup,(name,renametextvar,popup,error))).pack(side="right")
	tk.Entry(popup,textvariable=renametextvar).pack(side="left",expand=True,fill="x")
	error.pack(side="bottom",expand=True,fill="x")

def finishRenamingGroup(info):
	old,new,popup,error = info[0],info[1].get(),info[2],info[3]
	try: 
		i = glist.index(old)
	except: 
		error.configure(text="Could not find original")
		return
	try: 
		glist.index(new)
		error.configure(text="Name already in use")
		return
	except: pass

	glist[i]=new
	for k,v in vlistgroup.items():
		if v==old: vlistgroup[k]=new

	popup.destroy()
	displayGroups(groupZone)
	displayVehicles(vehicleZone)

def groupDelete(name):
	popup = tk.Toplevel(root)
	popup.title(f"Delete \"{name}\"")
	popup.geometry("350x80")
	error = tk.Label(popup,text="")
	count=0
	for _,v in vlistgroup.items():
		if v==name: count+=1

	tk.Button(popup,text="Cancel",command=lambda:popup.destroy()).pack(side="right")
	tk.Button(popup,text="Delete",command=runwith(finishDeletingGroup,(name,popup,error))).pack(side="right")
	tk.Label(popup,text=f"\"{name}\" has {count} Vehicles").pack(side="left",expand=True,fill="x")
	error.pack(side="bottom",expand=True,fill="x")

def finishDeletingGroup(info):
	old,popup,error = info[0],info[1],info[2]
	try: i = glist.index(old)
	except: error.configure(text="Could not find original"); return

	glist.remove(old)
	for k,v in vlistgroup.items():
		if v==old: vlistgroup[k]=None

	popup.destroy()
	displayGroups(groupZone)
	displayVehicles(vehicleZone)

def groupCreateNew():
	glist.append(f"Group {len(glist)+1}")
	displayGroups(groupZone)
		  
def displayGroups(zone):
	for i in zone.winfo_children(): i.destroy()
	tk.Radiobutton(zone,text="Default",value="Default",variable=selectedGroup).grid(row=1,column=0,sticky="w")
	tk.Button(zone,text=" + ",	command=groupCreateNew).grid(row=1,column=5,sticky="e")
	row = 1
	for i in glist: 
		row+=1; 
		tk.Radiobutton(zone,text=i,value=i,variable=selectedGroup).grid(row=row,column=0,sticky="w")
		tk.Button(zone,text=" 🖉 ",	command=runwith(groupRename  ,i)).grid(row=row,column=1,sticky="e")
		tk.Button(zone,text=" ⇑ ",	command=runwith(groupBumpUp  ,i)).grid(row=row,column=2,sticky="e")
		tk.Button(zone,text=" ⇓ ",	command=runwith(groupBumpDown,i)).grid(row=row,column=3,sticky="e")
		tk.Button(zone,text=" ↰ ",	command=runwith(groupMergeUp,i)).grid(row=row,column=4,sticky="e")
		tk.Button(zone,text=" 🗑 ",	command=runwith(groupDelete,i)).grid(row=row,column=5,sticky="e")

def renameVehicle(i):
	name = vlist[i].name[:-4]
	popup = tk.Toplevel(root)
	popup.title(f"Rename \"{name}\"")
	popup.geometry("350x80")
	renametextvar = tk.StringVar(value=str(name))
	error = tk.Label(popup,text="")
	tk.Button(popup,text="Cancel",command=lambda:popup.destroy()).pack(side="right")
	tk.Button(popup,text="Rename",command=runwith(finishRenamingVehicle,(name,renametextvar,popup,error,i))).pack(side="right")
	tk.Entry(popup,textvariable=renametextvar).pack(side="left",expand=True,fill="x")
	error.pack(side="bottom",expand=True,fill="x")

def finishRenamingVehicle(info):
	old,new,popup,error,i = info[0],info[1].get(),info[2],info[3],info[4]
	
	if old==new+".xml":
		error.configure(text="No change detected")
		return
	
	for v in vlist:
		if v.name==new+".xml":
			error.configure(text="Name already in use")
			return
	
	p = Path(f"{SAVE_PATH}/data/vehicles/{old}.xml")
	if p.exists(): p.rename(f"{SAVE_PATH}/data/vehicles/{new}.xml")
	vlist[i]=Path(f"{SAVE_PATH}/data/vehicles/{new}.xml")
	p = Path(f"{SAVE_PATH}/data/vehicles/{old}.png")
	if p.exists(): p.rename(f"{SAVE_PATH}/data/vehicles/{new}.png")
	p = Path(f"{SAVE_PATH}/data/vehicles/{old}")
	if p.exists(): p.rename(f"{SAVE_PATH}/data/vehicles/{new}")


	popup.destroy()
	displayVehicles(vehicleZone)

def loadData():
	global dir,savexml,vlist,vlistcheck,vlistselectall,vlistgroup,glist


	try:
		dir = Path(SAVE_PATH)
	except Exception as e:
		return (False,f"Error while accessing location", e)
	if not dir.is_dir(): return (False,f"Expected a file folder but did not recieve\n(exists: {dir.exists()}; is_file: {dir.is_file()})")


	vlist = []
	for i in sorted(Path(SAVE_PATH+"/data/vehicles").iterdir()):
		if i.is_file() and i.name[-4:]==".xml":
			vlist.append(i)
	for i in sorted(Path(SHOP_PATH).iterdir()):
		if i.is_dir():
			vlist.append(i)


	vlistcheck = []
	if len(vlist)==0: return (False,f"Found no vehicle save files")
	for _ in vlist: vlistcheck.append(tk.BooleanVar())
	vlistselectall = tk.BooleanVar()


	savexml = Path(SAVE_PATH+"/save.xml")
	if not savexml.exists(): return (False,f"Could not find save.xml")
	txt = savexml.read_text()
	txt = txt[txt.index("<vehicle_groups>")+16:txt.index("</vehicle_groups>")].replace("\t","").splitlines()
	vlistgroup={}
	glist=[]
	for line in txt:
		if line[:9]=="<g name=\"":
			glist.append(line[9:-2])
		if line[:10]=="<f value=\"":
			filename = line[10:-3]
			for i in range(len(vlist)):
				if vlist[i].name==filename or vlist[i].name==filename+".xml":
					vlistgroup[i]=glist[len(glist)-1]


	return (True, "Loaded data without exception")



def formEditor():
	resetRoot()
	global vehicleZone,groupZone
	
	actionbar = tk.Frame(root,width=700,height=30,bg="gray")
	actionbar.grid(row=0,column=0,columnspan=2,sticky="nw")

	tk.Checkbutton(actionbar,text="All",variable=vlistselectall,command=commandSelectAll).pack(side="left")
	tk.Button(actionbar,text="Assign"  ,command=  assignButtonBehavior).pack(side="left")
	tk.Button(actionbar,text="Filter"  ,command=  filterButtonBehavior).pack(side="left")
	tk.Button(actionbar,text="Defilter",command=defilterButtonBehavior).pack(side="left")
	tk.Button(actionbar,text="Refresh" ,command=formEditor).pack(side="left")
	tk.Button(actionbar,text="Read"    ,command=lambda: formEditor() if loadData()[0] else 0).pack(side="left")
	tk.Button(actionbar,text="Write"   ,command=writeGroupingToSaveFiles).pack(side="left")

	vContain,vehicleZone,_,_ = createScrollable(root,500,root.winfo_height()-30)
	vContain.grid(row=1,column=0,sticky="nw")
	displayVehicles(vehicleZone)
	
	
	
	gContain,groupZone,_,_ = createScrollable(root,root.winfo_width()-550,root.winfo_height()-30)
	gContain.grid(row=1,column=1,sticky="nw")
	displayGroups(groupZone)
	


def selectorExit(param):
	global SAVE_PATH,SHOP_PATH;
	
	if param[0]:
		SAVE_PATH=f"C:\\Users\\{param[0]}\\AppData\\Roaming\\Stormworks";
	else:
		SAVE_PATH=filedialog.askdirectory(title="Select Stormworks AppData Folder")
	
	SHOP_PATH = param[1].get()

	l=loadData();print(l);
	if l[0]:formEditor() 
	else:tk.Label(root, text=l[1]).pack(pady=(10, 0))
		
def formSelector():
	resetRoot()
	tk.Label(root, text="Select User:").pack(pady=(10, 0))
	textvariable = tk.StringVar(value="C:/Program Files (x86)/Steam/steamapps/workshop/content/573090")
	button_frame = tk.Frame(root)
	button_frame.pack(pady=5)

	for user in sorted(Path("C:/Users").iterdir()):
		user=str(user)[9:]
		if user in ("Public","All Users","Default","Default User","desktop.ini"): continue
		
		tk.Button(button_frame, text=f"User: {user}",bg="white",command=runwith(selectorExit,(user,textvariable))).pack(side=tk.LEFT, padx=5)
	tk.Button(button_frame, text=f"Custom Path",bg="white",command=runwith(selectorExit,(False,textvariable))).pack(side=tk.LEFT, padx=5)

	tk.Label(root,text="Author: ForzaMeccanica;   Version: 1.0.1;  Github:").pack(side="top")

	tk.Entry(root,textvariable=textvariable).pack(anchor="n",expand=True,fill="x",padx=5,pady=5)



# ---------- Startup ----------



root.update()

formSelector()

root.mainloop()