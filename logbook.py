import arts

types = ["Construction", "Renovation", "Demolition"]
statuses = ["Prep", "Ongoing", "Finished"]
construction = ['Permits','Design','Masonry','Carpentry','WindowWork','MetalWork','Furniture','ElectricalWork','Plumbing','PaintWork','SiteClearing','Earthwork']
renovation = ['Permits','Masonry','Carpentry','WindowWork',
'MetalWork','ElectricalWork','PaintWork']
demolition = ['Permits','SiteClearing','Earthwork']

def saveProjects(projectdic):
    project_file = open("projects.txt", "w")

    for k in projectdic:
        project_file.write(k + "?")
        project_file.write(projectdic[k]["project_type"] + "?")
        project_file.write(projectdic[k]["description"] + "?")
        project_file.write(projectdic[k]["project_status"] + "?")
        for key in projectdic[k]["services"]:
            project_file.write(key + "?")
            project_file.write(projectdic[k]["services"][key] + "?")
        project_file.write("\n")

    project_file.close()

def loadProjects(projectdic):
    project_file = open("projects.txt", "r")
    projects = project_file.readlines()

    for project in projects:
        details = project.split("?")
        services_supp = details[4:-1]

        services = {}
        
        # get service, ID pairs
        for i in range(0, len(services_supp)):
            if i % 2 == 1 or i == 1:
                services[services_supp[i - 1]] = services_supp[i]

        projectdic[details[0]] = {
            "project_type": details[1],
            "description": details[2],
            "project_status": details[3],
            "services": services
        }

    project_file.close()

def saveSuppliers(suppleirdic):
    supplier_file = open("suppliers.txt", "w")

    for s in suppleirdic:
        supplier_file.write(s + "?")
        supplier_file.write(suppleirdic[s]["supplier_name"] + "?")
        for t in suppleirdic[s]["services_types"]:
            supplier_file.write(t + "|")
        supplier_file.write("?")
        for s in suppleirdic[s]["services_provided"]:
            supplier_file.write(s + "|")
        supplier_file.write("\n")

    supplier_file.close()

def loadSuppliers(supplierdic):
    supplier_file = open("suppliers.txt", "r")
    suppliers = supplier_file.readlines()

    for s in suppliers:
        details = s.split("?")
        services_types = details[2].split("|")
        services_provided = details[3][:-1].split("|")

        supplierdic[details[0]] = {
            "supplier_name": details[1],
            "services_types": services_types,
            "services_provided": services_provided
        }

    supplier_file.close()

def saveLog(logbookdic):
    logbook = open("logbook.txt", "w")

    for l in logbookdic:
        logbook.write(l + "?")
        logbook.write(logbookdic[l]["action"] + "?")
        logbook.write(logbookdic[l]["project_id"] + "?")
        logbook.write(logbookdic[l]["supplier_id"] + "?")
        logbook.write(logbookdic[l]["remark"] + "\n")

    logbook.close()

def loadLog(logbookdic):
    logbook = open("logbook.txt", "r")
    logs = logbook.readlines()

    for log in logs:
        details = log[:-1].split("?")

        logbookdic[details[0]] = {
            "action": details[1],
            "project_id": details[2],
            "supplier_id": details[3],
            "remark": details[4]
        }

    logbook.close()


def menu(projectdic, supplierdic, logbookdic):
    while True:
        print(arts.logo)
        print("\tLogbook Section")
        print("\t1. View All Entries")
        print("\t2. Blacklist Supplier")
        print("\t3. Data Reset")
        print("\t0. Exit")
        print()

        choice = int(input("Choice: "))
        print()

        if choice == 1:
            viewAllEntries(logbookdic)
        elif choice == 2:
            blacklistSupplier(supplierdic, logbookdic)
        elif choice == 3:
            dataReset(projectdic, supplierdic, logbookdic)
        elif choice == 0:
            print("Goodbye!")
            break

def addLogEntry(action, projID, suppID, remark, logbookdic):
    log_id = "L" + str(len(logbookdic) + 1)

    logbookdic[log_id] = {
        "action": action,
        "project_id": projID,
        "supplier_id": suppID,
        "remark": remark
    }

    saveLog(logbookdic)

def viewAllEntries(logbookdic):
    for key in logbookdic:
        print(f"\tLog ID: {key}")
        print(f"\tAction: {logbookdic[key]["action"]}")
        print(f"\tProject ID: {logbookdic[key]["project_id"]}")
        print(f"\tSupplier ID: {logbookdic[key]["supplier_id"]}")
        print(f"\tRemark: {logbookdic[key]["remark"]}")
        print()

def blacklistSupplier(supplierdic, logbookdic):
    log_id = "L" + str(len(logbookdic) + 1)

    supp_id = input("Enter ID of supplier you want to add to blacklist: ")

    if supp_id in supplierdic:
        remark = input("Enter reason for blacklisting: ")
        logbookdic[log_id] = {
            "action": "blacklist_supplier",
            "project_id": "NA",
            "supplier_id": supp_id,
            "remark": remark
        }
    else:
        print("Supplier ID does not exist. Check suppliers info.")

def dataReset(projectdic, supplierdic, logbookdic):
    confirm = input("Are you sure you want to delete all data? (y/n): ")
    if confirm == "y":
        logbookdic.clear()
        supplierdic.clear()
        projectdic.clear()
        print("All data has been deleted.")
        saveLog(logbookdic)
        saveSuppliers(supplierdic)
        saveProjects(projectdic)
    else:
        print("Data reset cancelled.")
    


    
        
            
    

