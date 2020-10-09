import argparse
import os

msg = "Script for splitting up and compressing large chaptered multi-episode BD and DVD video backups. <3"

parser = argparse.ArgumentParser(description = msg) 

# Adding arguments
parser.add_argument("-c", "--Chapters", help = "Set number of chapters per episode", required=True, type=int) 
parser.add_argument("-n", "--TotalEpisodes", help = "Set the number of episodes in thie file", required=True, type=int)
parser.add_argument("-p", "--Preset", help = "Set a handbrake preset", required=True, type=str) 
parser.add_argument("-P", "--PresetFile", help = "Optionally you can load a handbrake preset JSON file with this", default="", type=str)
parser.add_argument("-l", "--Link", help = "If the OP and ED chapters are the first and last chapters in an episode automatically link them externally", action='store_true')
parser.add_argument("-s", "--StartingChapter", help = "Set the first chapter of the first episode in the file (default is \"1\")", default=1, type=int)  
parser.add_argument("-i", "--Input", help = "Input file", required=True, type=str)
parser.add_argument("-o", "--Output", help = "Output filename (no file extension, it will output like this \"[input]-[episode 1, 2, 3, etc].mkv\")", type=str)

# Read arguments from command line  
args = parser.parse_args()

# Setting up stuff
iterator = args.Chapters
max_chapter = args.Chapters * args.TotalEpisodes
episode_counter = 1
if args.Output is None:
    args.Output = args.Input

# Main loop
for x in range(args.StartingChapter, max_chapter, args.Chapters):
    cmd = "HandBrakeCLI --preset-import-file \"{}\" -Z \"{}\" -c {}-{} -i \"{}\" -o \"{} - episode {}.mkv\"".format(args.PresetFile, args.Preset, args.StartingChapter, args.Chapters, args.Input, args.Output, episode_counter)
    print(cmd)
    os.system(cmd)
    args.Chapters += iterator
    args.StartingChapter += iterator
    episode_counter += 1

# Check if you gotta do all this other stuff too and do it, maybe make this function work better
if args.Link == True:

# Make OP and ED segments, this part works fine obviously
    os.system("mkvmerge -o temp.mkv --split chapters:2,5 \"{} - episode 1.mkv\"".format(args.Output))

# Read segment UID for OP and ED
    for i in range(1, 5, 2):  
        print("mkvinfo \"temp-00{}.mkv\"".format(i))
        os.system("mkvinfo \"temp-00{}.mkv\"".format(i))
        os.system("mkvinfo \"temp-00{}.mkv\" > test".format(i))
        with open("test") as f:
            while True:
                line = f.readline()
                poo = line.find("Segment UID")
                if poo > 0:
                    line = line.lstrip("| + Segment UID: ")
                    line = line.rstrip("\n")
                    print("success")
                    if i == 1:
                        OP = line
                        os.rename("temp-001.mkv", "OP.mkv")
                    else:
                        ED = line
                        os.rename("temp-003.mkv", "ED.mkv")
                    break
                    
# Lets make external chapters!
    args.TotalEpisodes += 1
    for i in range(1, args.TotalEpisodes):       
        os.system("mkvmerge -o temp.mkv --split chapters:2,5 \"{} - episode {}.mkv\"".format(args.Output, i))
        print("mkvmerge -o {}_linked{}.mkv --link-to-previous \"{}\" --link-to-next \"{}\" \"{} - episode {}.mkv\"".format(args.Output, i, OP, ED, args.Output, i))
        os.system("mkvmerge -o {}_linked{}.mkv --link-to-previous \"{}\" --link-to-next \"{}\" \"temp-002.mkv\"".format(args.Output, i, OP, ED))
    for i in range(1, 4):
        os.remove("temp-00{}".format(i))

# Finish up 
print("\nuwu; All jobs done!\nUse -h if you need further instructions on how to use this script! ty <3")