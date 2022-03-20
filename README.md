# Lunch-bot alpha 0.1v
## Bot for creating text for choosing lunch locations

This text can be posted to chat and then people can react
to the text to indicate their preferred place to go for lunch.

Example output of the script is down below.

----
## Päevapakkumised 21.märts 
### 1️⃣ Delta kohvik:
* Pardi-confit kartulite/riisi/tatra, kastme ja salatiga. 5,80€
Duck confit with potates/rice/buckwheat, sauce and salad. 5,80€
* Rebitud sealiha kartulite/tatra, kastme ja salatiga. 5,50€
Pulled pork with potatoes/buckwheat, sauce and salad. 5,50€
* Kapsakotlet kartulite/riisi/tatra, kastme ja salatiga (V). 4,90€
Cabbage cutlet with potatoes/rice/buckwheat, sauce and salad (V). 4,90€
* Kana poolkoib kartulite/tatra, kastme ja salatiga. 4,80€
Chicken drumsticks with potatoes/buckwheat, sauce and salad. 4,80€
* Köögivilja püreesupp. 3,00/2,00€
Vegetable puree soup. 3,00/2,00€
### 2️⃣ Cafe Naiiv:
* Krõbekana kauss. 4,90€
* Falafeli kauss. 4,50€
### 3️⃣ The Grill:
* Gruusia Odzahuri: praetud sealiha kartulitega, paprika ja sibulaga, kaste, leib, maitsevesi. 5,00€

----

## Dependency's
* requests - for getting the päevapakkumised.ee page 
* bs4 - for parsing the HTML 
* pyperclip - for copying the text to clipboard
* babel.dates - for getting date as estonian