module median_filter #(
    parameter IMG_WIDTH  = 256,
    parameter IMG_HEIGHT = 256
)(
    input  wire        clk,
    input  wire        rst,
    input  wire [7:0]  pix_in,
    output reg  [7:0]  pix_out,
    output reg         out_valid,
    output reg  [15:0] rd_addr,
    output reg  [15:0] wr_addr,
    output reg         wr_en,
    output reg         done
);

reg [7:0] row0 [0:IMG_WIDTH-1];
reg [7:0] row1 [0:IMG_WIDTH-1];
reg [7:0] row2 [0:IMG_WIDTH-1];
reg [7:0] col_cnt;
reg [7:0] row_cnt;
reg       running;

// Stage 1 outputs
reg [7:0] p0,p1,p2,p3,p4,p5,p6,p7,p8;
reg       stage1_valid;
reg [7:0] stage1_center;

// Stage 2 outputs
reg [7:0] sorted [0:8];
reg       stage2_valid;
reg [7:0] stage2_center;

// Temp sort array
reg [7:0] t [0:8];

`define SWAP(a,b) \
    if (t[a] > t[b]) begin \
        t[a] = t[a] ^ t[b]; \
        t[b] = t[a] ^ t[b]; \
        t[a] = t[a] ^ t[b]; \
    end

//-----------------------------
// STAGE 1: Capture 3x3 window
//-----------------------------
always @(posedge clk) begin
    if (rst) begin
        rd_addr      <= 0;
        col_cnt      <= 0;
        row_cnt      <= 0;
        running      <= 1;
        stage1_valid <= 0;
        done         <= 0;
    end else begin
        stage1_valid <= 0;
        if (running) begin
            // Shift rows: row0 <- row1 <- row2 <- pix_in
            row0[col_cnt] <= row1[col_cnt];
            row1[col_cnt] <= row2[col_cnt];
            row2[col_cnt] <= pix_in;

            begin : win
                reg [7:0] c0, c2;
                c0 = (col_cnt == 0)           ? 0           : col_cnt - 1;
                c2 = (col_cnt == IMG_WIDTH-1) ? IMG_WIDTH-1 : col_cnt + 1;

                // Top row (oldest)
                p0 <= row0[c0]; p1 <= row0[col_cnt]; p2 <= row0[c2];
                // Middle row (center row)
                p3 <= row1[c0]; p4 <= row1[col_cnt]; p5 <= row1[c2];
                // Bottom row (newest buffered row)
                p6 <= row2[c0]; p7 <= row2[col_cnt]; p8 <= row2[c2];

                // Center pixel is middle of middle row
                stage1_center <= row1[col_cnt];
            end

            stage1_valid <= 1;
            rd_addr      <= rd_addr + 1;

            if (col_cnt == IMG_WIDTH-1) begin
                col_cnt <= 0;
                if (row_cnt == IMG_HEIGHT-1) begin
                    running <= 0;
                    done    <= 1;
                end else
                    row_cnt <= row_cnt + 1;
            end else
                col_cnt <= col_cnt + 1;
        end
    end
end

//-----------------------------
// STAGE 2: Sort window (bubble/network sort with fixed SWAP)
//-----------------------------
always @(posedge clk) begin
    stage2_valid  <= 0;
    stage2_center <= stage1_center;

    if (stage1_valid) begin
        t[0]=p0; t[1]=p1; t[2]=p2;
        t[3]=p3; t[4]=p4; t[5]=p5;
        t[6]=p6; t[7]=p7; t[8]=p8;

        // Sorting network for 9 elements
        `SWAP(0,1) `SWAP(3,4) `SWAP(6,7)
        `SWAP(1,2) `SWAP(4,5) `SWAP(7,8)
        `SWAP(0,1) `SWAP(3,4) `SWAP(6,7)
        `SWAP(0,3) `SWAP(1,4) `SWAP(2,5)
        `SWAP(3,6) `SWAP(4,7) `SWAP(5,8)
        `SWAP(0,3) `SWAP(1,4) `SWAP(2,5)
        `SWAP(1,3) `SWAP(2,4)
        `SWAP(2,3)

        sorted[0]<=t[0]; sorted[1]<=t[1]; sorted[2]<=t[2];
        sorted[3]<=t[3]; sorted[4]<=t[4]; sorted[5]<=t[5];
        sorted[6]<=t[6]; sorted[7]<=t[7]; sorted[8]<=t[8];

        stage2_valid <= 1;
    end
end

//-----------------------------
// STAGE 3: DBMF Decision
// Replace pixel if it is 0x00 (pepper) OR 0xFF (salt)
//-----------------------------
always @(posedge clk) begin
    if (rst) begin
        wr_addr   <= 0;
        out_valid <= 0;
        wr_en     <= 0;
        pix_out   <= 0;
    end else begin
        out_valid <= 0;
        wr_en     <= 0;

        if (stage2_valid) begin
            // DBMF: replace both salt (0xFF) and pepper (0x00) with median
            if (stage2_center == 8'h00 || stage2_center == 8'hFF)
                pix_out <= sorted[4];     // median of 9 = index 4
            else
                pix_out <= stage2_center; // clean pixel, pass through

            out_valid <= 1;
            wr_en     <= 1;
            wr_addr   <= wr_addr + 1;
        end
    end
end

endmodule