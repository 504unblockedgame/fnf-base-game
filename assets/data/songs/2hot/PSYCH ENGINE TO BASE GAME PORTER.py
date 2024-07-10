import glob
import json

# PSYCH ENGINE TO BASE GAME PORTER
# Made by tposejank

# Documentation
# - Structure
# Base game charts go as follows:

# ______________________________________

# version: int
# scrollSpeed: object {"difficulty": float}
# events: list {t: float, e: string, v: object}
# notes: object {
#     "difficulty": list {
#         t: float, d: int, l: float, k: string
#     }
# }
# generatedBy: string

# ______________________________________

# 'version' may be irrelevant
# 'scrollSpeed' contains the scroll speed for each difficulty
# 'events' is a list of events
# 'notes' contains the notes for each difficulty

# in events and notes:
# - t: time in milliseconds

# in events:
# - e: event name
# - v: event metadata, may also be an int (see bopeebo chart json)

# in notes:
# - d: note data
# - l: hold note duration (?)
# - k: optional, animation played (?)

# 'generatedBy' may be irrelevant as well

# - Metadata file:

# ______________________________________

# timeFormat: string
# artist: string
# playData: object {
#   album: string
#   previewStart: int
#   previewEnd: int
#   stage: string
#   characters: object {
#       player: string
#       girlfriend: string
#       opponent: string
#   },
#   songVariations: list
#   difficulties: list[string]
#   noteStyle: string
# }
# songName: string
# timeChanges: list[object]: {
#   d: float?
#   n: float?
#   t: float?
#   bt: list[int]
#   bpm: float
# }
# generatedBy: string
# looped: bool
# version: string

# ______________________________________

# timeFormat: is probably irrelevant right now, as in FNF charts the time has always been measured in milliseconds ('ms')
# artist: artist name.
# playData: object containing information you would previously find in a chart
# - album: album codename
# - previewStart: time in milliseconds at which the song preview starts, for freeplay? ive not seen used yet
# - previewEnd: time in milliseconds...
# - stage: the stage
# - characters: object containing the characters of the song
#   - player: bf
#   - girlfriend: girlfriend
#   - opponent: dad
# - songVariations: ive not looked through but probably for erect remixes
# - difficulties: a list containing the difficulties
# - noteStyle: notestyle (pixel or funkin)
# songName: the song name, but actually formatted, professionally named
# timeChanges: list containing objects containing idk what, but probably for bpm changes, since the chart doesnt have these
# - d: idk
# - n: idk
# - t: idk
# - bt: mixing?? idk
# - bpm: the bpm
# generatedBy: whatever
# looped: song loops? this is kinda useless,,, why did they add this
# version: the version of the game?

chartTemplate = {
    "version": "0.0.1",
    "scrollSpeed": {},
    "events": [],
    "notes": [],
    "generatedBy": "tposejank Psych Engine chart porter"
}

eventTemplate = {
    "t": None,
    "e": None,
    "v": None
}

focusCameraEventTemplate = {
    "t": None,
    "e": "FocusCamera",
    "v": {
        "char": None
    }
}

zoomCameraEventTemplate = {
    "t": None,
    "e": "ZoomCamera",
    "v": { 
        "duration": None, 
        "ease": None, # INSTANT - Instant 
        "zoom": None 
    }
}

playAnimationEventTemplate = {
    "t": None,
    "e": "PlayAnimation",
    "v": { 
        "target": None, 
        "anim": None, 
        "force": True # In Psych this is always true
    }
}

noteTemplate = {
    "t": None,
    "d": None,
    "l": None,
    # "k": None
    # Idk what "k" really does so we will not include it
}

