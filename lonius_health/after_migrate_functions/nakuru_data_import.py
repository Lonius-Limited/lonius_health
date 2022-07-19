import frappe
#price_list_rate
#item_description=f{},price_list='Liason Price List',selling=1
def upload():
    liason, pl =  get_liason()
    list(map(lambda x:actual_upload(x, pl), liason))  
    madison, pl2 = get_madison()
    list(map(lambda x:actual_upload(x, pl2), madison))  
    saham, pl3 = get_saham ()
    list(map(lambda x:actual_upload(x, pl3), saham))       
def actual_upload(b, pl):
    if not b.get("item"): return
    if not b.get("rate") : b["rate"] = 0.0
    sql = "UPDATE `tabItem Price` SET price_list_rate ={} WHERE item_description='{}' AND price_list='{}' AND selling=1;".format(float(b.get("rate")), b.get("item"), pl)
    print(sql)
    frappe.db.sql(sql)
def get_liason():
    payload = [
        {
            "item": "Consultation",
            "rate": "3000.00"
        },
        {
            "item": "Hospital Visits",
            "rate": "5000.00"
        },
        {
            "item": "Emergency Night Visits",
            "rate": "10000.00"
        },
        {
            "item": "Emergency Day Visits",
            "rate": "7000.00"
        },
        {
            "item": "ICU Visit (Daily Charges)",
            "rate": "7000.00"
        },
        {
            "item": "HDU Visit (Daily Charges)",
            "rate": "6000.00"
        },
        {
            "item": "Adenoidectomy & Septoplasty",
            "rate": "110000.00"
        },
        {
            "item": "Adenoidectomy (Adults)",
            "rate": "55000.00"
        },
        {
            "item": "Adenoidectomy (Paediatric)",
            "rate": "55000.00"
        },
        {
            "item": "Adenoidectomy Myringotomy & Insertion of Grommets",
            "rate": "65000.00"
        },
        {
            "item": "Adenotonsilectomy Myringotomy & Insertion of Grommets",
            "rate": "80000.00"
        },
        {
            "item": "Adenotonsillectomy (Adult)",
            "rate": "75000.00"
        },
        {
            "item": "Adenotonsillectomy (Paediatric)",
            "rate": "65000.00"
        },
        {
            "item": "Adenotonsillectomy + SMD",
            "rate": "85000.00"
        },
        {
            "item": "AS & Removal of Foreign Body - GA",
            "rate": "58000.00"
        },
        {
            "item": "AS/BAWO",
            "rate": "65000.00"
        },
        {
            "item": "AS/BAWO/Release of Tongue Tie",
            "rate": "70000.00"
        },
        {
            "item": "AS/SMD",
            "rate": "65000.00"
        },
        {
            "item": "AS/SMD/BAWO",
            "rate": "75000.00"
        },
        {
            "item": "AS/TS & Turbinoplasty",
            "rate": "95000.00"
        },
        {
            "item": "AS/TS/SMD Myringotomy & Insertion of Grommets",
            "rate": "105000.00"
        },
        {
            "item": "Audiometry – PTA (Pure tone)",
            "rate": "4000.00"
        },
        {
            "item": "Audiometry (Speech Audiometry – SRT/WRC)",
            "rate": "6000.00"
        },
        {
            "item": "Aural Polypectomy",
            "rate": "45000.00"
        },
        {
            "item": "Aural Toilet",
            "rate": "3000.00"
        },
        {
            "item": "Base of Tongue Reduction",
            "rate": "55000.00"
        },
        {
            "item": "BAWO – GA",
            "rate": "55000.00"
        },
        {
            "item": "BAWO – LA",
            "rate": "45000.00"
        },
        {
            "item": "BAWO/SMD",
            "rate": "60000.00"
        },
        {
            "item": "BERA (With Sedation)",
            "rate": "15000.00"
        },
        {
            "item": "BERA (Without Sedation)",
            "rate": "12000.00"
        },
        {
            "item": "Biopsy Parapharyngeal Mass",
            "rate": "50000.00"
        },
        {
            "item": "Brochoscopy,DL & Decanulation",
            "rate": "70000.00"
        },
        {
            "item": "Bronchoscopy – Diagnostic",
            "rate": "50000.00"
        },
        {
            "item": "Bronchoscopy & Dilatation",
            "rate": "75000.00"
        },
        {
            "item": "Bronchoscopy & FB Removal",
            "rate": "75000.00"
        },
        {
            "item": "Cervical Lymphnode Biopsy",
            "rate": "45000.00"
        },
        {
            "item": "Chemical Cautery",
            "rate": "15000.00"
        },
        {
            "item": "Choanoplasty",
            "rate": "160000.00"
        },
        {
            "item": "Cleaning Under Microscope (EUM)",
            "rate": "7500.00"
        },
        {
            "item": "Conchoplasty",
            "rate": "65000.00"
        },
        {
            "item": "D/L, Microlaryngeal E/o Papillomas & Injection of Cidojovir (Excludes cost\nof Cidojovir)",
            "rate": "130000.00"
        },
        {
            "item": "Direct Laryngoscopy",
            "rate": "50000.00"
        },
        {
            "item": "Direct Laryngoscopy & Biopsy",
            "rate": "65000.00"
        },
        {
            "item": "Direct Laryngoscopy & EUA",
            "rate": "65000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal Excision of Vocal Fold cyst",
            "rate": "75000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal E/o Papillomas",
            "rate": "90000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal Excision of Leukoplakia",
            "rate": "110000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal Excision of Polyps",
            "rate": "100000.00"
        },
        {
            "item": "Direct Laryngoscopy & MicroLaryngeal excision of Recurrent Laryngeal\nPapillomas",
            "rate": "110000.00"
        },
        {
            "item": "Direct Laryngoscopy & MicroLaryngeal Excision of Vocal Mass",
            "rate": "90000.00"
        },
        {
            "item": "Direct Laryngoscopy & MicroLaryngeal excision of Vocal Nodule",
            "rate": "75000.00"
        },
        {
            "item": "Direct Laryngoscopy & Tracheostomy",
            "rate": "85000.00"
        },
        {
            "item": "Douching",
            "rate": "2000.00"
        },
        {
            "item": "Drainage of Septal Abscess or I&D Furuncle GA",
            "rate": "30000.00"
        },
        {
            "item": "Drainage of Septal Abscess or I&D Furuncle LA",
            "rate": "20000.00"
        },
        {
            "item": "Dressing",
            "rate": "1500.00"
        },
        {
            "item": "Ear Bandits",
            "rate": "3000.00"
        },
        {
            "item": "Ear Plugs",
            "rate": "1000.00"
        },
        {
            "item": "Electro Cautery Littles Area (Epistaxis) – GA",
            "rate": "30000.00"
        },
        {
            "item": "Electro Cautery Littles Area (Epistaxis) – LA",
            "rate": "20000.00"
        },
        {
            "item": "Endoscopic DCR",
            "rate": "120000.00"
        },
        {
            "item": "Endoscopic Decompression of Optic Nerve",
            "rate": "120000.00"
        },
        {
            "item": "Endoscopic E/O Nasal Mass",
            "rate": "150000.00"
        },
        {
            "item": "Endoscopic Excision of PNS mass",
            "rate": "120000.00"
        },
        {
            "item": "Endoscopic Repair CSF Rhinorhea",
            "rate": "225000.00"
        },
        {
            "item": "Endoscopic Trans-sphenoidal E/o pituitary tumor.",
            "rate": "270000.00"
        },
        {
            "item": "Endoscopic Vocal Cord Laretalisation",
            "rate": "115000.00"
        },
        {
            "item": "Endoscopy – Flexible",
            "rate": "18000.00"
        },
        {
            "item": "Endoscopy – Rigid",
            "rate": "18000.00"
        },
        {
            "item": "Endoscopy (Nasal) + Biopsy (Flexible/Rigid)",
            "rate": "25000.00"
        },
        {
            "item": "EUA & Adenoidectomy",
            "rate": "50000.00"
        },
        {
            "item": "EUA & Aural Toilet",
            "rate": "30000.00"
        },
        {
            "item": "EUA & Biopsy – PNS (Rigid Nasoendoscopy under GA)",
            "rate": "45000.00"
        },
        {
            "item": "EUA & Control of Haemorrhage",
            "rate": "55000.00"
        },
        {
            "item": "EUA & Galvanocautery",
            "rate": "35000.00"
        },
        {
            "item": "EUA & R/O Foreign Body",
            "rate": "30000.00"
        },
        {
            "item": "EUA & R/O Nasal stents",
            "rate": "35000.00"
        },
        {
            "item": "EUA PNS & BAWO",
            "rate": "50000.00"
        },
        {
            "item": "EUA, Aural Toilet & Myringotomy + Insertion of Grommets",
            "rate": "50000.00"
        },
        {
            "item": "EUA, Nasal Cautery & Septoplasty",
            "rate": "80000.00"
        },
        {
            "item": "EUA/PNS BIOPSY/MYRINGOTOMY",
            "rate": "55000.00"
        },
        {
            "item": "Evacuation Of Haematoma",
            "rate": "40000.00"
        },
        {
            "item": "Excision Cystic Hygroma",
            "rate": "100000.00"
        },
        {
            "item": "Excision of Aural Exostosis",
            "rate": "95000.00"
        },
        {
            "item": "Excision of Auricular Cyst",
            "rate": "50000.00"
        },
        {
            "item": "Excision of Maxillary Mass",
            "rate": "120000.00"
        },
        {
            "item": "Excision of Nasal Synachea",
            "rate": "60000.00"
        },
        {
            "item": "Excision of Palatal Cyst",
            "rate": "75000.00"
        },
        {
            "item": "Excision of Parotid Cyst",
            "rate": "75000.00"
        },
        {
            "item": "Excision of Tongue Granuloma",
            "rate": "50000.00"
        },
        {
            "item": "Excision Ranula Cyst",
            "rate": "80000.00"
        },
        {
            "item": "Excision Thyroglossal Duct Cyst",
            "rate": "80000.00"
        },
        {
            "item": "Excision/ Galvanocautery Warts",
            "rate": "30000.00"
        },
        {
            "item": "FB Removal (Ear) – GA",
            "rate": "25000.00"
        },
        {
            "item": "FB Removal (Ear) – LA",
            "rate": "10000.00"
        },
        {
            "item": "FB Removal (Nose) – GA",
            "rate": "25000.00"
        },
        {
            "item": "FB Removal (Nose) – LA",
            "rate": "15000.00"
        },
        {
            "item": "FESS",
            "rate": "100000.00"
        },
        {
            "item": "FESS - Revision",
            "rate": "120000.00"
        },
        {
            "item": "FESS & Adenoidectomy",
            "rate": "120000.00"
        },
        {
            "item": "FESS & E/O Antrochoanal Polyps",
            "rate": "140000.00"
        },
        {
            "item": "FESS & Excision of Ethmoid Mass",
            "rate": "150000.00"
        },
        {
            "item": "Fess / BAWO / Septoplasty / Tympanoplasty",
            "rate": "130000.00"
        },
        {
            "item": "Fess & Polypectomy",
            "rate": "140000.00"
        },
        {
            "item": "FESS & Polypectomy - Revision",
            "rate": "150000.00"
        },
        {
            "item": "FESS & Repair of Oro-Antral Fistula",
            "rate": "140000.00"
        },
        {
            "item": "Fess + Chonchoplasty",
            "rate": "120000.00"
        },
        {
            "item": "Fess + Chonchoplasty + Turbinoplasty",
            "rate": "165000.00"
        },
        {
            "item": "FESS + Septoplasty",
            "rate": "140000.00"
        },
        {
            "item": "FESS + Tonsilectomy",
            "rate": "140000.00"
        },
        {
            "item": "FESS + Turbinoplasty",
            "rate": "140000.00"
        },
        {
            "item": "Fess + Turbinoplasty + Tonsilectomy",
            "rate": "165000.00"
        },
        {
            "item": "FESS and removal  of Aural  Keratosis",
            "rate": "110000.00"
        },
        {
            "item": "FESS, AS & TS",
            "rate": "155000.00"
        },
        {
            "item": "FESS, AS, TS, SMD",
            "rate": "165000.00"
        },
        {
            "item": "FESS, Polypectomy & Septoplasty",
            "rate": "170000.00"
        },
        {
            "item": "FESS, Polypectomy & Turbinoplasty",
            "rate": "165000.00"
        },
        {
            "item": "FESS, Septoplasty & Adenoidectomy - Revision",
            "rate": "170000.00"
        },
        {
            "item": "FESS, Turbinoplasty & AS",
            "rate": "165000.00"
        },
        {
            "item": "FESS, Turbinoplasty & Release of Nasal Synaechae",
            "rate": "150000.00"
        },
        {
            "item": "FESS, Turbinoplasty & SNE",
            "rate": "155000.00"
        },
        {
            "item": "FESS, Turbinoplasty, Septoplasty & Conchoplasty",
            "rate": "170000.00"
        },
        {
            "item": "Fess,Turbinoplasty & Septoplasty",
            "rate": "160000.00"
        },
        {
            "item": "FLEXIBLE ENDOSCOPIC EVALUATION OF SWALLOWING",
            "rate": "35000.00"
        },
        {
            "item": "Flexible Nasal Pharyngoscopy",
            "rate": "20000.00"
        },
        {
            "item": "Flexible Nasopharyngoscopy & Biopsy",
            "rate": "30000.00"
        },
        {
            "item": "Flexible Videolaryngoscopy & Voice assessment",
            "rate": "30000.00"
        },
        {
            "item": "Frenulectomy",
            "rate": "25000.00"
        },
        {
            "item": "Galvanocaurtery of nose",
            "rate": "25000.00"
        },
        {
            "item": "Glossectomy - Partial",
            "rate": "140000.00"
        },
        {
            "item": "HEARING AID FITTING",
            "rate": "5000.00"
        },
        {
            "item": "I & D Abscess (Neck) – GA",
            "rate": "25000.00"
        },
        {
            "item": "I & D Abscess (Neck) – LA",
            "rate": "15000.00"
        },
        {
            "item": "I & D and Biopsy",
            "rate": "55000.00"
        },
        {
            "item": "I & D Preauricular Abscess",
            "rate": "30000.00"
        },
        {
            "item": "I&D of Submandibular Abscess",
            "rate": "30000.00"
        },
        {
            "item": "I&D Peritonsilar Abscess",
            "rate": "50000.00"
        },
        {
            "item": "Incision and Drainage of Head and Neck abscess I&D)",
            "rate": "30000.00"
        },
        {
            "item": "Injection of Cidofovir",
            "rate": "85000.00"
        },
        {
            "item": "Insertion of Earwick",
            "rate": "10000.00"
        },
        {
            "item": "Keloid Excision{ear}",
            "rate": "45000.00"
        },
        {
            "item": "LARYNGEAL VIDEO STROBOSCOPY",
            "rate": "25000.00"
        },
        {
            "item": "Laryngectomy - Partial",
            "rate": "175000.00"
        },
        {
            "item": "Laryngectomy - Total",
            "rate": "210000.00"
        },
        {
            "item": "Laryngoscopy - Flexible",
            "rate": "18000.00"
        },
        {
            "item": "Laryngoscopy - Rigid",
            "rate": "18000.00"
        },
        {
            "item": "Laryngotracheal Reconstruction",
            "rate": "195000.00"
        },
        {
            "item": "Larynx Videostroboscopy",
            "rate": "25000.00"
        },
        {
            "item": "Larynx Videostroboscopy – Repeat",
            "rate": "15000.00"
        },
        {
            "item": "Lymphnode Biopsy – GA",
            "rate": "25000.00"
        },
        {
            "item": "Lymphnode Biopsy– LA",
            "rate": "20000.00"
        },
        {
            "item": "Mastoidectomy - Cortical",
            "rate": "130000.00"
        },
        {
            "item": "Mastoidectomy - Radical",
            "rate": "150000.00"
        },
        {
            "item": "Mastoidectomy - Revision",
            "rate": "180000.00"
        },
        {
            "item": "Maxillectomy – Partial",
            "rate": "95000.00"
        },
        {
            "item": "Maxillectomy – Total",
            "rate": "110000.00"
        },
        {
            "item": "Microlaryngeal Surgery",
            "rate": "90000.00"
        },
        {
            "item": "Modified Neck Dissection - Bilateral",
            "rate": "395000.00"
        },
        {
            "item": "Modified Neck Dissection - Unilateral",
            "rate": "200000.00"
        },
        {
            "item": "Myringotomy & Insertion of Grommets – GA",
            "rate": "55000.00"
        },
        {
            "item": "Myringotomy & Insertion of Grommets – LA",
            "rate": "45000.00"
        },
        {
            "item": "Myringotomy & Insertion of T-tube Grommets - Bilateral",
            "rate": "80000.00"
        },
        {
            "item": "Myringotomy & Insertion of T-tube Grommets - Unilateral",
            "rate": "60000.00"
        },
        {
            "item": "Myringotomy, Grommet insertion, EUA PNS biopsy",
            "rate": "80000.00"
        },
        {
            "item": "Nasal Biopsy",
            "rate": "27500.00"
        },
        {
            "item": "Nasal Cautery + SMD",
            "rate": "45000.00"
        },
        {
            "item": "Nasal Packing - Anterior",
            "rate": "10000.00"
        },
        {
            "item": "Nasal Polypectomy",
            "rate": "50000.00"
        },
        {
            "item": "Nasal Reconstruction - 1st Stage",
            "rate": "112500.00"
        },
        {
            "item": "Nasal Reconstruction - 2nd Stage",
            "rate": "90000.00"
        },
        {
            "item": "Nasal Toilet",
            "rate": "5000.00"
        },
        {
            "item": "Nasal vestibular Abcess drainage",
            "rate": "25000.00"
        },
        {
            "item": "Nasoendoscopy - Rigid",
            "rate": "15000.00"
        },
        {
            "item": "Nasopharyngoscopy",
            "rate": "20000.00"
        },
        {
            "item": "OAE",
            "rate": "5000.00"
        },
        {
            "item": "OCCUPATIONAL HEARING ASSESSMENT",
            "rate": "15000.00"
        },
        {
            "item": "Oesophagoscopy",
            "rate": "45000.00"
        },
        {
            "item": "Oesophagoscopy & FB Removal",
            "rate": "60000.00"
        },
        {
            "item": "Palatoplasty",
            "rate": "90000.00"
        },
        {
            "item": "Panaendoscopy",
            "rate": "75000.00"
        },
        {
            "item": "Panendoscopy & Excisional biopsy of Cervical Mass",
            "rate": "107500.00"
        },
        {
            "item": "Parotidectomy – Superficial",
            "rate": "140000.00"
        },
        {
            "item": "Parotidectomy – Total",
            "rate": "190000.00"
        },
        {
            "item": "Parotidectomy & Submandibular Gland Excision",
            "rate": "180000.00"
        },
        {
            "item": "PEADIATRIC HEARING ASSESSMENT",
            "rate": "5000.00"
        },
        {
            "item": "Peritonsillar Abscess Drainage",
            "rate": "50000.00"
        },
        {
            "item": "Pharyngoplasty",
            "rate": "110000.00"
        },
        {
            "item": "Polypectomy -Antrochoanal",
            "rate": "65000.00"
        },
        {
            "item": "Preauricular Sinus Excision – GA",
            "rate": "42500.00"
        },
        {
            "item": "Preauricular Sinus Excision – LA",
            "rate": "37500.00"
        },
        {
            "item": "Punch Biopsy",
            "rate": "15000.00"
        },
        {
            "item": "Realese of Tongue Tie",
            "rate": "25000.00"
        },
        {
            "item": "Reduction of Nasal Fracture – GA",
            "rate": "45000.00"
        },
        {
            "item": "Reduction of Nasal Fracture – LA",
            "rate": "35000.00"
        },
        {
            "item": "Release of Nasal Synaechae",
            "rate": "50000.00"
        },
        {
            "item": "Release of Nasal Synaechae & Turbinoplasty",
            "rate": "70000.00"
        },
        {
            "item": "Removal Aural Warts – GA",
            "rate": "20000.00"
        },
        {
            "item": "Removal Aural Warts – LA",
            "rate": "15000.00"
        },
        {
            "item": "Removal Of Grommets",
            "rate": "20000.00"
        },
        {
            "item": "Removal Of Impacted Wax /GA",
            "rate": "15000.00"
        },
        {
            "item": "Removal of maxillary pack",
            "rate": "20000.00"
        },
        {
            "item": "Removal Of Sutures",
            "rate": "1000.00"
        },
        {
            "item": "Rigid Nasoendoscopy/Hypopharyngoscopy/ Laryngoscopy",
            "rate": "50000.00"
        },
        {
            "item": "Septoplasty",
            "rate": "80000.00"
        },
        {
            "item": "Septoplasty & R/O of Nasal Synaechiae",
            "rate": "92500.00"
        },
        {
            "item": "Septoplasty + Turbinoplasty",
            "rate": "105000.00"
        },
        {
            "item": "Septoplasty, Palatoplasty & Turbinoplasty",
            "rate": "165500.00"
        },
        {
            "item": "Septoplasty, Turbinoplasty & Nasal Cautery",
            "rate": "120000.00"
        },
        {
            "item": "Septoplasty, Turbinoplasty & R/O Oronasal Fistula",
            "rate": "140000.00"
        },
        {
            "item": "Septoplasty,Turbinoplasty & Conchoplasty",
            "rate": "140000.00"
        },
        {
            "item": "Sleep Nasoendoscopy",
            "rate": "30000.00"
        },
        {
            "item": "Sleep Nasopharyngoscopy",
            "rate": "40000.00"
        },
        {
            "item": "Sleep Study - Ambulatory",
            "rate": "27500.00"
        },
        {
            "item": "Submandibular Gland Excision (Sialadenectomy) – Bilateral",
            "rate": "110000.00"
        },
        {
            "item": "Submandibular Gland Excision (Sialadenectomy) – Unilateral",
            "rate": "80000.00"
        },
        {
            "item": "Submucous Diathermy of Inferior Turbinates",
            "rate": "35000.00"
        },
        {
            "item": "Surgical toilet and suturing of facial wounds",
            "rate": "45000.00"
        },
        {
            "item": "Syringing",
            "rate": "5000.00"
        },
        {
            "item": "TINNITUS COUNSELLING",
            "rate": "5000.00"
        },
        {
            "item": "Tonsillectomy – Adults",
            "rate": "60000.00"
        },
        {
            "item": "Tonsillectomy – Children",
            "rate": "55000.00"
        },
        {
            "item": "Tonsillectomy + AS + BAWO",
            "rate": "90000.00"
        },
        {
            "item": "Tonsillectomy + AS + SMD",
            "rate": "95000.00"
        },
        {
            "item": "Tonsillectomy + Excision of Preauricular Sinus",
            "rate": "80000.00"
        },
        {
            "item": "Tonsillectomy + Insertion of Grommets - (Paediatric)",
            "rate": "70000.00"
        },
        {
            "item": "Tonsillectomy + Myringotomy + Insertion of Grommets",
            "rate": "80000.00"
        },
        {
            "item": "Tonsillectomy + Oesophagoscopy",
            "rate": "80000.00"
        },
        {
            "item": "Tonsillectomy + SMD",
            "rate": "60000.00"
        },
        {
            "item": "Tonsillectomy + SMD + Sleep Nasal Endoscopy",
            "rate": "90000.00"
        },
        {
            "item": "Tonsillectomy + Turbinoplasty + Conchoplasty",
            "rate": "122500.00"
        },
        {
            "item": "Tonsillectomy + Tympanoplasty - Unilateral",
            "rate": "115000.00"
        },
        {
            "item": "Tonsillectomy + Uvuloplasty",
            "rate": "115000.00"
        },
        {
            "item": "Tonsillectomy +AS",
            "rate": "60000.00"
        },
        {
            "item": "Tonsillectomy +AS + BAWO + SMD",
            "rate": "105000.00"
        },
        {
            "item": "Tonsillectomy +AS + Insertion of Grommets",
            "rate": "75000.00"
        },
        {
            "item": "Tonsillectomy and EUA",
            "rate": "65000.00"
        },
        {
            "item": "Tracheostomy",
            "rate": "65000.00"
        },
        {
            "item": "Turbinoplasty",
            "rate": "72000.00"
        },
        {
            "item": "Turbinoplasty & AS",
            "rate": "102000.00"
        },
        {
            "item": "Turbinoplasty & Conchoplasty",
            "rate": "114000.00"
        },
        {
            "item": "Turbinoplasty & E/O Septal Spur",
            "rate": "7200.00"
        },
        {
            "item": "Turbinoplasty & Palatoplasty",
            "rate": "153000.00"
        },
        {
            "item": "Turbinoplasty + UPPP",
            "rate": "228000.00"
        },
        {
            "item": "Turbinoplasty, Septoplasty & Release of Synaechiae",
            "rate": "156000.00"
        },
        {
            "item": "Turbinoplasty,Conchoplasty & Palatoplasty",
            "rate": "192000.00"
        },
        {
            "item": "Tympanomastoidectomy",
            "rate": "240000.00"
        },
        {
            "item": "TYMPANOMETRY",
            "rate": "6000.00"
        },
        {
            "item": "Tympanoplasty – Unilateral",
            "rate": "108000.00"
        },
        {
            "item": "Tympanoplasty– Bilateral",
            "rate": "171000.00"
        },
        {
            "item": "Uvulectomy",
            "rate": "42000.00"
        },
        {
            "item": "Uvulopalatopharyngoplasty (UPPP)",
            "rate": "204000.00"
        },
        {
            "item": "Uvulopalatopharyngoplasty (UPPP) + Septoplasty + Turbinoplasty",
            "rate": "264000.00"
        },
        {
            "item": "Uvulopalatopharyngoplasty (UPPP) + Turbinoplasty",
            "rate": "240000.00"
        },
        {
            "item": "Uvuloplasty",
            "rate": "99000.00"
        },
        {
            "item": "VESTIBULAR ASSESSMENT",
            "rate": "21600.00"
        },
        {
            "item": "VESTIBULAR REHABILITATION",
            "rate": "3600.00"
        },
        {
            "item": "Video Otoscopy",
            "rate": "4800.00"
        },
        {
            "item": "Video-Laryngoscopy",
            "rate": "78000.00"
        },
        {
            "item": "Vocal Cord Lateralisation + Arytenoidectomy",
            "rate": "84000.00"
        },
        {
            "item": "Vocal Cord Lateralisation + Arytenoidectomy",
            "rate": "78000.00"
        },
        {
            "item": "Vocal Fold Medialization",
            "rate": "138000.00"
        },
        {
            "item": "Voice Therapy",
            "rate": "6000.00"
        },
        {
            "item": "Voice Clinic / Evaluation",
            "rate": "7800.00"
        }
    ]
    return payload,'Liason Price List'
