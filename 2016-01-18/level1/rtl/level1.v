module level1(
	input clk,
	input shift,
	input d,
	
	output led1, /* still on when password is good */
	output led2,  /* blinking a la Arduino when password is good */
	output reg led3 /* last digit shifted in */
);

/* Password check */

parameter good_password = 64'b0011_1001_1100_0011__1010_1101_1111_0000__1110_0111_1001_1000__1110_0001_1011_1100;

reg [63:0] sr;

wire correct = sr == good_password;

initial sr = 64'd0;

always @(posedge shift) begin
	if(~correct) begin
		sr <= {sr[62:0], d};
		led3 <= d;
	end
end

/* LEDs */

assign led1 = correct;

reg [22:0] blink_counter;
always @(posedge clk) blink_counter <= blink_counter + 23'd1;

assign led2 = correct & blink_counter[22];

endmodule

