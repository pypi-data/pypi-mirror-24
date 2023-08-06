import os.path
import csv
from datetime import date
from urllib.request import urlretrieve
from zipfile import ZipFile
import numpy as np
import pandas as pd
from .reimbursements import AVAILABLE_YEARS, Reimbursements


class Dataset:
    def __init__(self, path, years=AVAILABLE_YEARS):
        self.path = path
        self.years = years if isinstance(years, list) else [years]

    def fetch(self):
        base_url = "http://www.camara.leg.br/cotas/Ano-{}.csv.zip"

        for year in self.years:
            zip_file_path = os.path.join(self.path, "Ano-{}.zip".format(year))
            url = base_url.format(year)
            urlretrieve(url, zip_file_path)
            zip_file = ZipFile(zip_file_path, 'r')
            zip_file.extractall(self.path)
            zip_file.close()
            os.remove(zip_file_path)

        urlretrieve('http://www2.camara.leg.br/transparencia/cota-para-exercicio-da-atividade-parlamentar/explicacoes-sobre-o-formato-dos-arquivos-xml',
                    os.path.join(self.path, 'datasets-format.html'))

    def convert_to_csv(self):
        # deprecated but still here so we don't break poor Rosie (for now)
        pass

    def translate(self):
        for year in self.years:
            csv_path = os.path.join(self.path, 'Ano-{}.csv'.format(year))
            self._translate_file(csv_path)

    def clean(self):
        reimbursements = Reimbursements(self.path, years=self.years)
        dataset = reimbursements.group(reimbursements.receipts)
        reimbursements.write_reimbursement_file(dataset)

    def _translate_file(self, csv_path):
        output_file_path = csv_path \
            .replace('.csv', '.xz') \
            .replace('Ano-', 'reimbursements-')

        data = pd.read_csv(csv_path,
                           encoding='utf-8',
                           delimiter=";",
                           quoting=csv.QUOTE_NONE,
                           dtype={'ideDocumento': np.str,
                                  'idecadastro': np.str,
                                  'nuCarteiraParlamentar': np.str,
                                  'codLegislatura': np.str,
                                  'txtCNPJCPF': np.str,
                                  'numRessarcimento': np.str},
                           converters={'vlrDocumento': self._parse_float,
                                       'vlrGlosa': self._parse_float,
                                       'vlrLiquido': self._parse_float,
                                       'vlrRestituicao': self._parse_float})

        data.rename(columns={
            'ideDocumento': 'document_id',
            'txNomeParlamentar': 'congressperson_name',
            'idecadastro': 'congressperson_id',
            'nuCarteiraParlamentar': 'congressperson_document',
            'nuLegislatura': 'term',
            'sgUF': 'state',
            'sgPartido': 'party',
            'codLegislatura': 'term_id',
            'numSubCota': 'subquota_number',
            'txtDescricao': 'subquota_description',
            'numEspecificacaoSubCota': 'subquota_group_id',
            'txtDescricaoEspecificacao': 'subquota_group_description',
            'txtFornecedor': 'supplier',
            'txtCNPJCPF': 'cnpj_cpf',
            'txtNumero': 'document_number',
            'indTipoDocumento': 'document_type',
            'datEmissao': 'issue_date',
            'vlrDocumento': 'document_value',
            'vlrGlosa': 'remark_value',
            'vlrLiquido': 'net_value',
            'numMes': 'month',
            'numAno': 'year',
            'numParcela': 'installment',
            'txtPassageiro': 'passenger',
            'txtTrecho': 'leg_of_the_trip',
            'numLote': 'batch_number',
            'numRessarcimento': 'reimbursement_number',
            'vlrRestituicao': 'reimbursement_value',
            'nuDeputadoId': 'applicant_id',
        }, inplace=True)

        subquotas = (
            (1, 'Maintenance of office supporting parliamentary activity'),
            (2, 'Locomotion, meal and lodging'),
            (3, 'Fuels and lubricants'),
            (4, 'Consultancy, research and technical work'),
            (5, 'Publicity of parliamentary activity'),
            (6, 'Purchase of office supplies'),
            (7, 'Software purchase or renting; Postal services; Subscriptions'),
            (8, 'Security service provided by specialized company'),
            (9, 'Flight tickets'),
            (10, 'Telecommunication'),
            (11, 'Postal services'),
            (12, 'Publication subscriptions'),
            (13, 'Congressperson meal'),
            (14, 'Lodging, except for congressperson from Distrito Federal'),
            (15, 'Automotive vehicle renting or watercraft charter'),
            (119, 'Aircraft renting or charter of aircraft'),
            (120, 'Automotive vehicle renting or charter'),
            (121, 'Watercraft renting or charter'),
            (122, 'Taxi, toll and parking'),
            (123, 'Terrestrial, maritime and fluvial tickets'),
            (137, 'Participation in course, talk or similar event'),
            (999, 'Flight ticket issue')
        )

        for code, name in subquotas:
            data.loc[data['subquota_number'] == code, ['subquota_description']] = name

        data.to_csv(output_file_path, compression='xz', index=False,
                    encoding='utf-8')

        return output_file_path

    def _parse_float(self, string):
        return float(string.replace(',', '.'))
