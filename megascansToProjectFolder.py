import maya.cmds as cmds
import shutil
import os

print("Megascans to Project Folder - Callum Stuart")

projectDir=cmds.workspace(q=True, dir=True)#Gets the dir of the project folder (Technically the scenes folder)
projectDir=projectDir.replace("scenes/","")#Removes the scenes bit so it's the project folder root
missing=[]
destination = projectDir+"sourceimages/"
maps=["Displacement","Ao","Albedo","Roughness","Normal","Metalness","Translucency","Opacity"]

#list all file nodes
all_files = cmds.ls(type='file')
#loop through them:
for files in all_files:
    try:#Used in case of broken texture links already being in the scene
        #get the file path:
        source = (cmds.getAttr(files + '.fileTextureName'))
        print(files)#Prints each of the textures
        destinationFolder=(files.split("\n"))[0]
        print(destinationFolder)
        for mapName in maps:
            destinationFolder=destinationFolder.replace(mapName,"")
        specificDestination=destination+destinationFolder+"/"
        print(specificDestination)
        os.makedirs(os.path.dirname(specificDestination), exist_ok=True)#Makes the folder to move the textures into
        shutil.copy(source,specificDestination)#Copies the file

        #strip source to repath, we only want the file name:
        source_strip = source.split('/')
        new_name = source_strip[-1:]
        new_path = (specificDestination + source_strip[-1:][0])
        
        #repath the texture
        cmds.setAttr(files+'.fileTextureName' , new_path , type='string')
        print("Done! \n")
    except FileNotFoundError:
        missing.append(files)    

print("Missing files (Probably broken links or permissions error):")
print(missing)