import arts, logbook

def menu(supplierdic, logbookdic):
    while True:
        print(arts.suppliers)
        print()
        print("\t[1] Add Supplier")
        print("\t[2] Add Project Type")
        print("\t[3] Remove Project Type")
        print("\t[4] Add Service Provided")
        print("\t[5] Remove Service Provided")
        print("\t[6] View Supplier")
        print("\t[7] View All Suppliers")
        print("\t[0] Exit")
        print()

        choice = input("Choice: ")
        if choice == "1":
            addSupplier(supplierdic, logbookdic)
        elif choice == "2":
            addProjectTypes(supplierdic, logbookdic)
        elif choice == "3":
            removeProjectTypes(supplierdic, logbookdic)
        elif choice == "4":
            addServiceProvided(supplierdic, logbookdic)
        elif choice == "5":
            removeServiceProvided(supplierdic, logbookdic)
        elif choice == "6":
            viewSupplier(supplierdic)
        elif choice == "7":
            viewAllSuppliers(supplierdic)
        elif choice == "0":
            print("Going back to main menu...")
            print()
            break
        else:
            print("Invalid choice. Try again.")

def addSupplier(supplierdic, logbookdic):
    supp_id = "S" + str(len(supplierdic) + 1)
    while True:
        supp_name = input("Enter supplier name: ")
        if supp_name == "":
            print("Supplier name cannot be empty.")
        else:
            break
            

    for key in supplierdic: #loop the dic and check if supplier already exists
        if supplierdic[key]["supplier_name"] == supp_name:
            print("Supplier already exists. Update supplier info instead.")
            return
    
    service_types = []
    while True:
        service_type = input(f"Enter project type provided by {supp_name}: ")
        if service_type in service_types: # avoid duplicates
            print("Supplier already provides this service.")
        elif service_type in logbook.types:
            service_types.append(service_type)
            if len(service_types) == 3:
                print("Supplier provides all types of projects.")
                break
            choice = input("Type added successfully. Do you want to add another type? (y/n): ")
            if choice == "n":
                break
        else:
            print("Type can only be Construction, Renovation, or Demolition.")

    services_provided = []

    while True:
        print()
        service_provided = input(f"Enter service provided by {supp_name} (type 'ALL' to add all services): ")
        if service_provided == "ALL":
            services_provided = logbook.construction
            break
        elif service_provided in service_types: # avoid duplicates
            print("Supplier already provides this service.")
        elif service_provided in logbook.construction:
            services_provided.append(service_provided)
            choice = input("Do you want to add another service? (y/n): ")
            if choice == "n":
                break
        else:
            print("Service provided can only be  Permits, Design, Masonry, Carpentry, WindowWork, MetalWork, Furniture, ElectricalWork, Plumbing, PaintWork, SiteClearing, Earthwork.")

    supplierdic[supp_id] = {
        "supplier_name": supp_name, 
        "services_types": service_types, 
        "services_provided": services_provided
    }

    print()
    print("Supplier added successfully.")

    logbook.addLogEntry("add_supplier", "NA", supp_id, "NA", logbookdic)
    logbook.saveSuppliers(supplierdic)

def addProjectTypes(supplierdic, logbookdic):
    supp_id = input("Enter ID of supplier you want to add project type to: ")

    if supp_id in supplierdic:
        while True:
            new_type = input("Enter new project type: ")
            if new_type in supplierdic[supp_id]["services_types"]: # avoid duplicates
                print(f"{new_type} services is already provided by this supplier.")
            elif new_type in logbook.types:
                supplierdic[supp_id]["services_types"].append(new_type)
                print()
                print("Project type added successfully.")
                break
            else:
                print("Type can only be Construction, Renovation, or Demolition.")
        logbook.addLogEntry("add_project_type", "NA", supp_id, new_type, logbookdic)
        logbook.saveSuppliers(supplierdic)
    else:
        print("Supplier ID does not exist. Check suppliers info.")
    
    

