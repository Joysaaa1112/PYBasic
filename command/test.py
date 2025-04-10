import json
import time
import streamingjson

s = '{"data":{"quantity":1,"currency":"CNY","unit_material_cost":6.57,"unit_material_desc":"6061铝合金，含20%损耗","unit_processing_cost":14.59,"unit_processing_desc":{"machine":12.16,"tool":2.43,"energy":0.0},"unit_post_proc_cost":0.0,"unit_post_proc_desc":[],"unit_total_cost":21.16,"pre_tax_total":21.16,"discount":0.0,"tax":2.75,"post_tax_total":23.91,"margin":0.2,"final_total":28.69,"unit_price":28.69,"profit":7.53,"labor_cost":12.16},"reports":{"material_cost":"6.57","surface_cost":"0.0","other_cost":"19.12","tax_cost":"2.75"}}'

def output():
    lexer = streamingjson.Lexer()
    for i in s:
        yield i
        lexer.append_string(i)
        craft_to_json(lexer)
        time.sleep(0.01)


def craft_to_json(lexer):
    j = lexer.complete_json()
    json_dict = json.loads(j)
    try:
        if json_dict.get('data').get('unit_material_cost') is not None:
            print('已获取到单件材料成本', json_dict.get('data').get('unit_material_cost'))
        if json_dict.get('data').get('unit_processing_cost') is not None:
            print('已获取到加工费用', json_dict.get('data').get('unit_processing_cost'))
        if json_dict.get('data').get('unit_total_cost') is not None:
            print('已获取到单件总费用', json_dict.get('data').get('unit_total_cost'))
        if json_dict.get('reports') is not None:
            print('已获取到单件总费用', json_dict.get('data').get('unit_total_cost'))
        # todo:
    except Exception as e:
        print(e)

if __name__ == '__main__':
    for s in output():
        print(s)