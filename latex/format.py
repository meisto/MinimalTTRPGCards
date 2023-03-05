#!/bin/python3
# ======================================================================
# Author: meisto
# Creation Date: Sun 05 Mar 2023 11:24:09 PM CET
# Description: -
# ======================================================================
import os
import subprocess

header = r"""
\documentclass{report} % Bsp: article, scrbook, book, report, letter, scrartcl, scrreprt
\usepackage{graphicx}
\usepackage[margin=15mm]{geometry}

\begin{document}
"""

footer = r'\end{document}'
def main():
    spell_list_file = "spelllist.txt"


    root_path = os.path.realpath(__file__)
    root_path = os.path.dirname(root_path)
    project_root_path = os.path.join(root_path, os.path.pardir)

    # Load required spells from spell list file
    required_spells = []
    with open(os.path.join(project_root_path, spell_list_file), mode='r') as f:
        required_spells = f.readlines()

    # Clean up
    for i, _ in enumerate(required_spells):
        required_spells[i] = required_spells[i].strip()

    #


    path = os.path.join(root_path, "spellcards_collection.tex")
    # print("Writing latex to file '" + path + "'.")

    with open(path, mode='w') as f:
        # Write prefix
        f.write(header)

        on_this_page = 0
        max_num = 8
        for i, spell in enumerate(required_spells):
            filename = spell.replace(" ", "_").lower() + ".pdf"
            filepath = os.path.join(project_root_path, "output", 
                "spells", filename)

            # Skip if no matching data can be found
            if not os.path.exists(filepath) or not os.path.isfile(filepath):
                print("[WARNING] Could not find spell '" + spell + "'.")
                continue


            if i == 0 or i == 1:
                f.write(r"\includegraphics[angle=90]{" + filepath + "}\n")
            else:
                f.write(r"\includegraphics{" + filepath + "}\n")


            on_this_page += 1

            # Linebreak once enough items on the page
            if on_this_page >= max_num:
                f.write(r"\newpage")
                f.write("\n\n")
                on_this_page = 0


        # Write postfix
        f.write(footer)
        f.flush()

    if os.path.exists(path) and os.path.isfile(path):
        os.chdir(root_path)
        subprocess.run(["pdflatex", "spellcards_collection.tex"], check=True)
        subprocess.run(
            [
                "rm",
                "spellcards_collection.log",
                "spellcards_collection.aux",
                "spellcards_collection.text",
            ],
            check = True
        )
            



if __name__ == "__main__":
    main()
