for pdf in `ls *.pdf`                                                                                                            ± main 0
do
  ocrmypdf $pdf ${pdf::-4}.ocr.pdf
done

for f in `ls *.ocr.pdf`
do
 mv $f ${f::-8}.pdf
done