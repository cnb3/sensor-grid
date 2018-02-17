install: config init

config:
	install -b -m0440 $(CURDIR)/etc/alfred.conf /etc/alfred.conf

init:
	install -b $(CURDIR)/init.d/alfred /etc/init.d/alfred
