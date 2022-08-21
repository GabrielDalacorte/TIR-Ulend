import calendar
import pprint

import numpy_financial as npf
from installments import installments
from investments import investments


class IRR:

    def __init__(self):
        self.json_finish = {}

    def data_treatments(self):
        """
        :return: Trata os valores.
        """
        for installments_values in installments:
            self.json_finish.update({installments_values['investment_id']: {}})

        for investments_values in investments:
            if investments_values['id'] in self.json_finish.keys():
                amount_value = f'-{investments_values["amount"]}'

                self.json_finish[investments_values['id']].update({'created_at': investments_values["created_at"],
                                                                   'investment_value': amount_value})

        for parcel_and_due_data in installments:
            self.json_finish[parcel_and_due_data['investment_id']].update({'parcel_date': []})

        for parcel_with_value in installments:
            date_new = parcel_with_value['due_date'].split('-')
            year = int(date_new[0])

            month = int(date_new[1])
            monthRange = calendar.monthrange(year, month)
            month_new = str(month).zfill(2)

            self.json_finish[parcel_with_value['investment_id']]['parcel_date'].append({parcel_with_value["due_date"]:
                                                                                        parcel_with_value["amount"]})
            for x in range(int(date_new[2]), monthRange[1]):
                day = str(x).zfill(2)
                date_new_format = f'{year}-{month_new}-{day}'

                if date_new_format not in parcel_with_value['due_date']:
                    self.json_finish[parcel_with_value['investment_id']]['parcel_date'].append({date_new_format: 0})

        return self.json_finish

    def return_irr(self):
        """
        :return: Retorna Valor IRR para cada valor investido/valor recebido
        """
        irr_lst = []
        irr_info = self.data_treatments()

        for key, values in irr_info.items():
            values.update({'values_irr_count': []})
            values['values_irr_count'].append(values['investment_value'])
            for values_amount in values['parcel_date']:
                for amount in values_amount.values():
                    if amount != 0:
                        values['values_irr_count'].append(amount)

            irr = round(npf.irr(values['values_irr_count']), 2)
            irr_lst.append({'id': key, 'irr': irr})

        return irr_lst

    def verify_info(self):
        """
        :return: Retorna Valores concatenados ( Valores abaixo ):
        id_data
        criado_em
        valor_investido
        data_parcela/parcela
        """
        for id_data, values in self.data_treatments().items():
            for value_parcel in values['parcel_date']:
                for due_date, parcel in value_parcel.items():
                    if parcel != 0:
                        info = f"""ID: {id_data} | "Criado em: {values['created_at']} | Investido: {values['investment_value']} | Data/Parcelas: {due_date} R$ {parcel}"""
                        # print info
                        return info

    def __str__(self):
        """
        :return: Retorna ID + Valor IRR
        """
        for values_irr in self.return_irr():
            # print value_irr
            return values_irr
