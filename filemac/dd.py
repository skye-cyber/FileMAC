from OCRTextExtractor import ExtractText
img_objs = ['/home/skye/Software Engineering/Y2/SEM2/RV/SPE 2210 Client Side Programming Year II Semester II_1.png']
text = ''
for i in img_objs:
    extract = ExtractText(i)
    tx = extract.OCR()
    print(tx)
    if tx is not None:
        text += tx
print(text)
