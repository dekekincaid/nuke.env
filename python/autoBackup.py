# A Jitendra Vaghani creation
# Copyright (c) 2008, Jitendra Vaghani  aka  "veejee"  email: veejee@veefxjee.com
#
# All rights reserved.
#
# Redistribution and use in compiled/source forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#         Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#         Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#         Neither the name of Jitendra Vaghani nor the names of
# its other contributors may be used to endorse or promote products derived
# from this software without specific prior written permission. 
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# USE AT YOUR OWN RISK
#
#------------------------------------
# AutoBackup System
#------------------------------------
# Version 1.0
#------------------------------------
# Worked with Nuke 4.6, 4.7, 5.0, 5.0 v1, 5.0 v2 (win), 
#------------------------------------
# Author:
# Jitendra Vaghani
# VFX supervisor
# Skywork Studios
#------------------------------------

import nuke
import os
import shutil

def autoBackup():
    root = nuke.toNode("root")
    srcPath = root.name()
    (dirPath, fileName) = os.path.split(srcPath)
    (Scene, Shot, Tail) = fileName.split("_")
    (Version, Extention) = Tail.split(".")
    #upVersion = int(Version[-2:]) + 1
    #upVersion = "0" + upVersion
    enumerationPulldown = "Project1 Project2 Project3"
    p = nuke.Panel("Select Project")    
    p.addEnumerationPulldown("Select NodeType:", enumerationPulldown)
    result = p.show()
    Project = p.value("Select NodeType:")
    backupSystem = "\\\skycomp\Projects_Backup"
    dstDir = backupSystem + "\\" + Project + "\\" + Scene    
 
    if os.path.isdir(dstDir):
        print "already exists"
    else:
        print "not exists"
        os.mkdir(dstDir)    
    dstDir = backupSystem + "\\" + Project + "\\" + Scene + "\\" + Shot   
 
    if os.path.isdir(dstDir):
        print "already exists"
    else:
        print "not exists"
        os.mkdir(dstDir)    

    dstPath = backupSystem + "\\" + Project + "\\" + Scene + "\\" + Shot + "\\" + fileName    
    print dstPath    
    shutil.copyfile(srcPath, dstPath)    
    nuke.message("File copied to " + dstPath)
