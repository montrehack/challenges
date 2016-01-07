
level1.bin: ./level1/rtl/level1.v common.pcf
	yosys -q -p "synth_ice40 -blif ./build/level1.blif" ./level1/rtl/level1.v
	yosys -q -p "synth_ice40 -edif ./build/level1_golden.edif" ./level1/rtl/level1.v
	arachne-pnr -p common.pcf ./build/level1.blif -o ./build/level1.txt
	icebox_edif ./build/level1.txt > ./build/level1.edif
	icepack ./build/level1.txt ./build/level1.bin

level0.bin: ./level0/rtl/level0.v common.pcf
	yosys -q -p "synth_ice40 -blif ./build/level0.blif" ./level0/rtl/level0.v
	yosys -q -p "synth_ice40 -edif ./build/level0_golden.edif" ./level0/rtl/level0.v
	arachne-pnr -p common.pcf ./build/level0.blif -o ./build/level0.txt
	icebox_edif ./build/level0.txt > ./build/level0.edif
	icepack ./build/level0.txt ./build/level0.bin

clean:
	rm -f ./build/level0.blif ./build/level0.txt ./build/level0.txt ./build/level0.bin ./build/level0.edif
