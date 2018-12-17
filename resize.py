from PIL import Image
size=500,500
im = Image.open("images/century.jpg")
output=im.resize((500,500))
name="images/with_logo.jpg"
output.save(name, "JPEG")


