import soundfile as sf
import numpy as np
import os
import sys

inputString = sys.argv[1]
inputString = inputString.replace("%", "")    #TODO: add support for secondary stress
inputString = inputString.replace(":", "")      #TODO: add support for syllable length
inputString = inputString.replace(" ", "")

consonantList = os.listdir("phonemes/consonant")
consonantList = list(map(lambda item: item.replace(".ogg", ""), consonantList))

vowelList = os.listdir("phonemes/stressed") + os.listdir("phonemes/unstressed")
vowelList = list(map(lambda item: item.replace(".ogg", ""), vowelList))

combinedList = vowelList + consonantList


def trimUntilInList(workingSyl):
    originalInput = workingSyl
    for i in range(len(workingSyl)):
        if workingSyl in combinedList:
            return workingSyl 
        else:
            if len(workingSyl) == 1:
                print("ERROR: could not resolve segment '" + originalInput + "'.")
                sys.exit()
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
    firstVowelDone = False
    for phoneme in phonemeList:
        path = ""

        if phoneme in consonantList:
            path = "consonant/"
        else:
            if stressed and not firstVowelDone:
                path = path + "stressed/"
            else:
                path = path + "unstressed/"

            firstVowelDone = True

        fullPath = "phonemes/" +path +phoneme +".ogg"

        if os.path.isfile(fullPath):
            audiodata, samplerate = sf.read(fullPath)
        else:
            print("ERROR: could not find " +fullPath)
            sys.exit()

        if firstDone:
            outputFrames = np.concatenate((outputFrames, audiodata))
        else:
            outputFrames = audiodata
            firstDone = True

    return outputFrames, samplerate


thisSyl = ""
inputString = inputString + "."
firstDone = False
stressed = False
for char in inputString:
    if char != "." and char != '"':
        thisSyl = thisSyl + char
    elif thisSyl != "":
        
        sylAudio, samplerate = synthesizeSyllable(searchForFiles(thisSyl), stressed)

        if firstDone:
            synthesizedOutput = np.concatenate((synthesizedOutput, sylAudio))
        else:
            synthesizedOutput = sylAudio
            firstDone = True
        
        stressed = False
        thisSyl = ""

    if char == '"':
        stressed = True

sf.write("output.wav", synthesizedOutput, samplerate)