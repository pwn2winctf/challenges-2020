# Write-up

## Note about bsc

If you try to compile stuff using a different build of bsc, it will complain about mismatch of standard library files:

```
The package `Dut' was compiled using a different version of the file
`Prelude.bo' than what was found in the path.
Please recompile the affected packages in dependency order or with -u.
```

So we just use the supplied container. It may be useful to call bsc ourselves with custom command line options.

One can build the container without the entry point by commenting out the `ENTRYPOINT` line in the [Dockerfile](Dockerfile), then:

```
docker build -t ip-protection .
```


## Dump the bytecode

In the [bsc](https://github.com/B-Lang-org/bsc) repository at GitHub, one can read:

> Additional flags of use to developers can be displayed with the following command:
> 
> `$ bsc -help-hidden`

Amongst lots of undocumented options:

```
Dump/kill after various passes:
[...]
-dinternal
-dbinary
-dfixup
[...]
```

If you try to use the `-dbinary` option, you realize it dumps the bytecode. You could also find this option by studying bsc's source code at GitHub.

```
docker run --rm ip-protection bsc -dbinary -verilog -cpp -Xcpp -DLICENSE_KEY=123 Tb.bs
```



## Analyze the bytecode

Looking for the string `"invalid license key"` at the dump, one finds the relevant excerpts of code:

```
let p :: Prelude.Integer
            p =
              0xFC497367DE3520436E844080242730ACAF44F16C31AD45070F6E28455A2DA126F1242008E5D29624A
0F47B2D28E9963A7CBFA75D
            -- IdProp: p[IdP_keep]
        in  let q :: Prelude.Integer
                q =
                  0xC68F4A48226124EB1D0FDDDCEACEC20253FDAD180D63BEB0057508A08ACF60EAF63E62FD6727C
582A085D4227410364E4E755205
                -- IdProp: q[IdP_keep]
            in  let c1 :: Prelude.Integer
                    c1 =
                      0x6138C614261B2F71D9DC990CD6865F8A178994094349A7C4ED286D8D23E2862674C058976
3725CDF1A08EF1DFBC89E703066A73C
                    -- IdProp: c1[IdP_keep]
                in  let c2 :: Prelude.Integer
                        c2 =
                          0x8AD2F15273E7933543E6761E3EA030650890F3233113D1DD04F43A30798A4EFFC8A7A
3F9F05CC9290FC990841A9198423642C7EF
                        -- IdProp: c2[IdP_keep]

[...]

                                (PrimIf
                                   (_m__ Prelude.PrimUnit)
                                   (PrimBNot
                                      (PrimIntegerEQ (PrimIntegerRem (PrimIntegerAdd q (PrimInteg
erMul k c2)) p) 2))
                                   (.Prelude.bind _m__ _tcdict1546
                                      Prelude.PrimUnit
                                      Prelude.PrimUnit
                                      (Prelude.bind_=
                                         _m__
                                         Prelude.Empty
                                         Prelude.PrimUnit
                                         _tcdict1546
                                         (Prelude.setStateName=
                                            _m__
                                            _c__
                                            Prelude.Empty
                                            _tcdict1001
                                            Prelude.primGetName
                                            (Prelude.addRules=
                                               _m__
                                               _c__
                                               _tcdict1001
                                               (PrimAddSchedPragmas
                                                  _
                                                  (PrimRule
                                                     "violation"
                                                     _
                                                     (PrimOrd
                                                        Prelude.Bool
                                                        1
                                                        (Prelude.True (PrimBuildUndefined Pre
lude.PrimUnit _ 1)))
                                                     (Prelude.toPrimAction=
                                                        Prelude.PrimUnit
                                                        (Prelude.bind_=
                                                           Prelude.ActionValue
                                                           Prelude.PrimUnit
                                                           Prelude.PrimUnit
                                                           Prelude.Prelude.Monad~Prelude.ActionVa
lue=
                                                           (Prelude.fromPrimAction=
                                                              Prelude.PrimUnit
                                                              (Prelude.$display "invalid license key"))
                                                           (Prelude.$finish= (PrimIntegerToBit
2 1))))))))
```

So the message is printed whenever `(PrimBNot (PrimIntegerEQ (PrimIntegerRem (PrimIntegerAdd q (PrimInteg
erMul k c2)) p) 2))` or, in alternate syntax, whenever `(q + k*c2) % p != 2`.


## Solving the equation

We can solve this equation by inverting `c2`, e.g. using Python with gmpy2:

```python
In [1]: import gmpy2

In [2]: p=0xFC497367DE3520436E844080242730ACAF44F16C31AD45070F6E28455A2DA126F1242008E5D29624A0F47B2D28E9963A7CBFA75D
   ...:

In [3]: q=0xC68F4A48226124EB1D0FDDDCEACEC20253FDAD180D63BEB0057508A08ACF60EAF63E62FD6727C582A085D4227410364E4E755205
   ...:

In [4]: c2=0x8AD2F15273E7933543E6761E3EA030650890F3233113D1DD04F43A30798A4EFFC8A7A3F9F05CC9290FC990841A9198423642C7E
   ...: F

In [5]: ((2-q)*gmpy2.invert(c2,p))%p
Out[5]: mpz(2900588852888817522482663339711888485418294656850552706711080114546549830073)
```

or just throw it at some CAS.


## Getting the flag

Now that you have the license key, just run the container's original entry point to print the flag.

```
$ docker run --rm ip-protection ./entrypoint.sh 2900588852888817522482663339711888485418294656850552706711080114546549830073
bsc -verilog -cpp -Xcpp -DLICENSE_KEY=2900588852888817522482663339711888485418294656850552706711080114546549830073 Tb.bs
Verilog file created: mkTb.v
bsc -verilog -e mkTb -o tb
Verilog binary file created: tb
./tb
CTF-BR{HW_1p_Pr073cT1on_1S_$3Cur1ty_By_oBscUr4n71Sm}
```
