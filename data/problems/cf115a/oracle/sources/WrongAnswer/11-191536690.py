'''
В компании работает n сотрудников, пронумерованных от 1 до n. У каждого сотрудника либо нет руководителя, либо есть ровно один непосредственный руководитель — некоторый другой сотрудник с другим номером. Сотрудник A называется начальником другого сотрудника B, если выполняется хотя бы одно из двух условий:

Сотрудник A — непосредственный руководитель сотрудника B.
У сотрудника B есть непосредственный руководитель, сотрудник C, такой, что A является начальником сотрудника C.
В структуре компании нет циклов. То есть никакой сотрудник не является начальником своего непосредственного руководителя.

Сегодня компания собирается организовать праздник. Для этого необходимо разделить всех n сотрудников на несколько групп: каждый человек должен относиться ровно к одной группе. Более того, в каждой группе не должно быть таких двух сотрудников A и B, что A является начальником B.

Ваша задача — найти наименьшее возможное количество таких групп.

Входные данные
Первая строка содержит целое число n (1 ≤ n ≤ 2000) — количество сотрудников.

Следующие n строк содержат целые числа pi (1 ≤ pi ≤ n или pi = -1). Каждое pi обозначает непосредственного руководителя i-го сотрудника. Если pi равно -1, то i-ый сотрудник не имеет непосредственного руководителя.

Гарантируется, что никакой сотрудник не является своим собственным непосредственным руководителем (pi ≠ i). Также гарантируется, что структура компании не содержит циклов.

Выходные данные
Выведите единственное целое число — минимальное количество групп, на которые можно разделить всех сотрудников.
'''
import sys
class Person ():
    def __init__ (self, val = None, head = None):
        self.val = val
        self.head = head

class Tree ():
    def __init__(self, persons):
        self.persons = persons
        self.groups = 0
        self.heads = []

    def dfs(self, person):
        if person.head != None:
            self.heads.append(person.val)
            if person.head != -1:
                self.dfs(person.head) 
            return
        else:
            self.heads.append(person.val)
            return

    def make_groups(self):
        groups = []
        for i, person in enumerate(self.persons):
            self.heads = []
            flag = True
            if i == 0:
                groups.append ([person.val])
            else:
                self.dfs(person)
                for group in groups:
                    if len (list (set (self.heads[1:]) & set (group) )) == 0:
                        group.append (person.val)
                        flag = False
                        break
                if flag:
                    groups.append ([person.val])
    
        return groups
                    


def main ():
    n = int(sys.stdin.readline().split()[0])
    persons = []
    for i in range(n):
        persons.append(Person(val = i + 1))
    for i in range(n):
        number = int (input().split()[0])
        if number != -1:
            persons[i].head = persons[number - 1]
    tree = Tree(persons)

    print (len(tree.make_groups()))
    tree.make_groups()
    return
if __name__ == '__main__':
    main()