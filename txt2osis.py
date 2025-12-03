# Create an OSIS XML file based on the .txt version of SR
import pandas as pd
import math
import re

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

 <osisText osisIDWork="StatResGNT" osisRefWork="Bible" xml:lang="grc" canonical="true">
  <header>
   <work osisWork="StatResGNT">
    <title>Statistical Restoration Greek New Testament</title>
    <identifier type="OSIS">Bible.StatResGNT</identifier>
    <refSystem>Bible.Calvin</refSystem>
   </work>
   <work osisWork="strong">
    <refSystem>Dict.Strongs</refSystem>
   </work>
   <work osisWork="packard">
    <refSystem>Dict.Packar</refSystem>
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
qm = 0 # quotation marks
ap = 0 # apostrophes

for word in sr_txt.itertuples():
    word_code = str(word[1])
    word_rawstring = str(word[2])
    # word_rawstring = str(word[3])

    morph = str(word[7])
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
        # print(f"    <comment qm=\"{qm}\" ap=\"{ap}\"/>") # for debugging
        verse_rawstring = "" # start with a new verse
    if book_chapter != book_chapter_old:
        if verses > 0: # a new chapter has been started
            print("   </chapter>")
    if book != book_old:
        if verses > 0: # a new book has been started
            print("  </div>")
        if qm != 0:
            raise ValueError("quotation mark is not closed in book")
        if ap != 0:
            raise ValueError("apostrophe is not closed in book")
    if book != book_old:
        # output the current book name
        print(f"  <div osisID=\"{book_formatted}\" type=\"book\">")
    if book_chapter != book_chapter_old:
        # output the current chapter name
        print(f"   <chapter osisID=\"{book_chapter_formatted}\">")
    book_chapter_verse_formatted = book_chapter_formatted + "." + str(int(verse))
    if verse_rawstring != "":
        verse_rawstring += " "

    # maintain double and single quote checkers...
    qm += word_rawstring.count("“")
    qm -= word_rawstring.count("”")
    ap += word_rawstring.count("‘")
    ap -= word_rawstring.count("’")
    if qm - ap < 0:
        raise ValueError("too many apostrophes compared to quotation marks")
    if qm - ap > 1:
        raise ValueError("too many quotation marks compared to apostrophes")
    if qm < 0:
        raise ValueError("too many closing quotation marks")
    if ap < 0:
        raise ValueError("too many closing apostrophes")

    if word_rawstring.startswith("¶"):
        word_rawstring = word_rawstring[1:]
        verse_rawstring += "<milestone type=\"x-p\" marker=\"¶\"/>"
    if "˚" in word_rawstring:
        pos = word_rawstring.index("˚")
        startstring = ""
        if pos > 0:
            startstring = word_rawstring[0:pos]
        word_rawstring = word_rawstring[pos+1:]

        # closing punctuation should not belong to the divine name...
        endstring = ""
        ends = ["\\!", "\\.", ",", "”", "’", ";", "·", "\\)"]
        ends = re.compile("|".join(ends))
        searchres = ends.search(word_rawstring)
        if searchres != None:
            ind = searchres.span()[0]
            endstring = word_rawstring[ind:]
            word_rawstring = word_rawstring[:ind]

        word_rawstring = startstring + "<divineName>" + word_rawstring  + "</divineName>" + endstring

    w_tag = "" # a w-tag (by default, there is no w-tag)
    if strong != "":
        w_tag += f" lemma=\"strong:G{strong}\""
    if morph != "":
        w_tag += f" morph=\"packard:{morph}\""
    if w_tag == "":
        verse_rawstring += word_rawstring
    else:
        verse_rawstring += f"<w{w_tag}>{word_rawstring}</w>"
    book_chapter_verse_old = book_chapter_verse
    book_chapter_old = book_chapter
    book_old = book

# finish Revelations
print(f"    <verse osisID=\"{book_chapter_verse_formatted}\">{verse_rawstring}</verse>")
print("   </chapter>")
print("  </div>") # book

print(osis_tail())
