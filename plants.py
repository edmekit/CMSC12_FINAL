import arts, logbook


def menu(projectdic,supplierdic, logbookdic, blacklisted):
    while True:
        print(arts.projects)
        print()
        print("\t[1] Add Project")
        print("\t[2] Delete Projects")
        print("\t[3] Delete All Project")
        print("\t[4] View Project")
        print("\t[5] View All Projects")
        print("\t[6] Update Project Status")
        print("\t[7] Change Supplier")
        print("\t[8] Change Type")
        print("\t[0] Exit")
        print()

        choice = input("Choice: ")
        if choice == "1":
            addProject(projectdic, logbookdic, supplierdic, blacklisted)
        elif choice == "2":
            deleteProject(projectdic, logbookdic)
        elif choice == "3":
            deleteAllProject(projectdic, logbookdic)
        elif choice == "4":
            viewProject(projectdic,supplierdic)
        elif choice == "5":
            viewAllprojects(projectdic,supplierdic)
        elif choice == "6":
            updateStatus(projectdic, logbookdic)
        elif choice == "7":
            changeSupplier(projectdic, supplierdic, logbookdic, blacklisted)
        elif choice == "8":
            changeType(projectdic,supplierdic, logbookdic, blacklisted)
        elif choice == "0":
            print("Going back to main menu...")
            print()
            break
        else:
            print("Invalid choice. Please try again.")
def addProject(projectdic, logbookdic, supplierdic, blacklisted):
    print()
    print(("=" * 15) + " ADD PROJECT " + ("=" * 15))
    proj_id = "P" + str(len(projectdic) + 1)
    # validate type
    while True:
        proj_type = input("Enter project type: ")
        if proj_type in logbook.types:
            break
        else:
            print("Type can only be Construction, Renovation, or Demolition.")

    description = input("Enter project description: ")
    while True:
        proj_status = input("Enter project status: ")
        if proj_status in logbook.statuses:
            break
        else:
            print("Status can only be Prep, Ongoing, or Finished.")
    
    services = {}
    
    # add corresponding services to dict and add "" as placeholder value
    for i in range(len(logbook.types[proj_type])):
        services[logbook.types[proj_type][i]] = ""

    for key in services: #fill services with suppliers
        providers = []
        for s in supplierdic:  # loop the supplier dictionary and look for suppliers that can provide the service
                if key in supplierdic[s]["services_provided"]:
                        providers.append(s)
        if len(providers) == 0:
            print(f"No supplier can provide {key} service. Add one later.")
            continue 
        while True:
            supplier = input(f"Enter supplier ID for {key} service: ")
            if supplier in supplierdic: #check if supplier exists
                if supplier in blacklisted:
                    print("Supplier is blacklisted. Please choose another supplier.")
                    continue
                elif key in supplierdic[supplier]["services_provided"]: #check if supplier can provide service
                    services[key] = supplier 
                    print(f"{supplierdic[supplier]["supplier_name"]} has been assigned for {key} service.")
                    break
                else:
                    print(f"{supplierdic[supplier]["supplier_name"]} cannot provide {key} service. Please choose another supplier.")
            else:
                print("Supplier ID does not exist. Please choose another supplier.")
    

    projectdic[proj_id] = {
        "project_type": proj_type,
        "description": description,
        "project_status": proj_status,
        "services" : services
    }

    print()
    print("Project has been added.")

    logbook.addLogEntry("add_project", proj_id, "NA", "NA", logbookdic)

    logbook.saveProjects(projectdic)

def deleteProject(projectdic, logbookdic):
    if len(projectdic) == 0:
        print("No projects to delete.")
        return
    print()
    print(("=" * 14) + " DELETE PROJECT " + ("=" * 14))
    project_id = input("Enter Project ID you want to delete: ")

    if project_id in projectdic:
        del projectdic[project_id]
        project_delete = [] #make a containerish for logs of project ID to delete to avoid runtime error 
        for key in logbookdic:
            if logbookdic[key]["project_id"] == project_id:
                project_delete.append(key)
        for i in project_delete: #loop throught the list and delete the log entries of the project in logbook
            del logbookdic[i]  
            print()
        print("Project has been deleted.")
        logbook.saveProjects(projectdic)
        logbook.saveLog(logbookdic)
    else:
        print("Project ID does not exist. View projects info.")


def deleteAllProject(projectdic, logbookdic):
    if len(projectdic) == 0:
        print("No projects to delete.")
        return
    print()
    print(("=" * 12) + " DELETE ALL PROJECTS " + ("=" * 12))
    projects_delete = []
    for key in logbookdic:
        if logbookdic[key]["project_id"] != "NA": # check if log entry has a project ID
            projects_delete.append(key)

    for i in projects_delete:
        del logbookdic[i]

    projectdic.clear()    
    print()
    print("All projects have been deleted.")
    logbook.saveProjects(projectdic)
    logbook.saveLog(logbookdic)

def viewProject(projectdic, supplierdic):
    print()
    print(("=" * 15) + " VIEW PROJECT " + ("=" * 15))
    proj_id = input("Enter Project ID you want to view: ")

    if proj_id in projectdic:
        print("\t Project ID:", proj_id)
        print("\t Project Type:", projectdic[proj_id]["project_type"]),
        print("\t Description:", projectdic[proj_id]["description"])
        print("\t Project Status:", projectdic[proj_id]["project_status"])
        print("\t Services: ")
        for k,v in projectdic[proj_id]["services"].items():
            if v == "":
                print(f"\t\tType: {k}, Supplier: None yet.")
            else:
                print(f"\t\tType: {k}, Supplier: {supplierdic[v]["supplier_name"]}")
    else: 
        print("Project ID does not exist. Check projects info.")
    
