# Algorithm Description

<!-- Nota: Variaveis nao inicializadas tambem sao sources. de todas as vulnerabilidades com a source a ser o nome da vulnerabilidade-->
<!-- Dizer linhas das vulnerabilidades para bonus -->
For each ***function*** of the program store:
  * The ***vulnerabilities*** for which it is a ***source***
  * The ***vulnerabilities*** for which it is a ***sink***
  * The ***vulnerabilities*** for which it is a ***sanitizer***

For each ***variable*** of the program store:
  <!-- {var_name: {"vuln": ..., "source":..., "sanitizer":... },....} -->
  * ***Sources*** of ***vulnerabilities*** it has passed through (format specified in comment)
  * ***Sanitizers*** and respective ***vulnerability*** it has passed through (vulnerability: list(sanitizers))

A **literal** has no vulnerability(empty)

An **unary expression** keeps the vulnerabilities of it's right hand expression

An **if/while expression** has the vulnerabilities of it's test expression (implicit data flow) (store in stack)

A **double expression** vulnerabilities is the concatenation of it's left hand and right hand expressions

When a variable is first seen it has a source of each of the vulnerabilities whose name is the variable name

When a variable is ***assigned*** it's ***sources*** and ***sanitizers*** are the ***sources*** and ***sanitizers*** of the right hand expression.

When a function call occurs test:
  * For each ***vulnerability*** the function is a ***sink*** for, see the function ***arguments***:
    * If any of them has a ***source*** of that ***vulnerability***: Store it for the output
  * For each ***vulnerability*** the function is a ***sanitizer*** for, see the function ***arguments***:
    * If any of them has a ***source*** of the same vulnerability, the resulting expression will also have that ***sanitizer*** for that ***vulnerability***
  * For each ***vulnerability*** the function is a ***source*** for:
    * The resulting ***expression*** will also have that ***source*** for that ***vulnerability***
  * For each ***argument***
    * The resulting ***expression*** will also have it's vulnerabilities (implicit information flow)
