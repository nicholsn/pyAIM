#!/usr/local/bin/python

__author__ = 'Nolan Nichols'

#module to parse xml
from lxml import etree
#module to work with NIfTi images
import nibabel as nb
#module to work with rdf mapping between AAL and FMAIDs
from rdflib import ConjunctiveGraph as Graph

#open the aal atlas as a single analyze volume in MNI152 space with integers from 1 - 116 for anatomy labels
aal = nb.load('aal2mni152.img')
aalArray = aal.get_data()

#open a fMRI zScore map for a single participant that is already in MNI space
fmri = nb.load('000640456777_visit2_zstat1.nii')
fmriArray = fmri.get_data()

#return a list of inputs to configure aimInstance based on anatomical entity (i.e., aalID)
def voxelsByLabel(aalArray, fmriArray, thresh):
    '''atlas is a NiBabel 3D array in MNI space. aalID is an integer 1-116 corresponding to a brain structure'''
    data = [] #list that stores 5 items... (x,y,z coordinates, aalID, and zScore)
    for x in range(aalArray.shape[0]):
        for y in range(aalArray.shape[1]):
            for z in range(aalArray.shape[2]):
                if float(aalArray[x,y,z]) != 0.0 and float(fmriArray[x,y,z] >= thresh): #only append coordinates for specific aalIDs
                    data.append((x, y, z, aalArray[x,y,z], fmriArray[x,y,z]))
    return sorted(data, key = lambda aal: data[3])

