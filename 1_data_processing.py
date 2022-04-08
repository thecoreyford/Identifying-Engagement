import os 
import pandas as pd 
import warnings

#================================================================
def splitInteractionsIntoCodingScheme(log):
    ''' Splits the log files into separate data frames for different groups of interactions
        See the coding scheme described in the paper, Figure X. '''

    noteEdit = log[log.description.str.contains("note") == True]
    
    navigate = log[log.description.str.contains("tab") == True]
    navigate = navigate.append(log[log.description.str.contains("bar selected") == True])
    
    playback = log[log.description.str.contains("play clicked") == True]
    playback = playback.append(log[log.description.str.contains("stop") == True])
    
    helps = log[log.description.str.contains("tutorial") == True]
    helps = helps.append(log[log.description.str.contains("help opened for") == True])
    
    building = log[log.description.str.contains("drag") == True]
    building = building.append(log[log.description.str.contains("was deleted") == True])
    building = building.append(log[log.description.str.contains("block added") == True])
    building = building.append(log[log.description.str.contains("connection made between") == True])
    
    param = log[log.description.str.contains("increased") == True]
    param = param.append(log[log.description.str.contains("cremented") == True])
    param = param.append(log[log.description.str.contains("decreased") == True])
    param = param.append(log[log.description.str.contains("array button clicked") == True])
    param = param.append(log[log.description.str.contains("set to") == True])
    
    saving = log[log.description.str.contains("menu bar pressed") == True]
    saving = saving.append(log[log.description.str.contains("new clicked") == True])
    saving = saving.append(log[log.description.str.contains("load clicked") == True])
    saving = saving.append(log[log.description.str.contains("save clicked") == True])
    saving = saving.append(log[log.description.str.contains("save as clicked") == True])
    saving = saving.append(log[log.description.str.contains("midi exported") == True])
    
    clipboard = log[log.description.str.contains("copied") == True]
    clipboard = clipboard.append(log[log.description.str.contains("pasted") == True])
    
    undo = log[log.description.str.contains("undo button pressed") == True] 
    
    return [noteEdit, navigate, playback, helps, building, param, saving, clipboard, undo]



