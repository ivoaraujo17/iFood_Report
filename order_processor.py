import pandas as pd


class OrderProcessor:
    def __init__(self, file):
        self.df = pd.read_excel(file)
    
    def run(self):
        self.df.rename(columns=lambda x: x.upper(), inplace=True)

        # Transform the content of the "FORMAS DE PAGAMENTO" column to lowercase
        self.df['FORMAS DE PAGAMENTO'] = self.df['FORMAS DE PAGAMENTO'].str.lower()

        # Order classification via store and ifood, if the payment method is cash or on delivery, it is classified as store, otherwise it is classified as ifood
        self.df['LOJA_IFOOD'] = self.df['FORMAS DE PAGAMENTO'].apply(lambda x: 'loja' if 'dinheiro' in x or 'na entrega' in x else 'ifood')

        # Canceled orders classification, if the column "ORIGEM DO CANCELAMENTO" is not null, the order is considered canceled
        self.df['CANCELADO'] = ~self.df['ORIGEM DO CANCELAMENTO'].isnull()

        # reduces payment methods to cash, credit, debit and online.
        # if the payment method contains "débito" and payment as store is classified as debit
        # if the payment method contains "crédito" and payment as store is classified as credit
        # if the payment method is "dinheiro" is classified as cash
        # if the order is from ifood, the payment method is classified as online
        self.df['PAGAMENTO'] = None
        self.df.loc[self.df['FORMAS DE PAGAMENTO'].str.contains('débito'), 'PAGAMENTO'] = 'Débito'
        self.df.loc[self.df['FORMAS DE PAGAMENTO'].str.contains('crédito'), 'PAGAMENTO'] = 'Crédito'
        self.df.loc[self.df['FORMAS DE PAGAMENTO'] == 'dinheiro', 'PAGAMENTO'] = 'Dinheiro'
        self.df.loc[self.df['LOJA_IFOOD'] == 'ifood', 'PAGAMENTO'] = 'Online'

        # verify if the column "PAGAMENTO" has any null value, if so, fill it with "Online"
        if self.df['PAGAMENTO'].isnull().any():
            self.df['PAGAMENTO'] = self.df['PAGAMENTO'].fillna('Online')
        
        # Fill the dictionary with the information
        dictionary = {}

        # Count of all orders, can be the number of lines in the table
        dictionary["Total de Pedidos"] = self.df.shape[0]

        # Count of orders where in the column LOJA_IFOOD == "ifood" where canceled is False
        dictionary["Pedidos Online"] = self.df[(self.df['LOJA_IFOOD'] == 'ifood') & ~self.df['CANCELADO']].shape[0]

        # Count of orders where in the column LOJA_IFOOD == "loja" where canceled is False
        dictionary["Pedidos Loja"] = self.df[(self.df['LOJA_IFOOD'] == 'loja') & ~self.df['CANCELADO']].shape[0]

        # Count of orders considering CANCELADO == True
        dictionary["Pedidos Cancelados"] = self.df[self.df['CANCELADO']].shape[0]

        # Gross sales considering only the sum of the column VALOR DOS ITENS and CANCELADO is False
        dictionary["Venda Bruta"] = (self.df['VALOR DOS ITENS'][~self.df['CANCELADO']].sum()).round(2)

        # Total delivery fee considering the sum of the column TAXA DE ENTREGA and CANCELADO is False
        dictionary["Taxa de Entrega"] = (self.df["TAXA DE ENTREGA"][~self.df['CANCELADO']].sum()).round(2)

        # Total service fee considering the sum of the column TAXA DE SERVIÇO and CANCELADO is False
        dictionary["Taxa de Serviço"] = (self.df['TAXA DE SERVIÇO'][~self.df['CANCELADO']].sum()).round(2)

        # Total delivery fee considering the sum of the column TAXA DE ENTREGA and CANCELADO is True
        dictionary["Taxa de Entrega Cancelado"] = (self.df["TAXA DE ENTREGA"][self.df['CANCELADO']].sum()).round(2)

        # Total service fee considering the sum of the column TAXA DE SERVIÇO and CANCELADO is True
        dictionary["Taxa de Serviço Cancelado"] = (self.df['TAXA DE SERVIÇO'][self.df['CANCELADO']].sum()).round(2)

        # Gross sales considering only the sum of the column VALOR DOS ITENS and CANCELADO is True
        dictionary["Venda Cancelada"] = (self.df['VALOR DOS ITENS'][self.df['CANCELADO']].sum()).round(2)

        # Total Manager considering the sum of the column VALOR DOS ITENS + TAXA DE SERVIÇO + TAXA DE SERVIÇO
        dictionary["Total Gestor"] =  self.df['VALOR DOS ITENS'].sum() + self.df['TAXA DE SERVIÇO'].sum() + self.df["TAXA DE ENTREGA"].sum()

        # Online incentive considering the sum of the column INCENTIVO PROMOCIONAL DO IFOOD and CANCELADO is False
        dictionary["Incentivo iFood"] = (self.df['INCENTIVO PROMOCIONAL DO IFOOD'][~self.df['CANCELADO']].sum()).round(2)

        # Store discount considering the sum of the column INCENTIVO PROMOCIONAL DA LOJA and CANCELADO is False
        dictionary["Desconto Loja"] = (self.df['INCENTIVO PROMOCIONAL DA LOJA'][~self.df['CANCELADO']].sum()).round(2)

        # Gross liquid sales considering only the sum of the column TOTAL PARCEIRO
        dictionary["Venda Líquida"] = (dictionary['Venda Bruta'] - dictionary["Desconto Loja"]).round(2)

        # Online Gross Sales considering only the sum of the column VALOR DOS ITENS and CANCELADO is False
        dictionary["Online"] = (self.df['VALOR DOS ITENS'][(self.df['LOJA_IFOOD'] == 'ifood') & ~self.df['CANCELADO']].sum() 
                                - self.df['INCENTIVO PROMOCIONAL DA LOJA'][(self.df['LOJA_IFOOD'] == 'ifood') & ~self.df['CANCELADO']].sum()
                                ).round(2)

        # Cash sales considering only the sum of the column VALOR DOS ITENS and CANCELADO is False and subtracts the store promotional incentive
        dictionary["Dinheiro"] = (self.df['VALOR DOS ITENS'][(self.df['PAGAMENTO'] == 'Dinheiro') & ~self.df['CANCELADO']].sum()
                                - self.df['INCENTIVO PROMOCIONAL DA LOJA'][(self.df['PAGAMENTO'] == 'Dinheiro') & ~self.df['CANCELADO']].sum()
                                  ).round(2)

        # Credit sales considering only the sum of the column VALOR DOS ITENS and CANCELADO is False and subtracts the store promotional incentive
        dictionary["Crédito"] = (self.df['VALOR DOS ITENS'][(self.df['PAGAMENTO'] == 'Crédito') & ~self.df['CANCELADO']].sum()
                                - self.df['INCENTIVO PROMOCIONAL DA LOJA'][(self.df['PAGAMENTO'] == 'Crédito') & ~self.df['CANCELADO']].sum()
                                 ).round(2)

        # Debit sales considering only the sum of the column VALOR DOS ITENS and CANCELADO is False and subtracts the store promotional incentive
        dictionary["Débito"] = (self.df['VALOR DOS ITENS'][(self.df['PAGAMENTO'] == 'Débito') & ~self.df['CANCELADO']].sum()
                                - self.df['INCENTIVO PROMOCIONAL DA LOJA'][(self.df['PAGAMENTO'] == 'Débito') & ~self.df['CANCELADO']].sum()
                                ).round(2)
        """print('==========================')
        for key, value in dictionary.items():
            print(f'{key}: {value}')
            if key == 'Pedidos Cancelados':
                print('==========================')    
            if key == 'Total Gestor':
                print('==========================')
            if key == 'Incentivo iFood':
               print('==========================')
               print('Venda Bruta:', dictionary['Venda Bruta'])    """
        
        return dictionary

if __name__ == '__main__':
    order_processor = OrderProcessor('pedidos.xlsx')
    order_processor.run()

    