#return an AIM instance based on the required coordinates, labels, and statistics
def aimInstance(x, y, z, fmaid, aalLabel, zScore, cagridId):
    ''' '''
    #Global variables for AIM template
    XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'
    XSI_TYPE = '{%s}type' % XSI_NS
    #create an AIM ImageAnnotation template, ImageAnnotation sub-tree w/attributes
    ImageAnnotation = etree.Element('ImageAnnotation')
    ImageAnnotation.attrib['aimVersion'] = '3.0'
    ImageAnnotation.attrib['cagridId'] = cagridId
    ImageAnnotation.attrib['codeMeaning'] = 'fMRI brain data'
    ImageAnnotation.attrib['codeValue'] = 'PIXEL DATA'
    ImageAnnotation.attrib['codingSchemeDesignator'] = 'PIXELDATA'
    ImageAnnotation.attrib['dateTime'] = ''
    ImageAnnotation.attrib['name'] = 'Example AIM file'
    ImageAnnotation.attrib['uniqueIdentifier'] = '1.3.6.1.4.1.25403.1095730355278.5896.20101123034021.3'
    #configure namespaces
    schemaLocation = '{%s}schemaLocation' % XSI_NS
    ImageAnnotation.attrib[schemaLocation] = 'gme://caCORE.caCORE/3.2/edu.northwestern.radiology.AIM AIM_v3_rv11_XML.xsd'
    #create an AIM ImageAnnotation template - calculationCollection sub-tree w/attributes
    calculationCollection = etree.SubElement(ImageAnnotation, 'calculationCollection')
    Calculation = etree.SubElement(calculationCollection, 'Calculation')
    Calculation.attrib['cagridId'] = cagridId
    Calculation.attrib['codeMeaning'] = 'Z Score'
    Calculation.attrib['codeValue'] = 'ZSCORE'
    Calculation.attrib['codingSchemeDesignator'] = 'FMRI'
    Calculation.attrib['description'] = 'Z Score'
    Calculation.attrib['uid'] = '1.3.6.1.4.1.25403.1095730355278.5896.20101123034021.1'
    #create an AIM ImageAnnotation template - referencedCalculationCollection *UNUSED*
    referencedCalculationCollection = etree.SubElement(Calculation, 'referencedCalculationCollection')
    #create an AIM ImageAnnotation template - calculationResultCollection sub-tree w/attributes
    calculationResultCollection = etree.SubElement(Calculation, 'calculationResultCollection')
    CalculationResult = etree.SubElement(calculationResultCollection, 'CalculationResult')
    CalculationResult.attrib['cagridId'] = cagridId
    CalculationResult.attrib['numberOfDimensions'] = '1'
    CalculationResult.attrib['type'] = 'Scalar'
    CalculationResult.attrib['unitOfMeasure'] = 'Zscore'
    calculationDataCollection = etree.SubElement(CalculationResult, 'calculationDataCollection')
    CalculationData = etree.SubElement(calculationDataCollection, 'CalculationData')
    CalculationData.attrib['cagridId'] = cagridId
    CalculationData.attrib['value'] = zScore.__str__() # fMRI z-score goes for a single coordinate
    #create an AIM ImageAnnotation template - coordinateCollection sub-tree w/attributes
    coordinateCollection = etree.SubElement(CalculationData,'coordinateCollection')
    Coordinate = etree.SubElement(coordinateCollection, 'Coordinate')
    Coordinate.attrib['cagridId'] = cagridId
    Coordinate.attrib['dimensionIndex'] = '0'
    Coordinate.attrib['position'] = '0'
    #create an AIM ImageAnnotation template - dimensionCollection sub-tree w/attributes
    dimensionCollection = etree.SubElement(CalculationResult,'dimensionCollection')
    Dimension = etree.SubElement(dimensionCollection, 'Dimension')
    Dimension.attrib['cagridId'] = cagridId
    Dimension.attrib['index'] = '0'
    Dimension.attrib['label'] = 'Value'
    Dimension.attrib['size'] = '1'
    #create an AIM ImageAnnotation template - user sub-tree w/attributes
    user = etree.SubElement(ImageAnnotation, 'user')
    User = etree.SubElement(user, 'User')
    User.attrib['cagridId'] = cagridId
    User.attrib['loginName'] = 'TEST'
    User.attrib['name'] = 'TEST'
    User.attrib['numberWithinRoleOfClinicalTrial'] = '2'
    User.attrib['roleInTrial'] = 'N/A'
    #create an AIM ImageAnnotation template - equipment sub-tree w/attributes
    equipment = etree.SubElement(ImageAnnotation, 'equipment')
    Equipment = etree.SubElement(equipment, 'Equipment')
    Equipment.attrib['cagridId'] = cagridId
    Equipment.attrib['manufacturerModelName'] = 'N/A'
    Equipment.attrib['manufacturerName'] = 'University'
    Equipment.attrib['softwareVersion'] = '3.0.0.0'
    #create an AIM ImageAnnotation template - anatomicEntityCollection sub-tree w/attributes
    anatomicEntityCollection = etree.SubElement(ImageAnnotation, 'anatomicEntityCollection')
    AnatomicEntity = etree.SubElement(anatomicEntityCollection, 'AnatomicEntity')
    AnatomicEntity.attrib['annotatorConfidence'] = '1'
    AnatomicEntity.attrib['cagridId'] = cagridId
    AnatomicEntity.attrib['codeMeaning'] = aalLabel #this info exists outside of atlas
    AnatomicEntity.attrib['codeValue'] = fmaid #changed from RID
    AnatomicEntity.attrib['codingSchemeDesignator'] = 'FMAID' #change to AAL or FMA
    AnatomicEntity.attrib['isPresent'] = 'True'
    AnatomicEntity.attrib['label'] = 'Pixel in %s' % aalLabel #should be 'Pixel in '+ %s codeMeaning
    #create an AIM ImageAnnotation template - imageReferenceCollection sub-tree w/attributes
    imageReferenceCollection = etree.SubElement(ImageAnnotation, 'imageReferenceCollection')
    ImageReference = etree.SubElement(imageReferenceCollection,'ImageReference')
    ImageReference.attrib['cagridId'] = cagridId
    ImageReference.attrib[XSI_TYPE] = 'DICOMImageReference'
    #create an AIM ImageAnnotation template - imageStudy sub-tree w/attributes
    imageStudy = etree.SubElement(ImageReference, 'imageStudy')
    ImageStudy = etree.SubElement(imageStudy, 'ImageStudy')
    ImageStudy.attrib['cagridId'] = cagridId
    ImageStudy.attrib['instanceUID'] = '1.3.6.1.4.1.9328.50.45.326662079066250663678557696078244480878'
    ImageStudy.attrib['startDate'] = '1887-11-19T00:00:00'
    ImageStudy.attrib['startTime'] = '000000'
    #create an AIM ImageAnnotation template - imageSeries sub-tree w/attributes
    imageSeries = etree.SubElement(ImageStudy,'imageSeries')
    ImageSeries = etree.SubElement(imageSeries, 'ImageSeries')
    ImageSeries.attrib['cagridId'] = cagridId
    ImageSeries.attrib['instanceUID'] = '1.3.6.1.4.1.9328.50.45.157809556490045867232259259088691970356'
    #create an AIM ImageAnnotation template - imageCollection sub-tree w/attributes
    imageCollection = etree.SubElement(ImageSeries, 'imageCollection')
    Image = etree.SubElement(imageCollection, 'Image')
    Image.attrib['cagridId'] = cagridId
    Image.attrib['sopClassUID'] = '1.2.840.10008.5.1.4.1.1.4'
    Image.attrib['sopInstanceUID'] = '1.3.6.1.4.1.9328.50.45.165186936095437264663872068604057093662'
    #create an AIM ImageAnnotation template - geometricShapeCollection sub-tree w/attributes
    geometricShapeCollection = etree.SubElement(ImageAnnotation, 'geometricShapeCollection')
    GeometricShape = etree.SubElement(geometricShapeCollection, 'GeometricShape')
    GeometricShape.attrib['cagridId'] = cagridId
    GeometricShape.attrib['includeFlag'] = 'true'
    GeometricShape.attrib['shapeIdentifier'] = '0'
    GeometricShape.attrib[XSI_TYPE] = 'Point'
    #create an AIM ImageAnnotation template - spatialCoordinateCollection sub-tree w/attributes
    spatialCoordinateCollection = etree.SubElement(GeometricShape, 'spatialCoordinateCollection')
    SpatialCoordinate = etree.SubElement(spatialCoordinateCollection, 'SpatialCoordinate')
    SpatialCoordinate.attrib['cagridId'] = cagridId
    SpatialCoordinate.attrib['coordinateIndex'] = '0'
    SpatialCoordinate.attrib['imageReferenceUID'] = '1.3.6.1.4.1.9328.50.45.165186936095437264663872068604057093662'
    SpatialCoordinate.attrib['referencedFrameNumber'] = '1'
    SpatialCoordinate.attrib['x'] = x.__str__()
    SpatialCoordinate.attrib['y'] = y.__str__()
    SpatialCoordinate.attrib['z'] = z.__str__()
    SpatialCoordinate.attrib[XSI_TYPE] = 'ThreeDimensionSpatialCoordinate' #updated for 3D
    #create an AIM ImageAnnotation template - person sub-tree w/attributes
    person = etree.SubElement(ImageAnnotation,'person')
    Person = etree.SubElement(person, 'Person')
    Person.attrib['cagridId'] = cagridId
    Person.attrib['id'] = 'NIF'
    Person.attrib['name'] = '265034'
    return ImageAnnotation

