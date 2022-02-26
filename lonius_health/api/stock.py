import frappe
import json
import os
import string


def items_upload():
    # Opening JSON file
    file_path = "{}/assets/lonius_health/files/all_items.json".format(
        os.getcwd())
    # file_path  ="/assets/files/all_items.json"
    print(file_path)
    with open(file_path) as f:

        # returns JSON object as
        # a dictionary

        data = json.load(f)
        # print(len(data))
        handle_uoms([x.get("stock_uom") for x in data])

        handle_item_groups([x.get("item_group") for x in data])

        handle_items(data)
        # Iterating through the json
        # list
        # for i in data:
        #     print(i)

        # Closing file
        f.close()


def handle_uoms(uoms):
    filtered = [x for x in uoms if not frappe.get_value("UOM", x)]
    for uom in filtered:
        args = dict(doctype="UOM", uom_name=uom, enabled=True)
        frappe.get_doc(args).insert()
        frappe.db.commit()
    return filtered


def handle_item_groups(item_groups):
    filtered = [x for x in item_groups if not frappe.get_value(
        "Item Group", dict(item_group_name=x))]
    for item_group in filtered:
        args = dict(doctype="Item Group",
                    item_group_name=item_group, enabled=True)
        frappe.get_doc(args).insert()
        frappe.db.commit()
    return filtered


def handle_items(items):
    def _make_item(row):
        pass
    filtered = list(filter(lambda x: not frappe.get_value(
        "Item", dict(item_name=x.get("item_name")), 'name'), items))
    list(map(lambda x: _make_item(x), filtered))


def upload_list():
    count = 0
    payload = keml().get("meds")
    for d in payload:
        count += 1
        if count < 35:
            continue
        print(count)
        d["medicine_name"] = d.pop("Medicine Name").rstrip(string.digits).strip().replace("\n","").replace("\r","")
        d["default_dosage_form"] = "" 
        if "Dosage" in list(d.keys()):
            d["default_dosage_form"] = d.pop("Dosage").rstrip(string.digits).strip().replace("\n","").replace("\r","")
        d["strength"] = "" 
        if "Strength / Size" in d.keys():
            d["strength"] = d.pop("Strength / Size").rstrip(string.digits).strip().replace("\n","").replace("\r","")
        d["doctype"] ="Drug"
        print(d)

        def _upload(args):
            if not frappe.get_value("Dosage Form",args.get("default_dosage_form")) and args.get("default_dosage_form"):
                frappe.get_doc(dict(doctype="Dosage Form",dosage_form=args.get("default_dosage_form"))).insert()
                frappe.db.commit()
            if not frappe.get_value("Drug", args.get("medicine_name")):         
                document = frappe.get_doc(args)
                document.append("drug_stock_detail",dict(dosage_form=args.get("default_dosage_form"), strength=args.get("strength")))
                document.insert()
                frappe.db.commit()
                return
            doc = frappe.get_doc("Drug",args.get("medicine_name"))
            doc.append("drug_stock_detail",dict(dosage_form=args.get("default_dosage_form"), strength=args.get("strength")))
            doc.save()
        _upload(d)
        # if frappe.get_value("Drug", new_name):
        #     frappe.delete_doc("Drug", d.get("name"))
        #     frappe.db.commit()
        #     continue
        # frappe.rename_doc("Drug", d.get("name"), new_name, merge=False)


