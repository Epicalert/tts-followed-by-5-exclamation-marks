import soundfile as sf

inputString = "eks.plOu.Zin"

fileList = ["e", "ks", "pl", "Ou", "Z", "i", "n"]

def trimUntilInList(workingSyl):
    for i in range(len(workingSyl)):
        if workingSyl in fileList:
            return workingSyl
        else:
            #trim one char off right of workingSyl
            workingSyl = workingSyl[:len(workingSyl) - 1]

def searchForFiles(syllable):
    output = []

    workingSyl = syllable

    while len(workingSyl) > 0:
        result = trimUntilInList(workingSyl)
        output = output + [result]
        workingSyl = workingSyl[len(result):]

    return output


thisSyl = ""
inputString = inputString + "."
for char in inputString:
    if char != ".":
        thisSyl = thisSyl + char
    else:
        print(searchForFiles(thisSyl))
        thisSyl = ""