#!/bin/sh
cp $1/iptvupdate/custom/xxx.sh $2/iptvupdate/custom/xxx.sh
status=$?
if [$status -ne 0]; then
	echo "B��d krytyczny. Plik $0 nie mo�e zosta� skopiowany, error[$status]."
	exit 1	
fi
cp $1/hosts/hostXXX.py $2/hosts/
cp $1/icons/logos/XXXlogo.png $2/icons/logos/
cp $1/icons/PlayerSelector/XXX*.png $2/icons/PlayerSelector/
status=$?
if [ $status -ne 0 ]; then
	echo "Uwaga nie uda-o si� skopiowa� XXX, error[$status]."
	exit 0
fi
echo "Wykonywanie $0 zako�czone sukcesem."
exit 0