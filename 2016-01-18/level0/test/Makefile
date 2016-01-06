SOURCES=tb_level0.v $(wildcard ../rtl/*.v)

all: sim

sim:
	cver $(SOURCES)

view:
	gtkwave level0.vcd

clean:
	rm -f verilog.log level0.vcd

.PHONY: clean sim view