def get_saham():
    payload =[
        {
            "item": "Consultation",
            "rate": "3600.00"
        },
        {
            "item": "Hospital Visits",
            "rate": "6000.00"
        },
        {
            "item": "Emergency Night Visits",
            "rate": "12000.00"
        },
        {
            "item": "Emergency Day Visits",
            "rate": "8400.00"
        },
        {
            "item": "ICU Visit (Daily Charges)",
            "rate": "8400.00"
        },
        {
            "item": "HDU Visit (Daily Charges)",
            "rate": "7200.00"
        },
        {
            "item": "Adenoidectomy & Septoplasty",
            "rate": "132000.00"
        },
        {
            "item": "Adenoidectomy (Adults)",
            "rate": "66000.00"
        },
        {
            "item": "Adenoidectomy (Paediatric)",
            "rate": "66000.00"
        },
        {
            "item": "Adenoidectomy Myringotomy & Insertion of Grommets",
            "rate": "78000.00"
        },
        {
            "item": "Adenotonsilectomy Myringotomy & Insertion of Grommets",
            "rate": "96000.00"
        },
        {
            "item": "Adenotonsillectomy (Adult)",
            "rate": "90000.00"
        },
        {
            "item": "Adenotonsillectomy (Paediatric)",
            "rate": "78000.00"
        },
        {
            "item": "Adenotonsillectomy + SMD",
            "rate": "102000.00"
        },
        {
            "item": "AS & Removal of Foreign Body - GA",
            "rate": "69600.00"
        },
        {
            "item": "AS/BAWO",
            "rate": "78000.00"
        },
        {
            "item": "AS/BAWO/Release of Tongue Tie",
            "rate": "84000.00"
        },
        {
            "item": "AS/SMD",
            "rate": "78000.00"
        },
        {
            "item": "AS/SMD/BAWO",
            "rate": "90000.00"
        },
        {
            "item": "AS/TS & Turbinoplasty",
            "rate": "114000.00"
        },
        {
            "item": "AS/TS/SMD Myringotomy & Insertion of Grommets",
            "rate": "126000.00"
        },
        {
            "item": "Audiometry – PTA (Pure tone)",
            "rate": "4800.00"
        },
        {
            "item": "Audiometry (Speech Audiometry – SRT/WRC)",
            "rate": "7200.00"
        },
        {
            "item": "Aural Polypectomy",
            "rate": "54000.00"
        },
        {
            "item": "Aural Toilet",
            "rate": "3600.00"
        },
        {
            "item": "Base of Tongue Reduction",
            "rate": "66000.00"
        },
        {
            "item": "BAWO – GA",
            "rate": "66000.00"
        },
        {
            "item": "BAWO – LA",
            "rate": "54000.00"
        },
        {
            "item": "BAWO/SMD",
            "rate": "72000.00"
        },
        {
            "item": "BERA (With Sedation)",
            "rate": "18000.00"
        },
        {
            "item": "BERA (Without Sedation)",
            "rate": "14400.00"
        },
        {
            "item": "Biopsy Parapharyngeal Mass",
            "rate": "60000.00"
        },
        {
            "item": "Brochoscopy,DL & Decanulation",
            "rate": "84000.00"
        },
        {
            "item": "Bronchoscopy – Diagnostic",
            "rate": "60000.00"
        },
        {
            "item": "Bronchoscopy & Dilatation",
            "rate": "90000.00"
        },
        {
            "item": "Bronchoscopy & FB Removal",
            "rate": "90000.00"
        },
        {
            "item": "Cervical Lymphnode Biopsy",
            "rate": "54000.00"
        },
        {
            "item": "Chemical Cautery",
            "rate": "18000.00"
        },
        {
            "item": "Choanoplasty",
            "rate": "192000.00"
        },
        {
            "item": "Cleaning Under Microscope (EUM)",
            "rate": "9000.00"
        },
        {
            "item": "Conchoplasty",
            "rate": "78000.00"
        },
        {
            "item": "D/L, Microlaryngeal E/o Papillomas & Injection of Cidojovir (Excludes cost\nof Cidojovir)",
            "rate": "156000.00"
        },
        {
            "item": "Direct Laryngoscopy",
            "rate": "60000.00"
        },
        {
            "item": "Direct Laryngoscopy & Biopsy",
            "rate": "78000.00"
        },
        {
            "item": "Direct Laryngoscopy & EUA",
            "rate": "78000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal Excision of Vocal Fold cyst",
            "rate": "90000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal E/o Papillomas",
            "rate": "108000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal Excision of Leukoplakia",
            "rate": "132000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal Excision of Polyps",
            "rate": "120000.00"
        },
        {
            "item": "Direct Laryngoscopy & MicroLaryngeal excision of Recurrent Laryngeal\nPapillomas",
            "rate": "132000.00"
        },
        {
            "item": "Direct Laryngoscopy & MicroLaryngeal Excision of Vocal Mass",
            "rate": "108000.00"
        },
        {
            "item": "Direct Laryngoscopy & MicroLaryngeal excision of Vocal Nodule",
            "rate": "90000.00"
        },
        {
            "item": "Direct Laryngoscopy & Tracheostomy",
            "rate": "102000.00"
        },
        {
            "item": "Douching",
            "rate": "2400.00"
        },
        {
            "item": "Drainage of Septal Abscess or I&D Furuncle GA",
            "rate": "36000.00"
        },
        {
            "item": "Drainage of Septal Abscess or I&D Furuncle LA",
            "rate": "24000.00"
        },
        {
            "item": "Dressing",
            "rate": "1800.00"
        },
        {
            "item": "Ear Bandits",
            "rate": "3600.00"
        },
        {
            "item": "Ear Plugs",
            "rate": "1200.00"
        },
        {
            "item": "Electro Cautery Littles Area (Epistaxis) – GA",
            "rate": "36000.00"
        },
        {
            "item": "Electro Cautery Littles Area (Epistaxis) – LA",
            "rate": "24000.00"
        },
        {
            "item": "Endoscopic DCR",
            "rate": "144000.00"
        },
        {
            "item": "Endoscopic Decompression of Optic Nerve",
            "rate": "144000.00"
        },
        {
            "item": "Endoscopic E/O Nasal Mass",
            "rate": "180000.00"
        },
        {
            "item": "Endoscopic Excision of PNS mass",
            "rate": "144000.00"
        },
        {
            "item": "Endoscopic Repair CSF Rhinorhea",
            "rate": "270000.00"
        },
        {
            "item": "Endoscopic Trans-sphenoidal E/o pituitary tumor.",
            "rate": "324000.00"
        },
        {
            "item": "Endoscopic Vocal Cord Laretalisation",
            "rate": "138000.00"
        },
        {
            "item": "Endoscopy – Flexible",
            "rate": "21600.00"
        },
        {
            "item": "Endoscopy – Rigid",
            "rate": "21600.00"
        },
        {
            "item": "Endoscopy (Nasal) + Biopsy (Flexible/Rigid)",
            "rate": "30000.00"
        },
        {
            "item": "EUA & Adenoidectomy",
            "rate": "60000.00"
        },
        {
            "item": "EUA & Aural Toilet",
            "rate": "36000.00"
        },
        {
            "item": "EUA & Biopsy – PNS (Rigid Nasoendoscopy under GA)",
            "rate": "54000.00"
        },
        {
            "item": "EUA & Control of Haemorrhage",
            "rate": "66000.00"
        },
        {
            "item": "EUA & Galvanocautery",
            "rate": "42000.00"
        },
        {
            "item": "EUA & R/O Foreign Body",
            "rate": "36000.00"
        },
        {
            "item": "EUA & R/O Nasal stents",
            "rate": "42000.00"
        },
        {
            "item": "EUA PNS & BAWO",
            "rate": "60000.00"
        },
        {
            "item": "EUA, Aural Toilet & Myringotomy + Insertion of Grommets",
            "rate": "50000.00"
        },
        {
            "item": "EUA, Nasal Cautery & Septoplasty",
            "rate": "80000.00"
        },
        {
            "item": "EUA/PNS BIOPSY/MYRINGOTOMY",
            "rate": "66000.00"
        },
        {
            "item": "Evacuation Of Haematoma",
            "rate": "48000.00"
        },
        {
            "item": "Excision Cystic Hygroma",
            "rate": "120000.00"
        },
        {
            "item": "Excision of Aural Exostosis",
            "rate": "114000.00"
        },
        {
            "item": "Excision of Auricular Cyst",
            "rate": "60000.00"
        },
        {
            "item": "Excision of Maxillary Mass",
            "rate": "144000.00"
        },
        {
            "item": "Excision of Nasal Synachea",
            "rate": "72000.00"
        },
        {
            "item": "Excision of Palatal Cyst",
            "rate": "90000.00"
        },
        {
            "item": "Excision of Parotid Cyst",
            "rate": "90000.00"
        },
        {
            "item": "Excision of Tongue Granuloma",
            "rate": "60000.00"
        },
        {
            "item": "Excision Ranula Cyst",
            "rate": "96000.00"
        },
        {
            "item": "Excision Thyroglossal Duct Cyst",
            "rate": "96000.00"
        },
        {
            "item": "Excision/ Galvanocautery Warts",
            "rate": "36000.00"
        },
        {
            "item": "FB Removal (Ear) – GA",
            "rate": "36000.00"
        },
        {
            "item": "FB Removal (Ear) – LA",
            "rate": "12000.00"
        },
        {
            "item": "FB Removal (Nose) – GA",
            "rate": "30000.00"
        },
        {
            "item": "FB Removal (Nose) – LA",
            "rate": "18000.00"
        },
        {
            "item": "FESS",
            "rate": "120000.00"
        },
        {
            "item": "FESS - Revision",
            "rate": "144000.00"
        },
        {
            "item": "FESS & Adenoidectomy",
            "rate": "144000.00"
        },
        {
            "item": "FESS & E/O Antrochoanal Polyps",
            "rate": "168000.00"
        },
        {
            "item": "FESS & Excision of Ethmoid Mass",
            "rate": "180000.00"
        },
        {
            "item": "Fess / BAWO / Septoplasty / Tympanoplasty",
            "rate": "156000.00"
        },
        {
            "item": "Fess & Polypectomy",
            "rate": "168000.00"
        },
        {
            "item": "FESS & Polypectomy - Revision",
            "rate": "180000.00"
        },
        {
            "item": "FESS & Repair of Oro-Antral Fistula",
            "rate": "168000.00"
        },
        {
            "item": "Fess + Chonchoplasty",
            "rate": "144000.00"
        },
        {
            "item": "Fess + Chonchoplasty + Turbinoplasty",
            "rate": "198000.00"
        },
        {
            "item": "FESS + Septoplasty",
            "rate": "168000.00"
        },
        {
            "item": "FESS + Tonsilectomy",
            "rate": "168000.00"
        },
        {
            "item": "FESS + Turbinoplasty",
            "rate": "168000.00"
        },
        {
            "item": "Fess + Turbinoplasty + Tonsilectomy",
            "rate": "198000.00"
        },
        {
            "item": "FESS and removal  of Aural  Keratosis",
            "rate": "132000.00"
        },
        {
            "item": "FESS, AS & TS",
            "rate": "186000.00"
        },
        {
            "item": "FESS, AS, TS, SMD",
            "rate": "198000.00"
        },
        {
            "item": "FESS, Polypectomy & Septoplasty",
            "rate": "204000.00"
        },
        {
            "item": "FESS, Polypectomy & Turbinoplasty",
            "rate": "198000.00"
        },
        {
            "item": "FESS, Septoplasty & Adenoidectomy - Revision",
            "rate": "204000.00"
        },
        {
            "item": "FESS, Turbinoplasty & AS",
            "rate": "198000.00"
        },
        {
            "item": "FESS, Turbinoplasty & Release of Nasal Synaechae",
            "rate": "150000.00"
        },
        {
            "item": "FESS, Turbinoplasty & SNE",
            "rate": "186000.00"
        },
        {
            "item": "FESS, Turbinoplasty, Septoplasty & Conchoplasty",
            "rate": "204000.00"
        },
        {
            "item": "Fess,Turbinoplasty & Septoplasty",
            "rate": "192000.00"
        },
        {
            "item": "FLEXIBLE ENDOSCOPIC EVALUATION OF SWALLOWING",
            "rate": "42000.00"
        },
        {
            "item": "Flexible Nasal Pharyngoscopy",
            "rate": "24000.00"
        },
        {
            "item": "Flexible Nasopharyngoscopy & Biopsy",
            "rate": "36000.00"
        },
        {
            "item": "Flexible Videolaryngoscopy & Voice assessment",
            "rate": "36000.00"
        },
        {
            "item": "Frenulectomy",
            "rate": "30000.00"
        },
        {
            "item": "Galvanocaurtery of nose",
            "rate": "30000.00"
        },
        {
            "item": "Glossectomy - Partial",
            "rate": "168000.00"
        },
        {
            "item": "HEARING AID FITTING",
            "rate": "6000.00"
        },
        {
            "item": "I & D Abscess (Neck) – GA",
            "rate": "30000.00"
        },
        {
            "item": "I & D Abscess (Neck) – LA",
            "rate": "18000.00"
        },
        {
            "item": "I & D and Biopsy",
            "rate": "66000.00"
        },
        {
            "item": "I & D Preauricular Abscess",
            "rate": "36000.00"
        },
        {
            "item": "I&D of Submandibular Abscess",
            "rate": "36000.00"
        },
        {
            "item": "I&D Peritonsilar Abscess",
            "rate": "60000.00"
        },
        {
            "item": "Incision and Drainage of Head and Neck abscess I&D)",
            "rate": "36000.00"
        },
        {
            "item": "Injection of Cidofovir",
            "rate": "102000.00"
        },
        {
            "item": "Insertion of Earwick",
            "rate": "12000.00"
        },
        {
            "item": "Keloid Excision{ear}",
            "rate": "54000.00"
        },
        {
            "item": "LARYNGEAL VIDEO STROBOSCOPY",
            "rate": "30000.00"
        },
        {
            "item": "Laryngectomy - Partial",
            "rate": "210000.00"
        },
        {
            "item": "Laryngectomy - Total",
            "rate": "252000.00"
        },
        {
            "item": "Laryngoscopy - Flexible",
            "rate": "21600.00"
        },
        {
            "item": "Laryngoscopy - Rigid",
            "rate": "21600.00"
        },
        {
            "item": "Laryngotracheal Reconstruction",
            "rate": "234000.00"
        },
        {
            "item": "Larynx Videostroboscopy",
            "rate": "30000.00"
        },
        {
            "item": "Larynx Videostroboscopy – Repeat",
            "rate": "18000.00"
        },
        {
            "item": "Lymphnode Biopsy – GA",
            "rate": "30000.00"
        },
        {
            "item": "Lymphnode Biopsy– LA",
            "rate": "24000.00"
        },
        {
            "item": "Mastoidectomy - Cortical",
            "rate": "156000.00"
        },
        {
            "item": "Mastoidectomy - Radical",
            "rate": "180000.00"
        },
        {
            "item": "Mastoidectomy - Revision",
            "rate": "216000.00"
        },
        {
            "item": "Maxillectomy – Partial",
            "rate": "114000.00"
        },
        {
            "item": "Maxillectomy – Total",
            "rate": "132000.00"
        },
        {
            "item": "Microlaryngeal Surgery",
            "rate": "108000.00"
        },
        {
            "item": "Modified Neck Dissection - Bilateral",
            "rate": "474000.00"
        },
        {
            "item": "Modified Neck Dissection - Unilateral",
            "rate": "240000.00"
        },
        {
            "item": "Myringotomy & Insertion of Grommets – GA",
            "rate": "66000.00"
        },
        {
            "item": "Myringotomy & Insertion of Grommets – LA",
            "rate": "54000.00"
        },
        {
            "item": "Myringotomy & Insertion of T-tube Grommets - Bilateral",
            "rate": "96000.00"
        },
        {
            "item": "Myringotomy & Insertion of T-tube Grommets - Unilateral",
            "rate": "72000.00"
        },
        {
            "item": "Myringotomy, Grommet insertion, EUA PNS biopsy",
            "rate": "96000.00"
        },
        {
            "item": "Nasal Biopsy",
            "rate": "33000.00"
        },
        {
            "item": "Nasal Cautery + SMD",
            "rate": "54000.00"
        },
        {
            "item": "Nasal Packing - Anterior",
            "rate": "12000.00"
        },
        {
            "item": "Nasal Polypectomy",
            "rate": "60000.00"
        },
        {
            "item": "Nasal Reconstruction - 1st Stage",
            "rate": "135000.00"
        },
        {
            "item": "Nasal Reconstruction - 2nd Stage",
            "rate": "108000.00"
        },
        {
            "item": "Nasal Toilet",
            "rate": "6000.00"
        },
        {
            "item": "Nasal vestibular Abcess drainage",
            "rate": "30000.00"
        },
        {
            "item": "Nasoendoscopy - Rigid",
            "rate": "18000.00"
        },
        {
            "item": "Nasopharyngoscopy",
            "rate": "24000.00"
        },
        {
            "item": "OAE",
            "rate": "6000.00"
        },
        {
            "item": "OCCUPATIONAL HEARING ASSESSMENT",
            "rate": "18000.00"
        },
        {
            "item": "Oesophagoscopy",
            "rate": "54000.00"
        },
        {
            "item": "Oesophagoscopy & FB Removal",
            "rate": "72000.00"
        },
        {
            "item": "Palatoplasty",
            "rate": "108000.00"
        },
        {
            "item": "Panaendoscopy",
            "rate": "90000.00"
        },
        {
            "item": "Panendoscopy & Excisional biopsy of Cervical Mass",
            "rate": "129000.00"
        },
        {
            "item": "Parotidectomy – Superficial",
            "rate": "168000.00"
        },
        {
            "item": "Parotidectomy – Total",
            "rate": "228000.00"
        },
        {
            "item": "Parotidectomy & Submandibular Gland Excision",
            "rate": "216000.00"
        },
        {
            "item": "PEADIATRIC HEARING ASSESSMENT",
            "rate": "6000.00"
        },
        {
            "item": "Peritonsillar Abscess Drainage",
            "rate": "60000.00"
        },
        {
            "item": "Pharyngoplasty",
            "rate": "132000.00"
        },
        {
            "item": "Polypectomy -Antrochoanal",
            "rate": "78000.00"
        },
        {
            "item": "Preauricular Sinus Excision – GA",
            "rate": "51000.00"
        },
        {
            "item": "Preauricular Sinus Excision – LA",
            "rate": "45000.00"
        },
        {
            "item": "Punch Biopsy",
            "rate": "18000.00"
        },
        {
            "item": "Realese of Tongue Tie",
            "rate": "30000.00"
        },
        {
            "item": "Reduction of Nasal Fracture – GA",
            "rate": "54000.00"
        },
        {
            "item": "Reduction of Nasal Fracture – LA",
            "rate": "42000.00"
        },
        {
            "item": "Release of Nasal Synaechae",
            "rate": "60000.00"
        },
        {
            "item": "Release of Nasal Synaechae & Turbinoplasty",
            "rate": "84000.00"
        },
        {
            "item": "Removal Aural Warts – GA",
            "rate": "24000.00"
        },
        {
            "item": "Removal Aural Warts – LA",
            "rate": "18000.00"
        },
        {
            "item": "Removal Of Grommets",
            "rate": "24000.00"
        },
        {
            "item": "Removal Of Impacted Wax /GA",
            "rate": "18000.00"
        },
        {
            "item": "Removal of maxillary pack",
            "rate": "24000.00"
        },
        {
            "item": "Removal Of Sutures",
            "rate": "1200.00"
        },
        {
            "item": "Rigid Nasoendoscopy/Hypopharyngoscopy/ Laryngoscopy",
            "rate": "60000.00"
        },
        {
            "item": "Septoplasty",
            "rate": "96000.00"
        },
        {
            "item": "Septoplasty & R/O of Nasal Synaechiae",
            "rate": "111000.00"
        },
        {
            "item": "Septoplasty + Turbinoplasty",
            "rate": "126000.00"
        },
        {
            "item": "Septoplasty, Palatoplasty & Turbinoplasty",
            "rate": "198600.00"
        },
        {
            "item": "Septoplasty, Turbinoplasty & Nasal Cautery",
            "rate": "144000.00"
        },
        {
            "item": "Septoplasty, Turbinoplasty & R/O Oronasal Fistula",
            "rate": "168000.00"
        },
        {
            "item": "Septoplasty,Turbinoplasty & Conchoplasty",
            "rate": "168000.00"
        },
        {
            "item": "Sleep Nasoendoscopy",
            "rate": "36000.00"
        },
        {
            "item": "Sleep Nasopharyngoscopy",
            "rate": "48000.00"
        },
        {
            "item": "Sleep Study - Ambulatory",
            "rate": "33000.00"
        },
        {
            "item": "Submandibular Gland Excision (Sialadenectomy) – Bilateral",
            "rate": "132000.00"
        },
        {
            "item": "Submandibular Gland Excision (Sialadenectomy) – Unilateral",
            "rate": "96000.00"
        },
        {
            "item": "Submucous Diathermy of Inferior Turbinates",
            "rate": "42000.00"
        },
        {
            "item": "Surgical toilet and suturing of facial wounds",
            "rate": "54000.00"
        },
        {
            "item": "Syringing",
            "rate": "6000.00"
        },
        {
            "item": "TINNITUS COUNSELLING",
            "rate": "6000.00"
        },
        {
            "item": "Tonsillectomy – Adults",
            "rate": "72000.00"
        },
        {
            "item": "Tonsillectomy – Children",
            "rate": "66000.00"
        },
        {
            "item": "Tonsillectomy + AS + BAWO",
            "rate": "108000.00"
        },
        {
            "item": "Tonsillectomy + AS + SMD",
            "rate": "114000.00"
        },
        {
            "item": "Tonsillectomy + Excision of Preauricular Sinus",
            "rate": "96000.00"
        },
        {
            "item": "Tonsillectomy + Insertion of Grommets - (Paediatric)",
            "rate": "84000.00"
        },
        {
            "item": "Tonsillectomy + Myringotomy + Insertion of Grommets",
            "rate": "96000.00"
        },
        {
            "item": "Tonsillectomy + Oesophagoscopy",
            "rate": "96000.00"
        },
        {
            "item": "Tonsillectomy + SMD",
            "rate": "72000.00"
        },
        {
            "item": "Tonsillectomy + SMD + Sleep Nasal Endoscopy",
            "rate": "108000.00"
        },
        {
            "item": "Tonsillectomy + Turbinoplasty + Conchoplasty",
            "rate": "147000.00"
        },
        {
            "item": "Tonsillectomy + Tympanoplasty - Unilateral",
            "rate": "138000.00"
        },
        {
            "item": "Tonsillectomy + Uvuloplasty",
            "rate": "138000.00"
        },
        {
            "item": "Tonsillectomy +AS + BAWO + SMD",
            "rate": "126000.00"
        },
        {
            "item": "Tonsillectomy and EUA",
            "rate": "78000.00"
        },
        {
            "item": "Thyroid Lobectomy ",
            "rate": "96000.00"
        },
        {
            "item": "Total thyroidectomy ",
            "rate": "136000.00"
        },
        {
            "item": "Tracheostomy",
            "rate": "78000.00"
        },
        {
            "item": "Turbinoplasty",
            "rate": "72000.00"
        },
        {
            "item": "Turbinoplasty & AS",
            "rate": "102000.00"
        },
        {
            "item": "Turbinoplasty & Conchoplasty",
            "rate": "114000.00"
        },
        {
            "item": "Turbinoplasty & E/O Septal Spur",
            "rate": "7200.00"
        },
        {
            "item": "Turbinoplasty & Palatoplasty",
            "rate": "153000.00"
        },
        {
            "item": "Turbinoplasty + UPPP",
            "rate": "228000.00"
        },
        {
            "item": "Turbinoplasty, Septoplasty & Release of Synaechiae",
            "rate": "156000.00"
        },
        {
            "item": "Turbinoplasty,Conchoplasty & Palatoplasty",
            "rate": "192000.00"
        },
        {
            "item": "Tympanomastoidectomy",
            "rate": "240000.00"
        },
        {
            "item": "TYMPANOMETRY",
            "rate": "6000.00"
        },
        {
            "item": "Tympanoplasty – Unilateral",
            "rate": "108000.00"
        },
        {
            "item": "Tympanoplasty– Bilateral",
            "rate": "171000.00"
        },
        {
            "item": "Uvulectomy",
            "rate": "42000.00"
        },
        {
            "item": "Uvulopalatopharyngoplasty (UPPP)",
            "rate": "204000.00"
        },
        {
            "item": "Uvulopalatopharyngoplasty (UPPP) + Septoplasty + Turbinoplasty",
            "rate": "264000.00"
        },
        {
            "item": "Uvulopalatopharyngoplasty (UPPP) + Turbinoplasty",
            "rate": "240000.00"
        },
        {
            "item": "Uvuloplasty",
            "rate": "99000.00"
        },
        {
            "item": "VESTIBULAR ASSESSMENT",
            "rate": "21600.00"
        },
        {
            "item": "VESTIBULAR REHABILITATION",
            "rate": "3600.00"
        },
        {
            "item": "Video Otoscopy",
            "rate": "4800.00"
        },
        {
            "item": "Video-Laryngoscopy",
            "rate": "78000.00"
        },
        {
            "item": "Vocal Cord Lateralisation + Arytenoidectomy",
            "rate": "84000.00"
        },
        {
            "item": "Vocal Cord Lateralisation + Arytenoidectomy",
            "rate": "78000.00"
        },
        {
            "item": "Vocal Fold Medialization",
            "rate": "138000.00"
        },
        {
            "item": "Voice Therapy",
            "rate": "6000.00"
        },
        {
            "item": "Voice Clinic / Evaluation",
            "rate": "7800.00"
        }
    ]
    return payload,'Saham Price List'
