SOURCES=tb_level1.v $(wildcard ../rtl/*.v)

all: sim

sim:
	cver $(SOURCES)

view:
	gtkwave level1.vcd

clean:
	rm -f verilog.log level1.vcd

.PHONY: clean sim view
