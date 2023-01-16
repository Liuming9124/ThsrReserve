# find allowed chars each for once

# init put chars in
init ='put string in'
# re record not repeat chars
re=[]

for i in init:
    r=0
    for j in re:
        if (i==j):
            r=1
    if r==1:
        continue
    else:
        re.append(i)
print(re)

# ['H', 'R', '3', '7', '5', 'Y', 'F', 'Z', 'C', '9', 'Q', 'T', 'N', '2', 'P', 'A', 'K', 'M', '4', '6', 'V', 'D', 'W', 'G']