import arts, logbook

def menu(projectdic,supplierdic, logbookdic, blacklisted):
    while True:
        print(arts.logo)
        print("\tProject Section")
        print("\t1. Add Project")
        print("\t2. Delete All Projects")
        print("\t3. Delete Project")
        print("\t4. View Project")
        print("\t5. View All Projects")
        print("\t6. Update Project Status")
        print("\t7. Change Supplier")
        print("\t8. Change Type")
        print("\t0. Exit")
        print()

        choice = int(input("Choice: "))
        if choice == 1:
            addProject(projectdic, logbookdic)
        elif choice == 2:
            deleteAllProject(projectdic, logbookdic)
        elif choice == 3:
            deleteProject(projectdic, logbookdic)
        elif choice == 4:
            viewProject(projectdic,supplierdic)
        elif choice == 5:
            viewAllprojects(projectdic,supplierdic)
        elif choice == 6:
            updateStatus(projectdic, logbookdic)
        elif choice == 7:
            changeSupplier(projectdic, supplierdic, logbookdic, blacklisted)
        elif choice == 8:
            changeType(projectdic,supplierdic, logbookdic, blacklisted)
        elif choice == 0:
            print("Goodbye!")
            break
def addProject(projectdic, logbookdic):
    print(arts.logo)
    proj_id = "P" + str(len(projectdic) + 1)
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

    if proj_type == "Construction":
        for i in range(0, len(logbook.construction)):
            services[logbook.construction[i]] = ""
    elif proj_type == "Renovation":
        for i in range(0, len(logbook.renovation)):
            services[logbook.renovation[i]] = ""
    elif proj_type == "Demolition":
        for i in range(0, len(logbook.demolition)):
            services[logbook.demolition[i]] = ""
    

    projectdic[proj_id] = {
        "project_type": proj_type,
        "description": description,
        "project_status": proj_status,
        "services" : services
    }

    print("Project has been added.")

    logbook.addLogEntry("add_project", proj_id, "NA", "NA", logbookdic)

    logbook.saveProjects(projectdic)

def deleteProject(projectdic, logbookdic):
    project_id = input("Enter Project ID you want to delete: ")

    if project_id in projectdic:
        del projectdic[project_id]
        project_delete = [] #make a containerish for logs of project ID to delete
        for key in logbookdic:
            if logbookdic[key]["project_id"] == project_id:
                project_delete.append(key)
        for i in project_delete: #loop throught the list and delete the log entries of the project in logbook
            del logbookdic[i]  
        print("Project has been deleted.")
        logbook.saveProjects(projectdic)
        logbook.saveLog(logbookdic)
    else:
        print("Project ID does not exist. View projects info.")


def deleteAllProject(projectdic, logbookdic):
    projects_delete = []
    for key in logbookdic:
        if logbookdic[key]["project_id"] != "NA": # check if log entry has a project ID
            projects_delete.append(key)

    for i in projects_delete:
        del logbookdic[i]

    projectdic.clear()    
    print("All projects have been deleted.")
    logbook.saveProjects(projectdic)
    logbook.saveLog(logbookdic)

def viewProject(projectdic, supplierdic):
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
    proj_id = input("Enter Project ID: ")
    if proj_id in projectdic:
        while True:
            proj_status = input("Enter project status: ")
            if proj_status == projectdic[proj_id]["project_status"]:
                print("Project status is the same. Please choose another status.")
            elif proj_status in logbook.statuses:
                projectdic[proj_id]["project_status"] = proj_status
                break
            else:
                print("Status can only be Prep, Ongoing, or Finished.")
        logbook.addLogEntry("update_status", proj_id, "NA","NAl",logbookdic)
        logbook.saveProjects(projectdic)
    else:
        print("Project ID does not exist. Check projects info.")

def changeSupplier(projectdic, supplierdic,logbookdic, blacklisted):
    if len(supplierdic) == 0:
        print("No suppliers yet. Add a supplier first.")
        return
    proj_id = input("Enter Project ID you want to change supplier: ")

    if proj_id in projectdic:
        if projectdic[proj_id]["project_status"] != "Finished": #check if project is still on prep or ongoing
            service = input("Enter which service you want to change supplier: ")
            if service in projectdic[proj_id]["services"]: #validate if service exists
                print("Here are the suppliers that can provide",service ,"service: ")
                for key in supplierdic:  # loop the supplier dictionary and look for suppliers that can provide the service
                    if service in supplierdic[key]["services_provided"]:
                        print(f"\tID: {key}, Name: {supplierdic[key]["supplier_name"]}")
                while True:
                    change_supplier = input(f"Enter ID of supplier to change {service} service to: ")

                    if change_supplier in blacklisted:
                        print("Supplier is blacklisted. Please choose another supplier.")
                    else:
                        projectdic[proj_id]["services"][service] = change_supplier
                        print("Supplier has been changed.")
                        break
                logbook.addLogEntry("change_supplier", proj_id, change_supplier, service, logbookdic)
                logbook.saveProjects(projectdic)
            else:
                print("Service does not exist. Check project info.")  
        else:
            print("Project is finished. Cannot change supplier.")
    else:
        print("Project ID does not exist. Check projects info.")

def changeType(projectdic,supplierdic,logbookdic, blacklisted):
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
            if new_type == "Construction":
                for i in range(0, len(logbook.construction)):
                    new_services[logbook.construction[i]] = ""
            elif new_type == "Renovation":
                for i in range(0, len(logbook.renovation)):
                    new_services[logbook.renovation[i]] = ""
            elif new_type == "Demolition":
                for i in range(0, len(logbook.demolition)):
                    new_services[logbook.demolition[i]] = ""

            #update project dict
            projectdic[proj_id]["project_type"] = new_type
            projectdic[proj_id]["services"] = new_services

            for key in new_services: #fill services with suppliers
                while True:
                    supplier = input(f"Enter supplier ID for {key} service: ")
                    if supplier in supplierdic: #check if supplier exists
                        if supplierdic[supplier]["supplier_name"] in blacklisted:
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
            logbook.addLogEntry("change_type", proj_id, "NA", "NA", logbookdic)
            logbook.saveProjects(projectdic)    
        else:
            print("Project type can only be changed while in prep stage.")
    else:
        print("Project ID does not exist. Check projects info.")

                


