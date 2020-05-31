release: Dut.bo
	tar -zcf ip-protection.tar.gz \
		--transform 's,^,ip-protection/,' \
		Dockerfile entrypoint.sh Makefile Tb.bs Dut.bo
run: Tb.bs Dut.bo
	bsc -verilog -cpp -Xcpp -DLICENSE_KEY=$(LICENSE_KEY) Tb.bs
	bsc -verilog -e mkTb -o tb
	./tb
Dut.bo: Dut.bsv
	bsc -verilog Dut.bsv
clean:
	rm -f ip-protection.tar.gz tb *.bo *.v