def processInteractionDataIntoWindows():
	items = {"ID": [],
			 "age": [],
			 "gender": [],
			 "musicLessonConfidence": [],
			 "musicNotationConfidence": [],
			 "blockBasedConfidence": [],
			 "computerConfidence": [],
			 "musicSoftwareConfidence": [],
			 "extraPressureRecorded": [],
			 "parentInRoom": [],
			 "noteEdit": [], 
	         "navigate": [], 
	         "playback": [], 
	         "help": [], 
	         "building": [], 
	         "paramChange": [], 
	         "saving": [], 
	         "clipboard": [], 
	         "undo": [],
	         "pleasure" : [],
	         "clearGoals": [],
	         "focusedAttention": [],
	         "clearCutFeedback": [],
	         "engagement": []}
	
	# Questionaire Data 
	gatheredAge= [9,10,9,9,9,11,11,10,9,9]
	gatheredGender= ["Female","Female","Male","Non-Binary","Female","Male","Male","Female","Male","Male"]
	gatheredMusicLessonConfidence= [2,4,5,2,4,3,4,4,2,2]
	gatheredMusicNotationConfidence= [2,1,5,2,4,4,2,4,1,1]
	gatheredBlockBasedConfidence= [4,5,4,2,4,5,5,5,2,4]
	gatheredComputerConfidence= [4,4,5,4,5,5,4,5,5,5]
	gatheredMusicSoftwareConfidence= [1,4,1,1,3,0,3,4,1,4]
	gatheredExtraPressure= [2,1,1,1,1,3,2,2,5,2]
	gatheredParentInRoom= [1,1,1,1,1,2,1,1,5,1]

	for file in os.listdir("raw_data_logs"):
	    if file.endswith(".csv"):
	        
	        print("Processing.... ", file)
	        
	        log = pd.read_csv("raw_data_logs/" + file)
	        
	        startTime = int(log[log.index == 0]["elapsedtime"])
	        endTime = int(log[log.index == (len(log) - 1)]["elapsedtime"])
	        
	        windowSize = 25000
	        hopSize = 25000
	        
	        containedPlay=0
	        current = startTime
	        while current <= endTime:
	            logChunk = log[log["elapsedtime"] >= current]
	            logChunk = logChunk[logChunk["elapsedtime"] <= (current+windowSize)]
	            
	            if len(logChunk) != 0:
	                #=ID==================================================
	                if file[1] == '1':
	                	if file[2] == '0':
	                		items["ID"].append("10")
	                	else:
	                		items["ID"].append("1")
	                else:
	                	items["ID"].append(file[1])
	                
	                

	                #=Questionare Data
	                idIndx = int(items["ID"][len(items["ID"]) - 1]) - 1
	                items["age"].append(gatheredAge[idIndx])
	                items["gender"].append(gatheredGender[idIndx])
	                items["musicLessonConfidence"].append(gatheredMusicLessonConfidence[idIndx])
	                items["musicNotationConfidence"].append(gatheredMusicNotationConfidence[idIndx])
	                items["blockBasedConfidence"].append(gatheredBlockBasedConfidence[idIndx])
	                items["computerConfidence"].append(gatheredComputerConfidence[idIndx])
	                items["musicSoftwareConfidence"].append(gatheredMusicSoftwareConfidence[idIndx])
	                items["extraPressureRecorded"].append(gatheredExtraPressure[idIndx])
	                items["parentInRoom"].append(gatheredParentInRoom[idIndx])


	                #=Interactions======================================
	                items["noteEdit"].append(len(splitInteractionsIntoCodingScheme(logChunk)[0]) / len(logChunk))
	                items["navigate"].append(len(splitInteractionsIntoCodingScheme(logChunk)[1]) / len(logChunk))
	                items["playback"].append(len(splitInteractionsIntoCodingScheme(logChunk)[2]) / len(logChunk))
	                items["help"].append(len(splitInteractionsIntoCodingScheme(logChunk)[3]) / len(logChunk))
	                items["building"].append(len(splitInteractionsIntoCodingScheme(logChunk)[4]) / len(logChunk))
	                items["paramChange"].append(len(splitInteractionsIntoCodingScheme(logChunk)[5]) / len(logChunk))
	                items["saving"].append(len(splitInteractionsIntoCodingScheme(logChunk)[6]) / len(logChunk))
	                items["clipboard"].append(len(splitInteractionsIntoCodingScheme(logChunk)[7]) / len(logChunk))
	                items["undo"].append(len(splitInteractionsIntoCodingScheme(logChunk)[8]) / len(logChunk))
	            
	            
	                #=Engagement Percentages====================================    
	                items["clearGoals"].append(len(logChunk[logChunk["clearGoals"] == 1]) / len(logChunk))
	                items["clearCutFeedback"].append(len(logChunk[logChunk["clearCutFeedback"] == 1]) / len(logChunk))
	                items["focusedAttention"].append(len(logChunk[logChunk["focusedAttention"] == 1]) / len(logChunk))
	                items["pleasure"].append(len(logChunk[logChunk["pleasure"] == 1]) / len(logChunk))
	                items["engagement"].append(len(logChunk[logChunk["allEngagement"] == 1]) / len(logChunk))
	            
	            #=Playback============================================
	            containedPlay += hopSize
	            current += hopSize

	windowedData = pd.DataFrame.from_dict(items)
	windowedData.describe()
	windowedData.to_csv("processed_data/dataset1.csv", 
						  index=False)

def processWindowedDataForDT():
	df = pd.read_csv('processed_data/dataset1.csv')
	df['engagement'] = df['engagement'].transform(lambda x: 'Engagement' if (x > 0.0) else 'No Engagement')
	df['pleasure'] = (df['pleasure'] > 0.0)
	df['clearGoals'] = (df['clearGoals'] > 0.0)
	df['focusedAttention'] = (df['focusedAttention'] > 0.0)
	df['clearCutFeedback'] = (df['clearCutFeedback'] > 0.0)
    
	df.drop(['ID', 'help', 'saving', 'clipboard', 'undo'], axis=1, inplace=True)
	df.to_csv('processed_data/dataset1b.csv', index=False)


#================================================================

if __name__ == "__main__":
	warnings.filterwarnings('ignore');
	processInteractionDataIntoWindows();
	processWindowedDataForDT();

    




