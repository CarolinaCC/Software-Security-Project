# Algorithm Description

For each ***function*** of the program store:
  * The ***vulnerabilities*** for which it is a ***source***
  * The ***vulnerabilities*** for which it is a ***sink***
  * The ***vulnerabilities*** for which it is a ***sanitizer***

For each ***variable*** of the program store:
  * ***Sources*** of ***vulnerabilities*** it has passed through (vulnerability: list(source))
  * ***Sanitizers*** and respective ***vulnerability*** it has passed through (vulnerability: list(sanitizers))

A **literal** has no ***sources*** nor ***sanitizers*** (empty)

An **unary expression** keeps the ***sources*** and ***sanitizers*** of it's right hand expression

An **if and while expression** have the ***sources*** and ***sanitizers*** of it's test expression (implicit data flow)

A **double expression** ***sources*** is the ***union of the sources*** of it's left hand and right hand expressions

A **double expression** ***sanitizers*** is the ***intersection of the sanitizers*** of it's left hand and right hand expressions according to the following algorithm:
   * For each ***sanitizer***:
     * If the ***sanitizer*** occurs on ***both expressions*** it is ***kept*** in the resulting expressions
     * If the ***sanitizer*** occurs on only ***one*** of the expressions:
       * If the ***other expression*** has a ***source*** for the ***vulnerability*** that is sanitized
         * The ***sanitizer*** is ***dropped***
       * Else
         * The ***sanitizer*** is ***kept***

When a variable is ***assigned*** it's ***sources*** and ***sanitizers*** are the ***sources*** and ***sanitizers*** of it's right hand expression.

When a function call occurs test:
  * For each ***vulnerability*** the function is a ***sink*** for, see the function ***arguments***:
    * If any of them has a ***source*** of that ***vulnerability***: Store it for the output
  * For each ***vulnerability*** the function is a ***sanitizer*** for, see the function ***arguments***:
    * If any of them has a ***source*** of the same vulnerability, the resulting expression will also have that ***sanitizer*** for that ***vulnerability***
  * For each ***vulnerability*** the function is a ***source*** for:
    * The resulting ***expression*** will also have that ***source*** for that ***vulnerability***
  * For each ***argument***
    * The resulting ***expression*** will also have it's ***sources*** and ***sanitizers*** (implicit information flow)
