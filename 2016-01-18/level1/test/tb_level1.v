module tb_level1();

reg shift;
reg d;

level1 dut(
	.clk(),
	.shift(shift),
	.d(d),
	
	.led1(),
	.led2()
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
reg [63:0] shifted;

always begin
	$dumpfile("level1.vcd");
	$dumpvars(0, dut);
	
	shift = 1'b0;
	shifted = 64'b0011_1001_1100_0011__1010_1101_1111_0000__1110_0111_1001_1000__1110_0001_1011_1100;
	for(i=0;i<64;i=i+1) begin
		d = shifted[63-i];
		shiftedge;
	end
	
	shiftedge;
	shiftedge;
	shiftedge;
	
	$finish;
end

endmodule
