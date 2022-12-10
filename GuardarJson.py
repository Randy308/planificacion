import json


class GuardarJson:
    myList = []

    def __init__(self):
        try:
            with open('test_nested.json', 'r') as openfile:
                self.myList = json.load(openfile)
        except IOError:
            print("A exception has occurred")

    def salvar(self):
        str_data = 'anormal string'
        int_data = 1
        float_data = 1.50
        list_data = [str_data, int_data, float_data]
        nested_list = [int_data, float_data, list_data]
        dictionary = {
            'int': int_data,
            'str': str_data,
            'float': float_data,
            'list': list_data,
            'nested list': nested_list
        }
        self.myList.append(dictionary)
        with open("test_nested.json", "w") as outfile:
            json.dump(self.myList, outfile, indent=4, sort_keys=False)

    def imprimir(self):
        with open('test_nested.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
            for dictionary in json_object:
                for k, v in dictionary.items():
                    print(k, v)
                    print(type(v))


if __name__ == '__main__':
    prueba = GuardarJson()
    #prueba.salvar()
    prueba.imprimir()
