print("Hello World")
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
import os
import pandas as pd
os.chdir('C:\\Users\\User\\Desktop\\Aflorithmic Labs')

#aeneas forced alignment
config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
task = Task(config_string=config_string)
task.audio_file_path_absolute = "Data/A tale of two cities/tale_of_two_cities_01_dickens_64kb_EDIT.wav"
task.text_file_path_absolute = "Data/A tale of two cities/a_tale_of_two_cities_chapter_1.txt"
task.sync_map_file_path_absolute = "Data/A tale of two cities/syncmap_atotc_c1.json"
ExecuteTask(task).execute()
task.output_sync_map_file()

#creating metadata and list of small audio clips
book = AudioSegment.from_mp3("Data/A tale of two cities/tale_of_two_cities_01_dickens_64kb_EDIT.wav")
with open("Data/A tale of two cities/syncmap_atotc_c1.json") as f: 
    syncmap = json.loads(f.read())

sentences = []
for fragment in syncmap['fragments']:
    if ((float(fragment['end'])*1000) - float(fragment['begin'])*1000) > 400:
        sentences.append({"audio":book[float(fragment['begin'])*1000:float(fragment['end'])*1000], "text":fragment['lines'][0], "start_time":float(fragment['begin']), "end_time":float(fragment['end']), "duration":float(fragment['end'])-float(fragment['begin'])})

df = pd.DataFrame(columns=['filename','text','start_time','end_time','duration'])

# export audio segment
for idx, sentence in enumerate(sentences):
    text = sentence['text'].lower()
    start_time = sentence["start_time"]
    end_time = sentence["end_time"]
    duration = sentence["duration"]
    sentence['audio'].export("Data/A tale of two cities/train_data/sample_"+str(idx)+".wav", format="wav")
    temp_df = pd.DataFrame([{'filename':"sample_"+str(idx)+".wav",'text':text,'start_time': start_time,'end_time':end_time,'duration':duration}], columns=['filename','text', "start_time", "end_time", "duration"])
    df = df.append(temp_df)

df = df.reset_index()

df.to_csv("Data/A tale of two cities/meta_data.csv",index=False)