#create a root AIM element for ImageAnnotations returned by aimInstance
AIM_ROOT = etree.Element('AIM-ROOT')

#read in rdf graph that maps AAL IDs and FMAIDs
fmaGraph = Graph()
fmaGraph.parse('AAL-FMA-Mapping.rdf')

#parse rdf into list
def fma2List(fmaGraph):
    fmaList = list()
    for s,p,o in fmaGraph:
        fmaList.append((str(s),str(p),str(o)))
    return sorted(fmaList) #sorting ensures correct indexing of aalIDs, fmaids, labels, etc in aalDict.

fmaList = fma2List(fmaGraph) #fmaList contains the aalID, FMAID, and AAL_Label

#organize fmaList into nested sets
def list2Nested(fmaList):
    aalList = list()
    while fmaList != []:
        tempList = list()
        for i in range(3):
            tempList.append(fmaList.pop())
        aalList.append((tempList[0][2],tempList[1][2],tempList[2][2]))
    return aalList

aalList = list2Nested(fmaList) #aalList is an organized tuple, mapping between aal and fma

#index the aal2Fma mapping as a dict keyed on the aalIDs for searching by aalID
def aalMap(aalList):
    aalDict = dict()
    for i in range(len(aalList)):
        aalTemp = aalList.pop()
        aalDict[aalTemp[2]] = list((aalTemp[1],aalTemp[0]))
    return aalDict

aalDict = aalMap(aalList) #aalDict is keyed on aalID

#currently configures the label to use for accessing coordinates
aalID = 72 #need to pass this as a list of aalIDs to generate AIMS for, possibly a vSparQL query of connectivity

#create the lookup table for coordinates, aalIDs, and zScores using voxelsByLabel
print 'Reading voxel by voxel labels and z-scores...'
lookup = voxelsByLabel(aalArray, fmriArray)
print 'Done!'

#iterate through voxelsByLabel using the lookup indices as input to configure AIM instance
print 'Building AIM xml file...'
while lookup != []:
    record = lookup.pop()
    x = record[0]
    y = record[1]
    z = record[2]
    aalID = record[3]
    fmaid = aalDict[str(aalID)][0] #mapping between aalID and fmaid
    aalLabel = aalDict[str(aalID)][1]
    zScore = record[4]
    cagridId = '%s-%s-%s' % (x,y,z)
    ImageAnnotation = aimInstance(x, y, z, fmaid, aalLabel, zScore, cagridId)
    AIM_ROOT.append(ImageAnnotation)

#create an element tree from AIM_ROOT returned from aimInstance and write the AIM file
aimTree = etree.ElementTree(AIM_ROOT)
print 'Writing demo AIM file for all Brain Labels'
aimTree.write('scratch/AIM-Whole-Brain.xml')
print 'Done!'