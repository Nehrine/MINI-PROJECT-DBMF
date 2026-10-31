module top (
    input  wire       clk,
    input  wire       rst_n,
    output wire [3:0] led
);

wire rst = ~rst_n;

wire [15:0] rd_addr;
wire [15:0] wr_addr;
wire [7:0]  pix_in;
wire [7:0]  pix_out;
wire        wr_en;
wire        out_valid;
wire        done;

bram_input u_bram_in (
    .clk  (clk),
    .addr (rd_addr),
    .dout (pix_in)
);

median_filter #(
    .IMG_WIDTH  (256),
    .IMG_HEIGHT (256)
) u_filter (
    .clk       (clk),
    .rst       (rst),
    .pix_in    (pix_in),
    .pix_out   (pix_out),
    .out_valid (out_valid),
    .rd_addr   (rd_addr),
    .wr_addr   (wr_addr),
    .wr_en     (wr_en),
    .done      (done)
);

bram_output u_bram_out (
    .clk  (clk),
    .addr (wr_addr),
    .din  (pix_out),
    .we   (wr_en),
    .dout ()
);

// ILA
ila_0 u_ila (
    .clk    (clk),
    .probe0 (pix_out),
    .probe1 (wr_addr),
    .probe2 (wr_en)
);

// LEDs
assign led[0] = 1'b1;
assign led[1] = ~done;
assign led[2] = done;
assign led[3] = 1'b1;

endmodule