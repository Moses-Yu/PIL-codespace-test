from PIL import Image
from PIL import ImageOps
import collections

def _kmp(needle, haystack, _dummy):  # Knuth-Morris-Pratt search algorithm implementation (to be used by screen capture)
    """
    TODO
    """
    # build table of shift amounts
    shifts = [1] * (len(needle) + 1)
    shift = 1
    for pos in range(len(needle)):
        while shift <= pos and needle[pos] != needle[pos - shift]:
            shift += shifts[pos - shift]
        shifts[pos + 1] = shift

    # do the actual search
    startPos = 0
    matchLen = 0
    for c in haystack:
        while matchLen == len(needle) or matchLen >= 0 and needle[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(needle):
            yield startPos

Box = collections.namedtuple('Box', 'left top width height')

def main():
    needleimage = open("image1.png", "rb")
    haystackimage = open("image.png", "rb")

    needleimage = Image.open(needleimage)
    haystackimage = Image.open(haystackimage)
    needleimage = ImageOps.grayscale(needleimage)
    haystackimage = ImageOps.grayscale(haystackimage)
    # needleimage.save("./hi.png")

    needleWidth, needleHeight = needleimage.size
    haystackWidth, haystackHeight = haystackimage.size

    needleImageData = tuple(needleimage.getdata())
    haystackImageData = tuple(haystackimage.getdata())

    needleImageRows = [
    needleImageData[y * needleWidth : (y + 1) * needleWidth] for y in range(needleHeight)
    ]
    needleImageFirstRow = needleImageRows[0]

    step = 1
    numMatchesFound = 0
    for y in range(haystackHeight):
        # print(y)  # start at the leftmost column
        for matchx in _kmp(
            needleImageFirstRow, haystackImageData[y * haystackWidth : (y + 1) * haystackWidth], step
        ):
            # print(matchx)
            foundMatch = True
            for searchy in range(1, needleHeight, step):
                haystackStart = (searchy + y) * haystackWidth + matchx
                if (
                    needleImageData[searchy * needleWidth : (searchy + 1) * needleWidth]
                    != haystackImageData[haystackStart : haystackStart + needleWidth]
                ):
                    foundMatch = False
                    break
            if foundMatch:
                # Match found, report the x, y, width, height of where the matching region is in haystack.
                numMatchesFound += 1
                yield(Box(matchx, y, needleWidth, needleHeight))
            
            # print(foundMatch)

result = main()
print(tuple(result))
