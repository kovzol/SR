# Issue "make" to create a Sword module, and "make SRGNT.zip" to create it as a .zip bundle.

ZTEXT_DIR=modules/texts/ztext/srgnt
NT_BZZ=$(ZTEXT_DIR)/nt.bzz
NT_BZV=$(ZTEXT_DIR)/nt.bzv
NT_BZS=$(ZTEXT_DIR)/nt.bzs
NT=$(NT_BZZ) $(NT_BZV) $(NT_BZS)

all: $(NT)

SR_osis.xml: SR.txt txt2osis.py
	python3 txt2osis.py > $@
$(NT): SR_osis.xml
	mkdir -p $(ZTEXT_DIR)
	osis2mod $(ZTEXT_DIR) $< -z z -v LXX
	@echo "Copy $(ZTEXT_DIR) and mods.d/srgnt.conf to your <SWORD_DIR> to finalize your installation."

SRGNT.zip: $(NT) mods.d/srgnt.conf
	zip -9r $@ $^
