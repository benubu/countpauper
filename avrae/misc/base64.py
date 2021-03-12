!alias base64 embed
<drac2>
a = '&*&'

ascii=""" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"""
asciitable={ch:code+32 for code,ch in enumerate(ascii)}
asciitable['\r']=13
asciitable['\n']=10
a_ascii=[asciitable.get(c) for c in a]

if any(ch is None for ch in a_ascii):
	err("Input needs to be ascii")

b64_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

ascii_bin_str = ""
output = ""

for c in a_ascii:
    ascii_bin_str += f'{c:08b}'  # construct a binary-representation string

numChunks = int(len(ascii_bin_str) / 6)  # how many 6
for i in range(numChunks):
    chunk = ascii_bin_str[i * 6: (i + 1) * 6]
    output += b64_index[int(chunk, base=2)]

leftoverBits = len(ascii_bin_str) % 6  # since the input was a multiple of 8, this must be 2 or 4
if leftoverBits > 0:
    leftover = ascii_bin_str[leftoverBits * -1:]
    if leftoverBits == 2:
        output += b64_index[int(leftover+('0' * 4), base=2)]
        output += ('=' * 2)
    elif leftoverBits == 4:
        output += b64_index[int(leftover+('0' * 2), base=2)]
        output += '='
</drac2>

{{f"-f 'Input|{a}'"}}
{{f"-f 'Encoded|{output}'"}}
-footer 'base64 encoding by Thrombo'