#!/usr/local/bin/python

__author__ = 'Nolan Nichols'

from urllib2 import urlopen
#module to parse xml
from lxml import etree
#module to work with NIfTi images
from nibabel import *
#module for parsing rdf
from rdflib.Graph import Graph
#module to read REST call from vSparQL service
import rdflib
#import sparql query service
rdflib.plugin.register('sparql', rdflib.query.Processor,
                       'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result,
                       'rdfextras.sparql.query', 'SPARQLQueryResult')

#call valueset service to run query mapping FMAIDs to AAL IDs
fmaid2aalURI = urlopen('http://xiphoid.biostr.washington.edu:8080/ValueSetService/ValueSet?qid=97')
fmaString = fmaid2aalURI.read()

#parse fma into an xml tree
fmaXML = etree.XML(fmaString)


#function to add AAL labels or FMAIDs to AIM

aim.append

#Global variables for AIM template
XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'
XSI_TYPE = '{%s}type' % XSI_NS

#create an AIM ImageAnnotation template, elements followed by attribs
ImageAnnotation = etree.Element('ImageAnnotation')
ImageAnnotation.attrib['aimVersion'] = '3.0'
ImageAnnotation.attrib['cagridId'] = '0'
ImageAnnotation.attrib['codeMeaning'] = 'fMRI brain data'
ImageAnnotation.attrib['codeValue'] = 'PIXEL DATA'
ImageAnnotation.attrib['codingSchemeDesignator'] = 'PIXELDATA'
ImageAnnotation.attrib['dateTime'] = ''
ImageAnnotation.attrib['name'] = 'Example AIM file'
ImageAnnotation.attrib['uniqueIdentifier'] = '1.3.6.1.4.1.25403.1095730355278.5896.20101123034021.3'
#configure namespaces
schemaLocation = '{%s}schemaLocation' % XSI_NS
ImageAnnotation.attrib[schemaLocation] = 'gme://caCORE.caCORE/3.2/edu.northwestern.radiology.AIM AIM_v3_rv11_XML.xsd'

#create an AIM ImageAnnotation template - calculationCollection subtree
calculationCollection = etree.SubElement(ImageAnnotation, 'calculationCollection')
Calculation = etree.SubElement(calculationCollection, 'Calculation')
Calculation.attrib['cagridId'] = '0'
Calculation.attrib['codeMeaning'] = 'Z Score'
Calculation.attrib['codeValue'] = 'ZSCORE'
Calculation.attrib['codingSchemeDesignator'] = 'FMRI'
Calculation.attrib['description'] = 'Z Score'
Calculation.attrib['uid'] = '1.3.6.1.4.1.25403.1095730355278.5896.20101123034021.1'

referencedCalculationCollection = etree.SubElement(Calculation, 'referencedCalculationCollection')
calculationResultCollection = etree.SubElement(Calculation, 'calculationResultCollection')
CalculationResult = etree.SubElement(calculationResultCollection, 'CalculationResult')
CalculationResult.attrib['cagridId'] = '0'
CalculationResult.attrib['numberOfDimensions'] = '1'
CalculationResult.attrib['type'] = 'Scalar'
CalculationResult.attrib['unitOfMeasure'] = 'Zscore'

#this is where the fMRI z-score goes for a single coordinate
calculationDataCollection = etree.SubElement(CalculationResult, 'calculationDataCollection')
CalculationData = etree.SubElement(calculationDataCollection, 'CalculationData')
CalculationData.attrib['cagridId'] = '0'
CalculationData.attrib['value'] = '1.665'

coordinateCollection = etree.SubElement(CalculationData,'coordinateCollection')
Coordinate = etree.SubElement(coordinateCollection, 'Coordinate')
Coordinate.attrib['cagridId'] = '0'
Coordinate.attrib['dimensionIndex'] = '0'
Coordinate.attrib['position'] = '0'

#this is the
dimensionCollection = etree.SubElement(CalculationResult,'dimensionCollection')
Dimension = etree.SubElement(dimensionCollection, 'Dimension')
Dimension.attrib['cagridId'] = '0'
Dimension.attrib['index'] = '0'
Dimension.attrib['label'] = 'Value'
Dimension.attrib['size'] = '1'

#create an AIM ImageAnnotation template - user subtree
user = etree.SubElement(ImageAnnotation, 'user')
User = etree.SubElement(user, 'User')
User.attrib['cagridId'] = '0'
User.attrib['loginName'] = 'TEST'
User.attrib['name'] = 'TEST'
User.attrib['numberWithinRoleOfClinicalTrial'] = '2'
User.attrib['roleInTrial'] = 'N/A'

#create an AIM ImageAnnotation template - equipment subtree
equipment = etree.SubElement(ImageAnnotation, 'equipment')
Equipment = etree.SubElement(equipment, 'Equipment')
Equipment.attrib['cagridId'] = '0'
Equipment.attrib['manufacturerModelName'] = 'N/A'
Equipment.attrib['cagridId'] = 'University'
Equipment.attrib['softwareVersion'] = '3.0.0.0'

