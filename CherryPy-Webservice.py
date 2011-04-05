#!/usr/local/bin/python

__author__ = 'Nolan Nichols'

#REST webservice
import os.path
import cherrypy
from cherrypy.lib.static import serve_file
from cherrypy import expose
import nii2aim as na


class ImageQuery:
    @expose
    def index(self):
        return "<h2>Welcome! This is the <i>NIfTI to Annotation Image Markup (AIM)</i> Web Service for Processing Brain Images</h2>"
    @expose
    def aal2aimByVoxel(self, aalID, fmriFile):
        na.aalID2aimByVoxel(aalID, fmriFile)
        return serve_file('/home/bnniii/aim-webservice/aim-temp/AIM-%s.xml' % aalID) # content_type='application/xml'
    @expose
    def aalID2aimMeanByLabel(self, aalID, fmriFile):
        na.aalID2MeanLabel(aalID, fmriFile)
        return serve_file('/home/bnniii/aim-webservice/aim-temp/AIM-%s.xml' % aalID) # content_type='application/xml'
    @expose
    def listTest(self, aalIDs):
        aalList = tuple(aalIDs)
        print type(aalIDs)
        print aalList
        print aalList[0]
        print aalList[0][0]
        for ID in range(len(aalList)):
            print aalList[ID]
        return str(aalList)

#configure ip address and port for web service
cherrypy.config.update({'server.socket_host': '128.95.228.21','server.socket_port': 8080,})

#start webservice
cherrypy.quickstart(ImageQuery())