def viewAllprojects(projectdic, supplierdic):
    if len(projectdic) == 0:
        print("No projects found. Add a project first.")
    else:
        print()
        print(("=" * 13) + " VIEW ALL PROJECTS " + ("=" * 13))
        for key in projectdic:
            print("\t Project ID:", key)
            print("\t Project Type:", projectdic[key]["project_type"]),
            print("\t Description:", projectdic[key]["description"])
            print("\t Project Status:", projectdic[key]["project_status"])
            print("\t Services: ")
            for k,v in projectdic[key]["services"].items():
                if v == "":
                    print(f"\t\tType: {k}, Supplier: None yet.")
                else:
                    print(f"\t\tType: {k}, Supplier: {supplierdic[v]["supplier_name"]}")
            print()

def updateStatus(projectdic, logbookdic):
    print()
    print(("=" * 11) + " UPDATE PROJECT STATUS " + ("=" * 11))
    proj_id = input("Enter Project ID: ")
    if proj_id in projectdic:
        while True:
            proj_status = input("Enter project status: ")
            if proj_status == projectdic[proj_id]["project_status"]:
                print("Project status is the same. Please choose another status.")
            elif proj_status in logbook.statuses:
                projectdic[proj_id]["project_status"] = proj_status
                print()
                print("Project status has been updated.")
                break
            else:
                print("Status can only be Prep, Ongoing, or Finished.")
        logbook.addLogEntry("update_status", proj_id, "NA","NA",logbookdic)
        logbook.saveProjects(projectdic)
    else:
        print("Project ID does not exist. Check projects info.")

def changeSupplier(projectdic, supplierdic,logbookdic, blacklisted):
    if len(supplierdic) == 0:
        print("No suppliers yet. Add a supplier first.")
        return
    print()
    print(("=" * 13) + " CHANGE SUPPLIER " + ("=" * 13))
    proj_id = input("Enter Project ID you want to change supplier: ")

    if proj_id in projectdic:
        if projectdic[proj_id]["project_status"] != "Finished": #check if project is still on prep or ongoing
            service = input("Enter which service you want to change supplier: ")
            if service in projectdic[proj_id]["services"]: #validate if service exists
                print("Here are the suppliers that can provide",service ,"service: ")
                providers = [] # contain ID of available suppliers
                
                for key in supplierdic:  # loop the supplier dictionary and look for suppliers that can provide the service
                    if service in supplierdic[key]["services_provided"]:
                        print(f"\tID: {key}, Name: {supplierdic[key]["supplier_name"]}")
                        providers.append(key)
                
                while True:
                    change_supplier = input(f"Enter ID of supplier to change {service} service to: ")
                    if change_supplier in supplierdic:
                        if change_supplier in blacklisted:
                            print("Supplier is blacklisted. Please choose another supplier.")
                        elif change_supplier in providers:
                            projectdic[proj_id]["services"][service] = change_supplier
                            print()
                            print("Supplier has been changed.")
                            break
                        else:
                            print("Supplier does not provide this service. Please choose in the ones provided.")
                    else:
                        print("Supplier does not exist. Choose from the ones provided.")
                logbook.addLogEntry("change_supplier", proj_id, change_supplier, service, logbookdic)
                logbook.saveProjects(projectdic)
            else:
                print("Service does not exist. Check project info.")  
        else:
            print("Project is finished. Cannot change supplier.")
    else:
        print("Project ID does not exist. Check projects info.")

def changeType(projectdic,supplierdic,logbookdic, blacklisted):
    print()
    print(("=" * 12) + " CHANGE PROJECT TYPE " + ("=" * 12))
    proj_id = input("Enter Project ID you want to change type: ")

    if proj_id in projectdic:
        if projectdic[proj_id]["project_status"] == "Prep":
            while True:
                new_type = input("Enter new project type: ")

                if new_type == projectdic[proj_id]["project_type"]:
                    print("Project type is the same. Please choose another type.")
                elif new_type in logbook.types:
                    break
                else:
                    print("Type can only be Construction, Renovation, or Demolition.")

            new_services = {}

            #put services to dict
            for i in range(0, len(logbook.types[new_type])):
                new_services[logbook.types[new_type][i]] = ""
           
            #update project dict
            projectdic[proj_id]["project_type"] = new_type
            projectdic[proj_id]["services"] = new_services
            
            for key in new_services: #fill services with suppliers
                providers = [] # contain ID of available suppliers
                
                for s in supplierdic:  # loop the supplier dictionary and look for suppliers that can provide the service
                    if key in supplierdic[s]["services_provided"]:
                        providers.append(s)
                if len(providers) == 0:
                    print(f"No supplier can provide {key} service. Add one later.")
                    continue  

                while True:
                    supplier = input(f"Enter supplier ID for {key} service: ")
                    if supplier in supplierdic: #check if supplier exists
                        if supplier in blacklisted:
                            print("Supplier is blacklisted. Please choose another supplier.")
                            continue
                        elif key in supplierdic[supplier]["services_provided"]: #check if supplier can provide service
                            new_services[key] = supplier 
                            print(f"{supplierdic[supplier]["supplier_name"]} has been assigned for {key} service.")
                            break
                        else:
                            print(f"{supplierdic[supplier]["supplier_name"]} cannot provide {key} service. Please choose another supplier.")
                    else:
                        print("Supplier ID does not exist. Please choose another supplier.")
            print()
            print("Project type has been changed.")
            logbook.addLogEntry("change_type", proj_id, "NA", "NA", logbookdic)
            logbook.saveProjects(projectdic)    
        else:
            print("Project type can only be changed while in prep stage.")
    else:
        print("Project ID does not exist. Check projects info.")

                