def removeProjectTypes(supplierdic, logbookdic):
    supp_id = input("Enter ID of supplier you want to remove project type from: ")

    if supp_id in supplierdic:
        while True:
            remove_type = input("Enter which project type you want to remove: ")
            if remove_type in supplierdic[supp_id]["services_types"]:
                supplierdic[supp_id]["services_types"].remove(remove_type)
                print()
                print("Project type removed successfully.")
                break
            elif remove_type in logbook.types:
                print(f"{remove_type} services is not provided by this supplier.")
            else:
                print("Type can only be Construction, Renovation, or Demolition.")
        logbook.addLogEntry("remove_project_type", "NA", supp_id, remove_type, logbookdic)
        logbook.saveSuppliers(supplierdic)
    else:
        print("Supplier ID does not exist. Check suppliers info.")

def addServiceProvided(supplierdic, logbookdic):
    supp_id = input("Enter ID of supplier you want to add service provided: ")

    if supp_id in supplierdic:
        while True:
            new_service = input(f"Enter new service provided by {supplierdic[supp_id]["supplier_name"]}: ")
            if new_service in supplierdic[supp_id]["services_provided"]:
                print(f"{new_service} is already provided by this supplier.")
            elif new_service in logbook.construction:
                supplierdic[supp_id]["services_provided"].append(new_service)
                print()
                print(f"Added {new_service} service successfully.")
                break
            else:
                print("Service provided can only be  Permits, Design, Masonry, Carpentry, WindowWork, MetalWork, Furniture, ElectricalWork, Plumbing, PaintWork, SiteClearing, Earthwork.")
        logbook.addLogEntry("add_service_provided", "NA", supp_id, new_service, logbookdic)
        logbook.saveSuppliers(supplierdic)
    else:
        print("Supplier ID does not exist. Check suppliers info.")

def removeServiceProvided(supplierdic, logbookdic):
    supp_id = input("Enter ID of supplier you want to remove service provided from: ")

    if supp_id in supplierdic:
        while True:
            service_type = input(f"Enter service provided by {supplierdic[supp_id]["supplier_name"]} you want to remove: ")

            if service_type in supplierdic[supp_id]["services_provided"]: 
                supplierdic[supp_id]["services_provided"].remove(service_type)
                print()
                print(f"Removed {service_type} service from supplier.")
                break
            elif service_type in logbook.construction: # if not in services provided bbut is a valid service
                print(f"{service_type} service is not provided by this supplier.")
            else:
                print("Service provided can only be  Permits, Design, Masonry, Carpentry, WindowWork, MetalWork, Furniture, ElectricalWork, Plumbing, PaintWork, SiteClearing, Earthwork.")
        logbook.addLogEntry("remove_service_provided", "NA", supp_id, service_type, logbookdic)
        logbook.saveSuppliers(supplierdic)
    else:
        print("Supplier ID does not exist. Check suppliers info.")

def viewSupplier(supplierdic):
    if len(supplierdic) == 0:
        print("No suppliers yet. Add one first.")
    supp_id = input("Enter ID of supplier you want to view: ")

    if supp_id in supplierdic:
        print("\t Supplier ID:", supp_id)
        print("\t Supplier Name:", supplierdic[supp_id]["supplier_name"]),
        print("\t Projects Types done: ")
        for i in supplierdic[supp_id]["services_types"]:
            print("\t\t", i)
        print("\t Services Provided: ")
        for i in supplierdic[supp_id]["services_provided"]:
            print("\t\t", i)
    else: 
        print("Supplier ID does not exist. Check projects info.")

def viewAllSuppliers(supplierdic):
    if len(supplierdic) == 0:
        print("No suppliers yet. Add one first.")
    for key in supplierdic:
        print("\t Supplier ID:", key)
        print("\t Supplier Name:", supplierdic[key]["supplier_name"]),
        print("\t Projects Types done: ")
        for i in supplierdic[key]["services_types"]:
            print("\t\t", i)
        print("\t Services Provided: ")
        for i in supplierdic[key]["services_provided"]:
            print("\t\t", i)
        print()