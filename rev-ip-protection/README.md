# IP Protection

## Description

Intellectual Property Protection Corp is the market leader on hardware IP protection. Their product protects IP cores with "proprietary military-strength encryption technology" so that they can only be instantiated in a hardware design by supplying the correct license key.

We were able to break into some Butcher Corp workstations and leak several IP cores they used in the rbs project. However, these IP cores are protected with IP Protection Corp technology, and we were not able to recover their license key.

We are now recruiting talented reverse engineers to help us. Are you able to understand how IP Protection Corp technology *really* works? Please find attached a simple demo. If you find the correct license key, the test bench (Tb) will retrieve the flag from the protected design under test (Dut) and print it to the output.

You can use Docker to run the test bench, e.g.:

```
docker build -t ip-protection .
docker run --rm ip-protection 123
```

## Descrição

A Intellectual Property Protection Corp é a empresa líder do mercado em proteção de propriedade intelectual de hardware. O produto deles protege IP cores com "tecnologia de criptografia proprietária de nível militar", de forma que só possam ser instanciados em um projeto de hardware caso fornecida a chave de licença correta.

Nós conseguimos invadir algumas máquinas da Butcher Corp e vazar vários IP cores que eles usaram no projeto rbs. No entanto, esses IP cores estão protegidos com tecnologia da IP Protection Corp, e não fomos capazes de recuperar a chave de licença deles.

Estamos agora recrutando pessoas com talento em engenharia reversa para nos ajudar. Você consegue entender como a tecnologia da IP Protection Corp *realmente* funciona? Por favor veja uma demonstração simples no arquivo anexo. Se você descobrir a chave de licença correta, o *test bench* (Tb) obterá a flag do pacote protegido *design under test* (Dut) e a mostrará na saída.

Você pode usar o Docker para executar o *test bench*, por exemplo:

```
docker build -t ip-protection .
docker run --rm ip-protection 123
```

## Categories

 * Reversing

## Write-up

 * [writeup.md](writeup.md)
