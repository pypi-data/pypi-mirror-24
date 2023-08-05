#!/usr/bin/env python
# Description = Compiles InterProScan data from XML files to table

import sys

try:
    import xml.etree.ElementTree as ET
except ImportError:
    print('Python package xmlis missing. Please install/update.')
    sys.exit(0)
import re

interpro_analysis_path = sys.argv[1]
interpro_xml = sys.argv[2]

interproid = open(
    interpro_analysis_path+'/interproid.tbl', 'w')
only_id_ipr_xml = open(
    interpro_analysis_path+'/only_id_ipr_xml.txt', 'w')
ipr_data_removed = open(
    interpro_analysis_path+'/ipr_data_removed.txt', 'w')

tree = ET.parse(interpro_xml)
root = tree.getroot()

for data in root.findall('interpro'):
    abstract_list = []
    member_db_list = []
    
    ipr_id = data.attrib.get('id')
    name = data.find('name').text
    only_id_ipr_xml.write('%s\t%s\n' % (ipr_id, name))
    
    member_list = data.findall('./member_list/*')
    external_doc = data.findall('./external_doc_list/*')
    db_list = [member_list, external_doc]
    for db_data in db_list:
        for db_elem in db_data:
            member_db_list.append(
                db_elem.attrib.get('dbkey'))
    whole_external_members = "|".join(
        sorted(list(set(member_db_list))))
    main_abstract = data.find('abstract').text
    abstract_list.append(main_abstract.replace(
        '\n', ' ').replace('[', ''))
    abstract_data = data.findall('./abstract/*')
    for abs_elem in abstract_data:
        abs_unordered = ET.tostring(abs_elem).strip()
        abs_ordered = str(abs_unordered).replace(
            "b'<p>", "").replace("</p>'", "")
        for each_abs_elem in abs_ordered.split('\n'):
            try:
                abs_list_elt = re.sub(
                '<[A-Za-z\/][^>]*>', '', each_abs_elem).replace(
                "\\n", "").replace("'b'.", "").replace(
                    "]", "").replace("[", "").replace(
                    "b')", "").replace("b'", "").replace(
                "'", "").replace(" ,", " ").replace(
                "()", "").replace(" .", ".").replace(",,", "")
                if len(abs_list_elt) > 2:
                    abstract_list.append(abs_list_elt)
            except AttributeError:
                pass
    full_abstract = (''.join(abstract_list))
    whole_abstract = re.sub(r'\s+', ' ', full_abstract)
    for external_members in member_db_list:
        try:
            interproid.write('\t'.join([ipr_id, external_members,
                          name, whole_abstract,
                          whole_external_members])+'\n')
        except UnicodeEncodeError:
            interproid.write('\t'.join([ipr_id, external_members,
                          name, repr(whole_abstract),
                          whole_external_members])+'\n')
        
    
for deleted_data in root.findall('deleted_entries'):
    for ipr_id_info in deleted_data:
        ipr_id = ipr_id_info.attrib.get('id').strip()
        ipr_data_removed.write('%s\n'%ipr_id)
ipr_data_removed.close()
only_id_ipr_xml.close()
interproid.close()
