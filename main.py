from sys import *

def dynamic_search(equipment:dict, max_capacity:int) -> list:
    mem_table = [[(0, '') for _ in range(max_capacity+1)] for _ in range(len(equipment)+1)]
    for i, name in enumerate(equipment.keys(), start=1):
        price, weight = equipment[name]
        for capacity in range(max_capacity+1):
            if weight <= capacity and mem_table[i-1][0][0] <= price + mem_table[i-1][capacity-weight][0]:
                mem_table[i][capacity] = (mem_table[i-1][capacity-weight][0] + price, 
                                          mem_table[i-1][capacity-weight][1] + name)
            else: mem_table[i][capacity] = (mem_table[i-1][capacity][0] - price, mem_table[i-1][capacity][1])
    return mem_table


def recursive_search(equipment:dict, capacity:int, pts:int, weight=0, survival_kit='') -> list:
    if not equipment: return [(survival_kit, pts)] if pts > 0 else []
    equipment = equipment.copy()
    combs = []
    for name in equipment:
        data = equipment.pop(name)
        if data[1] + weight <= capacity:
            combs += recursive_search(equipment, capacity, pts+data[0], weight+data[1], survival_kit + name)
        combs += recursive_search(equipment, capacity, pts-data[0], weight, survival_kit)
        return combs

def pretty_table(table:list) -> None:
    for row in table:
        [print(str(item[0]).ljust(3), item[1].ljust(7) , end='') for item in row]
        print()


def backpack_fill(backpack_size:tuple, backpack:list, item:tuple) -> list | None:
    def is_empty(section):
        if not section: return False
        for element in section:
            if element: return False
        return True

    for row in range(backpack_size[1]):
        for column in range(backpack_size[0]):
            if column + item[1] - 1 < backpack_size[0]:
                if is_empty(backpack[row][column:column+item[1]]):
                    for cell in range(item[1]): 
                        backpack[row][column+cell] = item[0]
                    return backpack

            elif row + item[1] - 1 < backpack_size[1]:
                if is_empty([x[column] for x in backpack[row:row+item[1]]]):
                    for cell in range(item[1]): backpack[row+cell][column] = item[0]
                    return backpack


def backpack_distribution(equipment:dict, backpack_size:tuple, survival_kit:str) -> list:
    backpack = [['' for _ in range(backpack_size[0])] for _ in range(backpack_size[1])]
    survival_kit = [(x, equipment[x][1]) for x in survival_kit]
    survival_kit.sort(key=lambda x: -x[1])
    while survival_kit:
        item = survival_kit[0]
        result = backpack_fill(backpack_size, backpack, item)
        if result:
            survival_kit.pop(0)
            backpack = result
    return backpack 


def output(backpack, pts=None):
    [print(*map(lambda x: f'[{x.ljust(1)}]', row), sep=',') for row in backpack]
    if pts is not None: print(f'Итоговые очки выживания: {pts}')


def extra_task(equipment:dict, start_pts:int, backpack_size:tuple) -> None:
    max_capacity = backpack_size[0] * backpack_size[1]
    table = dynamic_search(equipment, 7)
    survival_kit = table[-1][-1][1]
    pts = table[-1][-1][0] + start_pts
    backpack = backpack_distribution(equipment, (7, 1), survival_kit)
    print('\nНаилучшим вариантом для рюкзака из 7 ячеек является:')
    output(backpack, pts)
    if pts > 0: print('Следовательно существует решение для данного рюкзака')
    else: print('Следовательно для данного рюкзака не существует решений \n')

    print('Все комбинации вещей:')
    all_combinations = recursive_search(equipment, 8, start_pts)
    for combination in all_combinations:
        backpack = backpack_distribution(equipment, backpack_size, combination[0])
        output(backpack, combination[1])
        print()


def start():
    backpack_size = (2, 4)
    start_pts = 15
    equipment = {'r': (15, 3),
                 'p': (15, 2),
                 'a': (15, 2),
                 'm': (20, 2),
                 'i': (5, 1),
                 'k': (15, 1),
                 'x': (20, 3),
                 't': (25, 1),
                 'f': (15, 1),
                 'd': (10, 1),
                 's': (20, 2),
                 'c': (20, 2)}
    table = dynamic_search(equipment, backpack_size[0]*backpack_size[1])
    survival_kit = table[-1][-1][1]
    pts = table[-1][-1][0] + start_pts
    backpack = backpack_distribution(equipment, backpack_size, survival_kit)

    output(backpack, pts)
    extra_task(equipment, start_pts, backpack_size)


if __name__ == '__main__':
    setrecursionlimit(2000)
    start()
