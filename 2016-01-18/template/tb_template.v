module tb_level0();

reg shift;
reg d;

level0 dut(
	.io_13_9_1(),
	.io_0_8_1(shift),
	.io_13_9_0(d),
	
	.io_13_11_0(),
	.io_13_11_1(),
	.io_13_12_0()
);

task shiftedge;
begin
	shift = 1'b1;
	#10;
	shift = 1'b0;
	#10;
end
endtask

integer i;
reg shifted;

always begin
	$dumpfile("level0.vcd");
	$dumpvars(0, dut);
	
	shift = 1'b0;
	shifted = 1'b1;
	for(i=0;i<16;i=i+1) begin
		d = shifted;
		shiftedge;
	end
	
	shiftedge;
	shiftedge;
	shiftedge;
	
	$finish;
end

endmodule
