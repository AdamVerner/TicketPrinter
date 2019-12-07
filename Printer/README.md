#Printer Driver

## co kam?
#####src = zdrojáky k labelům (*.ezpx)

#####data = vygenerovaná data pro běh skriptu


## jak přidat label

1. start FakePrinter
2. Draw label in GoLabel app
3. set printer to FakePrinter address and port
4. select export.
5. verify, that all variables are detected correctly
    if something behaves unexpectedly try --preserve-label option and do it manually
8. done


## jak tisknout
Knihovna se dá používat buď jako knihovna a nebo jako aplikace.

nejaktuálnější informace se dají najít v:

python Printer.py -h


## NOTES
ve slozce data jsou podsložky s názvama templejtů.

Aby byla složka validní, musí obsahovat label.template a jestli je to 
potřeba, tak i příslušné BMP obrázky, ktere museji mit stejne jmeno jako ve zdrojaku

na konci ZPL skriptu, kterej se posila do tiskarnu MUSI byt 





