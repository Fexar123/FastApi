import qrcode


data_to_encode = "https://www.youtube.com/watch?v=OU3ISOeGwLE&list=PLQC1AzOdryAEoWv38AMufTHaGT8KzqScR"

qr = qrcode.QRCode()

qr.add_data(data_to_encode)

image = qr.make_image()

