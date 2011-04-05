__author__ = 'nolan'

#add missing tags
#dcm.AddNew( (0002,0002), 'UI', '1.2.840.10008.5.1.4.1.1.66.4')

# write_new.py
"""Simple example of writing a DICOM file from scratch using pydicom.

This example does not produce a DICOM standards compliant file as written,
you will have to change UIDs to valid values and add all required DICOM data
elements
"""
# Copyright (c) 2010 Darcy Mason
# This file is part of pydicom, released under a modified MIT license.
#    See the file license.txt included with this distribution, also
#    available at http://pydicom.googlecode.com
import sys
import os.path
import dicom
from dicom.dataset import Dataset, FileDataset
import dicom.UID

if __name__ == "__main__":
    print "---------------------------- "
    print "write_new.py example program"
    print "----------------------------"
    print "Demonstration of writing a DICOM file using pydicom"
    print "NOTE: this is only a demo. Writing a DICOM standards compliant file"
    print "would require official UIDs, and checking the DICOM standard to ensure"
    print "that all required data elements were present."
    print

    if sys.platform.lower().startswith("win"):
        filename = r"c:\temp\test.dcm"
        filename2 = r"c:\temp\test-explBig.dcm"
    else:
        homedir = os.path.expanduser("~")
        filename = os.path.join(homedir + "/Documents/UW/GrantApps/Neuroimaging-Ontology/nii2dcm", "test.dcm")
        filename2 = os.path.join(homedir+"/Documents/UW/GrantApps/Neuroimaging-Ontology/nii2dcm", "test-explBig.dcm")

    print "Setting file meta information..."
    # Populate required values for file meta information
        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.66.4' # Segmentation SOP Class
        file_meta.MediaStorageSOPInstanceUID = "1.2.840.10008.5.1.4.1.1.66.4" # !! Need valid UID here for real work
        file_meta.ImplementationClassUID = "1.2.840.10008.5.1.4.1.1.66.4" # !!! Need valid UIDs here

        # Required for Segmentation IOD
        file_meta.Modality = 'SEG'
        file_meta.SeriesNumber = '001'
        file_meta.ImageType = '1' # Derived = 1, Primary = 2
        file_meta.SamplesPerPixel = '1'
        file_meta.PhotometricInterpretation = 'MONOCHROME2'
        file_meta.PixelRepresentation = 0
        file_meta.BitsAllocated = 8 # Binary = 1
        file_meta.BitsStored = 8 # Binary = 1
        file_meta.HighBit = 7 # Binary = 0
        file_meta.SegmentationType = 'FRACTIONAL' #FRACTIONAL or BINARY
        file_meta.SegmentationFractionalType = 'OCCUPANCY' #Can be OCCUPANCY or PROBABILITY
        file_meta.MaximumFractionalValue = 116 # 116 is the number of labels in AAL
        file_meta.SegmentSequence = 'AAL' # List of segments?
        file_meta.SegmentNumber = 1 #Number identifying the segment



    print "Setting dataset values..."

    # Create the FileDataset instance (initially no data elements, but file_meta supplied)
    ds = FileDataset(filename, {}, file_meta=file_meta, preamble="\0"*128)

    # Add the data elements -- not trying to set all required here. Check DICOM standard
    ds.PatientsName = "Test^Firstname"
    ds.PatientID = "123456"

    # Populate required values for file meta information
    ds.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.66.4' # Segmentation SOP Class
    ds.MediaStorageSOPInstanceUID = "1.2.840.10008.5.1.4.1.1.66.4" # !! Need valid UID here for real work
    ds.ImplementationClassUID = "1.2.840.10008.5.1.4.1.1.66.4" # !!! Need valid UIDs here

    # Required for Segmentation IOD
    ds.Modality = 'SEG'
    ds.SeriesNumber = '001'
    ds.ImageType = '1' # Derived = 1, Primary = 2

    #Set image parameters
    ds.SpacingBetweenSlices = '2.0'
    ds.ImageOrientationPatient = ['-1', '0', '0', '0', '-1', '0']
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = 'MONOCHROME2'
    ds.Rows = 109
    ds.Columns = 91
    ds.PixelSpacing = ['-2.0', '2.0']
    ds.BitsAllocated = 8 # Binary = 1
    ds.BitsStored = 8 # Binary = 1
    ds.HighBit = 7 # Binary = 0
    ds.SegmentationType = 'FRACTIONAL' #FRACTIONAL or BINARY
    ds.SegmentationFractionalType = 'OCCUPANCY' #Can be OCCUPANCY or PROBABILITY
    ds.MaximumFractionalValue = 116 # 116 is the number of labels in AAL
    ds.PixelRepresentation = 1
    

    # Set the transfer syntax
    ds.is_little_endian = True
    ds.is_implicit_VR = True

    print "Writing test file", filename
    ds.save_as(filename)
    print "File saved."

    # Write as a different transfer syntax
    ds.file_meta.TransferSyntaxUID = dicom.UID.ExplicitVRBigEndian #XXX shouldn't need this but pydicom 0.9.5 bug not recognizing transfer syntax
    ds.is_little_endian = False
    ds.is_implicit_VR = False

    print "Writing test file as Big Endian Explicit VR", filename2
    ds.save_as(filename2)


