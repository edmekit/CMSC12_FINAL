import arts

types = ["Construction", "Renovation", "Demolition"]
statuses = ["Prep", "Ongoing", "Finished"]
construction = ['Permits','Design','Masonry','Carpentry','WindowWork','MetalWork','Furniture','ElectricalWork','Plumbing','PaintWork','SiteClearing','Earthwork']
renovation = ['Permits','Masonry','Carpentry','WindowWork',
'MetalWork','ElectricalWork','PaintWork']
demolition = ['Permits','SiteClearing','Earthwork']

def caesarCipher(text, shift):
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower = 'abcdefghijklmnopqrstuvwxyz'
    result = ''

    for char in text:
        # shifts letter by the shift para
        if char in upper:
            result += upper[(upper.index(char) + shift) % 26] 
        elif char in lower:
            result += lower[(lower.index(char) + shift) % 26]
        else:
            result += char # for non-letters, just add as is

    return result

def interpretCaesar(text, shift):
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower = 'abcdefghijklmnopqrstuvwxyz'
    result = ''

    for char in text:
        # returns back the shift in caesarcipher by simply changing the sign
        if char in upper:
            result += upper[(upper.index(char) - shift) % 26]
        elif char in lower:
            result += lower[(lower.index(char) - shift) % 26]
        else:
            result += char

    return result

def saveProjects(projectdic):
    project_file = open("projects.txt", "w")

    for proj in projectdic:
        project_file.write(caesarCipher(proj, 3) + "?")
        project_file.write(caesarCipher(projectdic[proj]["project_type"], 4) + "?")
        project_file.write(caesarCipher(projectdic[proj]["description"], 5) + "?")
        project_file.write(caesarCipher(projectdic[proj]["project_status"], 3) + "?")
        for key in projectdic[proj]["services"]:
            project_file.write(caesarCipher(key, 4) + "?") #save pair by service first then ID
            project_file.write(caesarCipher(projectdic[proj]["services"][key], 5) + "?")
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
            if i % 2 == 1:
                services[interpretCaesar(services_supp[i - 1], 4)] = interpretCaesar(services_supp[i], 5)

        projectdic[interpretCaesar(details[0], 3)] = {
            "project_type": interpretCaesar(details[1], 4),
            "description": interpretCaesar(details[2], 5),
            "project_status": interpretCaesar(details[3], 3),
            "services": services
        }

    project_file.close()

def saveSuppliers(supplierdic):
    supplier_file = open("suppliers.txt", "w")

    # seperate supplier ID, name, types and services with "?" and each type and service with "|"
    for s in supplierdic:
        supplier_file.write(caesarCipher(s, 5) + "?")
        supplier_file.write(caesarCipher(supplierdic[s]["supplier_name"], 4) + "?")
        for t in supplierdic[s]["services_types"]:
            supplier_file.write(caesarCipher(t, 4) + "|")
        supplier_file.write("?")
        for serv in supplierdic[s]["services_provided"]:
            supplier_file.write(caesarCipher(serv, 3) + "|")
        supplier_file.write("\n")

    supplier_file.close()

def loadSuppliers(supplierdic):
    supplier_file = open("suppliers.txt", "r")
    suppliers = supplier_file.readlines()

    for s in suppliers:
        details = s.split("?") #split into 4 parts
        services_types = details[2].split("|") # split the types and services
        services_provided = details[3][:-1].split("|")

        # interpret the caesar cipher and filter empty strings
        types = [interpretCaesar(i, 4) for i in services_types if i != ""]
        provided = [interpretCaesar(i, 3) for i in services_provided if i != ""]

        supplierdic[interpretCaesar(details[0], 5)] = {
            "supplier_name": interpretCaesar(details[1], 4),
            "services_types": types,
            "services_provided": provided
        }

    supplier_file.close()

def saveLog(logbookdic):
    logbook = open("logbook.txt", "w")

    for l in logbookdic:
        logbook.write(caesarCipher(l, 4) + "?")
        logbook.write(caesarCipher(logbookdic[l]["action"], 5) + "?")
        logbook.write(caesarCipher(logbookdic[l]["project_id"], 3) + "?")
        logbook.write(caesarCipher(logbookdic[l]["supplier_id"], 4) + "?")
        logbook.write(caesarCipher(logbookdic[l]["remark"], 5) + "\n")

    logbook.close()

def loadLog(logbookdic):
    logbook = open("logbook.txt", "r")
    logs = logbook.readlines()

    for log in logs:
        details = log[:-1].split("?")

        logbookdic[interpretCaesar(details[0], 4)] = {
            "action": interpretCaesar(details[1], 5),
            "project_id": interpretCaesar(details[2], 3),
            "supplier_id": interpretCaesar(details[3], 4),
            "remark": interpretCaesar(details[4], 5)
        }

    logbook.close()


def menu(projectdic, supplierdic, logbookdic, blacklisted):
    while True:
        print(arts.logs)
        print("\t[1] View All Entries")
        print("\t[2] Blacklist Supplier")
        print("\t[3] Data Reset")
        print("\t[0] Exit")
        print()

        choice = input("Choice: ")
        print()

        if choice == "1":
            viewAllEntries(logbookdic)
        elif choice == "2":
            blacklistSupplier(supplierdic, logbookdic, blacklisted)
        elif choice == "3":
            dataReset(projectdic, supplierdic, logbookdic)
        elif choice == "0":
            print("Going back to main menu...")
            print()
            break
        else:
            print("Invalid choice.")
            print()

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
    if len(logbookdic) == 0:
        print("No log entries.")
    for key in logbookdic:
        print(f"\tLog ID: {key}")
        print(f"\tAction: {logbookdic[key]["action"]}")
        print(f"\tProject ID: {logbookdic[key]["project_id"]}")
        print(f"\tSupplier ID: {logbookdic[key]["supplier_id"]}")
        print(f"\tRemark: {logbookdic[key]["remark"]}")
        print()

def blacklistSupplier(supplierdic, logbookdic, blacklisted):
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
        print()
        print(f"{supplierdic[supp_id]["supplier_name"]} has been blacklisted.")
        blacklisted.append(supp_id)
        saveLog(logbookdic)

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
    


    
        
            
    

