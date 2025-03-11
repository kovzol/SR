# Create an OSIS XML file based on the .txt version of SR
import pandas as pd
import math

numbertrans = {
    40: 'Matt',
    41: 'Mark',
    42: 'Luke',
    43: 'John',
    44: 'Acts',
    45: 'Rom',
    46: '1Cor',
    47: '2Cor',
    48: 'Gal',
    49: 'Eph',
    50: 'Phil',
    51: 'Col',
    52: '1Thess',
    53: '2Thess',
    54: '1Tim',
    55: '2Tim',
    56: 'Titus',
    57: 'Phlm',
    58: 'Heb',
    59: 'Jas',
    60: '1Pet',
    61: '2Pet',
    62: '1John',
    63: '2John',
    64: '3John',
    65: 'Jude',
    66: 'Rev'
}

def osis_head():
    return """<?xml version="1.0" encoding="UTF-8"?>
<osis
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace"
 xmlns:osis="http://www.bibletechnologies.net/2003/OSIS/namespace"
 xsi:schemaLocation="http://www.bibletechnologies.net/2003/OSIS/namespace https://www.crosswire.org/osis/osisCore.2.1.1.xsd">

 <osisText osisIDWork="SRGNT" osisRefWork="Bible" xml:lang="grc" canonical="true">
  <header>
   <work osisWork="SRGNT">
    <title>Bunning Heuristic Prototype Greek New Testament</title>
    <identifier type="OSIS">Bible.SRGNT</identifier>
    <refSystem>Bible.Calvin</refSystem>
   </work>
   <work osisWork="strong">
    <refSystem>Dict.Strongs</refSystem>
   </work>
  </header>
"""

def osis_tail():
    return """
 </osisText>

</osis>"""

print(osis_head())

sr_txt = pd.read_csv('SR.tsv', sep='\t', skiprows=0)
book_old = ""
book_chapter_old = ""
book_chapter_verse_old = ""
verse_rawstring = ""
verses = 0
for word in sr_txt.itertuples():
    word_code = str(word[1])
    word_rawstring = str(word[2])
    # word_rawstring = str(word[3])
    strong = word[5]
    if (type(strong) == int or type(strong) == float) and not math.isnan(strong):
        strong = int(strong)
        if strong % 10 != 0:
            strong = ""
        else:
            strong /= 10 # just remove the ending 0
            strong = int(strong)
    else:
        strong = ""
    book = word_code[0:2]
    chapter = word_code[2:5]
    verse = word_code[5:8]
    book_chapter = book + chapter
    book_chapter_verse = book_chapter + verse
    book_formatted = numbertrans[int(book)]
    book_chapter_formatted = book_formatted + "." + str(int(chapter))
    if book_chapter_verse != book_chapter_verse_old and verse_rawstring != "": # a new verse has been started
        verses += 1
        # output the old verse
        print(f"    <verse osisID=\"{book_chapter_verse_formatted}\">{verse_rawstring}</verse>")
        verse_rawstring = "" # start with a new verse
    if book_chapter != book_chapter_old:
        if verses > 0: # a new chapter has been started
            print("   </chapter>")
    if book != book_old:
        if verses > 0: # a new book has been started
            print("  </div>")
    if book != book_old:
        # output the current book name
        print(f"  <div osisID=\"{book_formatted}\" type=\"book\">")
    if book_chapter != book_chapter_old:
        # output the current chapter name
        print(f"   <chapter osisID=\"{book_chapter_formatted}\">")
    book_chapter_verse_formatted = book_chapter_formatted + "." + str(int(verse))
    if verse_rawstring != "":
        verse_rawstring += " "
    if strong == "":
        verse_rawstring += word_rawstring
    else:
        verse_rawstring += f"<w lemma=\"strong:G{strong}\">{word_rawstring}</w>"
    book_chapter_verse_old = book_chapter_verse
    book_chapter_old = book_chapter
    book_old = book

# finish Revelations
print(f"    <verse osisID=\"{book_chapter_verse_formatted}\">{verse_rawstring}</verse>")
print("   </chapter>")
print("  </div>") # book

print(osis_tail())
