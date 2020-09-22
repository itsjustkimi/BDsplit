import argparse
import os

msg = "Script for splitting up and compressing large chaptered multi-episode BD and DVD video backups. <3"

parser = argparse.ArgumentParser(description = msg) 

# Adding optional argument 
parser.add_argument("-c", "--Chapters", help = "Set number of chapters per episode.", required=True, type=int) 
parser.add_argument("-n", "--TotalEpisodes", help = "Set the number of episodes in thie file.", required=True, type=int)
parser.add_argument("-p", "--Preset", help = "Set a handbrake preset", required=True, type=str) 
parser.add_argument("-P", "--PresetFile", help = "Optionally you can load a handbrake preset JSON file with this", default="", type=str)
parser.add_argument("-s", "--StartingChapter", help = "Set the first chapter of the first episode in the file (default is \"1\")", default=1, type=int)  
parser.add_argument("-i", "--Input", help = "Input file.", required=True, type=str)

# Read arguments from command line  
args = parser.parse_args()

# Setting up stuff
iterator = args.Chapters
max_chapter = args.Chapters * args.TotalEpisodes
counter = 1

# Main loop 480pmod.json
for x in range(args.StartingChapter,max_chapter,args.Chapters):
    cmd = "HandBrakeCLI --preset-import-file \"{0}\" -Z \"{1}\" -c {2}-{3} -i \"{4}\" -o \"{4} - {5}.mkv\"".format(args.PresetFile, args.Preset, args.StartingChapter, args.Chapters, args.Input, counter)
    print(cmd)
    os.system(cmd)
    args.Chapters += iterator
    counter += 1

# Finish up 
print("\nuwu; All jobs done!\nUse -h if you need further instructions on how to use this script! ty <3")