metaTemplate = {
    "timeFormat": "ms",
    "artist": None, #ask
    "playData": {
        "album": "volume3",
        "previewStart": 0,
        "previewEnd": 15000,
        "stage": None, #ask
        "characters": {
                "player": None,
                "girlfriend": None,
                "opponent": None
            },
            "songVariations": [],
            "difficulties": [], # ask?
            "noteStyle": "funkin"
    },
    "songName": None, # ask
    "timeChanges": [{ "d": 4, "n": 4, "t": -1, "bt": [4, 4, 4, 4], "bpm": None }],
    "generatedBy": "tposejank Psych Engine chart porter",
    "looped": False,
    "version": "0.0.1"
}

def psychtofnf():
    print('EVENTS ARE EXPERIMENTAL!!')

    jsons = glob.glob('*.json')
    
    print('Cherrypick all charts to convert: (0,1,2)')
    for index, jsonf in enumerate(jsons):
        print(f'{index}: {jsonf}')

    chartChoice = input('Charts: ').split(',')

    chartlist = []
    eventsExists = False
    for chart in chartChoice:
        chartIndex = int(chart)

        chartfile = jsons[chartIndex]
        print(f'Added {chartfile}')
        chartlist.append(chartfile)

        if chartfile == 'events.json':
            eventsExists = True
            print('Events chart found')

    convertedChartTemplate = {
        "version": "2.0.0",
        "scrollSpeed": {"default": 1.0},
        "events": [],
        "notes": {},
        "generatedBy": "tposejank Psych Engine chart porter"
    }

    metaDataTemplate = {
        "timeFormat": "ms",
        "artist": None, #ask
        "playData": {
            "album": "volume3",
            "previewStart": 0,
            "previewEnd": 15000,
            "stage": None,
            "characters": {
                    "player": None,
                    "girlfriend": None,
                    "opponent": None
                },
                "songVariations": [],
                "difficulties": [], # ask?
                "noteStyle": "funkin"
        },
        "songName": None, # ask
        "timeChanges": [{ "d": 4, "n": 4, "t": -1, "bt": [4, 4, 4, 4], "bpm": None }],
        "generatedBy": "tposejank Psych Engine chart porter",
        "looped": False,
        "version": "2.2.0"
    }

    for fileName in chartlist:
        with open(fileName, 'r') as file:
            chartObject = json.loads(file.read())
            if fileName != 'events.json':
                fileSplit = fileName.split('-')
                diff = fileSplit[len(fileSplit) - 1]

                isNormal = len(fileSplit) == 1
                if isNormal:
                    diff = 'normal'
                
                noteArray = []
                for section in chartObject['song']['notes']:
                    for note in section['sectionNotes']:
                        data = note[1]
                        if section['mustHitSection'] == False: # BF notes always go first
                            if data < 4: # Opponent Note
                                data = data + 4
                            elif data >= 4: # Bf Note
                                data = data - 4
                        noteArray.append({"t": note[0], "d": data, "l": note[2]})
                
                convertedChartTemplate['scrollSpeed'][diff.replace('.json', '')] = chartObject['song']['speed'] + 1
                # convertedChartTemplate['bpm'] = chartObject['song']['bpm']
                convertedChartTemplate['notes'][diff.replace('.json', '')] = noteArray

                metaDataTemplate['playData']['stage'] = chartObject['song'].get('stage', 'mainStage')
                metaDataTemplate['playData']['characters']['player'] = chartObject['song'].get('player1', '')
                metaDataTemplate['playData']['characters']['girlfriend'] = chartObject['song'].get('player3', '')
                metaDataTemplate['playData']['characters']['opponent'] = chartObject['song'].get('player2', '')
                metaDataTemplate['timeChanges'][0]['bpm'] = chartObject['song']['bpm']
                metaDataTemplate['playData']['difficulties'].append(diff.replace('.json', ''))
            else:
                for event in chartObject.get('events', []):
                    time = event[0]
                    for packetedEvent in event[1]:
                        convertedChartTemplate['events'].append({"t": time, "e": packetedEvent[0], "v": {"value1": packetedEvent[1], "value2": packetedEvent[2]}})
                for section in chartObject['song']['notes']:
                    for note in section['sectionNotes']:
                        data = note[1]
                        if data == -1:
                            convertedChartTemplate['events'].append({"t": note[0], "e": note[2], "v": {"char": note[3]}})
    
    with open(chartlist[0].split('-')[0] + '-chart.json', 'w') as file:
        json.dump(convertedChartTemplate, file, indent=4)

    artist = input("Song artist: ")
    name = input("Song name: ")
    metaDataTemplate['artist'] = artist
    metaDataTemplate['songName'] = name

    with open(chartlist[0].split('-')[0] + '-metadata.json', 'w') as file:
        json.dump(metaDataTemplate, file, indent=4)

