from TableParser import TableParser


# вспомогательный тестовый парсер-заглушка для разработчика REST
class SillyParser(TableParser):
    def parse_pdf(self, input_file):
        return 'Excellent!'
