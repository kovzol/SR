# Issue "make" to create a Sword module, and "make StatResGNT.zip" to create it as a .zip bundle.

ZTEXT_DIR=modules/texts/ztext/statresgnt
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
	@echo "Copy $(ZTEXT_DIR) and mods.d/statresgnt.conf to your <SWORD_DIR> to finalize your installation."

StatResGNT.zip: $(NT) mods.d/statresgnt.conf
	zip -9r $@ $^

clean:
	rm -f $(NT) SR_osis.xml