def fnftopsych():
    print('Select -chart and -metadata.json')

    jsons = glob.glob('*.json')

    for index, jsonf in enumerate(jsons):
        print(f'{index}: {jsonf}')

    chartChoice = input('Chart Choice: ')
    metaChoice = input('Meta Choice: ')

    chartJSON = ''
    metaJSON = ''

    chartJSON = jsons[int(chartChoice)]
    metaJSON = jsons[int(metaChoice)]

    with open(metaJSON, 'r') as file:
        metaObj = json.loads(file.read())

    with open(chartJSON, 'r') as file:
        chartObj = json.loads(file.read())

    difficulties = metaObj['playData']['difficulties']

    for difficulty in difficulties:
        FNFChartTemplate = {
            "song": {
                "song": None,
                "bpm": None,
                "needsVoices": True,
                "player1": None,
                "player2": None,
                "speed": None,
                "notes": [],
                "stage": None
            },
            "generatedBy": "tposejank FNF to Psych Engine porter"
        }

        FNFChartTemplate['song']['speed'] = chartObj['scrollSpeed'].get(difficulty, 1)
        FNFChartTemplate['song']['song'] = metaObj['songName']
        FNFChartTemplate['song']['bpm'] = metaObj['timeChanges'][0]['bpm']
        FNFChartTemplate['song']['player1'] = metaObj['playData']['characters']['player']
        FNFChartTemplate['song']['player2'] = metaObj['playData']['characters']['opponent']
        FNFChartTemplate['song']['player3'] = metaObj['playData']['characters']['girlfriend']
        FNFChartTemplate['song']['stage'] = metaObj['playData']['stage']

        bpm = metaObj['timeChanges'][0]['bpm']
        beatLen = (60 / bpm) * 1000
        secLen = beatLen * 4

        curSecTime = 0
        nextSecTime = secLen
        curSec = 0
        FNFChartTemplate['song']['notes'].append({
            "sectionNotes": [],
            "lengthInSteps": 16,
            "mustHitSection": True,
            "bpm": 0,
            "changeBPM": False
        })

        for note in chartObj['notes'][difficulty]:
            time = note['t']
            data = note['d']
            dur = note['l']

            sectionNumber = curSec
            if curSec >= len(FNFChartTemplate['song']['notes']):
                sectionNumber = len(FNFChartTemplate['song']['notes']) - 1

            FNFChartTemplate['song']['notes'][sectionNumber]['sectionNotes'].append([
                time,
                data,
                dur
            ])
            
            if time >= nextSecTime:
                FNFChartTemplate['song']['notes'].append({
                    "sectionNotes": [],
                    "lengthInSteps": 16,
                    "mustHitSection": True,
                    "bpm": 0,
                    "changeBPM": False
                })

                curSec += 1
                curSecTime += secLen
                nextSecTime += secLen
        
            #print(curSec)

        with open(f'result-{difficulty}.json', 'w') as file:
            json.dump(FNFChartTemplate, file, indent=4)
        
def main():
    print('Select mode')
    print('0: Psych to FNF')
    print('1: FNF to Psych')

    mode = int(input('Choice: '))
    if mode == 0:
        psychtofnf()
    elif mode == 1:
        fnftopsych()

if __name__ == '__main__':
    main()