def get_madison():
    payload =[
        {
            "item": "Consultation",
            "rate": "3000.00"
        },
        {
            "item": "Hospital Visits",
            "rate": "5000.00"
        },
        {
            "item": "Emergency Night Visits",
            "rate": "8500.00"
        },
        {
            "item": "Emergency Day Visits",
            "rate": "6000.00"
        },
        {
            "item": "ICU Visit (Daily Charges)",
            "rate": "6000.00"
        },
        {
            "item": "HDU Visit (Daily Charges)",
            "rate": "5000.00"
        },
        {
            "item": "Adenoidectomy & Septoplasty",
            "rate": "100000.00"
        },
        {
            "item": "Adenoidectomy (Adults)",
            "rate": "50000.00"
        },
        {
            "item": "Adenoidectomy (Paediatric)",
            "rate": "50000.00"
        },
        {
            "item": "Adenoidectomy Myringotomy & Insertion of Grommets",
            "rate": "60000.00"
        },
        {
            "item": "Adenotonsilectomy Myringotomy & Insertion of Grommets",
            "rate": "72000.00"
        },
        {
            "item": "Adenotonsillectomy (Adult)",
            "rate": "65000.00"
        },
        {
            "item": "Adenotonsillectomy (Paediatric)",
            "rate": "60000.00"
        },
        {
            "item": "Adenotonsillectomy + SMD",
            "rate": "75000.00"
        },
        {
            "item": "AS & Removal of Foreign Body - GA",
            "rate": "50000.00"
        },
        {
            "item": "AS/BAWO",
            "rate": "60000.00"
        },
        {
            "item": "AS/BAWO/Release of Tongue Tie",
            "rate": "59750.00"
        },
        {
            "item": "AS/SMD",
            "rate": "55250.00"
        },
        {
            "item": "AS/SMD/BAWO",
            "rate": "63750.00"
        },
        {
            "item": "AS/TS & Turbinoplasty",
            "rate": "80750.00"
        },
        {
            "item": "AS/TS/SMD Myringotomy & Insertion of Grommets",
            "rate": "89250.00"
        },
        {
            "item": "Audiometry – PTA (Pure tone)",
            "rate": "4000.00"
        },
        {
            "item": "Audiometry (Speech Audiometry – SRT/WRC)",
            "rate": "5500.00"
        },
        {
            "item": "Aural Polypectomy",
            "rate": "38250.00"
        },
        {
            "item": "Aural Toilet",
            "rate": "2550.00"
        },
        {
            "item": "Base of Tongue Reduction",
            "rate": "46750.00"
        },
        {
            "item": "BAWO – GA",
            "rate": "46750.00"
        },
        {
            "item": "BAWO – LA",
            "rate": "38250.00"
        },
        {
            "item": "BAWO/SMD",
            "rate": "51000.00"
        },
        {
            "item": "BERA (With Sedation)",
            "rate": "15000.00"
        },
        {
            "item": "BERA (Without Sedation)",
            "rate": "12000.00"
        },
        {
            "item": "Biopsy Parapharyngeal Mass",
            "rate": "42500.00"
        },
        {
            "item": "Brochoscopy,DL & Decanulation",
            "rate": "59500.00"
        },
        {
            "item": "Bronchoscopy – Diagnostic",
            "rate": "42500.00"
        },
        {
            "item": "Bronchoscopy & Dilatation",
            "rate": "63750.00"
        },
        {
            "item": "Bronchoscopy & FB Removal",
            "rate": "70000.00"
        },
        {
            "item": "Cervical Lymphnode Biopsy",
            "rate": "40000.00"
        },
        {
            "item": "Chemical Cautery",
            "rate": "12750.00"
        },
        {
            "item": "Choanoplasty",
            "rate": "136000.00"
        },
        {
            "item": "Cleaning Under Microscope (EUM)",
            "rate": "7000.00"
        },
        {
            "item": "Conchoplasty",
            "rate": "55250.00"
        },
        {
            "item": "D/L, Microlaryngeal E/o Papillomas & Injection of Cidojovir (Excludes cost\nof Cidojovir)",
            "rate": "110500.00"
        },
        {
            "item": "Direct Laryngoscopy",
            "rate": "48000.00"
        },
        {
            "item": "Direct Laryngoscopy & Biopsy",
            "rate": "60000.00"
        },
        {
            "item": "Direct Laryngoscopy & EUA",
            "rate": "60000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal Excision of Vocal Fold cyst",
            "rate": "70000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal E/o Papillomas",
            "rate": "80000.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal Excision of Leukoplakia",
            "rate": "93500.00"
        },
        {
            "item": "Direct Laryngoscopy & Microlaryngeal Excision of Polyps",
            "rate": "85000.00"
        },
        {
            "item": "Direct Laryngoscopy & MicroLaryngeal excision of Recurrent Laryngeal\nPapillomas",
            "rate": "98500.00"
        },
        {
            "item": "Direct Laryngoscopy & MicroLaryngeal Excision of Vocal Mass",
            "rate": "85500.00"
        },
        {
            "item": "Direct Laryngoscopy & MicroLaryngeal excision of Vocal Nodule",
            "rate": "72000.00"
        },
        {
            "item": "Direct Laryngoscopy & Tracheostomy",
            "rate": "80000.00"
        },
        {
            "item": "Douching",
            "rate": "1700.00"
        },
        {
            "item": "Drainage of Septal Abscess or I&D Furuncle GA",
            "rate": "25500.00"
        },
        {
            "item": "Drainage of Septal Abscess or I&D Furuncle LA",
            "rate": "17000.00"
        },
        {
            "item": "Dressing",
            "rate": "1275.00"
        },
        {
            "item": "Ear Bandits",
            "rate": "2550.00"
        },
        {
            "item": "Ear Plugs",
            "rate": "1000.00"
        },
        {
            "item": "Electro Cautery Littles Area (Epistaxis) – GA",
            "rate": "25500.00"
        },
        {
            "item": "Electro Cautery Littles Area (Epistaxis) – LA",
            "rate": "17000.00"
        },
        {
            "item": "Endoscopic DCR",
            "rate": "120000.00"
        },
        {
            "item": "Endoscopic Decompression of Optic Nerve",
            "rate": "102000.00"
        },
        {
            "item": "Endoscopic E/O Nasal Mass",
            "rate": "140000.00"
        },
        {
            "item": "Endoscopic Excision of PNS mass",
            "rate": "115000.00"
        },
        {
            "item": "Endoscopic Repair CSF Rhinorhea",
            "rate": "200000.00"
        },
        {
            "item": "Endoscopic Trans-sphenoidal E/o pituitary tumor.",
            "rate": "250000.00"
        },
        {
            "item": "Endoscopic Vocal Cord Laretalisation",
            "rate": "110000.00"
        },
        {
            "item": "Endoscopy – Flexible",
            "rate": "18000.00"
        },
        {
            "item": "Endoscopy – Rigid",
            "rate": "18000.00"
        },
        {
            "item": "Endoscopy (Nasal) + Biopsy (Flexible/Rigid)",
            "rate": "25000.00"
        },
        {
            "item": "EUA & Adenoidectomy",
            "rate": "50000.00"
        },
        {
            "item": "EUA & Aural Toilet",
            "rate": "25500.00"
        },
        {
            "item": "EUA & Biopsy – PNS (Rigid Nasoendoscopy under GA)",
            "rate": "40000.00"
        },
        {
            "item": "EUA & Control of Haemorrhage",
            "rate": "48000.00"
        },
        {
            "item": "EUA & Galvanocautery",
            "rate": "29750.00"
        },
        {
            "item": "EUA & R/O Foreign Body",
            "rate": "30000.00"
        },
        {
            "item": "EUA & R/O Nasal stents",
            "rate": "30000.00"
        },
        {
            "item": "EUA PNS & BAWO",
            "rate": "42500.00"
        },
        {
            "item": "EUA, Aural Toilet & Myringotomy + Insertion of Grommets",
            "rate": "50000.00"
        },
        {
            "item": "EUA, Nasal Cautery & Septoplasty",
            "rate": "80000.00"
        },
        {
            "item": "EUA/PNS BIOPSY/MYRINGOTOMY",
            "rate": "55000.00"
        },
        {
            "item": "Evacuation Of Haematoma",
            "rate": "35000.00"
        },
        {
            "item": "Excision Cystic Hygroma",
            "rate": "100000.00"
        },
        {
            "item": "Excision of Aural Exostosis",
            "rate": "85000.00"
        },
        {
            "item": "Excision of Auricular Cyst",
            "rate": "45000.00"
        },
        {
            "item": "Excision of Maxillary Mass",
            "rate": "120000.00"
        },
        {
            "item": "Excision of Nasal Synachea",
            "rate": "55000.00"
        },
        {
            "item": "Excision of Palatal Cyst",
            "rate": "63750.00"
        },
        {
            "item": "Excision of Parotid Cyst",
            "rate": "75000.00"
        },
        {
            "item": "Excision of Tongue Granuloma",
            "rate": "42500.00"
        },
        {
            "item": "Excision Ranula Cyst",
            "rate": "72000.00"
        },
        {
            "item": "Excision Thyroglossal Duct Cyst",
            "rate": "72000.00"
        },
        {
            "item": "Excision/ Galvanocautery Warts",
            "rate": "26000.00"
        },
        {
            "item": "FB Removal (Ear) – GA",
            "rate": "25000.00"
        },
        {
            "item": "FB Removal (Ear) – LA",
            "rate": "10000.00"
        },
        {
            "item": "FB Removal (Nose) – GA",
            "rate": "25000.00"
        },
        {
            "item": "FB Removal (Nose) – LA",
            "rate": "15000.00"
        },
        {
            "item": "FESS",
            "rate": "100000.00"
        },
        {
            "item": "FESS - Revision",
            "rate": "120000.00"
        },
        {
            "item": "FESS & Adenoidectomy",
            "rate": "112000.00"
        },
        {
            "item": "FESS & E/O Antrochoanal Polyps",
            "rate": "130000.00"
        },
        {
            "item": "FESS & Excision of Ethmoid Mass",
            "rate": "140000.00"
        },
        {
            "item": "Fess / BAWO / Septoplasty / Tympanoplasty",
            "rate": "120000.00"
        },
        {
            "item": "Fess & Polypectomy",
            "rate": "130000.00"
        },
        {
            "item": "FESS & Polypectomy - Revision",
            "rate": "140000.00"
        },
        {
            "item": "FESS & Repair of Oro-Antral Fistula",
            "rate": "122000.00"
        },
        {
            "item": "Fess + Chonchoplasty",
            "rate": "120000.00"
        },
        {
            "item": "Fess + Chonchoplasty + Turbinoplasty",
            "rate": "150000.00"
        },
        {
            "item": "FESS + Septoplasty",
            "rate": "130000.00"
        },
        {
            "item": "FESS + Tonsilectomy",
            "rate": "130000.00"
        },
        {
            "item": "FESS + Turbinoplasty",
            "rate": "130000.00"
        },
        {
            "item": "Fess + Turbinoplasty + Tonsilectomy",
            "rate": "150000.00"
        },
        {
            "item": "FESS and removal  of Aural  Keratosis",
            "rate": "98500.00"
        },
        {
            "item": "FESS, AS & TS",
            "rate": "135000.00"
        },
        {
            "item": "FESS, AS, TS, SMD",
            "rate": "150000.00"
        },
        {
            "item": "FESS, Polypectomy & Septoplasty",
            "rate": "160000.00"
        },
        {
            "item": "FESS, Polypectomy & Turbinoplasty",
            "rate": "165000.00"
        },
        {
            "item": "FESS, Septoplasty & Adenoidectomy - Revision",
            "rate": "170000.00"
        },
        {
            "item": "FESS, Turbinoplasty & AS",
            "rate": "150000.00"
        },
        {
            "item": "FESS, Turbinoplasty & Release of Nasal Synaechae",
            "rate": "140000.00"
        },
        {
            "item": "FESS, Turbinoplasty & SNE",
            "rate": "150000.00"
        },
        {
            "item": "FESS, Turbinoplasty, Septoplasty & Conchoplasty",
            "rate": "158000.00"
        },
        {
            "item": "Fess,Turbinoplasty & Septoplasty",
            "rate": "150000.00"
        },
        {
            "item": "FLEXIBLE ENDOSCOPIC EVALUATION OF SWALLOWING",
            "rate": "32000.00"
        },
        {
            "item": "Flexible Nasal Pharyngoscopy",
            "rate": "18500.00"
        },
        {
            "item": "Flexible Nasopharyngoscopy & Biopsy",
            "rate": "30000.00"
        },
        {
            "item": "Flexible Videolaryngoscopy & Voice assessment",
            "rate": "28500.00"
        },
        {
            "item": "Frenulectomy",
            "rate": "22500.00"
        },
        {
            "item": "Galvanocaurtery of nose",
            "rate": "22500.00"
        },
        {
            "item": "Glossectomy - Partial",
            "rate": "124000.00"
        },
        {
            "item": "HEARING AID FITTING",
            "rate": "5000.00"
        },
        {
            "item": "I & D Abscess (Neck) – GA",
            "rate": "21250.00"
        },
        {
            "item": "I & D Abscess (Neck) – LA",
            "rate": "12750.00"
        },
        {
            "item": "I & D and Biopsy",
            "rate": "50000.00"
        },
        {
            "item": "I & D Preauricular Abscess",
            "rate": "30000.00"
        },
        {
            "item": "I&D of Submandibular Abscess",
            "rate": "30000.00"
        },
        {
            "item": "I&D Peritonsilar Abscess",
            "rate": "45000.00"
        },
        {
            "item": "Incision and Drainage of Head and Neck abscess I&D)",
            "rate": "30000.00"
        },
        {
            "item": "INDUSTRIAL HEARING CONSERVATION"
        },
        {
            "item": "Injection of Cidofovir",
            "rate": "75000.00"
        },
        {
            "item": "Insertion of Earwick",
            "rate": "10000.00"
        },
        {
            "item": "Keloid Excision{ear}",
            "rate": "40000.00"
        },
        {
            "item": "LARYNGEAL VIDEO STROBOSCOPY",
            "rate": "25000.00"
        },
        {
            "item": "Laryngectomy - Partial",
            "rate": "160000.00"
        },
        {
            "item": "Laryngectomy - Total",
            "rate": "200000.00"
        },
        {
            "item": "Laryngoscopy - Flexible",
            "rate": "18000.00"
        },
        {
            "item": "Laryngoscopy - Rigid",
            "rate": "18000.00"
        },
        {
            "item": "Laryngotracheal Reconstruction",
            "rate": "180000.00"
        },
        {
            "item": "Larynx Videostroboscopy",
            "rate": "25000.00"
        },
        {
            "item": "Larynx Videostroboscopy – Repeat",
            "rate": "15000.00"
        },
        {
            "item": "Lymphnode Biopsy – GA",
            "rate": "22000.00"
        },
        {
            "item": "Lymphnode Biopsy– LA",
            "rate": "18000.00"
        },
        {
            "item": "Mastoidectomy - Cortical",
            "rate": "120000.00"
        },
        {
            "item": "Mastoidectomy - Radical",
            "rate": "140000.00"
        },
        {
            "item": "Mastoidectomy - Revision",
            "rate": "175000.00"
        },
        {
            "item": "Maxillectomy – Partial",
            "rate": "90000.00"
        },
        {
            "item": "Maxillectomy – Total",
            "rate": "100000.00"
        },
        {
            "item": "Microlaryngeal Surgery",
            "rate": "90000.00"
        },
        {
            "item": "Modified Neck Dissection - Bilateral",
            "rate": "360000.00"
        },
        {
            "item": "Modified Neck Dissection - Unilateral",
            "rate": "180000.00"
        },
        {
            "item": "Myringotomy & Insertion of Grommets – GA",
            "rate": "50000.00"
        },
        {
            "item": "Myringotomy & Insertion of Grommets – LA",
            "rate": "40000.00"
        },
        {
            "item": "Myringotomy & Insertion of T-tube Grommets - Bilateral",
            "rate": "72000.00"
        },
        {
            "item": "Myringotomy & Insertion of T-tube Grommets - Unilateral",
            "rate": "54000.00"
        },
        {
            "item": "Myringotomy, Grommet insertion, EUA PNS biopsy",
            "rate": "72000.00"
        },
        {
            "item": "Nasal Biopsy",
            "rate": "25000.00"
        },
        {
            "item": "Nasal Cautery + SMD",
            "rate": "40000.00"
        },
        {
            "item": "Nasal Packing - Anterior",
            "rate": "10000.00"
        },
        {
            "item": "Nasal Polypectomy",
            "rate": "45000.00"
        },
        {
            "item": "Nasal Reconstruction - 1st Stage",
            "rate": "100000.00"
        },
        {
            "item": "Nasal Reconstruction - 2nd Stage",
            "rate": "85000.00"
        },
        {
            "item": "Nasal Toilet",
            "rate": "5000.00"
        },
        {
            "item": "Nasal vestibular Abcess drainage",
            "rate": "24000.00"
        },
        {
            "item": "Nasoendoscopy - Rigid",
            "rate": "15000.00"
        },
        {
            "item": "Nasopharyngoscopy",
            "rate": "20000.00"
        },
        {
            "item": "OAE",
            "rate": "5000.00"
        },
        {
            "item": "OCCUPATIONAL HEARING ASSESSMENT",
            "rate": "15000.00"
        },
        {
            "item": "Oesophagoscopy",
            "rate": "41000.00"
        },
        {
            "item": "Oesophagoscopy & FB Removal",
            "rate": "55000.00"
        },
        {
            "item": "Palatoplasty",
            "rate": "82500.00"
        },
        {
            "item": "Panaendoscopy",
            "rate": "70000.00"
        },
        {
            "item": "Panendoscopy & Excisional biopsy of Cervical Mass",
            "rate": "100000.00"
        },
        {
            "item": "Parotidectomy – Superficial",
            "rate": "130000.00"
        },
        {
            "item": "Parotidectomy – Total",
            "rate": "170000.00"
        },
        {
            "item": "Parotidectomy & Submandibular Gland Excision",
            "rate": "160000.00"
        },
        {
            "item": "PEADIATRIC HEARING ASSESSMENT",
            "rate": "5000.00"
        },
        {
            "item": "Peritonsillar Abscess Drainage",
            "rate": "45000.00"
        },
        {
            "item": "Pharyngoplasty",
            "rate": "98500.00"
        },
        {
            "item": "Polypectomy -Antrochoanal",
            "rate": "60000.00"
        },
        {
            "item": "Preauricular Sinus Excision – GA",
            "rate": "40000.00"
        },
        {
            "item": "Preauricular Sinus Excision – LA",
            "rate": "35000.00"
        },
        {
            "item": "Punch Biopsy",
            "rate": "14500.00"
        },
        {
            "item": "Realese of Tongue Tie",
            "rate": "22500.00"
        },
        {
            "item": "Reduction of Nasal Fracture – GA",
            "rate": "41000.00"
        },
        {
            "item": "Reduction of Nasal Fracture – LA",
            "rate": "32000.00"
        },
        {
            "item": "Release of Nasal Synaechae",
            "rate": "50000.00"
        },
        {
            "item": "Release of Nasal Synaechae & Turbinoplasty",
            "rate": "63500.00"
        },
        {
            "item": "Removal Aural Warts – GA",
            "rate": "20000.00"
        },
        {
            "item": "Removal Aural Warts – LA",
            "rate": "14500.00"
        },
        {
            "item": "Removal Of Grommets",
            "rate": "18500.00"
        },
        {
            "item": "Removal Of Impacted Wax /GA",
            "rate": "14000.00"
        },
        {
            "item": "Removal of maxillary pack",
            "rate": "18000.00"
        },
        {
            "item": "Removal Of Sutures",
            "rate": "1000.00"
        },
        {
            "item": "Rigid Nasoendoscopy/Hypopharyngoscopy/ Laryngoscopy",
            "rate": "45000.00"
        },
        {
            "item": "Septoplasty",
            "rate": "72000.00"
        },
        {
            "item": "Septoplasty & R/O of Nasal Synaechiae",
            "rate": "84000.00"
        },
        {
            "item": "Septoplasty + Turbinoplasty",
            "rate": "93500.00"
        },
        {
            "item": "Septoplasty, Palatoplasty & Turbinoplasty",
            "rate": "155000.00"
        },
        {
            "item": "Septoplasty, Turbinoplasty & Nasal Cautery",
            "rate": "112000.00"
        },
        {
            "item": "Septoplasty, Turbinoplasty & R/O Oronasal Fistula",
            "rate": "130000.00"
        },
        {
            "item": "Septoplasty,Turbinoplasty & Conchoplasty",
            "rate": "130000.00"
        },
        {
            "item": "Sleep Nasoendoscopy",
            "rate": "30000.00"
        },
        {
            "item": "Sleep Nasopharyngoscopy",
            "rate": "38500.00"
        },
        {
            "item": "Sleep Study - Ambulatory",
            "rate": "25000.00"
        },
        {
            "item": "Submandibular Gland Excision (Sialadenectomy) – Bilateral",
            "rate": "110000.00"
        },
        {
            "item": "Submandibular Gland Excision (Sialadenectomy) – Unilateral",
            "rate": "75000.00"
        },
        {
            "item": "Submucous Diathermy of Inferior Turbinates",
            "rate": "32000.00"
        },
        {
            "item": "Surgical toilet and suturing of facial wounds",
            "rate": "40000.00"
        },
        {
            "item": "Syringing",
            "rate": "5000.00"
        },
        {
            "item": "TINNITUS COUNSELLING",
            "rate": "5000.00"
        },
        {
            "item": "Tonsillectomy – Adults",
            "rate": "60000.00"
        },
        {
            "item": "Tonsillectomy – Children",
            "rate": "50000.00"
        },
        {
            "item": "Tonsillectomy + AS + BAWO",
            "rate": "82500.00"
        },
        {
            "item": "Tonsillectomy + AS + SMD",
            "rate": "87500.00"
        },
        {
            "item": "Tonsillectomy + Excision of Preauricular Sinus",
            "rate": "72000.00"
        },
        {
            "item": "Tonsillectomy + Insertion of Grommets - (Paediatric)",
            "rate": "65000.00"
        },
        {
            "item": "Tonsillectomy + Myringotomy + Insertion of Grommets",
            "rate": "72000.00"
        },
        {
            "item": "Tonsillectomy + Oesophagoscopy",
            "rate": "72000.00"
        },
        {
            "item": "Tonsillectomy + SMD",
            "rate": "55000.00"
        },
        {
            "item": "Tonsillectomy + SMD + Sleep Nasal Endoscopy",
            "rate": "87500.00"
        },
        {
            "item": "Tonsillectomy + Turbinoplasty + Conchoplasty",
            "rate": "115000.00"
        },
        {
            "item": "Tonsillectomy + Tympanoplasty - Unilateral",
            "rate": "102000.00"
        },
        {
            "item": "Tonsillectomy + Uvuloplasty",
            "rate": "102000.00"
        },
        {
            "item": "Tonsillectomy +AS",
            "rate": "55000.00"
        },
        {
            "item": "Tonsillectomy +AS + BAWO + SMD",
            "rate": "95000.00"
        },
        {
            "item": "Tonsillectomy +AS + Insertion of Grommets",
            "rate": "65000.00"
        },
        {
            "item": "Tonsillectomy and EUA",
            "rate": "60000.00"
        },
        {
            "item": "Tracheostomy",
            "rate": "62000.00"
        },
        {
            "item": "Turbinoplasty",
            "rate": "60000.00"
        },
        {
            "item": "Turbinoplasty & AS",
            "rate": "85000.00"
        },
        {
            "item": "Turbinoplasty & Conchoplasty",
            "rate": "95000.00"
        },
        {
            "item": "Turbinoplasty & E/O Septal Spur",
            "rate": "6000.00"
        },
        {
            "item": "Turbinoplasty & Palatoplasty",
            "rate": "127500.00"
        },
        {
            "item": "Turbinoplasty + UPPP",
            "rate": "190000.00"
        },
        {
            "item": "Turbinoplasty, Septoplasty & Release of Synaechiae",
            "rate": "130000.00"
        },
        {
            "item": "Turbinoplasty,Conchoplasty & Palatoplasty",
            "rate": "160000.00"
        },
        {
            "item": "Tympanomastoidectomy",
            "rate": "200000.00"
        },
        {
            "item": "TYMPANOMETRY",
            "rate": "5000.00"
        },
        {
            "item": "Tympanoplasty – Unilateral",
            "rate": "90000.00"
        },
        {
            "item": "Tympanoplasty– Bilateral",
            "rate": "142500.00"
        },
        {
            "item": "Uvulectomy",
            "rate": "35000.00"
        },
        {
            "item": "Uvulopalatopharyngoplasty (UPPP)",
            "rate": "170000.00"
        },
        {
            "item": "Uvulopalatopharyngoplasty (UPPP) + Septoplasty + Turbinoplasty",
            "rate": "220000.00"
        },
        {
            "item": "Uvulopalatopharyngoplasty (UPPP) + Turbinoplasty",
            "rate": "200000.00"
        },
        {
            "item": "Uvuloplasty",
            "rate": "82500.00"
        },
        {
            "item": "VESTIBULAR ASSESSMENT",
            "rate": "18000.00"
        },
        {
            "item": "VESTIBULAR REHABILITATION",
            "rate": "3000.00"
        },
        {
            "item": "Video Otoscopy",
            "rate": "4000.00"
        },
        {
            "item": "Video-Laryngoscopy",
            "rate": "65000.00"
        },
        {
            "item": "Vocal Cord Lateralisation + Arytenoidectomy",
            "rate": "70000.00"
        },
        {
            "item": "Vocal Cord Lateralisation + Arytenoidectomy",
            "rate": "65000.00"
        },
        {
            "item": "Vocal Fold Medialization",
            "rate": "115000.00"
        },
        {
            "item": "Voice Therapy",
            "rate": "5000.00"
        },
        {
            "item": "Voice Clinic / Evaluation",
            "rate": "6500.00"
        }
    ]
    return payload,'Madison Price List'