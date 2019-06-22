import soundfile as sf
import numpy as np
import os

inputString = "Eks\"ploU.ZIn"


consonantList = os.listdir("phonemes/consonant")
consonantList = list(map(lambda item: item.replace(".ogg", ""), consonantList))

vowelList = os.listdir("phonemes/end/stressed") + os.listdir("phonemes/end/unstressed") + os.listdir("phonemes/start/stressed") + os.listdir("phonemes/start/unstressed")
vowelList = list(map(lambda item: item.replace(".ogg", ""), vowelList))

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

def synthesizeSyllable(phonemeList, stressed):

    firstDone = False
    for phoneme in phonemeList:
        path = ""

        if phoneme in consonantList:
            path = "consonant/"
        else:
            if firstDone:
                path = "end/"
            else:
                path = "start/"

            if stressed:
                path = path + "stressed/"
            else:
                path = path + "unstressed/"

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
stressed = False
for char in inputString:
    if char != "." and char != '"':
        thisSyl = thisSyl + char
    elif thisSyl != "":
        
        sylAudio = synthesizeSyllable(searchForFiles(thisSyl), stressed)

        if firstDone:
            synthesizedOutput = np.concatenate((synthesizedOutput, sylAudio))
        else:
            synthesizedOutput = sylAudio
            firstDone = True
        
        stressed = False
        thisSyl = ""

    if char == '"':
        stressed = True

sf.write("output.wav", synthesizedOutput, 96000)