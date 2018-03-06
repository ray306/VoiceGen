form Variables
 sentence sound_file
 sentence read_path
 sentence output_dir
 real target_dur
endform

Read from file: read_path$
raw_dur = Get total duration
scale = target_dur/raw_dur

To Manipulation: 0.01, 75, 600

Create DurationTier: sound_file$, 0, raw_dur
Add point: 0, scale
Add point: raw_dur, scale

selectObject: "Manipulation "+sound_file$
plusObject: "DurationTier "+sound_file$
Replace duration tier

selectObject: "Manipulation "+sound_file$
Get resynthesis (overlap-add)

Save as WAV file: output_dir$+"/"+sound_file$+".wav"

########################
#
# Praat.exe --run change_duration.praat "piao3" "D:/lab/TTS/pinyin/source2/male/00/piao3.wav" "D:/lab/TTS/" 1.1
# 
########################
# sound_file$ = "bian3"
# read_path$ = "D:/lab/TTS/pinyin/source2/male/00/"+sound_file$+".wav"
# target_dur = 1.1

# Read from file: read_path$
# raw_dur = Get total duration
# scale = target_dur/raw_dur
# 
# To Manipulation: 0.01, 75, 600
# 
# Create DurationTier: sound_file$, 0, raw_dur
# Add point: 0, scale
# Add point: raw_dur, scale
# 
# selectObject: "Manipulation "+sound_file$
# plusObject: "DurationTier "+sound_file$
# Replace duration tier
# 
# selectObject: "Manipulation "+sound_file$
# Get resynthesis (overlap-add)

########################

# sound_file$ = "ai1"
# read_path$ = "D:/lab/TTS/pinyin/source2/male/-00/"+sound_file$+".wav"
# target_durs# = {0.2,0.4,0.6,0.8,1.0,1.2}
# 
# writeInfoLine: read_path$
# 
# raw_file = Read from file: read_path$
# 
# Play
# raw_dur = Get total duration
# 
# for target_dur_ind from 1 to 6
#     target_dur = target_durs#[target_dur_ind]
#     scale = target_dur/raw_dur
#     appendInfoLine: "target: ",target_dur," raw: ",raw_dur," scale: ",scale
#     
#     selectObject: raw_file 
#     To Manipulation: 0.01, 75, 600
#     Create DurationTier: sound_file$, 0, raw_dur 
#     Add point: 0, scale
#     Add point: raw_dur, scale
# 
#     selectObject: "Manipulation "+sound_file$
#     plusObject: "DurationTier "+sound_file$
#     Replace duration tier
# 
#     selectObject: "Manipulation "+sound_file$
#     Get resynthesis (overlap-add)
#     Play
# endfor# 