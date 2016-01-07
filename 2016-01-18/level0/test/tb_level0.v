module tb_level0();

reg shift;
reg d;

level0 dut(
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
reg [15:0] shifted;

always begin
	$dumpfile("level0.vcd");
	$dumpvars(0, dut);
	
	shift = 1'b0;
	shifted = 16'b0011_1001_1100_0011;
	for(i=0;i<16;i=i+1) begin
		d = shifted[15-i];
		shiftedge;
	end
	
	shiftedge;
	shiftedge;
	shiftedge;
	
	$finish;
end

endmodule
