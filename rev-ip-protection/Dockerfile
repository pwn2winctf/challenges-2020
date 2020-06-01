FROM thotypous/bsc-ubuntu1804
WORKDIR /ip-protection/
ADD entrypoint.sh Makefile Tb.bs Dut.bo /ip-protection/
RUN sed -ri '/Dut\.bsv/d' Makefile
ENTRYPOINT ["./entrypoint.sh"]
