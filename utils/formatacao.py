

class Formatacao:
    def __init__(self):
        ...


    def formatar_valor_float(self, valor):
        valor = (
            f"{valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        return valor 
    

    def formatar_valor_integer(self, valor):
        valor = (
            f"{valor:,}".replace(",",".")
        )
        
        return valor