'''
Script for extracting "Placemark" (waypoint) coordinates from KML files
and writing coordinates to file of specified format for use with robot.

KML files shall be of the form:
+ root
    + Document
        + Placemark
            + Point
                + coordinates
                    - longitude,latitude,altitude
'''
import csv
import json
import xml.etree.ElementTree as ETree

XML_NAMESPACE = 'http://www.opengis.net/kml/2.2'
PLACEMARK_TAG = 'Placemark'
POINT_TAG = 'Point'
COORDINATE_TAG = 'coordinates'


def extract_placemark_coords(kml_file, ret_data):
    '''
    Extracts placemark coordinates, if present, from KML file

    :param kml_file: KML file to parse
    :param ret_data: List for storing extracted coordinates
    :returns: Coordinates in list of lists [longitude, latitude]
    '''
    # Construct tags with namespace element
    ns_placement_tag = '{%s}%s' % (XML_NAMESPACE, PLACEMARK_TAG)
    ns_point_tag = '{%s}%s' % (XML_NAMESPACE, POINT_TAG)
    ns_coordinate_tag = '{%s}%s' % (XML_NAMESPACE, COORDINATE_TAG)

    # Read the tree of XML elements into memory
    tree = ETree.parse(kml_file)

    # Iterate over all 'Placemark' tags
    # 'Placemark' tags are not direct children of 'root'
    root = tree.getroot()

    for placemark in root.iter(ns_placement_tag):
        # Check that there is a 'Point' child element
        point_element = placemark.find(ns_point_tag)
        if point_element is None:
            continue

        # Check that there is a 'coordinates' child element
        coord_element = point_element.find(ns_coordinate_tag)
        if coord_element is None:
            continue

        # Extract the coordinates and format
        coord_str = coord_element.text.strip()
        coord_arr = coord_str.split(',')

        # Remove the altitude reading at the end of array
        try:
            coord_arr.pop()
        except IndexError:
            # Something went wrong and coordinate array was empty
            continue

        # Add to coordinate list
        ret_data.append(coord_arr)


def write_csv(outfile_name, data):
    '''
    Writes the coordinates to a CSV file with format 'long,lat'.

    :param outfile_name: Name of output file
    :param data: List of lists of coordinates -> [long, lat]
    '''
    file_name = outfile_name + '.csv'

    # Use newline = '' as recommended in csv docs
    with open(file_name, 'w', newline='') as csv_file:
        # CSV writer defaults are sufficient
        writer = csv.writer(csv_file)

        # Write coordinates
        writer.writerows(data)


def write_json(outfile_name, data):
    '''
    Writes the coordinates to a JSON file with format:

    {
        "placemark": count,
        "longitude": value,
        "latitude": value
    }

    :param outfile_name: Name of output file
    :param data: List of lists of coordinates -> [long, lat]
    '''
    ROOT_FIELD = 'route'

    file_name = outfile_name + '.json'
    count = 0

    # Construct JSON format to write to file
    json_data = {}
    json_data[ROOT_FIELD] = []
    name_field = PLACEMARK_TAG.lower()

    for coord in data:
        count += 1

        json_data[ROOT_FIELD].append({
            name_field: count,
            'longitude': coord[0],
            'latitude': coord[1]
        })

    # Write JSON to file. Use indent=4 to make it look pretty.
    with open(file_name, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def write_xml(outfile_name, data):
    '''
    Writes the coordinates to an XML file with format:

    <Placemark>longitude,latitude<\\Placemark>

    :param outfile_name: Name of output file
    :param data: List of lists of coordinates -> [long, lat]
    '''
    ROOT_TAG = 'Route'

    file_name = outfile_name + '.xml'

    # Construct the XML structure
    root = ETree.Element(ROOT_TAG)

    for coord in data:
        value_str = ','.join(c for c in coord)
        ETree.SubElement(root, PLACEMARK_TAG).text = value_str

    # Create XML tree and write to file
    tree = ETree.ElementTree(root)
    tree.write(file_name)


if __name__ == '__main__':
    import argparse
    import os.path as op

    parser = argparse.ArgumentParser()

    # Add required positional argument for passing kml file and outfile name
    parser.add_argument('infile', type=str,
                        help='KML file to extract \'Placemark\' data from')
    parser.add_argument('outfile_name', type=str,
                        help='Name for output file')

    # Add optional conversion type flag arguments
    # Only one of these flags may be specified at a time
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-c', '--csv', action='store_true',
                       help='Store extracted data in CSV format (default)')
    group.add_argument('-j', '--json', action='store_true',
                       help='Store extracted data in JSON format')
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
        exit(1)

    if file_ext not in valid_extensions:
        # File does not have appropriate extension
        print('\'.%s\' is not a valid file extension' % file_ext)

        ext_str = ', '.join(ext for ext in valid_extensions)
        print('Valid extensions: %s' % ext_str)
        exit(1)

    # Get the placemark coordinates in a list of lists [long, lat]
    extracted_coords = []
    extract_placemark_coords(args.infile, extracted_coords)

    if len(extracted_coords) == 0:
        print('KML file \'%s\' contained no \'Placemark\' coordinates'
              % args.infile)
        exit(1)

    # Write out coordinates to the appropriate file format
    # CSV is the default format
    if args.json:
        write_json(args.outfile_name, extracted_coords)

    elif args.xml:
        write_xml(args.outfile_name, extracted_coords)

    else:
        write_csv(args.outfile_name, extracted_coords)
