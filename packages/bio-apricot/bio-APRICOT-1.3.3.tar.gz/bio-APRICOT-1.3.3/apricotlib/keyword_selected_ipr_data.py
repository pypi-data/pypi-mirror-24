#!/usr/bin/env python
# Description = selects domains from interpro database


class RnaRelatedDomainSelection(object):
    '''classification of data'''
    def __init__(self, keywords_file,
                 ipr_whole_data_file,
                 interpro_mapped_cdd,
                 domain_data_path):
        self._keywords_file = keywords_file
        self._ipr_whole_data_file = ipr_whole_data_file
        self._interpro_mapped_cdd = interpro_mapped_cdd
        self._domain_data_path = domain_data_path
        
        self.ipr_whole_data_list = []
        self._ipr_dict = {}
        self._mapped_interpro_length = {}
        
    def read_keyword_file(self):
        '''reads user provided keywords for domain selection'''
        self.keyword_list = [rna_keyword.strip()
                             for rna_keyword in open(
                                self._keywords_file)]
        return self.keyword_list
    
    def read_interpro_mapped_cdd_file(self):
        '''Parses cdd interpro mapped file for
        the extraction of common information'''
        with open(self._interpro_mapped_cdd, 'r') as in_fh:
            for entry in in_fh:
                cdd_member = entry.split('\t')[3]
                domain_length = entry.split('\t')[4].strip()
                self._mapped_interpro_length[cdd_member] = domain_length
        self._mapped_interpro_length
        
    def read_ipr_whole_data_file(self):
        '''Parses CDD annotation data from table'''
        with open(self._ipr_whole_data_file, 'r') as in_fh:
            for ipr_id_entry in in_fh:
                self.ipr_whole_data_list.append(ipr_id_entry.strip())
                self._ipr_dict[ipr_id_entry.strip()] = ipr_id_entry.strip(
                    ).split('\t')[2]
        return self.ipr_whole_data_list, self._ipr_dict
        
    def create_keyword_selected_domain_file(self):
        '''Creates a file with CDD derived domain of interest'''
        self._keyword_annotation_dict = {}
        self._keyword_selected_domain = []
        for ipr_entry in self.ipr_whole_data_list:
            for keyword in self.keyword_list:
                if ' ' in keyword:
                    key_list = []
                    for each_key in keyword.split(' '):
                        key_list.append(each_key)
                    match = re.search(r'\b%s*|\W%s\b'%(key_list[0].lower(),
                                                       key_list[1].lower()),
                                      self._ipr_dict[ipr_entry])
                    if match:
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(ipr_entry)
                else:
                    match = re.search(r'\b%s\b' % keyword, self._ipr_dict[
                        ipr_entry])
                    if match:
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(ipr_entry)
        for fkeyword in self.keyword_list:
            fkeyword = fkeyword.replace(' ', '_')
            with open(self._domain_data_path +'/' +
                      fkeyword+'_related_ipr_ids.tab', 'w') as key_fh:
                if self._keyword_annotation_dict.get(fkeyword):
                    for each_entry in self._keyword_annotation_dict[fkeyword]:
                        each_entry = each_entry.replace(each_entry.split(
                            '\t')[3], " ".join(each_entry.split('\t')[3].split(
                            ))).replace(';', ',')
                        cdd_id = each_entry.split('\t')[1]
                        if cdd_id in set(self._mapped_interpro_length.keys()):
                            length = self._mapped_interpro_length[cdd_id]
                        else:
                            length = 'NA'
                        self._keyword_selected_domain.append("%s\t%s" % (
                            each_entry, length))
                        key_fh.write("%s\t%s\n" % (each_entry, length))
        uniq_keyword_selected_domains = list(
            set(self._keyword_selected_domain))
        with open(self._domain_data_path+'/all_keyword_selected_ipr_data.tab',
                  'w') as keyword_selected_domain_file:
            for domain_entry in uniq_keyword_selected_domains:
                keyword_selected_domain_file.write(
                    '%s\n' % str(domain_entry))
