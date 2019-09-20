'''
Script for extracting "Placemark" (waypoint) coordinates from KML files
and writing coordinates to file of specified format

KML files shall be of the form:
root
    + Document
        + Placemark
            + Point
                + coordinates
                    - longitude,latitude,altitude
'''
import xml.etree.ElementTree as ETree

XML_NAMESPACE = 'http://www.opengis.net/kml/2.2'


def extract_placemark_coords(kml_file, ret_data):
    '''
    Extracts placemark coordinates from XML file if present

    :param kml_file: KML file to parse
    :param ret_data: List for storing extracted coordinates
    :returns: Coordinates in list of tuples (longitude, latitude)
    '''
    PLACEMARK_TAG = '{%s}Placemark' % XML_NAMESPACE
    POINT_TAG = '{%s}Point' % XML_NAMESPACE
    COORDINATE_TAG = '{%s}coordinates' % XML_NAMESPACE
    LONG_INDEX = 0
    LAT_INDEX = 1

    # Read the tree of XML elements into memory
    tree = ETree.parse(kml_file)

    # Iterate over all 'Placemark' tags
    # 'Placemark' tags are not direct children of 'root'
    root = tree.getroot()

    for placemark in root.iter(PLACEMARK_TAG):
        # Check that there is a 'Point' child element
        point_element = placemark.find(POINT_TAG)
        if point_element is None:
            continue

        # Check to make sure 'coordinates' child element exists
        coord_element = point_element.find(COORDINATE_TAG)
        if coord_element is None:
            continue

        # Extract the coordinates and format
        coord_str = coord_element.text.strip()
        coord_arr = coord_str.split(',')
        coord_tup = (coord_arr[LONG_INDEX].strip(),
                     coord_arr[LAT_INDEX].strip())

        # Add to coordinate list
        ret_data.append(coord_tup)


if __name__ == '__main__':
    import argparse
    import os.path as op

    parser = argparse.ArgumentParser()

    # Add required positional argument for passing kml file
    parser.add_argument('infile', type=str,
                        help='KML file to extract \'Placemark\' data from')
    parser.add_argument('outfile_name', type=str,
                        help='Name for output file')

    # Add optional conversion type flag arguments
    # Only one of these flags may be specified at a time
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-c', '--csv', action='store_true', default=True,
                       help='Store extracted data in CSV format (default)')
    group.add_argument('-i', '--ini', action='store_true',
                       help='Store extracted data in INI format')
    group.add_argument('-x', '--xml', action='store_true',
                       help='Store extracted data in XML format')

    # Parse the passed arguments
    args = parser.parse_args()

    # Error check arguments
    valid_extensions = ['kml']
    file_ext = args.infile.split('.')[-1]

    if not op.isfile(args.infile):
        # File does not exist
        print('File \'%s\' does not exist.' % args.infile)

    elif file_ext not in valid_extensions:
        # File does not have appropriate extension
        print('\'.%s\' is not a valid file extension' % file_ext)

        ext_str = ', '.join(ext for ext in valid_extensions)
        print('Valid extensions: %s' % ext_str)

    # Get the placemark coordinates in list of tuples (long, lat)
    extracted_data = []
    extract_placemark_coords(args.infile, extracted_data)

    print(extracted_data)