def keml():
    return {
        "meds": [
            {
                "Medicine Name": "2-chamber bag for central  administration",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "1 litre"
            },
            {
                "Medicine Name": "3-chamber bag for   peripheral administration",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "1 litre547"
            },
            {
                "Medicine Name": "3-chamber bag for   peripheral administration",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "1.5 litre548"
            },
            {
                "Medicine Name": "3-chamber bag for   peripheral administration  for Medum chain   Triglycerides (MCT) / Long  chain Triglycerides (LCT)",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "1 litre549"
            },
            {
                "Medicine Name": "3-chamber bag for   peripheral administration  for Medum chain   Triglycerides (MCT) / Long  chain Triglycerides (LCT)",
                "Strength / Size": "1.5 litre549"
            },
            {
                "Medicine Name": "3-chamber bag for central  administration",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "1 litre550"
            },
            {
                "Medicine Name": "3-chamber bag for central  administration",
                "Strength / Size": "2 litres551"
            },
            {
                "Medicine Name": "3-chamber bag for central  administration for Medum  chain Triglycerides (MCT) /  Long chain Triglycerides  (LCT)",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "1 litre552"
            },
            {
                "Medicine Name": "3-chamber bag for central  administration for Medum  chain Triglycerides (MCT) /  Long chain Triglycerides  (LCT)",
                "Strength / Size": "2 litres553"
            },
            {
                "Medicine Name": "Abacavir (ABC)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Abacavir + lamivudine  (ABC/3TC)",
                "Dosage": "Tablet (dispersible, \r\nscored)",
                "Strength / Size": "120mg (as sulphate) + \r\n60mg"
            },
            {
                "Medicine Name": "Abacavir + lamivudine  (ABC/3TC)",
                "Dosage": "Tablet",
                "Strength / Size": "600mg (as sulphate) + \r\n300mg"
            },
            {
                "Medicine Name": "Abacavir + Lamivudine +  Lopinavir + ritonavir   (ABC/3TC/LPV/r)",
                "Dosage": "Granules for oral  \r\nsuspension",
                "Strength / Size": "30mg (as sulphate) + \r\n15mg + 40mg + 10mg"
            },
            {
                "Medicine Name": "Abatacept",
                "Dosage": "PFI (IV)",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Abiraterone",
                "Dosage": "Tablet",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Acetazolamide",
                "Dosage": "Tablet",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Acetylcysteine",
                "Dosage": "Injection",
                "Strength / Size": "200mg/mL (10mL amp)"
            },
            {
                "Medicine Name": "Acetylsalicylic acid   (Aspirin)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Acetylsalicylic acid  (Aspirin)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Acetylsalicylic acid  (Aspirin)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Acetylsalicylic acid  (Aspirin)",
                "Dosage": "Tablet",
                "Strength / Size": "75mg"
            },
            {
                "Medicine Name": "Acyclovir",
                "Dosage": "PFI",
                "Strength / Size": "250mg vial (as sodium \r\nsalt)"
            },
            {
                "Medicine Name": "Acyclovir",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Acyclovir",
                "Dosage": "Eye ointment",
                "Strength / Size": "3%"
            },
            {
                "Medicine Name": "Adalimumab",
                "Dosage": "Injection",
                "Strength / Size": "40mg/0.4mL"
            },
            {
                "Medicine Name": "Adenosine",
                "Dosage": "Injection",
                "Strength / Size": "6mg/2mL"
            },
            {
                "Medicine Name": "Adult nutritionally   complete isocaloric   formula",
                "Dosage": "Powder",
                "Strength / Size": "400g"
            },
            {
                "Medicine Name": "Adult nutritionally  complete peptide based  formula",
                "Dosage": "Powder",
                "Strength / Size": "20 to 30g sachet"
            },
            {
                "Medicine Name": "Adult trace elements",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "10mL"
            },
            {
                "Medicine Name": "Albendazole",
                "Dosage": "Tablet (chewable)90",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Albendazole",
                "Dosage": "Suspension91",
                "Strength / Size": "100mg/5mL"
            },
            {
                "Medicine Name": "Albendazole",
                "Dosage": "Tablet (chewable)",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Alcohol-based hand rub",
                "Dosage": "Solution",
                "Strength / Size": "Isopropyl alcohol 75% \r\n(500mL dispenser)"
            },
            {
                "Medicine Name": "Alendronic acid",
                "Dosage": "Tablet",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Alendronic acid",
                "Strength / Size": "70mg"
            },
            {
                "Medicine Name": "Allopurinol",
                "Dosage": "Tablet",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Allopurinol",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "All-trans retinoid acid  (ATRA)",
                "Dosage": "Capsule",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Amidotrizoate",
                "Dosage": "Solution  \r\n(oral and rectal use)",
                "Strength / Size": "370-420mg iodine/mL \r\n(as sodium or \r\nmeglumine salt) \r\n(100mL)"
            },
            {
                "Medicine Name": "Amikacin",
                "Dosage": "Injection",
                "Strength / Size": "50mg (as sulphate)/mL \r\nin 2ml vial [c]96"
            },
            {
                "Medicine Name": "Amikacin",
                "Dosage": "Injection",
                "Strength / Size": "250mg (as sulphate)/mL \r\nin 2ml vial"
            },
            {
                "Medicine Name": "Amikacin (Am)",
                "Dosage": "PFI",
                "Strength / Size": "1g (as sulphate) vial"
            },
            {
                "Medicine Name": "Amiloride",
                "Dosage": "Tablet",
                "Strength / Size": "5mg (as HCl)"
            },
            {
                "Medicine Name": "Amino acids",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "21g amino acid +  \r\n12g glutamine per \r\n100mL bottle555"
            },
            {
                "Medicine Name": "Amino acids",
                "Strength / Size": "5-6% with glucose  \r\n(100ml bottle) [c]556"
            },
            {
                "Medicine Name": "Amino acids",
                "Strength / Size": "7% (500ml bottle)557"
            },
            {
                "Medicine Name": "Amino acids",
                "Strength / Size": "8% (500ml bottle)558"
            },
            {
                "Medicine Name": "Amino acids",
                "Strength / Size": "10% with electrolytes \r\n(500ml bottle)559"
            },
            {
                "Medicine Name": "Amino acids and Vitamin  granules",
                "Dosage": "Powder",
                "Strength / Size": "5 to 10g sachet"
            },
            {
                "Medicine Name": "Amiodarone",
                "Dosage": "Injection303",
                "Strength / Size": "50mg (as HCl)/mL in \r\n3mL"
            },
            {
                "Medicine Name": "Amiodarone",
                "Dosage": "Tablet304",
                "Strength / Size": "100mg (as HCl)"
            },
            {
                "Medicine Name": "Amiodarone",
                "Strength / Size": "200mg (as HCl)"
            },
            {
                "Medicine Name": "Amitriptyline",
                "Dosage": "Tablet",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Amitriptyline",
                "Dosage": "Tablet",
                "Strength / Size": "25mg (as HCl)"
            },
            {
                "Medicine Name": "Amlodipine",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Amlodipine +   Hydrochlorothiazide  (HCTZ)",
                "Dosage": "Tablet",
                "Strength / Size": "5mg + 12.5mg"
            },
            {
                "Medicine Name": "Amoxicillin",
                "Dosage": "Tablet  \r\n(dispersible, scored)",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Amoxicillin",
                "Dosage": "Capsule",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Amoxicillin + clavulanic  acid",
                "Dosage": "Tablet  \r\n(dispersible, scored)98",
                "Strength / Size": "250mg + 62.5mg  \r\n(i.e. 312.5mg)"
            },
            {
                "Medicine Name": "Amoxicillin + clavulanic  acid",
                "Dosage": "Tablet98",
                "Strength / Size": "875mg + 125mg (i.e. 1g)"
            },
            {
                "Medicine Name": "Amoxicillin + clavulanic  acid",
                "Dosage": "PFI99",
                "Strength / Size": "500mg + 100mg"
            },
            {
                "Medicine Name": "Amoxicillin + clavulanic  acid",
                "Strength / Size": "1g + 200mg"
            },
            {
                "Medicine Name": "Amoxicillin + clavulanic  acid (Co-Amoxiclav)",
                "Dosage": "Tablet",
                "Strength / Size": "875mg + 125mg (1g)"
            },
            {
                "Medicine Name": "Amphotericin B",
                "Dosage": "PFI",
                "Strength / Size": "50mg (as sodium \r\ndeoxycholate) vial"
            },
            {
                "Medicine Name": "Amphotericin B",
                "Dosage": "PFI",
                "Strength / Size": "(Liposomal) 50mg vial"
            },
            {
                "Medicine Name": "Ampicillin",
                "Dosage": "PFI",
                "Strength / Size": "500mg vial"
            },
            {
                "Medicine Name": "Anastrozole",
                "Dosage": "Tablet",
                "Strength / Size": "1mg"
            },
            {
                "Medicine Name": "Anti Snake venom   immunoglobulin",
                "Dosage": "Injection  \r\n(for IV infusion)",
                "Strength / Size": "Monovalent serum (for \r\nBoomslang \r\n(Dyspholidus typus, \r\nAfrican) bites), vial397"
            },
            {
                "Medicine Name": "Anti Snake venom   immunoglobulin",
                "Strength / Size": "Polyvalent serum \r\n(African) (10mL vial)398"
            },
            {
                "Medicine Name": "Anti-D immunoglobulin",
                "Dosage": "PFI + diluent",
                "Strength / Size": "750 IU/mL (2mL vial)"
            },
            {
                "Medicine Name": "Anti-Hepatitis B   immunoglobulin (HBIG)",
                "Dosage": "Injection",
                "Strength / Size": "100 IU/mL"
            },
            {
                "Medicine Name": "Anti-Rabies   immunoglobulin",
                "Dosage": "Injection",
                "Strength / Size": "200 IU/mL (5mL vial)"
            },
            {
                "Medicine Name": "Anti-Tetanus   immunoglobulin",
                "Dosage": "Injection",
                "Strength / Size": "500 IU vial"
            },
            {
                "Medicine Name": "Antithymocyte globulin  (ATG) (rabbit)",
                "Dosage": "PFI",
                "Strength / Size": "25mg vial"
            },
            {
                "Medicine Name": "Aripiprazole",
                "Dosage": "Tablet",
                "Strength / Size": "15mg"
            },
            {
                "Medicine Name": "Arsenic trioxide",
                "Dosage": "Concentrate solution \r\nfor Infusion",
                "Strength / Size": "1mg/mL"
            },
            {
                "Medicine Name": "Artemether",
                "Dosage": "Injection (oily, IM)",
                "Strength / Size": "80mg/mL in 1mL amp"
            },
            {
                "Medicine Name": "Artemether +   lumefantrine (AL)",
                "Dosage": "Tablet171",
                "Strength / Size": "20mg + 120mg"
            },
            {
                "Medicine Name": "Artemether +   lumefantrine (AL)",
                "Dosage": "Tablet (dispersible)172",
                "Strength / Size": "20mg + 120mg [c]"
            },
            {
                "Medicine Name": "Artesunate",
                "Dosage": "Injection (IM/IV)",
                "Strength / Size": "30mg vial174"
            },
            {
                "Medicine Name": "Artesunate",
                "Strength / Size": "60mg vial175"
            },
            {
                "Medicine Name": "Artesunate +   Pyronaridine   tetraphosphate",
                "Dosage": "Tablet (f/c)",
                "Strength / Size": "60mg + 180mg"
            },
            {
                "Medicine Name": "Artesunate +   Pyronaridine   tetraphosphate",
                "Dosage": "Granules for oral  \r\nsuspension",
                "Strength / Size": "20mg + 60mg [c]"
            },
            {
                "Medicine Name": "Ascorbic acid (Vit C)",
                "Dosage": "Tablet",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Asparaginase",
                "Dosage": "PFI",
                "Strength / Size": "10,000 IU vial"
            },
            {
                "Medicine Name": "Atazanavir (ATV)",
                "Dosage": "Capsule",
                "Strength / Size": "100mg (as sulphate)"
            },
            {
                "Medicine Name": "Atazanavir + Ritonavir  (ATV/r)",
                "Dosage": "Tablet (heat-stable)",
                "Strength / Size": "300mg + 100mg"
            },
            {
                "Medicine Name": "Atovaquone + Proguanil182   Tablet (f/c)",
                "Strength / Size": "62.5mg (as HCl) + 25mg"
            },
            {
                "Medicine Name": "Atovaquone + Proguanil182   Tablet (f/c)",
                "Strength / Size": "250mg (as HCl) + 100mg"
            },
            {
                "Medicine Name": "Atracurium",
                "Dosage": "Injection",
                "Strength / Size": "10mg (as besilate)/mL  \r\n(5mL amp)"
            },
            {
                "Medicine Name": "Atropine",
                "Dosage": "Injection",
                "Strength / Size": "1mg (as sulphate)/1mL \r\namp"
            },
            {
                "Medicine Name": "Atropine",
                "Dosage": "Eye drops",
                "Strength / Size": "0.1% (as sulphate) [c]421"
            },
            {
                "Medicine Name": "Atropine",
                "Dosage": "Eye drops",
                "Strength / Size": "0.5% (as sulphate)"
            },
            {
                "Medicine Name": "Atropine sulphate",
                "Dosage": "Injection",
                "Strength / Size": "1mg/1mL amp"
            },
            {
                "Medicine Name": "Azathioprine",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Azathioprine",
                "Dosage": "Tablet",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Azithromycin",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "500mg (anhydrous)"
            },
            {
                "Medicine Name": "Azithromycin",
                "Dosage": "PFOL",
                "Strength / Size": "200mg/5mL"
            },
            {
                "Medicine Name": "Azithromycin",
                "Dosage": "Eye drops",
                "Strength / Size": "1.5%"
            },
            {
                "Medicine Name": "B vitamins, high  potency",
                "Dosage": "Injection (IV)",
                "Strength / Size": "Pair of amps. (2 x 5mL)"
            },
            {
                "Medicine Name": "Barium sulphate",
                "Dosage": "Suspension (aq)",
                "Strength / Size": "95% w/w concentration \r\n(1 litre)"
            },
            {
                "Medicine Name": "Barium sulphate",
                "Dosage": "Paste  \r\n(for oral or rectal use)349",
                "Strength / Size": "92% w/w concentration"
            },
            {
                "Medicine Name": "Basiliximab",
                "Dosage": "PFI",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "BCG vaccine   (live attenuated)",
                "Dosage": "PFI + diluent",
                "Strength / Size": "1mL vial (multi dose)"
            },
            {
                "Medicine Name": "Bedaquiline (Bdq)",
                "Dosage": "Tablet",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Bendamustine",
                "Dosage": "Injection",
                "Strength / Size": "100mg/20mL vial"
            },
            {
                "Medicine Name": "Benzathine   benzylpenicillin",
                "Dosage": "PFI",
                "Strength / Size": "900mg (1.2MU) vial"
            },
            {
                "Medicine Name": "Benzhexol",
                "Dosage": "Tablet",
                "Strength / Size": "5mg (as HCl)"
            },
            {
                "Medicine Name": "Benzoyl peroxide",
                "Dosage": "Gel",
                "Strength / Size": "5% (30g)"
            },
            {
                "Medicine Name": "Benztropine",
                "Dosage": "Injection",
                "Strength / Size": "2mg/2mL"
            },
            {
                "Medicine Name": "Benzyl Benzoate",
                "Dosage": "Lotion",
                "Strength / Size": "25% (50mL)"
            },
            {
                "Medicine Name": "Benzyl Benzoate",
                "Dosage": "Lotion",
                "Strength / Size": "25% (50mL)"
            },
            {
                "Medicine Name": "Benzylpenicillin",
                "Dosage": "PFI",
                "Strength / Size": "600mg (1MU) (as \r\nsodium or potassium \r\nsalt) vial104"
            },
            {
                "Medicine Name": "Benzylpenicillin",
                "Strength / Size": "3g (5MU) (as sodium or \r\npotassium salt) vial"
            },
            {
                "Medicine Name": "Betamethasone",
                "Dosage": "Cream332",
                "Strength / Size": "0.1% (as valerate)"
            },
            {
                "Medicine Name": "Betamethasone",
                "Dosage": "Ointment333",
                "Strength / Size": "0.1% (as valerate)"
            },
            {
                "Medicine Name": "Bicalutamide",
                "Dosage": "Tablet",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Bisacodyl",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Bisacodyl",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Bisacodyl",
                "Dosage": "Suppository",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Bisoprolol",
                "Dosage": "Tablet",
                "Strength / Size": "1.25mg"
            },
            {
                "Medicine Name": "Bisoprolol",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Bisoprolol",
                "Dosage": "Tablet",
                "Strength / Size": "1.25mg"
            },
            {
                "Medicine Name": "Bisoprolol",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Bisoprolol",
                "Dosage": "Tablet",
                "Strength / Size": "1.25mg"
            },
            {
                "Medicine Name": "Bisoprolol",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Bleomycin",
                "Dosage": "PFI",
                "Strength / Size": "15mg vial (as sulphate)"
            },
            {
                "Medicine Name": "Bortezomib",
                "Dosage": "PFI",
                "Strength / Size": "3.5mg vial"
            },
            {
                "Medicine Name": "Bromazepam",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "3mg"
            },
            {
                "Medicine Name": "Budesonide",
                "Dosage": "Inhalation (aerosol)",
                "Strength / Size": "100 micrograms/dose  \r\n(200 dose)"
            },
            {
                "Medicine Name": "Budesonide",
                "Strength / Size": "200 micrograms/dose  \r\n(200 dose)"
            },
            {
                "Medicine Name": "Budesonide",
                "Dosage": "Nasal spray",
                "Strength / Size": "100 micrograms / \r\nmetered dose [c]"
            },
            {
                "Medicine Name": "Budesonide + Formoterol",
                "Dosage": "Dry powder inhaler",
                "Strength / Size": "100 micrograms +  \r\n6mg/metered dose  \r\n(120 dose)"
            },
            {
                "Medicine Name": "Budesonide + Formoterol",
                "Strength / Size": "200 micrograms +  \r\n6mg/metered dose  \r\n(120 dose)"
            },
            {
                "Medicine Name": "Bupivacaine",
                "Dosage": "Injection",
                "Strength / Size": "0.5% (as HCl) (10mL vial)"
            },
            {
                "Medicine Name": "Bupivacaine",
                "Dosage": "Injection (spinal)25",
                "Strength / Size": "0.5% (as HCl) (5mg/mL) \r\n+ glucose 8% (80mg/mL)  \r\n(4mL amp)"
            },
            {
                "Medicine Name": "Buprenorphine",
                "Dosage": "Tablet (sublingual)",
                "Strength / Size": "2mg (as HCl)"
            },
            {
                "Medicine Name": "Buprenorphine",
                "Dosage": "Tablet (sublingual)",
                "Strength / Size": "8mg (as HCl)"
            },
            {
                "Medicine Name": "Buprenorphine +  Naloxone",
                "Dosage": "Tablet (sublingual)",
                "Strength / Size": "2mg + 500 micrograms \r\n(both as HCl)"
            },
            {
                "Medicine Name": "Buprenorphine +  Naloxone",
                "Dosage": "Tablet (sublingual)",
                "Strength / Size": "8mg + 2mg (both as \r\nHCl)"
            },
            {
                "Medicine Name": "Bupropion",
                "Dosage": "Tablet",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Caffeine citrate",
                "Dosage": "Injection",
                "Strength / Size": "20mg/mL (3mL vial) [c]"
            },
            {
                "Medicine Name": "Caffeine citrate",
                "Dosage": "Oral liquid (drops)",
                "Strength / Size": "20mg/mL (as disodium \r\nphosphate) [c]"
            },
            {
                "Medicine Name": "Calamine",
                "Dosage": "Lotion",
                "Strength / Size": "15%"
            },
            {
                "Medicine Name": "Calamine",
                "Dosage": "Lotion",
                "Strength / Size": "15%"
            },
            {
                "Medicine Name": "Calcitriol (Vit D3)",
                "Dosage": "Capsule",
                "Strength / Size": "250 micrograms"
            },
            {
                "Medicine Name": "Calcitriol (Vit D3)",
                "Dosage": "Injection",
                "Strength / Size": "1 microgram/mL (1 mL)"
            },
            {
                "Medicine Name": "Calcium carbonate",
                "Dosage": "Tablet",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Calcium carbonate",
                "Dosage": "Tablet (chewable)",
                "Strength / Size": "1.25g"
            },
            {
                "Medicine Name": "Calcium folinate",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (5mL vial)"
            },
            {
                "Medicine Name": "Calcium folinate",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (5mL vial)"
            },
            {
                "Medicine Name": "Calcium folinate",
                "Strength / Size": "10mg/mL (30mL vial)"
            },
            {
                "Medicine Name": "Calcium folinate",
                "Dosage": "Tablet",
                "Strength / Size": "15mg"
            },
            {
                "Medicine Name": "Calcium gluconate",
                "Dosage": "Injection",
                "Strength / Size": "100mg/mL in 10mL amp"
            },
            {
                "Medicine Name": "Calcium gluconate",
                "Dosage": "Injection",
                "Strength / Size": "100mg/mL (10%) (10mL \r\namp)"
            },
            {
                "Medicine Name": "Calcium gluconate",
                "Dosage": "Injection",
                "Strength / Size": "100mg/mL (10%) (10mL \r\namp)"
            },
            {
                "Medicine Name": "Capecitabine",
                "Dosage": "Tablet",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Capecitabine",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Capecitabine",
                "Dosage": "Tablet",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Capecitabine",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Carbamazepine",
                "Dosage": "Oral liquid",
                "Strength / Size": "100mg/5mL"
            },
            {
                "Medicine Name": "Carbamazepine",
                "Dosage": "Tablet (cross-scored)",
                "Strength / Size": "200mg (cross-scored)"
            },
            {
                "Medicine Name": "Carbamazepine",
                "Dosage": "Tablet (cross-scored)",
                "Strength / Size": "200mg"
            },
            {
                "Medicine Name": "Carbetocin",
                "Dosage": "Injection (heat stable)",
                "Strength / Size": "100 micrograms/mL"
            },
            {
                "Medicine Name": "Carbimazole",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Carboplatin",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (15mL vial)"
            },
            {
                "Medicine Name": "Carboplatin",
                "Strength / Size": "10mg/mL (45mL vial)"
            },
            {
                "Medicine Name": "Carvedilol",
                "Dosage": "Tablet",
                "Strength / Size": "6.25mg"
            },
            {
                "Medicine Name": "Carvedilol",
                "Strength / Size": "12.5mg"
            },
            {
                "Medicine Name": "Carvedilol",
                "Dosage": "Tablet",
                "Strength / Size": "6.25mg"
            },
            {
                "Medicine Name": "Carvedilol",
                "Strength / Size": "12.5mg"
            },
            {
                "Medicine Name": "Carvedilol",
                "Dosage": "Tablet",
                "Strength / Size": "6.25mg"
            },
            {
                "Medicine Name": "Carvedilol",
                "Strength / Size": "12.5mg"
            },
            {
                "Medicine Name": "Carvedilol",
                "Dosage": "Tablet",
                "Strength / Size": "12.5mg"
            },
            {
                "Medicine Name": "Cefazolin",
                "Dosage": "PFI",
                "Strength / Size": "1g (as sodium salt) in \r\nvial"
            },
            {
                "Medicine Name": "Cefixime",
                "Dosage": "Tablet",
                "Strength / Size": "400mg (as trihydrate)"
            },
            {
                "Medicine Name": "Ceftazidime",
                "Dosage": "PFI",
                "Strength / Size": "250mg (as \r\npentahydrate) vial"
            },
            {
                "Medicine Name": "Ceftazidime",
                "Strength / Size": "1g (as pentahydrate) vial"
            },
            {
                "Medicine Name": "Ceftriaxone",
                "Dosage": "Injection (IM/IV)",
                "Strength / Size": "250mg  (as sodium salt) \r\n[c]107"
            },
            {
                "Medicine Name": "Ceftriaxone",
                "Strength / Size": "1g (as sodium salt)108"
            },
            {
                "Medicine Name": "Celecoxib",
                "Dosage": "Tablet",
                "Strength / Size": "200mg"
            },
            {
                "Medicine Name": "Chlorambucil",
                "Dosage": "Tablet",
                "Strength / Size": "2mg"
            },
            {
                "Medicine Name": "Chlorhexidine",
                "Dosage": "Solution for dilution",
                "Strength / Size": "5% (as gluconate/ \r\ndigluconate)"
            },
            {
                "Medicine Name": "Chlorhexidine",
                "Dosage": "Gel",
                "Strength / Size": "7.1% (as digluconate) (20 \r\ng tube) [c]"
            },
            {
                "Medicine Name": "Chlorhexidine",
                "Dosage": "Solution (mouthwash)",
                "Strength / Size": "0.2% (as \r\ngluconate/digluconate)"
            },
            {
                "Medicine Name": "Chlorpheniramine",
                "Dosage": "Injection52",
                "Strength / Size": "10mg (as maleate)/1mL \r\namp"
            },
            {
                "Medicine Name": "Chlorpheniramine",
                "Dosage": "Oral liquid53",
                "Strength / Size": "2mg (as maleate)/5mL"
            },
            {
                "Medicine Name": "Chlorpromazine",
                "Dosage": "Injection",
                "Strength / Size": "25mg/mL (as HCl) (2mL \r\namp)"
            },
            {
                "Medicine Name": "Chlorpromazine",
                "Dosage": "Tablet",
                "Strength / Size": "50mg (as HCl)451"
            },
            {
                "Medicine Name": "Chlorpromazine",
                "Strength / Size": "100mg (as HCl)"
            },
            {
                "Medicine Name": "Cholecalciferol (Vit D3)",
                "Dosage": "Oral liquid (drops)533",
                "Strength / Size": "400 IU/mL [c]"
            },
            {
                "Medicine Name": "Cholecalciferol (Vit D3)",
                "Dosage": "Injection (IM/Oral)534",
                "Strength / Size": "300,000 IU/1mL amp"
            },
            {
                "Medicine Name": "Cholera vaccine",
                "Dosage": "Oral suspension",
                "Strength / Size": "1.5mL vial (single dose)  \r\nsingle dose vial"
            },
            {
                "Medicine Name": "Cinnarizine",
                "Dosage": "Tablet",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Ciprofloxacin",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "500mg (as HCl)"
            },
            {
                "Medicine Name": "Ciprofloxacin",
                "Dosage": "Solution (ear drops)",
                "Strength / Size": "0.3% (as HCl)"
            },
            {
                "Medicine Name": "Ciprofloxacin +   Dexamethasone",
                "Dosage": "Solution (ear drops)",
                "Strength / Size": "0.3% (as HCl) + 0.1%"
            },
            {
                "Medicine Name": "Cisatracurium",
                "Dosage": "Injection",
                "Strength / Size": "2mg (as besilate)/mL  \r\n(10mL amp)"
            },
            {
                "Medicine Name": "Cisplatin",
                "Dosage": "Injection",
                "Strength / Size": "1mg/mL (50mL vial)"
            },
            {
                "Medicine Name": "Clarithromycin",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Clindamycin",
                "Dosage": "Capsule",
                "Strength / Size": "150mg (as HCl)"
            },
            {
                "Medicine Name": "Clindamycin",
                "Dosage": "Injection",
                "Strength / Size": "150mg (as \r\nphosphate)/mL (2mL \r\nvial)"
            },
            {
                "Medicine Name": "Clindamycin",
                "Dosage": "Oral liquid",
                "Strength / Size": "75mg (as \r\npalmitate)/5mL [c]"
            },
            {
                "Medicine Name": "Clobetasone propionate",
                "Dosage": "Ointment",
                "Strength / Size": "0.05%"
            },
            {
                "Medicine Name": "Clofazamine",
                "Dosage": "Capsule",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Clofazamine",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Clofazimine (Cfx)",
                "Dosage": "Capsule",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Clofazimine (Cfx)",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Clomifene (Clomiphene)",
                "Dosage": "Tablet",
                "Strength / Size": "50mg (as citrate)"
            },
            {
                "Medicine Name": "Clopidogrel",
                "Dosage": "Tablet",
                "Strength / Size": "75mg"
            },
            {
                "Medicine Name": "Clotrimazole",
                "Dosage": "Vaginal tablet",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Clotrimazole",
                "Dosage": "Cream",
                "Strength / Size": "1%"
            },
            {
                "Medicine Name": "Clotrimazole",
                "Dosage": "Solution (ear drops)",
                "Strength / Size": "1%"
            },
            {
                "Medicine Name": "Clozapine",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Coagulation factor IX",
                "Dosage": "PFI (Extended half-life)",
                "Strength / Size": "250 IU/vial"
            },
            {
                "Medicine Name": "Coagulation factor IX",
                "Strength / Size": "500 IU/vial"
            },
            {
                "Medicine Name": "Coagulation factor IX",
                "Strength / Size": "1,000 IU vial"
            },
            {
                "Medicine Name": "Coagulation factor VIII",
                "Dosage": "PFI (Extended half-life)",
                "Strength / Size": "250 IU vial"
            },
            {
                "Medicine Name": "Coagulation factor VIII",
                "Strength / Size": "500 IU vial"
            },
            {
                "Medicine Name": "Coagulation factor VIII",
                "Strength / Size": "1,000 IU vial"
            },
            {
                "Medicine Name": "Colchicine",
                "Dosage": "Tablet",
                "Strength / Size": "500 micrograms"
            },
            {
                "Medicine Name": "Colistin",
                "Dosage": "PFI",
                "Strength / Size": "1MU (as colistimethate \r\nsodium) vial"
            },
            {
                "Medicine Name": "Collagenase   clostridiopeptidase A  +  Proteases",
                "Dosage": "Ointment",
                "Strength / Size": "1.2 units + 0.24 units \r\n(15g)"
            },
            {
                "Medicine Name": "Conjugated Estrogens",
                "Dosage": "Tablet380",
                "Strength / Size": "300 micrograms"
            },
            {
                "Medicine Name": "Conjugated Estrogens",
                "Dosage": "Cream (Vaginal)381",
                "Strength / Size": "0.625mg/g (30g)"
            },
            {
                "Medicine Name": "Copper 64 (Cu 64)",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Copper-containing  device"
            },
            {
                "Medicine Name": "Cotrimoxazole  (Sulfamethoxazole +   Trimethoprim)",
                "Dosage": "Injection122",
                "Strength / Size": "96mg/mL (5mL amp)"
            },
            {
                "Medicine Name": "Cotrimoxazole  (Sulfamethoxazole +   Trimethoprim)",
                "Dosage": "Oral liquid123",
                "Strength / Size": "240mg/5mL [c]"
            },
            {
                "Medicine Name": "Cotrimoxazole  (Sulfamethoxazole +   Trimethoprim)",
                "Dosage": "Tablet (scored)123",
                "Strength / Size": "800 + 160mg"
            },
            {
                "Medicine Name": "Cotrimoxazole  (Sulfamethoxazole +   Trimethoprim)",
                "Dosage": "Oral liquid",
                "Strength / Size": "240mg/5mL [c]"
            },
            {
                "Medicine Name": "Cotrimoxazole  (Sulfamethoxazole +   Trimethoprim)",
                "Dosage": "Tablet",
                "Strength / Size": "800 + 160mg"
            },
            {
                "Medicine Name": "Cotrimoxazole  (Sulfamethoxazole +   Trimethoprim)",
                "Dosage": "Injection",
                "Strength / Size": "96mg/mL (5mL amp)"
            },
            {
                "Medicine Name": "Cotrimoxazole  (Sulfamethoxazole +   Trimethoprim)",
                "Dosage": "Oral liquid",
                "Strength / Size": "240mg/5mL [c]"
            },
            {
                "Medicine Name": "Cotrimoxazole  (Sulfamethoxazole +   Trimethoprim)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "800 + 160mg"
            },
            {
                "Medicine Name": "Crotamiton",
                "Dosage": "Cream",
                "Strength / Size": "10% (30g)"
            },
            {
                "Medicine Name": "Crotamiton",
                "Dosage": "Cream",
                "Strength / Size": "10% (30g)"
            },
            {
                "Medicine Name": "Cyclophosphamide",
                "Dosage": "PFI",
                "Strength / Size": "500mg vial"
            },
            {
                "Medicine Name": "Cyclophosphamide",
                "Strength / Size": "1g vial"
            },
            {
                "Medicine Name": "Cyclophosphamide",
                "Dosage": "PFI",
                "Strength / Size": "500mg vial"
            },
            {
                "Medicine Name": "Cyclophosphamide",
                "Dosage": "PFI",
                "Strength / Size": "1g vial"
            },
            {
                "Medicine Name": "Cyclophosphamide",
                "Dosage": "Tablet",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Cycloserine (Cs)",
                "Dosage": "Tablet",
                "Strength / Size": "125mg [c]"
            },
            {
                "Medicine Name": "Cycloserine (Cs)",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Cyclosporin",
                "Dosage": "Capsule",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Cyclosporin",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Cyclosporin",
                "Dosage": "Concentrate for  \r\ninjection196",
                "Strength / Size": "50mg/mL in 1mL amp"
            },
            {
                "Medicine Name": "Cytarabine",
                "Dosage": "PFI",
                "Strength / Size": "100mg vial"
            },
            {
                "Medicine Name": "Cytarabine",
                "Strength / Size": "1g vial"
            },
            {
                "Medicine Name": "Dacarbazine",
                "Dosage": "PFI",
                "Strength / Size": "200mg vial (as citrate)"
            },
            {
                "Medicine Name": "Dactinomycin   (Actinomycin D)",
                "Dosage": "PFI",
                "Strength / Size": "500 micrograms vial"
            },
            {
                "Medicine Name": "Danazol",
                "Dosage": "Capsule",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Dantrolene",
                "Dosage": "Injection",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Dantrolene",
                "Dosage": "Injection",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Dapsone",
                "Dosage": "Tablet",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Dapsone",
                "Dosage": "Tablet",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Dapsone",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Darunavir (DRV)",
                "Dosage": "Tablet",
                "Strength / Size": "75mg"
            },
            {
                "Medicine Name": "Darunavir (DRV)",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Darunavir (DRV)",
                "Dosage": "Tablet (f/c)",
                "Strength / Size": "600mg"
            },
            {
                "Medicine Name": "Darunavir (DRV)",
                "Dosage": "Oral liquid",
                "Strength / Size": "10mg/mL (200mL)"
            },
            {
                "Medicine Name": "Daunorubicin",
                "Dosage": "PFI",
                "Strength / Size": "20mg vial (as HCl)"
            },
            {
                "Medicine Name": "Daunorubicin",
                "Strength / Size": "50mg vial (as HCl)"
            },
            {
                "Medicine Name": "Deferasirox",
                "Dosage": "Tablet",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Deferoxamine",
                "Dosage": "PFI",
                "Strength / Size": "500mg (as mesilate) vial"
            },
            {
                "Medicine Name": "Deferoxamine mesilate",
                "Dosage": "PFI",
                "Strength / Size": "500mg vial"
            },
            {
                "Medicine Name": "Delamanid (Dlm)",
                "Dosage": "Tablet",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Dexamethasone",
                "Dosage": "Injection",
                "Strength / Size": "4mg (as sodium  \r\nphosphate)/1mL amp"
            },
            {
                "Medicine Name": "Dexamethasone",
                "Dosage": "Tablet",
                "Strength / Size": "500 micrograms"
            },
            {
                "Medicine Name": "Dexamethasone",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "4mg"
            },
            {
                "Medicine Name": "Dexamethasone",
                "Dosage": "Injection",
                "Strength / Size": "4mg (as sodium  \r\nphosphate)/1mL amp"
            },
            {
                "Medicine Name": "Dexamethasone",
                "Dosage": "Injection",
                "Strength / Size": "4mg/1mL amp (as \r\nsodium phosphate)"
            },
            {
                "Medicine Name": "Dexamethasone",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "4mg"
            },
            {
                "Medicine Name": "Dexamethasone",
                "Dosage": "Tablet",
                "Strength / Size": "4mg"
            },
            {
                "Medicine Name": "Dexamethasone",
                "Dosage": "Injection",
                "Strength / Size": "4mg (as disodium  \r\nphosphate)/mL"
            },
            {
                "Medicine Name": "Dexketoprofen",
                "Dosage": "Tablet",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Dexmedetomidine",
                "Dosage": "Injection",
                "Strength / Size": "100 micrograms/mL \r\n(2mL)"
            },
            {
                "Medicine Name": "Dexmedetomidine",
                "Dosage": "Injection",
                "Strength / Size": "100 micrograms/mL \r\n(2mL)"
            },
            {
                "Medicine Name": "Diazepam",
                "Dosage": "Injection",
                "Strength / Size": "5mg/mL (2mL amp)"
            },
            {
                "Medicine Name": "Diazepam",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Diazepam",
                "Dosage": "Rectal gel",
                "Strength / Size": "5mg/mL (0.5mL tube)"
            },
            {
                "Medicine Name": "Dienogest",
                "Dosage": "Tablet",
                "Strength / Size": "2mg"
            },
            {
                "Medicine Name": "Diethylcarbamazine (DEC)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "100mg  \r\n(as dihydrogen citrate)"
            },
            {
                "Medicine Name": "Diethylstilboestrol  (DES)",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Digoxin",
                "Dosage": "Oral liquid305",
                "Strength / Size": "50 micrograms/mL"
            },
            {
                "Medicine Name": "Digoxin",
                "Dosage": "Tablet",
                "Strength / Size": "250 micrograms"
            },
            {
                "Medicine Name": "Digoxin",
                "Dosage": "Oral liquid318",
                "Strength / Size": "50 micrograms/mL"
            },
            {
                "Medicine Name": "Digoxin",
                "Dosage": "Tablet",
                "Strength / Size": "125 micrograms"
            },
            {
                "Medicine Name": "Dihydroartemisinin +   Piperaquine (DHA-PPQ)",
                "Dosage": "Tablet",
                "Strength / Size": "20mg + 160mg"
            },
            {
                "Medicine Name": "Dihydroartemisinin +   Piperaquine (DHA-PPQ)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "40mg + 320mg"
            },
            {
                "Medicine Name": "Dihydrocodeine   phosphate",
                "Dosage": "Tablet",
                "Strength / Size": "30mg"
            },
            {
                "Medicine Name": "Diloxanide",
                "Dosage": "Tablet",
                "Strength / Size": "500mg (as furoate)"
            },
            {
                "Medicine Name": "Diloxanide furoate +   Metronidazole",
                "Dosage": "Oral liquid",
                "Strength / Size": "250mg + 200mg"
            },
            {
                "Medicine Name": "Diloxanide furoate +   Metronidazole",
                "Dosage": "Tablet",
                "Strength / Size": "500mg + 400mg"
            },
            {
                "Medicine Name": "Dimercaptosuccinic acid (DMSA)"
            },
            {
                "Medicine Name": "Distilled water",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Dithranol",
                "Dosage": "Paste",
                "Strength / Size": "2%"
            },
            {
                "Medicine Name": "Divalproex sodium",
                "Dosage": "Tablet",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Divalproex sodium",
                "Dosage": "Tablet",
                "Strength / Size": "750mg"
            },
            {
                "Medicine Name": "Dobutamine",
                "Dosage": "Injection (solution)",
                "Strength / Size": "12.5mg/mL (20mL)"
            },
            {
                "Medicine Name": "Docetaxel",
                "Dosage": "Injection (premixed)",
                "Strength / Size": "20mg vial"
            },
            {
                "Medicine Name": "Docetaxel",
                "Strength / Size": "80mg vial"
            },
            {
                "Medicine Name": "Dolutegravir (DTG)",
                "Dosage": "Tablet",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Domperidone",
                "Dosage": "Oral liquid",
                "Strength / Size": "5mg/5mL"
            },
            {
                "Medicine Name": "Domperidone",
                "Dosage": "Tablet",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Dopamine",
                "Dosage": "Injection",
                "Strength / Size": "40mg/mL (as HCl) (5mL \r\nvial)"
            },
            {
                "Medicine Name": "Dorzolamide",
                "Dosage": "Eye drops",
                "Strength / Size": "2% (as HCl)"
            },
            {
                "Medicine Name": "Doxazosin",
                "Dosage": "Tablet",
                "Strength / Size": "2mg"
            },
            {
                "Medicine Name": "Doxorubicin",
                "Dosage": "PFI or Solution for \r\nInjection219",
                "Strength / Size": "10mg vial (as HCl)"
            },
            {
                "Medicine Name": "Doxorubicin",
                "Strength / Size": "50mg vial (as HCl)"
            },
            {
                "Medicine Name": "Doxycycline",
                "Dosage": "Tablet / Capsule",
                "Strength / Size": "100mg (as hyclate)"
            },
            {
                "Medicine Name": "Doxycycline",
                "Dosage": "Capsule",
                "Strength / Size": "100mg (as HCl \r\nor hyclate)"
            },
            {
                "Medicine Name": "Doxycycline",
                "Dosage": "Capsule",
                "Strength / Size": "100mg (as HCl)"
            },
            {
                "Medicine Name": "DPT + HiB + Hep B vaccine  (pentavalent)",
                "Dosage": "Injection (suspension)",
                "Strength / Size": "5mL vial (10 doses)"
            },
            {
                "Medicine Name": "Efavirenz (EFV)",
                "Dosage": "Tablet",
                "Strength / Size": "200mg (cross-scored) \r\n[c]"
            },
            {
                "Medicine Name": "Eflornithine",
                "Dosage": "Injection",
                "Strength / Size": "200mg (as \r\nHCl)/mL in 100mL bottle"
            },
            {
                "Medicine Name": "Enalapril",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "5mg (as hydrogen \r\nmaleate)"
            },
            {
                "Medicine Name": "Enalapril",
                "Dosage": "Tablet",
                "Strength / Size": "10mg  \r\n(as hydrogen maleate)"
            },
            {
                "Medicine Name": "Enalapril",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "5mg (as hydrogen \r\nmaleate)"
            },
            {
                "Medicine Name": "Enoxaparin",
                "Dosage": "Injection (prefilled and \r\ncalibrated syringe)",
                "Strength / Size": "40mg/0.4mL"
            },
            {
                "Medicine Name": "Enoxaparin",
                "Strength / Size": "80mg/0.8mL"
            },
            {
                "Medicine Name": "Entecavir",
                "Dosage": "Oral liquid",
                "Strength / Size": "0.05mg/mL"
            },
            {
                "Medicine Name": "Entecavir",
                "Dosage": "Tablet",
                "Strength / Size": "0.5mg"
            },
            {
                "Medicine Name": "Ephedrine",
                "Dosage": "Injection",
                "Strength / Size": "30mg (as HCl)/1mL"
            },
            {
                "Medicine Name": "Epinephrine  (adrenaline)",
                "Dosage": "Injection",
                "Strength / Size": "1mg/1mL amp"
            },
            {
                "Medicine Name": "Epinephrine (adrenaline)",
                "Dosage": "Injection",
                "Strength / Size": "1mg (as sodium  \r\nphosphate)/1mL amp"
            },
            {
                "Medicine Name": "Ergocalciferol (Vit D2)",
                "Dosage": "Oral liquid",
                "Strength / Size": "250 micrograms (10,000 \r\nIU)/mL"
            },
            {
                "Medicine Name": "Ergocalciferol (Vit D2)",
                "Dosage": "Tablet / Capsule",
                "Strength / Size": "250 micrograms (10,000 \r\nIU)"
            },
            {
                "Medicine Name": "Ergocalciferol (Vit D2)",
                "Strength / Size": "1.25mg (50,000 IU)"
            },
            {
                "Medicine Name": "Ergometrine",
                "Dosage": "Injection",
                "Strength / Size": "500 micrograms  \r\n(as hydrogen \r\nmaleate)/1mL amp"
            },
            {
                "Medicine Name": "Ertapenem ",
                "Dosage": "PFI",
                "Strength / Size": "1g"
            },
            {
                "Medicine Name": "Erythromycin",
                "Dosage": "Eye ointment",
                "Strength / Size": "0.5% [c]"
            },
            {
                "Medicine Name": "Erythropoetin (alpha or  beta) stimulating agents",
                "Dosage": "Injection  \r\n(prefilled syringe)",
                "Strength / Size": "2,000 IU/ 0.5mL"
            },
            {
                "Medicine Name": "Escitalopram",
                "Dosage": "Tablet",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Escitalopram",
                "Dosage": "Tablet",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Estradiol",
                "Dosage": "Transdermal patch",
                "Strength / Size": "0.1mg/day"
            },
            {
                "Medicine Name": "Etanercept",
                "Dosage": "Injection",
                "Strength / Size": "25mg vial492"
            },
            {
                "Medicine Name": "Etanercept",
                "Strength / Size": "50mg vial493"
            },
            {
                "Medicine Name": "Etanercept",
                "Dosage": "Injection",
                "Strength / Size": "25mg vial"
            },
            {
                "Medicine Name": "Etanercept",
                "Dosage": "Injection",
                "Strength / Size": "50mg vial"
            },
            {
                "Medicine Name": "Ethambutol (E)",
                "Dosage": "Tablet",
                "Strength / Size": "100mg (dispersible)"
            },
            {
                "Medicine Name": "Ethambutol (E)",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Ethanol",
                "Dosage": "Injection",
                "Strength / Size": "100% (10mL amp)"
            },
            {
                "Medicine Name": "Ethanol",
                "Dosage": "Solution",
                "Strength / Size": "70% (denatured)"
            },
            {
                "Medicine Name": "Ethanol, Medicinal",
                "Dosage": "Oral liquid",
                "Strength / Size": "95-96%"
            },
            {
                "Medicine Name": "Ethinylestradiol +   Norethisterone",
                "Dosage": "Tablet",
                "Strength / Size": "35 micrograms + 1mg"
            },
            {
                "Medicine Name": "Etoposide",
                "Dosage": "Capsule",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Etoposide",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Etoposide",
                "Dosage": "Injection",
                "Strength / Size": "20mg/mL (5mL vial)"
            },
            {
                "Medicine Name": "Etravirine (ETV)",
                "Dosage": "Tablet",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Etravirine (ETV)",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Etravirine (ETV)",
                "Strength / Size": "200mg"
            },
            {
                "Medicine Name": "Everolimus",
                "Dosage": "Tablet",
                "Strength / Size": "500 micrograms (or \r\n0.5mg)"
            },
            {
                "Medicine Name": "Fat (lipid)",
                "Dosage": "Infusion (emulsion) (IV)",
                "Strength / Size": "20% (100mL) [c]560"
            },
            {
                "Medicine Name": "Fat (lipid)",
                "Strength / Size": "20% (500mL)561"
            },
            {
                "Medicine Name": "Fat-soluble vitamins   (for adults)",
                "Strength / Size": "10mL563"
            },
            {
                "Medicine Name": "Fat-soluble vitamins   (for infants and children)",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "10mL [c]562"
            },
            {
                "Medicine Name": "Febuxostat",
                "Dosage": "Tablet",
                "Strength / Size": "40mg"
            },
            {
                "Medicine Name": "Fentanyl",
                "Dosage": "Injection  \r\n(preservative-free)",
                "Strength / Size": "50 micrograms  \r\n(as citrate)/mL (2mL \r\namp)"
            },
            {
                "Medicine Name": "Fentanyl",
                "Dosage": "Transdermal patch",
                "Strength / Size": "25 micrograms/hr42"
            },
            {
                "Medicine Name": "Fentanyl",
                "Dosage": "Transdermal patch",
                "Strength / Size": "50 micrograms/hr43"
            },
            {
                "Medicine Name": "Ferrous salt",
                "Dosage": "Oral liquid (drops)",
                "Strength / Size": "Equivalent to 25mg \r\n(iron as sulphate)/mL"
            },
            {
                "Medicine Name": "Ferrous salt",
                "Dosage": "Tablet (f/c)",
                "Strength / Size": "60-65mg elemental iron"
            },
            {
                "Medicine Name": "Ferrous salt + Folic acid",
                "Dosage": "Tablet",
                "Strength / Size": "60-65mg elemental iron \r\n+ 400 micrograms"
            },
            {
                "Medicine Name": "Filgrastim",
                "Dosage": "Injection (prefilled \r\nsyringe)",
                "Strength / Size": "120 micrograms/0.2mL"
            },
            {
                "Medicine Name": "Filgrastim",
                "Strength / Size": "300 micrograms/0.5mL"
            },
            {
                "Medicine Name": "Finasteride",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Flucloxacillin",
                "Dosage": "Capsule110",
                "Strength / Size": "250mg (as sodium salt)"
            },
            {
                "Medicine Name": "Flucloxacillin",
                "Dosage": "PFOL110",
                "Strength / Size": "125mg (as sodium \r\nsalt)/5mL"
            },
            {
                "Medicine Name": "Flucloxacillin",
                "Dosage": "PFI111",
                "Strength / Size": "500mg (as sodium salt) \r\nvial"
            },
            {
                "Medicine Name": "Fluconazole",
                "Dosage": "Tablet / Capsule",
                "Strength / Size": "150mg139"
            },
            {
                "Medicine Name": "Fluconazole",
                "Strength / Size": "200mg"
            },
            {
                "Medicine Name": "Fluconazole",
                "Dosage": "Injection140",
                "Strength / Size": "2mg/mL (100mL bottle)"
            },
            {
                "Medicine Name": "Fluconazole",
                "Dosage": "Oral liquid140",
                "Strength / Size": "50mg/5mL"
            },
            {
                "Medicine Name": "Flucytosine",
                "Dosage": "Capsule",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Fludrocortisone",
                "Dosage": "Tablet",
                "Strength / Size": "100 micrograms  \r\n(as acetate)"
            },
            {
                "Medicine Name": "Flumazenil",
                "Dosage": "Injection",
                "Strength / Size": "100 micrograms/mL  \r\n(5mL amp)"
            },
            {
                "Medicine Name": "Fluorescein",
                "Dosage": "Test strip",
                "Strength / Size": "0.6mg"
            },
            {
                "Medicine Name": "Fluorodeoxyglucose (FDG)",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Fluoromethalone",
                "Dosage": "Eye drops",
                "Strength / Size": "0.1%"
            },
            {
                "Medicine Name": "Fluorouracil",
                "Dosage": "Injection",
                "Strength / Size": "50mg/mL (5mL vial)"
            },
            {
                "Medicine Name": "Fluoxetine",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "20mg (as HCl)"
            },
            {
                "Medicine Name": "Flupentixol",
                "Dosage": "Injection (oily, depot)",
                "Strength / Size": "20mg/mL (as \r\ndecanoate) (2mL amp)"
            },
            {
                "Medicine Name": "Fluphenazine",
                "Dosage": "Injection (oily, depot)",
                "Strength / Size": "25mg/1mL (as \r\ndecanoate) amp"
            },
            {
                "Medicine Name": "Fluticasone",
                "Dosage": "Nasal spray",
                "Strength / Size": "27.5 micrograms  \r\n(as propionate or \r\nfuroate)"
            },
            {
                "Medicine Name": "Folic acid",
                "Dosage": "Tablet",
                "Strength / Size": "400 micrograms283"
            },
            {
                "Medicine Name": "Folic acid",
                "Strength / Size": "5mg284"
            },
            {
                "Medicine Name": "Fomepizole",
                "Dosage": "Injection",
                "Strength / Size": "5mg (as sulphate)/mL \r\n(20mL amp)"
            },
            {
                "Medicine Name": "Fortified Blended Food  (FBF)",
                "Dosage": "Flour",
                "Strength / Size": "415kcal/100g (Sachet)596"
            },
            {
                "Medicine Name": "Fortified Blended Food  (FBF)",
                "Strength / Size": "435kcal/100g (Sachet)597"
            },
            {
                "Medicine Name": "Fortified Blended Food  (FBF)",
                "Strength / Size": "450kcal/100g (Sachet)598"
            },
            {
                "Medicine Name": "Fortified Blended Food  (FBF)",
                "Strength / Size": "1,000 kcal/250g (Bag or \r\nSachet)599"
            },
            {
                "Medicine Name": "Fosaprepitant",
                "Dosage": "Injection",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Fosfomycin",
                "Dosage": "Granules for oral  \r\nsuspension127",
                "Strength / Size": "3g sachet"
            },
            {
                "Medicine Name": "Fosfomycin",
                "Dosage": "PFI128",
                "Strength / Size": "3g (as sodium) vial"
            },
            {
                "Medicine Name": "Furosemide",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (2mL amp)"
            },
            {
                "Medicine Name": "Furosemide",
                "Dosage": "Tablet (cross-scored)320",
                "Strength / Size": "40mg"
            },
            {
                "Medicine Name": "Furosemide",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (2mL amp)"
            },
            {
                "Medicine Name": "Furosemide",
                "Dosage": "Oral liquid",
                "Strength / Size": "20mg/5mL [c]361"
            },
            {
                "Medicine Name": "Furosemide",
                "Dosage": "Tablet (cross-scored)",
                "Strength / Size": "40mg"
            },
            {
                "Medicine Name": "Fusidic acid",
                "Dosage": "Ointment",
                "Strength / Size": "2% (15g)"
            },
            {
                "Medicine Name": "Gabapentin",
                "Dosage": "Tablet",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Gabapentin",
                "Dosage": "Tablet",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Gadobutrol",
                "Dosage": "Injection (solution) (IV)",
                "Strength / Size": "1mmol/mL (7.5mL)355"
            },
            {
                "Medicine Name": "Gadobutrol",
                "Dosage": "Injection (solution) (IV)",
                "Strength / Size": "1mmol/mL (15mL)355"
            },
            {
                "Medicine Name": "Gadodiamide",
                "Dosage": "Injection (solution) (IV)",
                "Strength / Size": "0.5 mmol/mL (20mL)356"
            },
            {
                "Medicine Name": "Gadopentate   dimeglumine",
                "Dosage": "Injection (solution) (IV)",
                "Strength / Size": "0.5 mmol/mL (10mL)357"
            },
            {
                "Medicine Name": "Gadopentate   dimeglumine",
                "Strength / Size": "0.5 mmol/mL (15mL)357"
            },
            {
                "Medicine Name": "Gallium-68 dotatate",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Gancyclovir",
                "Dosage": "PFI",
                "Strength / Size": "500mg vial"
            },
            {
                "Medicine Name": "Gefitinib",
                "Dosage": "Tablet",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Gelatin-based colloid",
                "Dosage": "Solution for Infusion",
                "Strength / Size": "4%"
            },
            {
                "Medicine Name": "Gemcitabine",
                "Dosage": "PFI",
                "Strength / Size": "200mg vial"
            },
            {
                "Medicine Name": "Gemcitabine",
                "Strength / Size": "1g vial"
            },
            {
                "Medicine Name": "Gentamicin",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (as sulphate)  \r\n(2mL vial)"
            },
            {
                "Medicine Name": "Gentamicin",
                "Strength / Size": "40mg/mL (as sulphate)  \r\n(2mL vial)"
            },
            {
                "Medicine Name": "Gentamicin",
                "Dosage": "Eye drops",
                "Strength / Size": "0.3% (as sulphate)"
            },
            {
                "Medicine Name": "Gentamicin +   Dexamethasone",
                "Dosage": "Eye drops",
                "Strength / Size": "0.3% + 0.1%"
            },
            {
                "Medicine Name": "Gliclazide",
                "Dosage": "Tablet (m/r)",
                "Strength / Size": "30mg"
            },
            {
                "Medicine Name": "Gliclazide",
                "Dosage": "Tablet (i/r)",
                "Strength / Size": "40mg"
            },
            {
                "Medicine Name": "Glucose",
                "Dosage": "Injectable solution",
                "Strength / Size": "5% (isotonic)  \r\n(500mL infusion pack)"
            },
            {
                "Medicine Name": "Glucose",
                "Strength / Size": "10% (hypertonic)  \r\n(500mL infusion pack)"
            },
            {
                "Medicine Name": "Glucose",
                "Strength / Size": "50% (hypertonic)  \r\n(50mL amp)522"
            },
            {
                "Medicine Name": "Glucose + Sodium   chloride",
                "Dosage": "Injectable solution",
                "Strength / Size": "5% + 0.9% [c]"
            },
            {
                "Medicine Name": "Glutaral",
                "Dosage": "Solution",
                "Strength / Size": "2%"
            },
            {
                "Medicine Name": "Glyceryl trinitrate",
                "Dosage": "Tablet (sublingual)",
                "Strength / Size": "500 micrograms"
            },
            {
                "Medicine Name": "Glycopyrronium",
                "Dosage": "Injection",
                "Strength / Size": "200 micrograms  \r\n(as bromide)/mL"
            },
            {
                "Medicine Name": "Golimumab",
                "Dosage": "Injection (solution) (SC)",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Goserelin",
                "Dosage": "Implant (in syringe \r\napplicator)",
                "Strength / Size": "3.6mg (as acetate)258"
            },
            {
                "Medicine Name": "Goserelin",
                "Strength / Size": "10.8mg (as acetate)257"
            },
            {
                "Medicine Name": "Goserelin",
                "Dosage": "Injection (depot, SC)",
                "Strength / Size": "3.6mg (as acetate)"
            },
            {
                "Medicine Name": "Griseofulvin",
                "Dosage": "Tablet",
                "Strength / Size": "125mg"
            },
            {
                "Medicine Name": "Griseofulvin",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Haemodialysis solution",
                "Dosage": "Parenteral solution",
                "Strength / Size": "Of appropriate  \r\ncomposition"
            },
            {
                "Medicine Name": "Haloperidol",
                "Dosage": "Injection",
                "Strength / Size": "5mg/1mL amp"
            },
            {
                "Medicine Name": "Haloperidol",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Haloperidol",
                "Dosage": "Injection",
                "Strength / Size": "5mg/1mL amp"
            },
            {
                "Medicine Name": "Haloperidol",
                "Dosage": "Injection (oily)",
                "Strength / Size": "50mg/1mL amp"
            },
            {
                "Medicine Name": "Haloperidol",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Halothane",
                "Dosage": "Inhalation",
                "Strength / Size": "250mL"
            },
            {
                "Medicine Name": "Heparin sodium",
                "Dosage": "Injection",
                "Strength / Size": "5,000 IU/mL (5mL vial)"
            },
            {
                "Medicine Name": "Hepatitis A vaccine",
                "Dosage": "Injection",
                "Strength / Size": "80 units (Paed)"
            },
            {
                "Medicine Name": "Hepatitis A vaccine",
                "Strength / Size": "160 units (Adult)"
            },
            {
                "Medicine Name": "Hepatitis B vaccine",
                "Dosage": "Injection (suspension)",
                "Strength / Size": "Single dose vial"
            },
            {
                "Medicine Name": "Hepatitis B vaccine",
                "Strength / Size": "Multi dose vial"
            },
            {
                "Medicine Name": "Hepatobiliary iminodiacetic acid (HIDA)"
            },
            {
                "Medicine Name": "Hexamethylpropyleneamineoxime (HMPAO)"
            },
            {
                "Medicine Name": "High calorie, high protein  formula",
                "Dosage": "Powder588",
                "Strength / Size": "200g"
            },
            {
                "Medicine Name": "High calorie, high protein  formula",
                "Dosage": "Diskettes589",
                "Strength / Size": "200g"
            },
            {
                "Medicine Name": "High energy, high protein  oral sip feed",
                "Dosage": "Liquid",
                "Strength / Size": "200mL"
            },
            {
                "Medicine Name": "HPV vaccine   (quadrivalent)",
                "Dosage": "Injection",
                "Strength / Size": "Single or multi dose vial"
            },
            {
                "Medicine Name": "Human albumin  infusion",
                "Dosage": "Solution",
                "Strength / Size": "5%"
            },
            {
                "Medicine Name": "Human albumin  infusion",
                "Strength / Size": "20%"
            },
            {
                "Medicine Name": "Human chorionic   gonadotropin (HCG)",
                "Dosage": "Injection",
                "Strength / Size": "5,000 IU/vial"
            },
            {
                "Medicine Name": "Human Epidermal growth  factor (recombinant)",
                "Dosage": "Gel (water-based)",
                "Strength / Size": "60 micrograms (15g)"
            },
            {
                "Medicine Name": "Human menopausal   gonadotropin (HMG)",
                "Dosage": "Injection",
                "Strength / Size": "75 IU"
            },
            {
                "Medicine Name": "Human Platelet derived  growth factor   (recombitant)",
                "Dosage": "Gel (water-based)",
                "Strength / Size": "100 micrograms (15g)"
            },
            {
                "Medicine Name": "Hydralazine",
                "Dosage": "Injection313",
                "Strength / Size": "20mg (as HCl)"
            },
            {
                "Medicine Name": "Hydralazine",
                "Dosage": "Tablet",
                "Strength / Size": "25mg (as HCl)"
            },
            {
                "Medicine Name": "Hydralazine",
                "Dosage": "Tablet",
                "Strength / Size": "50mg (as HCl)"
            },
            {
                "Medicine Name": "Hydralazine",
                "Dosage": "Tablet",
                "Strength / Size": "25mg (as HCl)"
            },
            {
                "Medicine Name": "Hydralazine",
                "Strength / Size": "50mg (as HCl)"
            },
            {
                "Medicine Name": "Hydrochlorothiazide  (HCTZ)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Hydrocortisone",
                "Dosage": "PFI",
                "Strength / Size": "100mg  \r\n(as sod. succinate) vial"
            },
            {
                "Medicine Name": "Hydrocortisone",
                "Dosage": "PFI",
                "Strength / Size": "100mg vial  \r\n(as sodium succinate)"
            },
            {
                "Medicine Name": "Hydrocortisone",
                "Dosage": "Cream",
                "Strength / Size": "1% (as acetate)"
            },
            {
                "Medicine Name": "Hydrocortisone",
                "Dosage": "Ointment",
                "Strength / Size": "1% (as acetate)"
            },
            {
                "Medicine Name": "Hydrocortisone",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Hydrocortisone",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Hydrogen peroxide",
                "Dosage": "Solution (ear drops)",
                "Strength / Size": "3% (stabilised)"
            },
            {
                "Medicine Name": "Hydroxocobalamin   (Vit B12)",
                "Dosage": "Injection",
                "Strength / Size": "1mg/1mL amp (as HCl,  \r\nacetate or sulphate)"
            },
            {
                "Medicine Name": "Hydroxycarbamide   (Hydroxyurea)",
                "Dosage": "SODF",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Hydroxycarbamide   (Hydroxyurea)",
                "Dosage": "Capsule",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Hydroxycarbamide   (Hydroxyurea)",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Hydroxycarbamide   (Hydroxyurea)",
                "Dosage": "SODF292",
                "Strength / Size": "100mg/45mL"
            },
            {
                "Medicine Name": "Hydroxychloroquine  (HCQ)",
                "Dosage": "Tablet",
                "Strength / Size": "200mg (as sulphate)"
            },
            {
                "Medicine Name": "Hydroxyethyl starch",
                "Dosage": "Solution for Infusion",
                "Strength / Size": "6%"
            },
            {
                "Medicine Name": "Hyoscine butylbromide",
                "Dosage": "Injection",
                "Strength / Size": "20mg/1mL amp"
            },
            {
                "Medicine Name": "Hyoscine butylbromide",
                "Dosage": "Tablet48",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Hypertonic saline",
                "Dosage": "Eye drops",
                "Strength / Size": "3%"
            },
            {
                "Medicine Name": "Hypocaloric sip feed with  fibre",
                "Dosage": "Liquid",
                "Strength / Size": "200mL"
            },
            {
                "Medicine Name": "Ibuprofen",
                "Dosage": "Oral liquid",
                "Strength / Size": "100mg/5mL [c]"
            },
            {
                "Medicine Name": "Ibuprofen",
                "Dosage": "Tablet",
                "Strength / Size": "200mg"
            },
            {
                "Medicine Name": "Ibuprofen",
                "Dosage": "Tablet",
                "Strength / Size": "200mg [c]"
            },
            {
                "Medicine Name": "Ibuprofen",
                "Dosage": "Injection solution",
                "Strength / Size": "5mg/mL (2mL amp) [c]"
            },
            {
                "Medicine Name": "Ifosfamide + Mesna",
                "Dosage": "Injection",
                "Strength / Size": "1g + 600mg"
            },
            {
                "Medicine Name": "Ifosfamide + Mesna",
                "Strength / Size": "2g + 1200mg"
            },
            {
                "Medicine Name": "Imatinib",
                "Dosage": "Tablet",
                "Strength / Size": "400mg (as mesylate)"
            },
            {
                "Medicine Name": "Imatinib",
                "Dosage": "Tablet",
                "Strength / Size": "100mg (as mesylate)"
            },
            {
                "Medicine Name": "Imatinib",
                "Strength / Size": "400mg (as mesylate)"
            },
            {
                "Medicine Name": "Iminodiacetic acid"
            },
            {
                "Medicine Name": "Imipenem + Cilastatin",
                "Dosage": "PFI",
                "Strength / Size": "250mg + 250mg vial"
            },
            {
                "Medicine Name": "Imipenem + Cilastatin",
                "Strength / Size": "500mg + 500mg vial"
            },
            {
                "Medicine Name": "Infliximab",
                "Dosage": "PFI",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Insulin,   intermediate-acting",
                "Dosage": "Injection",
                "Strength / Size": "100 IU/mL (10mL vial)"
            },
            {
                "Medicine Name": "Insulin, Long-acting  (basal) [Glargine]",
                "Dosage": "Injection",
                "Strength / Size": "100 IU/mL (10mL vial)"
            },
            {
                "Medicine Name": "Insulin, Premixed   (Short acting +   Intermediate acting)",
                "Dosage": "Injection",
                "Strength / Size": "100 IU/mL (10mL vial)"
            },
            {
                "Medicine Name": "Insulin, Premixed   (Ultra short acting +   Intermediate acting)",
                "Dosage": "Injection",
                "Strength / Size": "100 IU/mL (10mL vial)"
            },
            {
                "Medicine Name": "Insulin, Short acting   (Soluble)",
                "Dosage": "Injection",
                "Strength / Size": "100 IU/mL (10mL vial)"
            },
            {
                "Medicine Name": "Insulin, Ultra short-acting  (Rapid)",
                "Dosage": "Injection",
                "Strength / Size": "100 IU/mL (10mL vial)"
            },
            {
                "Medicine Name": "Intraperitoneal dialysis  solution (CAPD)",
                "Dosage": "Parenteral solution",
                "Strength / Size": "Of appropriate  \r\ncomposition"
            },
            {
                "Medicine Name": "Iodine 123",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Iodine 131",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Ipratropium bromide",
                "Dosage": "Inhalation (aerosol)",
                "Strength / Size": "20 micrograms/metered \r\ndose (200 dose)"
            },
            {
                "Medicine Name": "Ipratropium bromide",
                "Dosage": "Nebuliser solution",
                "Strength / Size": "500 micrograms/2mL \r\nunit dose vial (isotonic)"
            },
            {
                "Medicine Name": "Irinotecan",
                "Dosage": "Injection",
                "Strength / Size": "20mg/mL (2mL vial)"
            },
            {
                "Medicine Name": "Irinotecan",
                "Strength / Size": "20mg/mL (5mL vial)"
            },
            {
                "Medicine Name": "Iron sucrose",
                "Dosage": "Injection",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Isoflurane",
                "Dosage": "Inhalation",
                "Strength / Size": "250mL"
            },
            {
                "Medicine Name": "Isoniazid (H)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Isoniazid (H)",
                "Dosage": "Tablet",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Isoniazid (H)",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Iso-osmolar contrast  media",
                "Dosage": "Solution for IV \r\ninjection/infusion",
                "Strength / Size": "320mg iodine/mL \r\n(100mL)"
            },
            {
                "Medicine Name": "Isosorbide dinitrate",
                "Dosage": "Tablet",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Isosorbide dinitrate",
                "Dosage": "Tablet",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Itraconazole",
                "Dosage": "Capsule",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Ivabradine",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Ivabradine",
                "Dosage": "Tablet",
                "Strength / Size": "7.5mg"
            },
            {
                "Medicine Name": "Ivermectin",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "3mg"
            },
            {
                "Medicine Name": "Ivermectin",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "3mg"
            },
            {
                "Medicine Name": "Ketamine",
                "Dosage": "Injection",
                "Strength / Size": "50mg (as HCl)/mL (10mL \r\nvial)"
            },
            {
                "Medicine Name": "Ketamine",
                "Dosage": "Injection",
                "Strength / Size": "50mg (as HCl)/mL (10mL \r\nvial)"
            },
            {
                "Medicine Name": "Ketorolac",
                "Dosage": "Injection (IM/IV)",
                "Strength / Size": "30mg/mL"
            },
            {
                "Medicine Name": "Ketorolac trometamol",
                "Dosage": "Eye drops",
                "Strength / Size": "0.5%"
            },
            {
                "Medicine Name": "Labetalol",
                "Dosage": "Injection",
                "Strength / Size": "5mg/mL (20mL amp)"
            },
            {
                "Medicine Name": "Lactulose",
                "Dosage": "Oral liquid",
                "Strength / Size": "3.1-3.7g/5mL"
            },
            {
                "Medicine Name": "Lactulose",
                "Dosage": "Oral liquid",
                "Strength / Size": "3.1-3.7g/5mL"
            },
            {
                "Medicine Name": "Lamivudine (3TC)",
                "Dosage": "Oral liquid",
                "Strength / Size": "50mg/5mL"
            },
            {
                "Medicine Name": "Lamivudine (3TC)",
                "Dosage": "Tablet",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Lamivudine (3TC)",
                "Dosage": "Oral liquid",
                "Strength / Size": "50mg/5mL"
            },
            {
                "Medicine Name": "Lamotrigine",
                "Dosage": "Tablet",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Lamotrigine",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Lamotrigine",
                "Strength / Size": "5mg  \r\n(chewable, dispersible)"
            },
            {
                "Medicine Name": "Lamotrigine",
                "Strength / Size": "25mg  \r\n(chewable, dispersible)"
            },
            {
                "Medicine Name": "Lansoprazole",
                "Dosage": "Tablet (dispersible)",
                "Strength / Size": "15mg [c]"
            },
            {
                "Medicine Name": "Latanoprost",
                "Dosage": "Solution (eye-drops)",
                "Strength / Size": "0.005%"
            },
            {
                "Medicine Name": "Leflunomide",
                "Dosage": "Tablet",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Lenalidomide",
                "Dosage": "Capsule",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Lenalidomide",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Letrozole",
                "Dosage": "Tablets",
                "Strength / Size": "2.5mg"
            },
            {
                "Medicine Name": "Levetiracetam",
                "Dosage": "Injection (IV)80",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Levetiracetam",
                "Dosage": "Tablet (scored)81",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Levodopa + Carbidopa",
                "Dosage": "Tablet",
                "Strength / Size": "100mg + 10mg"
            },
            {
                "Medicine Name": "Levodopa + Carbidopa",
                "Strength / Size": "250mg + 25mg"
            },
            {
                "Medicine Name": "Levofloxacin (Lfx)",
                "Dosage": "Tablet (dispersible)",
                "Strength / Size": "100mg [c]"
            },
            {
                "Medicine Name": "Levofloxacin (Lfx)",
                "Dosage": "Tablet",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Levofloxacin (Lfx)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Levofloxacin (Lfx)",
                "Dosage": "Tablet",
                "Strength / Size": "750mg"
            },
            {
                "Medicine Name": "Levonorgestrel",
                "Dosage": "Tablet",
                "Strength / Size": "30 micrograms426"
            },
            {
                "Medicine Name": "Levonorgestrel",
                "Strength / Size": "1.5mg"
            },
            {
                "Medicine Name": "Levonorgestrel",
                "Dosage": "Tablet",
                "Strength / Size": "750 micrograms  \r\n(pack of 2)427"
            },
            {
                "Medicine Name": "Levonorgestrel (LNG)",
                "Dosage": "LNG-releasing  \r\nIntrauterine system \r\n(LNG-IUS)",
                "Strength / Size": "Reservoir with 52mg"
            },
            {
                "Medicine Name": "Levonorgestrel (LNG)",
                "Dosage": "LNG-releasing  \r\nIntrauterine system \r\n(LNG-IUS)",
                "Strength / Size": "Reservoir with 52mg"
            },
            {
                "Medicine Name": "Levonorgestrel-releasing  implant",
                "Dosage": "Implant",
                "Strength / Size": "150mg (2 x 75mg rods)"
            },
            {
                "Medicine Name": "Levothyroxine",
                "Dosage": "Tablet",
                "Strength / Size": "25 micrograms  \r\n(as sodium salt) [c]"
            },
            {
                "Medicine Name": "Levothyroxine",
                "Strength / Size": "50 micrograms (as \r\nsodium salt)"
            },
            {
                "Medicine Name": "Levothyroxine",
                "Strength / Size": "100 micrograms (as \r\nsodium salt)"
            },
            {
                "Medicine Name": "Lignocaine",
                "Dosage": "Injection  \r\n(preservative-free)28",
                "Strength / Size": "1% (as HCl) (vial)"
            },
            {
                "Medicine Name": "Lignocaine",
                "Dosage": "Injection",
                "Strength / Size": "2% (as HCl) (30mL vial)"
            },
            {
                "Medicine Name": "Lignocaine",
                "Dosage": "Topical spray",
                "Strength / Size": "2% (as HCl)"
            },
            {
                "Medicine Name": "Lignocaine",
                "Dosage": "Spray",
                "Strength / Size": "10mg/metered dose  \r\n(actuation)"
            },
            {
                "Medicine Name": "Lignocaine + Epinephrine  (Adrenaline)",
                "Dosage": "Dental cartridge",
                "Strength / Size": "2% + 1:80,000  \r\n(1.8mL cartridge)"
            },
            {
                "Medicine Name": "Lignocaine + Epinephrine  (Adrenaline)",
                "Dosage": "Injection29",
                "Strength / Size": "2% (HCl or sulphate) + \r\n1:200,000 in vial"
            },
            {
                "Medicine Name": "Linezolid",
                "Dosage": "Injection (IV)129",
                "Strength / Size": "2mg/mL in 300mL bag"
            },
            {
                "Medicine Name": "Linezolid",
                "Dosage": "Tablet130",
                "Strength / Size": "600mg"
            },
            {
                "Medicine Name": "Linezolid (Lzd)",
                "Dosage": "Tablet (dispersible)",
                "Strength / Size": "150mg [c]"
            },
            {
                "Medicine Name": "Linezolid (Lzd)",
                "Dosage": "Tablet",
                "Strength / Size": "600mg"
            },
            {
                "Medicine Name": "Lipid emulsion",
                "Dosage": "Injection",
                "Strength / Size": "20% (200 to 500mL)"
            },
            {
                "Medicine Name": "Liposomal Doxorubicin",
                "Dosage": "Solution for Injection",
                "Strength / Size": "20mg vial"
            },
            {
                "Medicine Name": "Liquid paraffin",
                "Dosage": "Nasal drops",
                "Strength / Size": "100%"
            },
            {
                "Medicine Name": "Lisinopril +   Hydrochlorothiazide",
                "Dosage": "Tablet",
                "Strength / Size": "20mg + 12.5mg"
            },
            {
                "Medicine Name": "Lithium carbonate",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Lithium carbonate",
                "Dosage": "Tablet (m/r)",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Loperamide",
                "Dosage": "Capsule",
                "Strength / Size": "2mg"
            },
            {
                "Medicine Name": "Lopinavir + ritonavir  (LPV/r)",
                "Dosage": "Oral liquid150",
                "Strength / Size": "400mg + 100mg/5mL"
            },
            {
                "Medicine Name": "Lopinavir + ritonavir  (LPV/r)",
                "Dosage": "Tablet (heat-stable)",
                "Strength / Size": "100mg + 25mg"
            },
            {
                "Medicine Name": "Lopinavir + ritonavir  (LPV/r)",
                "Strength / Size": "200mg + 50mg"
            },
            {
                "Medicine Name": "Lopinavir + ritonavir  (LPV/r)",
                "Dosage": "Oral Pellets (capsule)151",
                "Strength / Size": "40mg + 10mg [c]"
            },
            {
                "Medicine Name": "Loratadine",
                "Dosage": "Tablet",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Lorazepam",
                "Dosage": "Injection",
                "Strength / Size": "4mg/1mL amp"
            },
            {
                "Medicine Name": "Losartan",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Losartan +   Hydrochlorothiazide  (HCTZ)",
                "Dosage": "Tablet",
                "Strength / Size": "50mg + 12.5mg"
            },
            {
                "Medicine Name": "Low fat formula",
                "Dosage": "Powder",
                "Strength / Size": "200g to 500g"
            },
            {
                "Medicine Name": "Lugol‚Äôs Iodine solution",
                "Dosage": "PFOL",
                "Strength / Size": "~130mg total iodine/mL"
            },
            {
                "Medicine Name": "Lutetium-177 dotatate",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Magnesium chloride",
                "Dosage": "Tablet",
                "Strength / Size": "71.5mg (containing \r\nCalcium as carbonate \r\n119mg per tablet)"
            },
            {
                "Medicine Name": "Magnesium sulphate",
                "Dosage": "Injection",
                "Strength / Size": "500mg/mL (50%), (10mL \r\namp/vial)"
            },
            {
                "Medicine Name": "Malaria vaccine",
                "Dosage": "Injection",
                "Strength / Size": "1mL vial (2 doses)"
            },
            {
                "Medicine Name": "Mannitol",
                "Dosage": "Injectable solution",
                "Strength / Size": "20%"
            },
            {
                "Medicine Name": "Measles + Rubella vaccine  (MR)",
                "Dosage": "PFI + diluent",
                "Strength / Size": "5mL vial (10 doses)"
            },
            {
                "Medicine Name": "Measles vaccine   (live attenuated)",
                "Dosage": "PFI + diluent",
                "Strength / Size": "5mL vial (10 doses)"
            },
            {
                "Medicine Name": "Mebendazole",
                "Dosage": "Tablet (chewable,  \r\ndispersible)",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Medical air",
                "Dosage": "Inhalation (medical gas)"
            },
            {
                "Medicine Name": "Medroxyprogesterone  acetate (DMPA)",
                "Dosage": "Depot Injection (IM)428",
                "Strength / Size": "150mg/1mL  \r\n(prefilled syringe)"
            },
            {
                "Medicine Name": "Medroxyprogesterone  acetate (DMPA)",
                "Dosage": "Depot Injection (SC)429",
                "Strength / Size": "104 mg/0.65 mL  \r\n(prefilled syringe)"
            },
            {
                "Medicine Name": "Mefloquine",
                "Dosage": "Tablet",
                "Strength / Size": "250mg (as HCl)"
            },
            {
                "Medicine Name": "Melarsoprol",
                "Dosage": "Injection",
                "Strength / Size": "3.6% solution (= 180mg), \r\n5mL amp"
            },
            {
                "Medicine Name": "Melatonin",
                "Dosage": "Tablet (soluble)",
                "Strength / Size": "4mg"
            },
            {
                "Medicine Name": "Melphalan",
                "Dosage": "Tablet",
                "Strength / Size": "2mg"
            },
            {
                "Medicine Name": "Melphalan",
                "Dosage": "PFI229",
                "Strength / Size": "50mg vial"
            },
            {
                "Medicine Name": "Meningococcal meningitis  vaccine",
                "Dosage": "Injection",
                "Strength / Size": "Single or multi dose"
            },
            {
                "Medicine Name": "Mercaptoacetyltriglycine (MAG)",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Mercaptopurine",
                "Dosage": "Tablet",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Meropenem",
                "Dosage": "PFI",
                "Strength / Size": "500mg (as trihydrate)"
            },
            {
                "Medicine Name": "Mesalazine",
                "Dosage": "Tablet (e/c)",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Mesna",
                "Dosage": "Injection",
                "Strength / Size": "100mg/mL (2mL amp)276"
            },
            {
                "Medicine Name": "Mesna",
                "Strength / Size": "100mg/mL (4mL amp)277"
            },
            {
                "Medicine Name": "Mesna",
                "Dosage": "Tablet",
                "Strength / Size": "400mg277"
            },
            {
                "Medicine Name": "Metformin",
                "Dosage": "Tablet",
                "Strength / Size": "500mg (as HCl)"
            },
            {
                "Medicine Name": "Metformin",
                "Strength / Size": "500mg (as HCl) [c]388"
            },
            {
                "Medicine Name": "Methadone",
                "Dosage": "Oral liquid",
                "Strength / Size": "5mg/mL (as HCl)  \r\n(concentrate)"
            },
            {
                "Medicine Name": "Methotrexate",
                "Dosage": "PFI (preservative-free)",
                "Strength / Size": "25mg (as sodium \r\nsalt)/mL (2mL vial)"
            },
            {
                "Medicine Name": "Methotrexate",
                "Strength / Size": "25mg (as sodium \r\nsalt)/mL (20mL vial)232"
            },
            {
                "Medicine Name": "Methotrexate",
                "Dosage": "Tablet",
                "Strength / Size": "2.5mg (as sodium salt)"
            },
            {
                "Medicine Name": "Methotrexate",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Methotrexate (MTX)",
                "Dosage": "Tablet",
                "Strength / Size": "2.5mg (as sodium salt)"
            },
            {
                "Medicine Name": "Methotrexate (MTX)",
                "Dosage": "Injection  \r\n(prefilled syringe)489",
                "Strength / Size": "10mg/mL (0.4mL)"
            },
            {
                "Medicine Name": "Methotrexate (MTX)",
                "Strength / Size": "25mg/mL (0.4mL)"
            },
            {
                "Medicine Name": "Methotrexate (MTX)",
                "Dosage": "Tablet",
                "Strength / Size": "2.5mg (as sodium salt)"
            },
            {
                "Medicine Name": "Methotrexate (MTX)",
                "Dosage": "Injection (prefilled \r\nsyringe)501",
                "Strength / Size": "10mg/mL (0.4mL)"
            },
            {
                "Medicine Name": "Methotrexate (MTX)",
                "Strength / Size": "25mg/mL (0.4mL)"
            },
            {
                "Medicine Name": "Methyl cellulose",
                "Dosage": "Eye drops",
                "Strength / Size": "0.3 - 1%"
            },
            {
                "Medicine Name": "Methyldopa",
                "Dosage": "Tablet (f/c)",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Methylene diphosphonate (MDP)",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Methylprednisolone",
                "Dosage": "PFI",
                "Strength / Size": "125mg  \r\n(as sodium succinate)"
            },
            {
                "Medicine Name": "Methylprednisolone",
                "Strength / Size": "500mg  \r\n(as sodium succinate)"
            },
            {
                "Medicine Name": "Methylprednisolone",
                "Dosage": "PFI",
                "Strength / Size": "500mg  \r\n(as sodium succinate) \r\n[c]"
            },
            {
                "Medicine Name": "Methylprednisolone",
                "Dosage": "PFI",
                "Strength / Size": "1g vial  \r\n(as sodium succinate)"
            },
            {
                "Medicine Name": "Metoclopramide",
                "Dosage": "Injection",
                "Strength / Size": "5mg/mL (2mL amp)"
            },
            {
                "Medicine Name": "Metoclopramide",
                "Dosage": "Tablet",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Metoclopramide",
                "Dosage": "Injection",
                "Strength / Size": "5mg/mL (2mL amp)"
            },
            {
                "Medicine Name": "Metoclopramide",
                "Dosage": "Tablet",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Metolazone",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Metronidazole",
                "Dosage": "Injection113",
                "Strength / Size": "5mg/mL (100mL vial)"
            },
            {
                "Medicine Name": "Metronidazole",
                "Dosage": "Oral liquid114",
                "Strength / Size": "200mg/5mL (as \r\nbenzoate)"
            },
            {
                "Medicine Name": "Metronidazole",
                "Dosage": "Tablet (f/c, scored)114",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Metronidazole",
                "Dosage": "Injection",
                "Strength / Size": "500mg/100mL vial"
            },
            {
                "Medicine Name": "Metronidazole",
                "Dosage": "Oral liquid",
                "Strength / Size": "200mg/5mL (as \r\nbenzoate)"
            },
            {
                "Medicine Name": "Metronidazole",
                "Dosage": "Tablet",
                "Strength / Size": "400mg (scored)"
            },
            {
                "Medicine Name": "Metronidazole",
                "Dosage": "Gel",
                "Strength / Size": "0.75% or 0.80%"
            },
            {
                "Medicine Name": "Miconazole",
                "Dosage": "Cream",
                "Strength / Size": "2% (as nitrate)"
            },
            {
                "Medicine Name": "Midazolam",
                "Dosage": "Injection",
                "Strength / Size": "1mg (as HCl)/mL (5mL \r\namp)"
            },
            {
                "Medicine Name": "Midazolam",
                "Dosage": "Injection",
                "Strength / Size": "1mg (as HCl)/mL (5mL \r\namp)"
            },
            {
                "Medicine Name": "Midazolam",
                "Dosage": "Injection85",
                "Strength / Size": "1mg (as HCl)/mL (5mL \r\namp)"
            },
            {
                "Medicine Name": "Midazolam",
                "Strength / Size": "10mg/mL"
            },
            {
                "Medicine Name": "Midazolam",
                "Dosage": "Oromucosal solution86",
                "Strength / Size": "5mg/mL"
            },
            {
                "Medicine Name": "Midazolam",
                "Strength / Size": "10mg/mL"
            },
            {
                "Medicine Name": "Midazolam",
                "Dosage": "Injection (IM)",
                "Strength / Size": "5mg/mL (3mL amp)"
            },
            {
                "Medicine Name": "Mifepristone +   Misoprostol",
                "Dosage": "Tablet",
                "Strength / Size": "200mg + 200 \r\nmicrograms"
            },
            {
                "Medicine Name": "Milrinone",
                "Dosage": "Injection (solution)",
                "Strength / Size": "1mg/mL (10mL)"
            },
            {
                "Medicine Name": "Mirtazapine",
                "Dosage": "Tablet",
                "Strength / Size": "15mg"
            },
            {
                "Medicine Name": "Mirtazapine",
                "Dosage": "Tablet",
                "Strength / Size": "15mg"
            },
            {
                "Medicine Name": "Misoprostol",
                "Dosage": "Tablet",
                "Strength / Size": "200 micrograms437"
            },
            {
                "Medicine Name": "Misoprostol",
                "Dosage": "Vaginal tablet",
                "Strength / Size": "25 micrograms"
            },
            {
                "Medicine Name": "Mometasone",
                "Dosage": "Ointment",
                "Strength / Size": "0.1% (as furoate) (30g)"
            },
            {
                "Medicine Name": "Montelukast",
                "Dosage": "Tablet (chewable)",
                "Strength / Size": "5mg (as sodium salt)473"
            },
            {
                "Medicine Name": "Montelukast",
                "Dosage": "Tablet",
                "Strength / Size": "10mg (as sodium salt)"
            },
            {
                "Medicine Name": "Morphine",
                "Dosage": "Injection",
                "Strength / Size": "10mg (as HCl or \r\nsulphate) /1mL amp"
            },
            {
                "Medicine Name": "Morphine",
                "Dosage": "Injection",
                "Strength / Size": "10mg (as HCl or \r\nsulphate) /1mL amp"
            },
            {
                "Medicine Name": "Morphine",
                "Dosage": "Injection (for Infusion)45   30mg/mL"
            },
            {
                "Medicine Name": "Morphine",
                "Dosage": "Oral liquid",
                "Strength / Size": "1mg (as HCl or \r\nsulphate)/mL"
            },
            {
                "Medicine Name": "Morphine",
                "Dosage": "Oral liquid",
                "Strength / Size": "10mg (as HCl or \r\nsulphate)/mL"
            },
            {
                "Medicine Name": "Morphine",
                "Dosage": "Tablet (m/r)",
                "Strength / Size": "30mg (sulphate)"
            },
            {
                "Medicine Name": "Moxifloxacin (Mfx)",
                "Dosage": "Tablet (dispersible)",
                "Strength / Size": "100mg [c]"
            },
            {
                "Medicine Name": "Moxifloxacin (Mfx)",
                "Dosage": "Tablet",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Mupirocin",
                "Dosage": "Ointment",
                "Strength / Size": "2% (15g)"
            },
            {
                "Medicine Name": "Mycophenolate mofetil",
                "Dosage": "Tablet",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Mycophenolate mofetil",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Mycophenolic acid",
                "Dosage": "Tablet (e/c)",
                "Strength / Size": "180mg (as \r\nmycophenolate sodium)"
            },
            {
                "Medicine Name": "Mycophenolic acid",
                "Strength / Size": "360mg (as \r\nmycophenolate sodium)"
            },
            {
                "Medicine Name": "Naloxone",
                "Dosage": "Injection",
                "Strength / Size": "400 micrograms  \r\n(as HCl)/1mL amp"
            },
            {
                "Medicine Name": "Naltrexone",
                "Dosage": "Tablet466",
                "Strength / Size": "50mg (as HCl)"
            },
            {
                "Medicine Name": "Naltrexone",
                "Dosage": "Injection467  \r\n(IM, suspension for \r\nextended release)",
                "Strength / Size": "380mg (as HCl)"
            },
            {
                "Medicine Name": "Naltrexone",
                "Dosage": "Implant",
                "Strength / Size": "765mg (as HCl)468"
            },
            {
                "Medicine Name": "Natamycin",
                "Dosage": "Eye drops",
                "Strength / Size": "5%"
            },
            {
                "Medicine Name": "Neomycin +   Betamethasone",
                "Dosage": "Solution (ear & nasal \r\ndrops)",
                "Strength / Size": "0.5% (as sulphate) + \r\n(0.1% as sodium \r\nphosphate)"
            },
            {
                "Medicine Name": "Neostigmine",
                "Dosage": "Injection",
                "Strength / Size": "2.5mg  \r\n(as metasulphate)/1mL \r\namp"
            },
            {
                "Medicine Name": "Nevirapine (NVP)",
                "Dosage": "Oral liquid",
                "Strength / Size": "10mg/mL"
            },
            {
                "Medicine Name": "Nevirapine (NVP)",
                "Dosage": "Tablet (dispersible)",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Niacinamide",
                "Dosage": "Tablet",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Nicotine (NRT)",
                "Dosage": "Chewing gum",
                "Strength / Size": "2mg"
            },
            {
                "Medicine Name": "Nicotine (NRT)",
                "Strength / Size": "4mg"
            },
            {
                "Medicine Name": "Nicotine (NRT)",
                "Dosage": "Transdermal patch470",
                "Strength / Size": "7-21mg/24 hours"
            },
            {
                "Medicine Name": "Nifedipine",
                "Dosage": "Tablet (s/r)",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Nifurtimox",
                "Dosage": "Tablet",
                "Strength / Size": "120mg"
            },
            {
                "Medicine Name": "Nilotinib",
                "Dosage": "Capsule",
                "Strength / Size": "200mg"
            },
            {
                "Medicine Name": "Nitrofurantoin",
                "Dosage": "Oral liquid",
                "Strength / Size": "25mg/5mL [c]"
            },
            {
                "Medicine Name": "Nitrofurantoin",
                "Dosage": "Tablet",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Nitroglycerin (NTG)",
                "Dosage": "Injection",
                "Strength / Size": "2.5mg/mL (10mL) amp"
            },
            {
                "Medicine Name": "Nitrous oxide",
                "Dosage": "Inhalation (medical gas)"
            },
            {
                "Medicine Name": "Non ionic low osmolar  water-soluble iodinated  contrast media",
                "Dosage": "Injection",
                "Strength / Size": "300mg iodine/mL \r\n(50mL) [c]351"
            },
            {
                "Medicine Name": "Non ionic low osmolar  water-soluble iodinated  contrast media",
                "Strength / Size": "300mg iodine/mL \r\n(100mL) [c]351"
            },
            {
                "Medicine Name": "Non ionic low osmolar  water-soluble iodinated  contrast media",
                "Strength / Size": "350mg iodine/mL \r\n(50mL)352"
            },
            {
                "Medicine Name": "Non ionic low osmolar  water-soluble iodinated  contrast media",
                "Strength / Size": "350mg iodine/mL \r\n(100mL)352"
            },
            {
                "Medicine Name": "Non ionic low osmolar  water-soluble iodinated  contrast media",
                "Strength / Size": "300mg iodine/mL \r\n(50mL) [For intrathecal, \r\noral, intra-cavitary and  \r\nintravenous use] [c]353"
            },
            {
                "Medicine Name": "Non ionic low osmolar  water-soluble iodinated  contrast media",
                "Strength / Size": "300mg iodine/mL \r\n(100mL) [For \r\nintrathecal, oral,  \r\nintra-cavitary and  \r\nintravenous use] [c]353"
            },
            {
                "Medicine Name": "Non ionic low osmolar  water-soluble iodinated  contrast media",
                "Strength / Size": "350mg iodine/mL (50ml) \r\n[For oral, intra-cavitary \r\nand intravenous use]354"
            },
            {
                "Medicine Name": "Non ionic low osmolar  water-soluble iodinated  contrast media",
                "Strength / Size": "350mg iodine/mL \r\n(100ml) [For oral,  \r\nintra-cavitary and \r\nintravenous use]354"
            },
            {
                "Medicine Name": "Norepinephrine   (Noradrenaline)",
                "Dosage": "Injection",
                "Strength / Size": "1mg/mL"
            },
            {
                "Medicine Name": "Normal immunoglobulin297   Injection (IV)",
                "Strength / Size": "5% protein solution \r\n(100mL vial)"
            },
            {
                "Medicine Name": "Normal immunoglobulin297   Injection (IV)",
                "Strength / Size": "10% protein solution \r\n(100mL vial)"
            },
            {
                "Medicine Name": "Nutritionally complete   Iso-caloric paediatric tube  feed",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Nutritionally complete   liquid low sodium   formula",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Nutritionally complete  diet, fibre-free for tube  feeding",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Nutritionally complete  diet, fibre-free for tube  feeding",
                "Strength / Size": "1000mL"
            },
            {
                "Medicine Name": "Nutritionally complete  formula with fibre for  tube feeding",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Nutritionally complete  formula with fibre for  tube feeding",
                "Strength / Size": "1000mL"
            },
            {
                "Medicine Name": "Nutritionally complete  glutamine-enriched liquid  formula",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Nutritionally complete  high protein energy sip  feed",
                "Dosage": "Liquid",
                "Strength / Size": "200mL"
            },
            {
                "Medicine Name": "Nutritionally complete  liquid diet, isocaloric",
                "Dosage": "Liquid",
                "Strength / Size": "1000mL"
            },
            {
                "Medicine Name": "Nutritionally complete  with Medium Chain  Triglyceride peptide diet",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Nutritionally complete low  glycemic index formula",
                "Dosage": "Powder",
                "Strength / Size": "400g sachet"
            },
            {
                "Medicine Name": "Nutritionally complete Sip  feed",
                "Dosage": "Liquid",
                "Strength / Size": "200mL"
            },
            {
                "Medicine Name": "Nutritionally complete,   normal caloric diet for   diabetes tube feed, with  fibre",
                "Dosage": "Liquid",
                "Strength / Size": "200mL"
            },
            {
                "Medicine Name": "Nutritionally complete,   normal caloric diet for   diabetes tube feed, with  fibre",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Nutritionally complete,  hydrolysed diet with fibre",
                "Dosage": "Liquid",
                "Strength / Size": "1000mL"
            },
            {
                "Medicine Name": "Nystatin",
                "Dosage": "Oral liquid (suspension)",
                "Strength / Size": "100,000 IU/mL [c]"
            },
            {
                "Medicine Name": "Ofloxacin",
                "Dosage": "Eye drops",
                "Strength / Size": "0.3% (as sulphate)"
            },
            {
                "Medicine Name": "Olanzapine",
                "Dosage": "PFI",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Olanzapine",
                "Dosage": "Tablet (dispersible)",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Olanzepine",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Omega 3 fatty acids",
                "Dosage": "Tablet / Capsule538",
                "Strength / Size": "1g"
            },
            {
                "Medicine Name": "Omega 3 fatty acids",
                "Dosage": "Liquid539",
                "Strength / Size": "250mg to 500mg/100mL \r\n(100 to 200mL)"
            },
            {
                "Medicine Name": "Omeprazole",
                "Dosage": "PFI365",
                "Strength / Size": "40mg (as sodium salt) \r\nvial"
            },
            {
                "Medicine Name": "Omeprazole",
                "Dosage": "Capsule",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Ondansetron",
                "Dosage": "Injection50",
                "Strength / Size": "2mg (as HCl)/mL (2mL \r\namp)"
            },
            {
                "Medicine Name": "Ondansetron",
                "Dosage": "Oral liquid51",
                "Strength / Size": "4mg base/5mL [c]"
            },
            {
                "Medicine Name": "Ondansetron",
                "Dosage": "Tablet50",
                "Strength / Size": "4mg (as HCl)"
            },
            {
                "Medicine Name": "Ondansetron",
                "Dosage": "Injection370",
                "Strength / Size": "2mg (as HCl)/mL (2mL \r\namp)"
            },
            {
                "Medicine Name": "Ondansetron",
                "Dosage": "Oral liquid371",
                "Strength / Size": "4mg base/5mL [c]"
            },
            {
                "Medicine Name": "Ondansetron",
                "Dosage": "Tablet370",
                "Strength / Size": "4mg (as HCl)"
            },
            {
                "Medicine Name": "Oral rehydration   salts + Zinc sulphate",
                "Dosage": "Co-pack (4 sachets + 10 \r\ntablets)",
                "Strength / Size": "PFOL in sachet to make \r\n500mL + 20mg tablet  \r\n(dispersible) [c]"
            },
            {
                "Medicine Name": "Oral rehydration salts   (ORS)",
                "Dosage": "PFOL (to make 500mL)",
                "Strength / Size": "Sachet  \r\n(WHO low-osmolarity \r\nformula)"
            },
            {
                "Medicine Name": "Oral rehydration salts  (ORS)",
                "Dosage": "PFOL (to make 500mL)",
                "Strength / Size": "Sachet  \r\n(WHO low-osmolarity \r\nformula)"
            },
            {
                "Medicine Name": "Oral rehydration salts +  Zinc sulphate",
                "Dosage": "Co-pack (4 sachets + 10 \r\ntablets)",
                "Strength / Size": "PFOL in sachet to make \r\n500mL + 20mg tablet  \r\n(dispersible) [c]"
            },
            {
                "Medicine Name": "Oseltamivir",
                "Dosage": "Oral powder",
                "Strength / Size": "12mg/mL"
            },
            {
                "Medicine Name": "Oxaliplatin",
                "Dosage": "Solution for Injection",
                "Strength / Size": "2mg/mL (25mL vial)"
            },
            {
                "Medicine Name": "Oxaliplatin",
                "Strength / Size": "2mg/mL (50mL vial)"
            },
            {
                "Medicine Name": "Oxygen",
                "Dosage": "Inhalation (medical gas)"
            },
            {
                "Medicine Name": "Oxytocin",
                "Dosage": "Injection",
                "Strength / Size": "10 IU/1mL amp"
            },
            {
                "Medicine Name": "Paclitaxel",
                "Dosage": "Concentrate (for IV \r\ninfusion)",
                "Strength / Size": "6mg/mL (5mL vial)"
            },
            {
                "Medicine Name": "Paclitaxel",
                "Strength / Size": "6mg/mL (16.7mL vial)"
            },
            {
                "Medicine Name": "Paclitaxel",
                "Strength / Size": "6mg/mL (50mL vial)"
            },
            {
                "Medicine Name": "Paediatric nutritionally  complete isocaloric   formula",
                "Dosage": "Powder",
                "Strength / Size": "400g [c]"
            },
            {
                "Medicine Name": "Paediatric nutritionally  complete peptide based  formula",
                "Dosage": "Powder",
                "Strength / Size": "400g [c]"
            },
            {
                "Medicine Name": "Paediatric trace  elements",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "10mL [c]"
            },
            {
                "Medicine Name": "Paliperidone palmitate",
                "Dosage": "Injection",
                "Strength / Size": "75mg/mL"
            },
            {
                "Medicine Name": "Paliperidone palmitate",
                "Strength / Size": "100mg/mL"
            },
            {
                "Medicine Name": "Paliperidone palmitate",
                "Strength / Size": "150mg/mL"
            },
            {
                "Medicine Name": "p-aminosalicylic acid (PAS)  Granules",
                "Strength / Size": "4g sachet"
            },
            {
                "Medicine Name": "Papain + Urea   (Papain-urea topical)",
                "Dosage": "Ointment",
                "Strength / Size": "521,700 IU + 100mg \r\n(15g)"
            },
            {
                "Medicine Name": "Paracetamol",
                "Dosage": "Injection  \r\n(for IV infusion)40",
                "Strength / Size": "10mg/mL (100mL vial)"
            },
            {
                "Medicine Name": "Paracetamol",
                "Dosage": "Oral liquid",
                "Strength / Size": "120mg/5mL [c]"
            },
            {
                "Medicine Name": "Paracetamol",
                "Dosage": "Suppository",
                "Strength / Size": "125mg [c]"
            },
            {
                "Medicine Name": "Paracetamol",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Paracetamol",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Paromomycin",
                "Dosage": "Injection solution (IM)",
                "Strength / Size": "375mg/mL (as sulphate) \r\n(2mL amp)"
            },
            {
                "Medicine Name": "Pembrolizumab",
                "Dosage": "Injection",
                "Strength / Size": "100mg/4mL"
            },
            {
                "Medicine Name": "Penicillamine",
                "Dosage": "Tablet",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Phenobarbital   (Phenobarbitone) sodium",
                "Dosage": "Injection",
                "Strength / Size": "30mg/1mL amp [c]87"
            },
            {
                "Medicine Name": "Phenobarbital   (Phenobarbitone) sodium",
                "Strength / Size": "200mg/1mL amp"
            },
            {
                "Medicine Name": "Phenobarbital   (Phenobarbitone) sodium",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "30mg"
            },
            {
                "Medicine Name": "Phenoxybenzamine",
                "Dosage": "Capsule",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Phenoxymethylpenicilllin  (Penicillin V)",
                "Dosage": "PFOL",
                "Strength / Size": "250mg (as potassium \r\nsalt)/5mL"
            },
            {
                "Medicine Name": "Phenoxymethylpenicilllin  (Penicillin V)",
                "Dosage": "Tablet",
                "Strength / Size": "250mg (as potassium \r\nsalt)"
            },
            {
                "Medicine Name": "Phenylephrine",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL"
            },
            {
                "Medicine Name": "Phenytoin sodium",
                "Dosage": "Injection",
                "Strength / Size": "50mg/mL (5mL vial)"
            },
            {
                "Medicine Name": "Phenytoin sodium",
                "Dosage": "Oral liquid",
                "Strength / Size": "30mg/5mL"
            },
            {
                "Medicine Name": "Phenytoin sodium",
                "Dosage": "Tablet / Capsule",
                "Strength / Size": "50mg88"
            },
            {
                "Medicine Name": "Phenytoin sodium",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Phytomenadione (Vit K1)",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (1mL amp)"
            },
            {
                "Medicine Name": "Phytomenadione (Vit K1)",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (0.2mL) amp \r\n[c]286"
            },
            {
                "Medicine Name": "Phytomenadione (Vit K1)",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (1mL amp)"
            },
            {
                "Medicine Name": "Pilocarpine",
                "Dosage": "Solution (eye-drops)",
                "Strength / Size": "4% (as HCl or nitrate)"
            },
            {
                "Medicine Name": "Piperacillin +  Tazobactam",
                "Dosage": "PFI",
                "Strength / Size": "4g (as sodium salt) + \r\n500mg (as sodium salt)"
            },
            {
                "Medicine Name": "Plasma, fresh-frozen"
            },
            {
                "Medicine Name": "Platelets"
            },
            {
                "Medicine Name": "Pneumococcal vaccine (10- valent ads. conjugate)",
                "Dosage": "Injection (suspension)",
                "Strength / Size": "2mL vial (4 doses)"
            },
            {
                "Medicine Name": "Pneumococcal vaccine (13  valent or higher adsorbed  conjugate)",
                "Dosage": "Injection (syringe)",
                "Strength / Size": "Single or multi dose vial"
            },
            {
                "Medicine Name": "Podophyllin resin",
                "Dosage": "Solution",
                "Strength / Size": "15% (in benzoin tincture) \r\n(15mL)"
            },
            {
                "Medicine Name": "Point of use Water   treatment",
                "Dosage": "Solution",
                "Strength / Size": "1.2% Sodium \r\nhypochlorite [NaOCl] \r\n(150mL)"
            },
            {
                "Medicine Name": "Polio vaccine (IPV)",
                "Dosage": "Injection",
                "Strength / Size": "Multi dose vial"
            },
            {
                "Medicine Name": "Polio vaccine, oral (OPV)  (live attenuated)",
                "Dosage": "Oral drops",
                "Strength / Size": "10mL vial (20 doses)"
            },
            {
                "Medicine Name": "Polygeline",
                "Dosage": "Infusion (IV)",
                "Strength / Size": "3.5% (500mL pack)"
            },
            {
                "Medicine Name": "Polymyxin B",
                "Dosage": "PFI",
                "Strength / Size": "500,000 IU vial"
            },
            {
                "Medicine Name": "Potassium chloride",
                "Dosage": "Tablet (e/r)",
                "Strength / Size": "600mg"
            },
            {
                "Medicine Name": "Potassium chloride",
                "Dosage": "Injectable solution for \r\ndilution",
                "Strength / Size": "15% (10mL amp) [c]"
            },
            {
                "Medicine Name": "Povidone iodine",
                "Dosage": "Solution",
                "Strength / Size": "10% (equiv. to Iodine 1%)"
            },
            {
                "Medicine Name": "Pralidoxime",
                "Dosage": "PFI",
                "Strength / Size": "1g (as chloride or \r\nmesilate) vial"
            },
            {
                "Medicine Name": "Pramipexole",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "180 micrograms base"
            },
            {
                "Medicine Name": "Pramipexole",
                "Strength / Size": "700 micrograms base"
            },
            {
                "Medicine Name": "Praziquantel",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "600mg"
            },
            {
                "Medicine Name": "Praziquantel",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "600mg"
            },
            {
                "Medicine Name": "Prazosin",
                "Dosage": "Capsule",
                "Strength / Size": "1mg"
            },
            {
                "Medicine Name": "Prazosin",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Prednisolone",
                "Dosage": "Oral liquid",
                "Strength / Size": "15mg/5mL [c]"
            },
            {
                "Medicine Name": "Prednisolone",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Prednisolone",
                "Dosage": "Oral liquid",
                "Strength / Size": "15mg/5mL [c]"
            },
            {
                "Medicine Name": "Prednisolone",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Prednisolone",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Prednisolone",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Prednisolone",
                "Dosage": "Oral liquid",
                "Strength / Size": "15mg/mL [c]"
            },
            {
                "Medicine Name": "Prednisolone",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Prednisolone",
                "Dosage": "Tablet",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Prednisolone",
                "Dosage": "Eye drops",
                "Strength / Size": "1% (as acetate) (5mL)"
            },
            {
                "Medicine Name": "Primaquine",
                "Dosage": "Tablet",
                "Strength / Size": "7.5mg (as diphosphate)"
            },
            {
                "Medicine Name": "Primaquine",
                "Strength / Size": "15mg (as diphosphate)"
            },
            {
                "Medicine Name": "Probenecid",
                "Dosage": "Tablet",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Procarbazine",
                "Dosage": "Capsule",
                "Strength / Size": "50mg (as HCl)"
            },
            {
                "Medicine Name": "Proguanil",
                "Dosage": "Tablet",
                "Strength / Size": "100mg (as HCl)"
            },
            {
                "Medicine Name": "Propofol",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (20mL vial)"
            },
            {
                "Medicine Name": "Propofol",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (20mL vial)"
            },
            {
                "Medicine Name": "Propranolol",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "40mg"
            },
            {
                "Medicine Name": "Propylthiouracil",
                "Dosage": "Tablet",
                "Strength / Size": "50mg"
            },
            {
                "Medicine Name": "Prostaglandin E2",
                "Dosage": "Vaginal tablet",
                "Strength / Size": "3mg"
            },
            {
                "Medicine Name": "Prostaglandin E2",
                "Dosage": "Injection solution",
                "Strength / Size": "1mg/mL [c]"
            },
            {
                "Medicine Name": "Protamine",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (as sulphate) \r\n(5mL amp)"
            },
            {
                "Medicine Name": "Prothionamide (Pto)",
                "Dosage": "Tablet",
                "Strength / Size": "250mg"
            },
            {
                "Medicine Name": "Pyrazinamide (Z)",
                "Dosage": "Tablet",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Pyrazinamide (Z)",
                "Dosage": "Tablet (dispersible)",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Pyrazinamide (Z)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Pyridostigmine",
                "Dosage": "Tablet",
                "Strength / Size": "60mg (as bromide)"
            },
            {
                "Medicine Name": "Pyridoxine (Vit B6)",
                "Dosage": "Tablet",
                "Strength / Size": "25mg (as HCl)541"
            },
            {
                "Medicine Name": "Pyridoxine (Vit B6)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "50mg (as HCl)"
            },
            {
                "Medicine Name": "Pyrimethamine",
                "Dosage": "Tablet",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Quetiapine",
                "Dosage": "Tablet (i/r, scored)",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Quetiapine",
                "Dosage": "Tablet (e/r)",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Quetiapine",
                "Dosage": "Tablet (i/r, scored)",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Quetiapine",
                "Dosage": "Tablet (i/r, scored)",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Quetiapine",
                "Dosage": "Tablet (e/r)",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Quetiapine",
                "Dosage": "Tablet (i/r, scored)",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Quinine",
                "Dosage": "Injection180",
                "Strength / Size": "300mg/mL (as HCl) \r\n(2mL amp)"
            },
            {
                "Medicine Name": "Quinine",
                "Dosage": "Tablet (f/c)181",
                "Strength / Size": "300mg  \r\n(as sulphate or \r\nbisulphate)"
            },
            {
                "Medicine Name": "Rabies vaccine   (cell culture)",
                "Dosage": "Injection",
                "Strength / Size": "Single dose  \r\n(Purified Verocell / \r\nHuman diploid)"
            },
            {
                "Medicine Name": "Raltegravir (RAL)",
                "Dosage": "Tablet",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Raltegravir (RAL)",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Raltegravir (RAL)",
                "Strength / Size": "400mg (f/c)"
            },
            {
                "Medicine Name": "Raltegravir (RAL)",
                "Dosage": "Granules for oral  \r\nsuspension",
                "Strength / Size": "100mg sachet"
            },
            {
                "Medicine Name": "Rasburicase",
                "Dosage": "Injection",
                "Strength / Size": "7.5mg/vial"
            },
            {
                "Medicine Name": "Ready to use  supplemental food (RUSF)",
                "Dosage": "Oral paste / bar / liquid / \r\npowder",
                "Strength / Size": "Standard formula  \r\n(minimum 350 \r\nKcal/100g)601"
            },
            {
                "Medicine Name": "Ready to use  supplemental food (RUSF)",
                "Strength / Size": "Standard formula  \r\n(minimum 510 \r\nKcal/100g)602"
            },
            {
                "Medicine Name": "Ready to use therapeutic  food (RUTF)",
                "Dosage": "Oral paste / bar / liquid / \r\npowder",
                "Strength / Size": "Standard formula  \r\n(minimum 500 \r\nKcal/100g)"
            },
            {
                "Medicine Name": "Red blood cells"
            },
            {
                "Medicine Name": "Rehydration solution for  malnutrition (ReSoMal)",
                "Dosage": "PFOL (to make 1L)",
                "Strength / Size": "Sachet (42g)  \r\n(WHO formula)"
            },
            {
                "Medicine Name": "Rehydration solution for  malnutrition (ReSoMal)",
                "Dosage": "PFOL (to make 1L)",
                "Strength / Size": "Sachet (42g)  \r\n(WHO formula)"
            },
            {
                "Medicine Name": "Remifentanyl",
                "Dosage": "PFI",
                "Strength / Size": "2mg/2mL"
            },
            {
                "Medicine Name": "Remifentanyl",
                "Dosage": "PFI",
                "Strength / Size": "2mg/2mL"
            },
            {
                "Medicine Name": "Retinol (Vit A)",
                "Dosage": "Capsule",
                "Strength / Size": "50,000 IU (as palmitate)"
            },
            {
                "Medicine Name": "Retinol (Vit A)",
                "Strength / Size": "100,000 IU (as \r\npalmitate)"
            },
            {
                "Medicine Name": "Retinol (Vit A)",
                "Strength / Size": "200,000 IU (as \r\npalmitate)"
            },
            {
                "Medicine Name": "Ribavirin",
                "Dosage": "Injection (IV)",
                "Strength / Size": "800mg in 10mL \r\nphosphate buffer \r\nsolution"
            },
            {
                "Medicine Name": "Ribavirin",
                "Dosage": "Capsule",
                "Strength / Size": "200mg"
            },
            {
                "Medicine Name": "Rifabutin",
                "Dosage": "Capsule",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Rifampicin (R)",
                "Dosage": "Tablet / Capsule",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Rifampicin (R)",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Rifampicin (R)",
                "Dosage": "Capsule",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Rifampicin (R)",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Rifampicin + Isoniazid  (RH)",
                "Dosage": "Tablet",
                "Strength / Size": "150mg + 75mg"
            },
            {
                "Medicine Name": "Rifampicin + Isoniazid  (RH)",
                "Strength / Size": "75mg + 50mg [c]"
            },
            {
                "Medicine Name": "Rifampicin + Isoniazid +  Pyrazinamide (RHZ)",
                "Dosage": "Tablet",
                "Strength / Size": "75mg + 50mg + 150mg \r\n[c]"
            },
            {
                "Medicine Name": "Rifampicin + Isoniazid +  Pyrazinamide +   Ethambutol (RHZE)",
                "Dosage": "Tablet",
                "Strength / Size": "150mg + 75mg + 400mg \r\n+ 275mg"
            },
            {
                "Medicine Name": "Rifapentine",
                "Dosage": "Tablet",
                "Strength / Size": "150mg"
            },
            {
                "Medicine Name": "Risperidone",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "2mg"
            },
            {
                "Medicine Name": "Ritonavir (RTV)",
                "Dosage": "Oral liquid",
                "Strength / Size": "400mg/5mL"
            },
            {
                "Medicine Name": "Ritonavir (RTV)",
                "Dosage": "Tablet (heat-stable)",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Ritonavir (RTV)",
                "Dosage": "Oral powder",
                "Strength / Size": "100mg sachet [c]"
            },
            {
                "Medicine Name": "Rituximab",
                "Dosage": "Injection (IV)",
                "Strength / Size": "10mg/mL (10mL vial)"
            },
            {
                "Medicine Name": "Rituximab",
                "Strength / Size": "10mg/mL (50mL vial)"
            },
            {
                "Medicine Name": "Rituximab",
                "Dosage": "Injection (IV)",
                "Strength / Size": "10mg/mL (10mL vial)"
            },
            {
                "Medicine Name": "Rituximab",
                "Strength / Size": "10mg/mL (50mL vial)"
            },
            {
                "Medicine Name": "Rituximab",
                "Dosage": "Injection (IV)",
                "Strength / Size": "10mg/mL (10mL vial)"
            },
            {
                "Medicine Name": "Rituximab",
                "Strength / Size": "10mg/mL (50mL vial)"
            },
            {
                "Medicine Name": "Rivaroxaban",
                "Dosage": "Tablet",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Rivaroxaban",
                "Strength / Size": "15mg"
            },
            {
                "Medicine Name": "Rivaroxaban",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Rotavirus vaccine",
                "Dosage": "Oral suspension",
                "Strength / Size": "Single dose vial"
            },
            {
                "Medicine Name": "Sacubitril + Valsartan",
                "Dosage": "Tablet (f/c)",
                "Strength / Size": "24mg + 26mg"
            },
            {
                "Medicine Name": "Salbutamol",
                "Dosage": "Injection",
                "Strength / Size": "500 micrograms  \r\n(as sulphate)/mL  \r\n(5mL amp)"
            },
            {
                "Medicine Name": "Salbutamol",
                "Dosage": "Nebuliser solution",
                "Strength / Size": "5mg/mL (as sulphate)"
            },
            {
                "Medicine Name": "Salbutamol +   Beclomethasone",
                "Dosage": "Inhalation (aerosol)",
                "Strength / Size": "100 micrograms +  \r\n50 micrograms"
            },
            {
                "Medicine Name": "Salbutamol + Ipratropium",
                "Dosage": "Nebuliser solution",
                "Strength / Size": "200 micrograms  \r\n(as sulphate) + 1mg  \r\n(as bromide) per 1mL  \r\n(2.5mL amp)"
            },
            {
                "Medicine Name": "Salicylic acid",
                "Dosage": "Ointment",
                "Strength / Size": "3%"
            },
            {
                "Medicine Name": "Semi elemental peptide  based formula for tube  feed",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Sesta methoxyisobutylisonitrile (sestamibi)",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Sevelamer",
                "Dosage": "Tablet",
                "Strength / Size": "400mg"
            },
            {
                "Medicine Name": "Sevelamer",
                "Strength / Size": "800mg"
            },
            {
                "Medicine Name": "Sevoflurane",
                "Dosage": "Liquid",
                "Strength / Size": "250mL"
            },
            {
                "Medicine Name": "Sildenafil",
                "Dosage": "PFOL",
                "Strength / Size": "10mg/mL"
            },
            {
                "Medicine Name": "Silver ion",
                "Dosage": "Solution",
                "Strength / Size": "0.01% (100mL)"
            },
            {
                "Medicine Name": "Silver ion",
                "Strength / Size": "0.01% (250mL)"
            },
            {
                "Medicine Name": "Silver sulphadiazine",
                "Dosage": "Cream",
                "Strength / Size": "1% (50g)"
            },
            {
                "Medicine Name": "Silver sulphadiazine",
                "Dosage": "Cream",
                "Strength / Size": "1% (50g)"
            },
            {
                "Medicine Name": "Silver sulphadiazine",
                "Strength / Size": "1% (250g)"
            },
            {
                "Medicine Name": "Sodium acid phosphate",
                "Dosage": "Tablets (effervescent)",
                "Strength / Size": "1.936g (equivalent to \r\nphosphorus 500mg)"
            },
            {
                "Medicine Name": "Sodium chloride",
                "Dosage": "Solution (nasal drops)",
                "Strength / Size": "0.90%"
            },
            {
                "Medicine Name": "Sodium chloride",
                "Dosage": "Tablet",
                "Strength / Size": "600g"
            },
            {
                "Medicine Name": "Sodium chloride",
                "Dosage": "Injectable solution \r\n(infusion)",
                "Strength / Size": "0.45% (hypotonic)  \r\n(500mL) [in collapsible \r\nbottle or Euro cap]525"
            },
            {
                "Medicine Name": "Sodium chloride",
                "Strength / Size": "0.9% (isotonic) \r\n(500mL)526"
            },
            {
                "Medicine Name": "Sodium chloride",
                "Dosage": "Injectable solution",
                "Strength / Size": "3% (hypertonic) (10mL \r\namp) [c]527"
            },
            {
                "Medicine Name": "Sodium citrate + Citric acid  (Shohl‚Äôs solution)",
                "Dosage": "Oral solution",
                "Strength / Size": "500mg + 334mg/5mL \r\n(30mL)"
            },
            {
                "Medicine Name": "Sodium hydrogen   carbonate   (Sodium bicarbonate)",
                "Dosage": "Injectable solution",
                "Strength / Size": "8.4% (10mL amp)"
            },
            {
                "Medicine Name": "Sodium hydrogen   carbonate (bicarbonate)",
                "Dosage": "Injectable solution",
                "Strength / Size": "8.4% (10mL amp)"
            },
            {
                "Medicine Name": "Sodium hydrogen   carbonate (Sodium   bicarbonate)",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "600mg"
            },
            {
                "Medicine Name": "Sodium hydrogen   carbonate (Sodium   bicarbonate)",
                "Strength / Size": "1g"
            },
            {
                "Medicine Name": "Sodium hypochlorite",
                "Dosage": "Solution",
                "Strength / Size": "4-6% chlorine"
            },
            {
                "Medicine Name": "Sodium lactate compound  (Hartmanns / Ringers  lactate)",
                "Dosage": "Injectable solution \r\n(infusion)",
                "Strength / Size": "BP formula (500mL)"
            },
            {
                "Medicine Name": "Sodium nitrite",
                "Dosage": "Injection",
                "Strength / Size": "30mg/mL (10mL amp)"
            },
            {
                "Medicine Name": "Sodium polystyrene   sulphonate",
                "Dosage": "Powder",
                "Strength / Size": "450mg"
            },
            {
                "Medicine Name": "Sodium stibogluconate",
                "Dosage": "Injection",
                "Strength / Size": "100mg/mL (100mL amp)"
            },
            {
                "Medicine Name": "Sodium thiosulphate",
                "Dosage": "Injection",
                "Strength / Size": "250mg/mL (50mL amp)"
            },
            {
                "Medicine Name": "Specialized   Semi-elemental peptide  formula",
                "Dosage": "Powder",
                "Strength / Size": "400g"
            },
            {
                "Medicine Name": "Specialized Hepatic   formula",
                "Dosage": "Powder",
                "Strength / Size": "Sachet"
            },
            {
                "Medicine Name": "Specialized hepatic liquid  formula",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Specialized hepatic sip  feed",
                "Dosage": "Liquid",
                "Strength / Size": "200mL"
            },
            {
                "Medicine Name": "Specialized high energy  protein drink (with   hydrolyzed protein, fat  free, lactose free and   gluten free)",
                "Dosage": "Liquid",
                "Strength / Size": "200mL"
            },
            {
                "Medicine Name": "Specialized hypercaloric  liquid formula feed",
                "Dosage": "Liquid",
                "Strength / Size": "500mL"
            },
            {
                "Medicine Name": "Specialized Renal  formula",
                "Dosage": "Powder",
                "Strength / Size": "400g"
            },
            {
                "Medicine Name": "Spironolactone",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Spironolactone",
                "Dosage": "Tablet (cross-scored)",
                "Strength / Size": "25mg"
            },
            {
                "Medicine Name": "Spironolactone",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "100mg362"
            },
            {
                "Medicine Name": "Succimer   [Dimercaptosuccinic acid  (DMSA)]",
                "Dosage": "Capsule",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Sulfadiazine",
                "Dosage": "Tablet",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Sulfadoxine +   Pyrimethamine",
                "Dosage": "Tablet",
                "Strength / Size": "500mg + 25mg"
            },
            {
                "Medicine Name": "Sulfasalazine (SSZ)",
                "Dosage": "Tablet",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Surfactant",
                "Dosage": "Suspension for  \r\nintratracheal instillation",
                "Strength / Size": "25mg/mL [c]447"
            },
            {
                "Medicine Name": "Surfactant",
                "Strength / Size": "80mg/mL [c]448"
            },
            {
                "Medicine Name": "Suxamethonium",
                "Dosage": "Injection",
                "Strength / Size": "50mg (as chloride)/mL \r\n(2mL amp)"
            },
            {
                "Medicine Name": "Tacrolimus",
                "Dosage": "Concentrate  \r\n(for IV infusion)",
                "Strength / Size": "5mg/1mL amp"
            },
            {
                "Medicine Name": "Tacrolimus",
                "Dosage": "Capsule",
                "Strength / Size": "500 micrograms"
            },
            {
                "Medicine Name": "Tacrolimus",
                "Strength / Size": "1mg"
            },
            {
                "Medicine Name": "Tacrolimus",
                "Strength / Size": "5mg"
            },
            {
                "Medicine Name": "Tacrolimus",
                "Dosage": "Ointment",
                "Strength / Size": "0.03% (as monohydrate) \r\n(10g)"
            },
            {
                "Medicine Name": "Tacrolimus",
                "Strength / Size": "0.1% (as monohydrate) \r\n(10g)"
            },
            {
                "Medicine Name": "Tamoxifen",
                "Dosage": "Tablet",
                "Strength / Size": "20mg (as citrate)"
            },
            {
                "Medicine Name": "Tamsulosin",
                "Dosage": "Tablet",
                "Strength / Size": "400 micrograms  (as \r\nHCl)"
            },
            {
                "Medicine Name": "Technetium-99m generator",
                "Dosage": "6"
            },
            {
                "Medicine Name": "Teicoplanin",
                "Dosage": "Injection",
                "Strength / Size": "200mg"
            },
            {
                "Medicine Name": "Telmisartan +   Hydrochlorothiazide",
                "Dosage": "Tablet",
                "Strength / Size": "40mg + 12.5mg"
            },
            {
                "Medicine Name": "Telmisartan +   Hydrochlorothiazide",
                "Strength / Size": "80mg + 12.5mg"
            },
            {
                "Medicine Name": "Telmisartan +  Amlodipine",
                "Dosage": "Tablet",
                "Strength / Size": "40mg + 5mg"
            },
            {
                "Medicine Name": "Tenofovir + Emtricitabine  (TDF/FTC)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg + 200mg"
            },
            {
                "Medicine Name": "Tenofovir + Lamivudine  (TDF/3TC)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg + 300mg"
            },
            {
                "Medicine Name": "Tenofovir + Lamivudine +  Dolutegravir   (TDF/3TC/DTG)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg + 300mg + 50mg"
            },
            {
                "Medicine Name": "Tenofovir + Lamivudine +  Efavirenz (TDF/3TC/EFV)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg + 300mg + \r\n400mg"
            },
            {
                "Medicine Name": "Tenofovir disoproxil   fumarate (TDF)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Tenofovir disoproxil   fumarate (TDF)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Terbinafine",
                "Dosage": "Tablet",
                "Strength / Size": "125mg"
            },
            {
                "Medicine Name": "Terbinafine",
                "Dosage": "Cream",
                "Strength / Size": "1% (as HCl)"
            },
            {
                "Medicine Name": "Terizidone (Trd)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Testosterone",
                "Dosage": "Gel378",
                "Strength / Size": "1%"
            },
            {
                "Medicine Name": "Testosterone",
                "Dosage": "Injection (oily)379",
                "Strength / Size": "250mg (as \r\nenanthate)/1mL amp"
            },
            {
                "Medicine Name": "Tetanus + Diphtheria (Td)  vaccine",
                "Dosage": "Injection",
                "Strength / Size": "10mL vial (20 doses)"
            },
            {
                "Medicine Name": "Tetanus + Diphtheria +   Pertussis (Tdap) vaccine",
                "Dosage": "Injection",
                "Strength / Size": "0.5mL (single dose)"
            },
            {
                "Medicine Name": "Tetanus toxoid   (adsorbed)",
                "Dosage": "Injection (suspension)",
                "Strength / Size": "10mL vial (20 doses)"
            },
            {
                "Medicine Name": "Tetracycline",
                "Dosage": "Eye ointment",
                "Strength / Size": "1% (as HCl)"
            },
            {
                "Medicine Name": "Thalidomide",
                "Dosage": "Capsule",
                "Strength / Size": "100mg"
            },
            {
                "Medicine Name": "Thiamine (Vit B1)",
                "Dosage": "Tablet",
                "Strength / Size": "50mg (as HCl)"
            },
            {
                "Medicine Name": "Thiamine (Vit B1)",
                "Dosage": "Tablet",
                "Strength / Size": "50mg (as HCl)"
            },
            {
                "Medicine Name": "Thiopental sodium",
                "Dosage": "PFI",
                "Strength / Size": "500mg vial"
            },
            {
                "Medicine Name": "Tigecycline",
                "Dosage": "PFI",
                "Strength / Size": "50mg vial"
            },
            {
                "Medicine Name": "Tinidazole",
                "Dosage": "Tablet (f/c)",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Tinidazole",
                "Dosage": "Tablet (f/c)",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Tioguanine",
                "Dosage": "SODF",
                "Strength / Size": "40mg [c]"
            },
            {
                "Medicine Name": "Tiotropium",
                "Dosage": "Powder for inhalation in \r\na capsule",
                "Strength / Size": "18 micrograms / capsule"
            },
            {
                "Medicine Name": "Tocilizumab",
                "Dosage": "Injection (solution for IV \r\ninfusion)",
                "Strength / Size": "20mg/mL (4mL vial)"
            },
            {
                "Medicine Name": "Tocilizumab",
                "Dosage": "Injection (solution for IV \r\ninfusion)",
                "Strength / Size": "20mg/mL (4mL vial)"
            },
            {
                "Medicine Name": "Tolvaptan",
                "Dosage": "Tablet",
                "Strength / Size": "15mg"
            },
            {
                "Medicine Name": "Topotecan",
                "Dosage": "Injection",
                "Strength / Size": "2.5mg"
            },
            {
                "Medicine Name": "Torasemide",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Total parenteral nutrition  (TPN) with Medum chain  Triglycerides (MCT) / Long  chain Triglycerides (LCT)",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "625mL bag565"
            },
            {
                "Medicine Name": "Total parenteral nutrition  (TPN) with Medum chain  Triglycerides (MCT) / Long  chain Triglycerides (LCT)",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "1,250mL bag566"
            },
            {
                "Medicine Name": "Tranexamic acid",
                "Dosage": "Injection",
                "Strength / Size": "100mg/mL (5mL amp)"
            },
            {
                "Medicine Name": "Tranexamic acid",
                "Dosage": "Tablet",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Tranexamic acid",
                "Dosage": "Injection",
                "Strength / Size": "100mg/mL (10mL amp)"
            },
            {
                "Medicine Name": "Trastuzumab",
                "Dosage": "PFI",
                "Strength / Size": "150mg vial"
            },
            {
                "Medicine Name": "Trastuzumab",
                "Strength / Size": "440mg vial + diluent"
            },
            {
                "Medicine Name": "Triamcinolone acetonide417   Injection",
                "Dosage": "(aq. suspension)",
                "Strength / Size": "40mg/1mL amp"
            },
            {
                "Medicine Name": "Trimetazidine",
                "Dosage": "Tablet (m/r)",
                "Strength / Size": "35mg"
            },
            {
                "Medicine Name": "Tropicamide +   Phenylephrine",
                "Dosage": "Eye drops",
                "Strength / Size": "0.8% + 5% w/v"
            },
            {
                "Medicine Name": "Tropicamide +   phenylephrine",
                "Dosage": "Eye drops",
                "Strength / Size": "0.8% + 5% w/v"
            },
            {
                "Medicine Name": "Tuberculin, purified  protein,  derivative (PPD)",
                "Dosage": "Injection (solution)",
                "Strength / Size": "0.1mL vial (single dose)"
            },
            {
                "Medicine Name": "Typhoid vaccine",
                "Dosage": "Injection (solution)",
                "Strength / Size": "Single or multi dose"
            },
            {
                "Medicine Name": "Valgancyclovir",
                "Dosage": "Tablet",
                "Strength / Size": "450mg"
            },
            {
                "Medicine Name": "Valproic acid   (Sodium Valproate)",
                "Dosage": "Injection89",
                "Strength / Size": "100mg/mL in 4mL amp"
            },
            {
                "Medicine Name": "Valproic acid   (Sodium Valproate)",
                "Strength / Size": "100mg/mL in 10mL amp"
            },
            {
                "Medicine Name": "Valproic acid   (Sodium Valproate)",
                "Dosage": "Oral liquid",
                "Strength / Size": "200mg/5mL"
            },
            {
                "Medicine Name": "Valproic acid   (Sodium Valproate)",
                "Dosage": "Tablet (e/c)",
                "Strength / Size": "200mg"
            },
            {
                "Medicine Name": "Valproic acid   (Sodium Valproate)",
                "Strength / Size": "500mg"
            },
            {
                "Medicine Name": "Vancomycin",
                "Dosage": "PFI",
                "Strength / Size": "500mg vial (as HCl)"
            },
            {
                "Medicine Name": "Vasopressin",
                "Dosage": "Injection",
                "Strength / Size": "20 units/mL"
            },
            {
                "Medicine Name": "Vecuronium",
                "Dosage": "PFI",
                "Strength / Size": "10mg (as bromide) vial \r\n[c]"
            },
            {
                "Medicine Name": "Verapamil",
                "Dosage": "Tablet",
                "Strength / Size": "40mg (as HCl)"
            },
            {
                "Medicine Name": "Verapamil",
                "Dosage": "Tablet (s/r)",
                "Strength / Size": "240mg (as HCl)"
            },
            {
                "Medicine Name": "Vinblastine",
                "Dosage": "Injection",
                "Strength / Size": "1mg/mL (as sulphate) \r\n(10mL vial)"
            },
            {
                "Medicine Name": "Vincristine",
                "Dosage": "PFI",
                "Strength / Size": "1mg (as sulphate) vial"
            },
            {
                "Medicine Name": "Vinorelbine",
                "Dosage": "Injection",
                "Strength / Size": "10mg/mL (1mL vial)"
            },
            {
                "Medicine Name": "Vinorelbine",
                "Strength / Size": "10mg/mL (5mL vial)"
            },
            {
                "Medicine Name": "Vitamin B12 (Cobalamin)544   Tablet",
                "Strength / Size": "500 micrograms"
            },
            {
                "Medicine Name": "Vitamins & Minerals mix543   Powder",
                "Strength / Size": "1g sachet [c]"
            },
            {
                "Medicine Name": "Voriconazole",
                "Dosage": "PFI",
                "Strength / Size": "200mg vial"
            },
            {
                "Medicine Name": "Warfarin",
                "Dosage": "Tablet (scored)",
                "Strength / Size": "1mg (as sodium salt)"
            },
            {
                "Medicine Name": "Warfarin",
                "Strength / Size": "5mg (as sodium salt)"
            },
            {
                "Medicine Name": "Water for injection",
                "Dosage": "Injection",
                "Strength / Size": "10 mL amp"
            },
            {
                "Medicine Name": "Water-soluble vitamins",
                "Dosage": "Solution for IV infusion",
                "Strength / Size": "10mL"
            },
            {
                "Medicine Name": "White soft paraffin   (Petroleum jelly)",
                "Dosage": "Topical application",
                "Strength / Size": "100g"
            },
            {
                "Medicine Name": "Whole blood"
            },
            {
                "Medicine Name": "Xylometazoline",
                "Dosage": "Nasal spray",
                "Strength / Size": "0.05%"
            },
            {
                "Medicine Name": "Zidovudine (AZT or ZDV)",
                "Dosage": "Oral liquid",
                "Strength / Size": "50mg/5mL"
            },
            {
                "Medicine Name": "Zidovudine (AZT or ZDV)",
                "Dosage": "Tablet",
                "Strength / Size": "300mg"
            },
            {
                "Medicine Name": "Zidovudine + Lamivudine  (AZT/3TC)",
                "Dosage": "Tablet",
                "Strength / Size": "60mg + 30mg [c]"
            },
            {
                "Medicine Name": "Zidovudine + Lamivudine  (AZT/3TC)",
                "Strength / Size": "300mg + 150mg"
            },
            {
                "Medicine Name": "Zinc Hyaluronate   (zinc-hyaluronan)",
                "Dosage": "Gel (water-based)",
                "Strength / Size": "15g"
            },
            {
                "Medicine Name": "Zinc sulphate",
                "Dosage": "Tablet (dispersible)",
                "Strength / Size": "20mg"
            },
            {
                "Medicine Name": "Zoledronic acid",
                "Dosage": "Concentrate solution \r\nfor Infusion",
                "Strength / Size": "800 micrograms/mL  \r\n(in 5mL vial)"
            },
            {
                "Medicine Name": "Zoledronic acid",
                "Dosage": "Injection",
                "Strength / Size": "5mg (in 100mL)"
            },
            {
                "Medicine Name": "Zolpidem",
                "Dosage": "Tablet",
                "Strength / Size": "10mg"
            },
            {
                "Medicine Name": "Zuclopenthixol",
                "Dosage": "Injection (oily)456",
                "Strength / Size": "100mg/mL (as acetate) \r\n(2mL amp)"
            },
            {
                "Medicine Name": "Zuclopenthixol",
                "Dosage": "Injection (oily, depot)457",
                "Strength / Size": "200mg/1mL (as \r\ndecanoate) amp"
            },
            {
                "Medicine Name": "Zuclopenthixol",
                "Dosage": "Oral drops458",
                "Strength / Size": "20mg/mL (20mL)"
            }
        ]
    }

#bench new-site osh.lonius.co.ke --admin-password 'velo@2020' --mariadb-root-username erpuser --mariadb-root-password 'velo@2020'

