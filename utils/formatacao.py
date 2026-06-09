

class Formatacao:
    def __init__(self):
        ...


    def formatar_valor_float(self, df):
        df["valor_formatado"] = (
            df["orcamento_consolidado_fundo"]
            .apply(
                lambda x:
                f"R$ {x:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
        )

        return df 
    

    def formatar_valor_integer(self, valor):
        valor = (
            f"{valor:,}".replace(",",".")
        )
        
        return valor