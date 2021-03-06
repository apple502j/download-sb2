"""
    Copyright (C) 2018 apple502j
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
    
    Scratch 2.0 Project downloader
    1. Go to directory
    2. Run download("ID")
    3. Get ID.sb2
    
    NOTE: Scratch 1.4 projects will fail.
    You need scratchapi2: Install by pip.
"""
import os
import json
import shutil
from os.path import splitext
import scratchapi2

def download(pid):
    pid=str(pid)
    try:
        os.mkdir(pid)
    except:
        pass
    os.chdir(pid)
    scratchapi2.Project(pid).save_json("project.json")
    with open("project.json","r",encoding="utf-8") as pjson:
        j=json.load(pjson)
    
    last={"img":0,"wav":0}

    def getname(fn):
        dust, ext=splitext(fn)
        iswav=(ext==".wav")
        if iswav:
            s="{0}{1}".format(last["wav"], ext)
            last["wav"]+=1
        else:
            s="{0}{1}".format(last["img"], ext)
            last["img"]+=1
        return s

    exists=[]
    name=j["penLayerMD5"]
    print("Pen Layer")
    j["penLayerID"]=last["img"]
    with open(getname(name), "wb") as asset:
        scratchapi2.Misc().save_asset(name, asset)
    
    c=0
    for sprite in j["children"]:
        d=0
        for sound in sprite.get("sounds",[]):
            name=sound["md5"]
            if name in exists:
                #continue
                pass
            else:
                exists.append(name)
            j["children"][c]["sounds"][d]["soundID"]=last["wav"]
            with open(getname(name), "wb") as asset:
                print(f"Sprite {sprite['objName']} Sound {sound['soundName']}")
                scratchapi2.Misc().save_asset(name, asset)
            
            d+=1
        d=0
        for costume in sprite.get("costumes",[]):
            name=costume["baseLayerMD5"]
            if name in exists:
                continue
            else:
                exists.append(name)
            j["children"][c]["costumes"][d]["baseLayerID"]=last["img"]
            with open(getname(name), "wb") as asset:
                print(f"Sprite {sprite['objName']} Costume {costume['costumeName']}")
                scratchapi2.Misc().save_asset(name, asset)
            
            d+=1
        c+=1
    c=0
    for stage_sound in j["sounds"]:
        name=stage_sound["md5"]
        if name in exists:
            #continue
            pass
        else:
            exists.append(name)
        j["sounds"][c]["soundID"]=last["wav"]
        with open(getname(name), "wb") as asset:
            print(f"Stage Sound {stage_sound['soundName']}")
            scratchapi2.Misc().save_asset(name, asset)
        
        c+=1
    c=0
    for back in j["costumes"]:
        name=back["baseLayerMD5"]
        if name in exists:
            continue
        else:
            exists.append(name)
        j["costumes"][d]["baseLayerID"]=last["img"]
        with open(getname(name), "wb") as asset:
            print(f"Backdrop {back['costumeName']}")
            scratchapi2.Misc().save_asset(name, asset)
        
        c+=1
    with open("project.json","w",encoding="utf-8") as pjson:
        json.dump(j, pjson, indent=4)
    os.chdir("..")
    shutil.make_archive(pid, "zip", pid)
    os.rename(f"{pid}.zip", f"{pid}.sb2")
