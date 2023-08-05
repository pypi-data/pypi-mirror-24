#!/usr/bin/env python
# description = "Identifies keyword selected domains from InterPro database."

import os
import sys

try:
    from urllib.request import urlopen
except ImportError:
    print('Python package urllib is missing. Please install/update.\n')
    sys.exit(0)
try:
    import xml.etree.ElementTree as ET
    XML_PARSE = '{http://uniprot.org/uniprot}'
except ImportError:
    print('Python package xml is missing. Please install/update.')
    sys.exit(0)


class CollectUniprotInformation(object):
    def __init__(self, query_to_uid, uniprot_xml_path,
                 uniprot_fasta_path, uniprot_feature_table):
        self._query_to_uid = query_to_uid
        self._uniprot_xml_path = uniprot_xml_path
        self._uniprot_fasta_path = uniprot_fasta_path
        self._uniprot_feature_table = uniprot_feature_table

    def create_feature_table(self):
        '''create feature files from uniprot xml'''
        self._new_xml_detail(
            self._uniprot_xml_path, self._uniprot_feature_table)
        print('Table containing features from xml file is created/updated.')
        
    def _get_uniprot_xml(self, uid, xml_path):
        ''''''
        xml_file = open(xml_path+'/'+uid+'.xml', 'w')
        xml_url = 'http://www.uniprot.org/uniprot/%s.xml'%uid
        response = urlopen(xml_url)
        html = str(response.read()).replace("b", '').replace("'", "")
        for entry in html.split('\\n'):
            if 'UTF-8' in entry:
                xml_file.write(str('<?xml version="1.0" encoding="UTF-8"?>\n'))
            else:
                xml_file.write("%s\n" % entry)
        xml_file.close()
        
    def _get_uniprot_fasta(self, uid, fasta_path):
        ''''''
        fasta_file = open(fasta_path+'/'+uid+'.fasta', 'w')
        fasta_url = 'http://www.uniprot.org/uniprot/%s.fasta'%uid
        response = urlopen(fasta_url)
        html = str(response.read()).replace("b", '').replace("'", "")
        for entry in html.split('\\n'):
            fasta_file.write("%s\n" % entry)
        fasta_file.close()
        
    def _new_xml_detail(self, query_xml_path, feature_table_tsv):
        '''Creates new feature file in result_path from
        all the xml files present in uniprot_xml_path'''
        
        with open(feature_table_tsv ,'w') as feature_table:
            feature_table.write("\t".join(['Entry', 'Name', 'Gene',
                                'Locus-tag', 'Organism',
                                'Pubmed-ID', 'EMBL-ID',
                                'RefSeq-ID', 'KEGG-ID',
                                'PDB-ID', 'GO', 'InterPro-ID',
                                'Pfam-ID', 'Existance-Type'])+'\n')
            for each_xml in os.listdir(query_xml_path):
                self._get_info_from_xml(query_xml_path+'/'+each_xml, feature_table)
                
    def _get_info_from_xml(self, each_xml, feature_table):
    
        '''stores info from each xml file'''
        tree = ET.parse(each_xml)
        for item in tree.getiterator(XML_PARSE+'uniprot'):
            protein_parse = item.findall(XML_PARSE+'entry')
            UPorganism = []
            for protein in protein_parse:
                self._get_xml_protein_feature(protein, feature_table)
                
    def _get_xml_protein_feature(self, protein, feature_table):
        '''get all the features'''
        info = []
        accession = self._get_accession(protein)#accession
        info.append(accession)
        name = self._get_name(protein) #name
        info.append(name)
        gene_name = self._get_genename(protein) #gene name
        info.append(gene_name)
        gene_locus_name = self._get_gene_locus_name(protein) 
        info.append(gene_locus_name)
        organism = self._get_organism(protein)#species
        info.append(organism)
        pubmed_id = self._get_pubmed_id(protein)
        info.append(pubmed_id)
        embl_id = self._get_embl_id(protein)
        info.append(embl_id)
        refseq_id = self._get_refseq_id(protein)
        info.append(refseq_id)
        kegg_id = self._get_kegg_id(protein)
        info.append(kegg_id)
        pdb_id = self._get_pdb_data(protein)
        info.append(pdb_id)
        go_data = self._get_go_data(protein)
        info.append(go_data)
        interpro_data = self._get_interpro_data(protein)
        info.append(interpro_data)
        pfam_data = self._get_pfam_data(protein)
        info.append(pfam_data)
        existance = self._get_existance_type(protein)
        info.append(existance)
        for eachinfo in info:
            feature_table.write("%s\t"%eachinfo)
        feature_table.write('\n')
            
    def _get_accession(self, protein):
        '''Get all accession codes for this protein'''
        accession_list = []
        accession = protein.findtext(XML_PARSE+'accession')
        return accession

    def _get_name(self, protein):
        '''Get the name of the protein'''
        try:
            name = protein.find(XML_PARSE+'protein').find(
                XML_PARSE+'recommendedName').findtext(
                XML_PARSE+'fullName')
        except AttributeError:
            try:
                name = protein.find(XML_PARSE+'protein').find(
                    XML_PARSE+'submittedName').findtext(
                XML_PARSE+'fullName')
            except AttributeError:
                name = protein.find(XML_PARSE+'protein').find(
                    XML_PARSE+'sumittedName').findtext(
                XML_PARSE+'fullName')
        return name
    
    def _get_genename(self, protein):
        '''Get the gene name'''
        try:
            gene_name = protein.find(
                XML_PARSE+'gene').findtext(
                XML_PARSE+'name')
            return gene_name
        except:
            gene_name = 'None'
            return gene_name
    
    def _get_gene_locus_name(self, protein):
        '''Get the gene locus name'''
        locus_list = []
        try:
            gene_name = protein.find(
                XML_PARSE+'gene').findall(XML_PARSE+'name')
            for locus_tag in gene_name:
                if locus_tag.get('type') == 'ordered locus':
                    locus = locus_tag.text
                    locus_list.append(locus)
            gene_locus = ','.join(locus_list)
            return gene_locus
        except:
            gene_locus = 'None'
            return gene_locus
    
    def _get_organism(self, protein):
        '''Get the species name'''
        organism_list = protein.find(
            XML_PARSE+'organism').findall(
            XML_PARSE+'name')
        for organism in organism_list:
            organism_name = organism.text
            return organism_name
        
    def _get_pubmed_id(self, protein):
        '''get pubmed id'''
        ref_database = protein.find(
            XML_PARSE+'reference').find(
            XML_PARSE+'citation').findall(
            XML_PARSE+'dReference')
        for feature in ref_database:
            if feature.get('type') == 'PuMed':
                pubmed_id = feature.get('id')
                return pubmed_id
    
    def _get_embl_id(self, protein):
        '''get database reference for embl'''
        ref_database = protein.findall(
            XML_PARSE+'dReference')
        for feature in ref_database:
            if feature.get('type') == 'EMBL':
                embl_id = feature.get('id')
                return embl_id
    
    def _get_refseq_id(self, protein):
        '''get database reference for refseq'''
        ref_database = protein.findall(
            XML_PARSE+'dReference')
        for feature in ref_database:
            if feature.get('type') == 'RefSeq':
                seq_ref_id = feature.get('id')
                return seq_ref_id
    
    def _get_kegg_id(self, protein):
        '''get database reference for kegg'''
        ref_database = protein.findall(
            XML_PARSE+'dReference')
        for feature in ref_database:
            if feature.get('type') == 'KEGG':
                kegg_id = feature.get('id')
                return kegg_id
    
    def _get_geneid(self, protein):
        '''get database reference for GeneID'''
        ref_database = protein.findall(
            XML_PARSE+'dReference')
        for feature in ref_database:
            if feature.get('type') == 'GeneID':
                gene_ref_id = feature.get('id')
                return gene_ref_id
            
    def _get_pdb_data(self, protein):
        '''get database reference for PDBsum'''
        ref_database = protein.findall(
            XML_PARSE+'dReference')
        for feature in ref_database:
            if feature.get('type') == 'PDBsum':
                pdb_id = feature.get('id')
                return pdb_id
            
    def _get_go_data(self, protein):
        '''get database reference for GO'''
        feature_list = []
        go_terms = set()
        ref_database = protein.findall(
            XML_PARSE+'dReference')
        for feature in ref_database:
            if feature.get('type') == 'GO':
                feature_list.append(feature)
                for each_feature in feature_list:
                    go_id = feature.get('id')
                    go_des_list = feature.findall(
                        XML_PARSE+'property')
                    for each_go_des in go_des_list:
                        if each_go_des.get('type') == 'term':
                            go_des = each_go_des.get('value')
                            go_terms.add('%s->%s'%(go_id, go_des))
        go_terms = str(go_terms).strip('[]').strip("''")
        print(go_terms)
        return go_terms
    
    def _get_interpro_data(self, protein):
        '''get database reference for InterPro'''
        feature_list = []
        interpro = []
        ref_database = protein.findall(XML_PARSE+'dReference')
        for feature in ref_database:
            if feature.get('type') == 'InterPro':
                feature_list.append(feature)
                for each_feature in feature_list:
                    ipr_id = feature.get('id')
                    ipr_des_list = feature.findall(
                        XML_PARSE+'property')
                    for each_ipr_des in ipr_des_list:
                        if each_ipr_des.get(
                            'type') == 'entry name':
                            ipr_des = each_ipr_des.get('value')
                            interpro.append('%s->%s'%(
                                ipr_id, ipr_des))
                            
        interpro = str(interpro).strip('[]').strip("''")
        return interpro
     
    def _get_pfam_data(self, protein):
        '''get database reference for Pfam'''
        feature_list = []
        pfam = []
        ref_database = protein.findall(
            XML_PARSE+'dReference')
        for feature in ref_database:
            if feature.get('type') == 'Pfam':
                feature_list.append(feature)
                for each_feature in feature_list:
                    pfam_id = feature.get('id')
                    pfam_des_list = feature.findall(
                        XML_PARSE+'property')
                    for each_pfam_des in pfam_des_list:
                        if each_pfam_des.get(
                            'type') == 'entry name':
                            pfam_des = each_pfam_des.get('value')
                            pfam.append(
                                '%s->%s'%(pfam_id, pfam_des))
                            
        pfam = str(pfam).strip('[]').strip("''")
        return pfam
    
    def _get_existance_type(self, protein):
        '''get existance type as predicted or experimentally derived'''
        prot_exist = protein.findall(XML_PARSE+'proteinExistence')
        for exist_type in prot_exist:
            return exist_type.get('type')
