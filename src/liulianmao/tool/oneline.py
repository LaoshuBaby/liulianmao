with open("1.txt","r") as f:
    data=f.read()

with open("1.txt","w") as f:
    f.write(data.replace("\n","\\n\n"))