#create an AIM ImageAnnotation template - anatomicEntityCollection subtree
anatomicEntityCollection = etree.SubElement(ImageAnnotation, 'anatomicEntityCollection')
AnatomicEntity = etree.SubElement(anatomicEntityCollection, 'AnatomicEntity')
AnatomicEntity.attrib['annotatorConfidence'] = '1'
AnatomicEntity.attrib['cagridId'] = '0'
AnatomicEntity.attrib['codeMeaning'] = 'Temporal lobe'
AnatomicEntity.attrib['codeValue'] = 'RID6476'
AnatomicEntity.attrib['codingSchemeDesignator'] = 'RadLex'
AnatomicEntity.attrib['isPresent'] = 'True'
AnatomicEntity.attrib['label'] = 'Pixel in temporal lobe'

#create an AIM ImageAnnotation template - imageReferenceCollection subtree
imageReferenceCollection = etree.SubElement(ImageAnnotation, 'imageReferenceCollection')
ImageReference = etree.SubElement(imageReferenceCollection,'ImageReference')
ImageReference.attrib['cagridId'] = '0'
ImageReference.attrib[XSI_TYPE] = 'DICOMImageReference'

imageStudy = etree.SubElement(ImageReference, 'imageStudy')
ImageStudy = etree.SubElement(imageStudy, 'ImageStudy')
ImageStudy.attrib['cagridId'] = '0'
ImageStudy.attrib['instanceUID'] = '1.3.6.1.4.1.9328.50.45.326662079066250663678557696078244480878'
ImageStudy.attrib['startDate'] = '1887-11-19T00:00:00'
ImageStudy.attrib['startTime'] = '000000'

imageSeries = etree.SubElement(ImageStudy,'imageSeries')
ImageSeries = etree.SubElement(imageSeries, 'ImageSeries')
ImageSeries.attrib['cagridId'] = '0'
ImageSeries.attrib['instanceUID'] = '1.3.6.1.4.1.9328.50.45.157809556490045867232259259088691970356'

imageCollection = etree.SubElement(ImageSeries, 'imageCollection')
Image = etree.SubElement(imageCollection, 'Image')
Image.attrib['cagridId'] = '0'
Image.attrib['sopClassUID'] = '1.2.840.10008.5.1.4.1.1.4'
Image.attrib['sopInstanceUID'] = '1.3.6.1.4.1.9328.50.45.165186936095437264663872068604057093662'

#create an AIM ImageAnnotation template - geometricShapeCollection subtree
geometricShapeCollection = etree.SubElement(ImageAnnotation, 'geometricShapeCollection')
GeometricShape = etree.SubElement(geometricShapeCollection, 'GeometricShape')
GeometricShape.attrib['cagridId'] = '0'
GeometricShape.attrib['includeFlag'] = 'true'
GeometricShape.attrib['shapeIdentifier'] = '0'
GeometricShape.attrib[XSI_TYPE] = 'Point'


spatialCoordinateCollection = etree.SubElement(GeometricShape, 'spatialCoordinateCollection')
SpatialCoordinate = etree.SubElement(spatialCoordinateCollection, 'SpatialCoordinate')
SpatialCoordinate.attrib['cagridId'] = '0'
SpatialCoordinate.attrib['coordinateIndex'] = '0'
SpatialCoordinate.attrib['imageReferenceUID'] = '1.3.6.1.4.1.9328.50.45.165186936095437264663872068604057093662'
SpatialCoordinate.attrib['referencedFrameNumber'] = '1'
SpatialCoordinate.attrib['x'] = '81.1414947509766'
SpatialCoordinate.attrib['y'] = '117.969573974609'
SpatialCoordinate.attrib[XSI_TYPE] = 'TwoDimensionSpatialCoordinate'

#create an AIM ImageAnnotation template - person subtree
person = etree.SubElement(ImageAnnotation,'person')
Person = etree.SubElement(person, 'Person')
Person.attrib['cagridId'] = '0'
Person.attrib['id'] = 'NIF'
Person.attrib['name'] = '265034'

#create an element tree from ImageAnnotation
aimTree = etree.ElementTree(ImageAnnotation)


from dicom import *

dcmFile = 'xaal_to_a152_023.dcm'

# load
dcm = ReadFile(dcmFile)
data = dcm.pixel_array
for i in range(109):
    for j in range(91):
        if data[i,j] > 0:
            print i, j, data[i,j]

def voxelIter(img, id):
    data = []
    for i in range(91):
        for j in range(108):
            for k in range(91):
                if img[i,j,k] == id:
                    data.append((i,j,k,img[i,j,k]))
    return data

#
def voxelsByLabel(aalArray, aalID, fmriArray):
    '''atlas is a NiBabel 3D array in MNI space. aalID is an integer 1-116 corresponding to a brain structure'''
    data = [] #list that stores 5 items... (x,y,z coordinates, aalID, and zScore)
    for x in range(aalArray.shape[0]):
        for y in range(aalArray.shape[1]):
            for z in range(aalArray.shape[2]):
                if aalArray[x,y,z] == aalID: #only append coordinates for specific aalIDs
                    data.append((x, y, z, aalArray[x,y,z], fmriArray[x,y,z]))
    return data

