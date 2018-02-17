import sys
import random
import datetime
import json
import time


'''
ДЗ 2 
Программа генерирует случайным образом числа в заданных границах (пример от 0 до 10). 
Границы задаются через агрументы командной строки. 
Количество заданий, количество попыток, путь к файлу с результатми задается из файла настроек (config.json) 
Показывает числа и необходимую операцию (Найди произведение 2 и 4, найдите разность 243 и 102) 
Ждет когда человек введет результат 
После ввода человеком результата, она проверяет правильность введенного значения и время 
'''
 
file_conf = "config.json" 
operations = {0:["Умножение", "*"],
              1:["Сложение", "+"],
              2:["Вычитание", "-"],  
              3:["Целочисленное деление", "//"],
              4:["Остаток по модулю", "%"]
             }

results = {"name": "",
           "isWinner":"False",
           "qty_attempts":0,
           "time":""
          }

qty_tasks = 0
qty_attempts = 0
nickname = "User"
qty_true = 0


def read_to_dict(fn): 
    d ={} 
    try:
        with open(fn, 'r',encoding="utf-8") as file: 
            d = json.load(file) 
    except FileNotFoundError:
         print ("Error. Can't find file " + fn)
         d = {"qty_attempts": 5, "qty_tasks": 6,  "path": ""}
    return d 

def save_result(output, path): 
    with open(path + output, 'a') as fp:
        json.dump(results, fp)

def output_problem(cur_task, number,  oper, qty_cur_attempts, first_number, last_number) :
    out = "Задача № " + str(number)  + "\n"
    out += "Осталось задач: " + str(cur_task) + ", осталось попыток: " + str(qty_cur_attempts) + ", решено: " + str(qty_true)  + "\n"
    out += "Тип операции: " + operations[oper][0].upper() + " " + "\n"
    out += "Вычислить: " + str(first_number) + " " + operations[oper][1] + " " + str(last_number) 
    return out

 
if __name__ == "__main__":
    left = 0
    right = 0
    if len(sys.argv) != 3:
        print("Ошибка! Вы должны задать два вещественных числа на границах в параметрах командной строки!") 
        exit()
    else:
        try:
            left = int (sys.argv[1]) 
            right = int(sys.argv[2])
        except ValueError:
            print("Ошибка. Введенные аргументы не являются вещественными числами")
    #счиатаем настройки
    sets = read_to_dict(file_conf)
   

    qty_vars = len(operations)
    qty_tasks = sets['qty_tasks']
    qty_attempts = sets['qty_attempts'] 
    print("Кол-во задач: " + str(qty_tasks) + ", кол-во попыток: " + str(qty_attempts) + "\n")
    results["name"] = input("Введите ваше имя:")
    try:
        input("Нажмите enter, чтобы начать игру")
    except SyntaxError:
        pass
    time_start = datetime.datetime.now()
    num = 1
    cur_task = qty_tasks 
    for i in range(sets['qty_tasks']):
        #выберем рандомную операцию
        oper = int(random.random() * qty_vars)       
        #выберем числа
        first_number = int (random.randrange(left, right))
        last_number =  int (random.randrange(left, right))
        qty_cur_attempts = qty_attempts
        task_res = False
        while qty_cur_attempts >= 1:
            #выводим время игры
            timediff = datetime.datetime.now().timestamp() - time_start.timestamp()
            print("Время игры: " + "%.2dh: %.2dm: %.2ds" % (timediff//3600, timediff // 60 % 60, timediff % 60)  , end="\n")
            print(output_problem(cur_task, num, oper, qty_cur_attempts, first_number, last_number))
            try:
                res = int (input())
                exec ('res_corr = ' + str(first_number) + " " + operations[oper][1] + " " + str(last_number))
                if (res == res_corr):
                    print("Ответ верный! " + "\n")
                    task_res = True
                    break
                else:
                    print("Ответ неверный! Попробуйте еще раз" + "\n")
                    if (qty_cur_attempts == 1):
                        print("Верный ответ: " + str(res_corr) + "\n")    
            except ValueError:
                    print("Ошибка. Нужно ввести целочисленное значение\n")
                    
            except SyntaxError:
                pass
            qty_cur_attempts  -= 1

        if (task_res == False):
            break 
        else:
            qty_true += 1
        num += 1
        cur_task -= 1
        #добавим использованные попытки
        results["qty_attempts"] += qty_attempts - qty_cur_attempts + 1
    timediff = datetime.datetime.now().timestamp() - time_start.timestamp()
    if task_res  != True:
        results["isWinner"] = False
        str_result = "Вы проиграли"
    else:
        results["isWinner"] = True
        str_result = "Вы победили!"
    results["time"] = "%.2dh: %.2dm: %.2ds" % (timediff//3600, timediff // 60 % 60, timediff % 60)
    save_result(sets["result_table"], sets["path"])
    print("Конец игры. " + str_result + " Ваше имя:" +  results["name"] + ". Время игры: " + results["time"], end="\n")
    
