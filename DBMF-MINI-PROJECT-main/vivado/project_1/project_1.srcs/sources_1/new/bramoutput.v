module bram_output (
    input  wire        clk,
    input  wire [15:0] addr,
    input  wire [7:0]  din,
    input  wire        we,
    output reg  [7:0]  dout
);
    (* ram_style = "block" *)
    reg [7:0] mem [0:65535];

    always @(posedge clk) begin
        if (we) mem[addr] <= din;
        dout <= mem[addr];
    end

endmodule