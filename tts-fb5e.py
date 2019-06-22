import soundfile as sf
import numpy as np

inputString = "Eks.ploU.ZIn"

vowelList = ["E", "oU", "I"]
consonantList = ["ks", "pl", "Z", "n"]
combinedList = vowelList + consonantList

def trimUntilInList(workingSyl):
    for i in range(len(workingSyl)):
        if workingSyl in combinedList:
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

def synthesizeSyllable(phonemeList):

    firstDone = False
    for phoneme in phonemeList:
        path = ""
        if phoneme in consonantList:
            path = "consonant/"
        elif firstDone:
            path = "end/"
        else:
            path = "start/"

        audiodata, samplerate = sf.read("phonemes/" +path +phoneme +".ogg")

        if firstDone:
            outputFrames = np.concatenate((outputFrames, audiodata))
        else:
            outputFrames = audiodata
            firstDone = True

    return outputFrames


thisSyl = ""
inputString = inputString + "."
firstDone = False
for char in inputString:
    if char != ".":
        thisSyl = thisSyl + char
    else:
        sylAudio = synthesizeSyllable(searchForFiles(thisSyl))

        if firstDone:
            synthesizedOutput = np.concatenate((synthesizedOutput, sylAudio))
        else:
            synthesizedOutput = sylAudio
            firstDone = True
        
        thisSyl = ""

sf.write("output.wav", synthesizedOutput, 96000)