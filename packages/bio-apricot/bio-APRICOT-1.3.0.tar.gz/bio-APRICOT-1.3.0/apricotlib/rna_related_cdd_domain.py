#!/usr/bin/env python
# Description = RNA related CDD domain

import re


class RnaRelatedCDDSelection(object):
    '''classification of data'''
    def __init__(self, keywords_file,
                 cdd_whole_data_file,
                 interpro_mapped_cdd,
                 domain_data_path):
        self._keywords_file = keywords_file
        self._cdd_whole_data_file = cdd_whole_data_file
        self._interpro_mapped_cdd = interpro_mapped_cdd
        self._domain_data_path = domain_data_path
        
        self.cdd_whole_data_list = []
        self._cdd_dict = {}
        self._mapped_cdd_members = {}
    
    def select_cdd_domains(self):
        ''''''
        self.read_keyword_file()
        self.read_interpro_mapped_cdd_file()
        self.read_cdd_whole_data_file()
        self.create_rna_related_domain_file()
        
    def read_keyword_file(self):
        '''reads keywords for domain selection'''
        self._keyword_list = [rna_keyword.strip()
                              for rna_keyword in open(
                                self._keywords_file, 'r')]
        return self._keyword_list
    
    def read_interpro_mapped_cdd_file(self):
        '''Parses interpro cdd mapped file to extract common information'''
        with open(self._interpro_mapped_cdd, 'r') as in_fh:
            for entry in in_fh:
                ipr_id = entry.strip().split('\t')[0]
                ipr_members = entry.strip().split('\t')[1]
                cdd_id = entry.strip().split('\t')[2]
                cdd_member = entry.strip().split('\t')[3]
                domain_length = entry.strip().split('\t')[4]
                self._mapped_cdd_members[cdd_member] = ipr_members
        self._mapped_cdd_members
    
    def read_cdd_whole_data_file(self):
        '''Parses CDD annotation data from table'''
        with open(self._cdd_whole_data_file, 'r') as cdd_data_fh:
            for cdd_entry in cdd_data_fh:
                if 'smart' in cdd_entry.split('\t')[1]:
                    cdd_entry = cdd_entry.replace(
                        cdd_entry.split('\t')[1], 'SM'+cdd_entry.split(
                            '\t')[1].split('smart')[-1])
                elif 'pfam' in cdd_entry.split('\t')[1]:
                    cdd_entry = cdd_entry.replace(
                        cdd_entry.split('\t')[1], 'PF'+cdd_entry.split(
                            '\t')[1].split('pfam')[-1])
                cdd_domain = cdd_entry.split('\t')[1]
                if cdd_domain in self._mapped_cdd_members.keys():
                    members = self._mapped_cdd_members[cdd_domain]
                else:
                    members = 'NA'
                self.cdd_whole_data_list.append(
                    cdd_entry.strip())
                self._cdd_dict[cdd_entry.strip()] = cdd_entry.strip(
                    ).split('\t')[3]
        return self.cdd_whole_data_list, self._cdd_dict
    
    def create_rna_related_domain_file(self):
        '''Creates RNA related domain list'''
        self._keyword_annotation_dict = {}
        self._rna_related_domain = []
        for cdd_entry in self.cdd_whole_data_list:
            for keyword in self._keyword_list:
                if ' ' in keyword:
                    key_list = []
                    for each_key in keyword.split(' '):
                        key_list.append(each_key)
                    match = re.search(r'\b%s*|\W%s\b'%(key_list[0].lower(),
                                                       key_list[1].lower()),
                                      self._cdd_dict[cdd_entry])
                    if match:
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(cdd_entry)
                else:
                    match = re.search(r'\b%s\b'%keyword, self._cdd_dict[cdd_entry])
                    if match:
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(cdd_entry)
                        
        for fkeyword in self._keyword_list:
            fkeyword = fkeyword.replace(' ', '_')
            with open(self._domain_data_path+'/'+fkeyword+'_related_cdd_ids.tab',
                      'w') as keyword_specific_domain:
                if self._keyword_annotation_dict.get(fkeyword):
                    for each_entry in self._keyword_annotation_dict[fkeyword]:
                        each_entry = each_entry.replace(
                            each_entry.split('\t')[3], " ".join(
                                each_entry.split('\t')[3].split())).replace(';', ',')
                        cdd_domain = each_entry.split('\t')[1]
                        if cdd_domain in set(self._mapped_cdd_members.keys()):
                            members = self._mapped_cdd_members[cdd_domain]
                        else:
                            members = 'NA'
                        keyword_specific_domain.write('%s\t%s\t%s\n'%(
                            '\t'.join(each_entry.split('\t')[0:-1]), members,
                            each_entry.split('\t')[-1]))
                        self._rna_related_domain.append(('%s\t%s\t%s'%(
                            '\t'.join(each_entry.split('\t')[0:-1]), members,
                            each_entry.split('\t')[-1])))
            
        uniq_rna_related_domains = list(set(self._rna_related_domain))
        with open(self._domain_data_path+'/all_rna_related_cdd_data.tab',
                  'w') as rna_related_domain_file:
            for domain_entry in uniq_rna_related_domains:
                rna_related_domain_file.write('%s\n'%str(domain_entry))
