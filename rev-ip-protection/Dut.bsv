interface Dut;
	method Bit#(1) out;
endinterface

module mkDut#(Integer k)(Dut);
	Integer p  = 'hfc497367de3520436e844080242730acaf44f16c31ad45070f6e28455a2da126f1242008e5d29624a0f47b2d28e9963a7cbfa75d;
	Integer q  = 'hc68f4a48226124eb1d0fdddceacec20253fdad180d63beb0057508a08acf60eaf63e62fd6727c582a085d4227410364e4e755205;
	Integer c1 = 'h6138c614261b2f71d9dc990cd6865f8a178994094349a7c4ed286d8d23e2862674c0589763725cdf1a08ef1dfbc89e703066a73c;
	Integer c2 = 'h8ad2f15273e7933543e6761e3ea030650890f3233113d1dd04f43a30798a4effc8a7a3f9f05cc9290fc990841a9198423642c7ef;

	Reg#(Bit#(416)) st <- mkReg(fromInteger((q+k*c1)%p));
	rule upd;
		st <= st << 1;
	endrule

	if ((q+k*c2)%p != 2) begin
		rule violation;
			$display("invalid license key");
			$finish(1);
		endrule
	end

	method Bit#(1) out = st[415];
endmodule
