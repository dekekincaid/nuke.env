from cgtypes import vec3
from cgtypes import mat3
import math

class vrayCameraAttributes:
	def translateX(self):
		list=nuke.thisNode().metadata('exr/cameraTransform',nuke.frame(),'view')
		if (list==None):
			return 0
		else:
			return list[12]
	def translateY(self):
		list=nuke.thisNode().metadata('exr/cameraTransform',nuke.frame(),'view')
		if (list==None):
			return 0
		else:
			return list[13]
	def translateZ(self):
		list=nuke.thisNode().metadata('exr/cameraTransform',nuke.frame(),'view')
		if (list==None):
			return 0
		else:
			return list[14]

	def rotationX(self):		
		list=nuke.thisNode().metadata('exr/cameraTransform',nuke.frame(),'view')		
		if (list==None):
			print 'NoneType'
			return 0
		else:
			list.pop(15)
			list.pop(14)
			list.pop(13)
			list.pop(12)
			list.pop(11)
			list.pop(7)
			list.pop(3)		
			
			M=mat3(list)
			swappedM=mat3(list)
			swappedM.setRow(1,M.getRow(2)*-1.0)
			swappedM.setRow(2,M.getRow(1))
			
			eulerAngles=swappedM.toEulerXYZ()
			return math.degrees(eulerAngles[0])
			
	def rotationY(self):		
		list=nuke.thisNode().metadata('exr/cameraTransform',nuke.frame(),'view')
		if (list==None):
			print 'NoneType'
			return 0
		else:
			list.pop(15)
			list.pop(14)
			list.pop(13)
			list.pop(12)
			list.pop(11)
			list.pop(7)
			list.pop(3)		
			
			M=mat3(list)
			swappedM=mat3(list)
			swappedM.setRow(1,M.getRow(2)*-1.0)
			swappedM.setRow(2,M.getRow(1))
			
			eulerAngles=swappedM.toEulerXYZ()
			return math.degrees(eulerAngles[1])
		
	def rotationZ(self):		
		list=nuke.thisNode().metadata('exr/cameraTransform',nuke.frame(),'view')
		if (list==None):
			print 'NoneType'
			return 0
		else:
			list.pop(15)
			list.pop(14)
			list.pop(13)
			list.pop(12)
			list.pop(11)
			list.pop(7)
			list.pop(3)		
			
			M=mat3(list)
			swappedM=mat3(list)
			swappedM.setRow(1,M.getRow(2)*-1.0)
			swappedM.setRow(2,M.getRow(1))
			
			eulerAngles=swappedM.toEulerXYZ()
			return math.degrees(eulerAngles[2])		