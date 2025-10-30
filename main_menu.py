import arts, plants, logbook, supplier
logbookdic = {}
projectdic = {}
supplierdic = {}
blacklisted = [] # contains supplier ID

#load from files
logbook.loadProjects(projectdic)
logbook.loadSuppliers(supplierdic)
logbook.loadLog(logbookdic)

#get blacklisted suppliers from logbook
for log in logbookdic:
	if logbookdic[log]["action"] == "blacklist_supplier":
		blacklisted.append(logbookdic[log]["supplier_id"])

while True:
	print(arts.name)
	print()
	print("Hello!")
	print("What would you like to do?")
	print()
	
	print("\t[1] Project Section")
	print("\t[2] Supplier Section")
	print("\t[3] Logbook Section")
	print("\t[0] Exit")
	print()

	choice = input("Choice: ")
	print()
	
	if choice == "1":
		plants.menu(projectdic,supplierdic,logbookdic, blacklisted)
	elif choice == "2":
		supplier.menu(supplierdic, logbookdic)
	elif choice == "3":
		logbook.menu(projectdic, supplierdic, logbookdic)
	elif choice == "0":
		print("I hope you had a nice experience. Goodbye!")
		break
	else:
		print("Invalid choice.")
		print()
    
        