`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 26.03.2026 11:49:56
// Design Name: 
// Module Name: braminput
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module bram_input (
    input  wire        clk,
    input  wire [15:0] addr,
    output reg  [7:0]  dout
);

    (* ram_style = "block" *)
    reg [7:0] mem [0:65535];

    initial begin
        $readmemh("C:/DBMF/noisy_image3.mem", mem);
    end

    always @(posedge clk) begin
        dout <= mem[addr];
    end

endmodule
