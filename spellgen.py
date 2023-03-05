# ======================================================================
# Author: meisto
# Creation Date: Sat 04 Mar 2023 10:47:43 PM CET
# Description: -
# ======================================================================
import scribus
import json
import os
import sys

size = (60, 80)
margins = (0,0,0,0) 


def setTextKeepStyle(field_name, new_value):

    try:
        scribus.getTextLength(field_name)
    except:
        print("[ERROR] Could not find field '" + field_name + "'.")
        sys.exit(2)



    l = scribus.getTextLength(field_name)
    scribus.selectText(0, l, field_name)
    scribus.deleteText(field_name)
    scribus.insertText(new_value, 0, field_name)








def run():
    sourcefiles = ["test.json"]

    # Open template
    scribus.openDoc("templates/spell.sla")

    ## Relevant Fields:
    # SpellName
    # SpellType
    # CastingTime
    # Range
    # Components
    # Duration
    # Description
    field_names = ["SpellName", "SpellType", "CastingTime", "Range",
        "Duration", "Description"]

    for sourcefile in sourcefiles:
        # Load spell description from json file
        desc = {}
        with open(sourcefile, mode='r') as f:
            
            desc = json.load(f)

            for i in field_names:
                assert i in desc, "Field '" + i + "' not found in source file."

        # Set all fields to the read values
        for fn in field_names:
            print("\nSetting " + fn)
            setTextKeepStyle(fn, desc[fn])


            
        filename =  desc["SpellName"].replace(" ", "_").lower() + ".pdf"
        filename = os.path.join("output", "spells", filename)

        op = scribus.PDFfile()
        op.file = str(filename)
        op.save()




if __name__ == "__main__":
    run()
