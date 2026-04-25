import random

class Node:
    """Узел циклического списка (аналог TNode в Pascal)"""
    def __init__(self, data):
        self.data = data
        self.next = None

class CyclicLinkedList:
    def __init__(self):
        self.head = None
        self.count = 0

    def _get_node_at(self, index):
        """Внутренняя функция поиска узла (аналог GetNodeAt)"""
        if self.head is None or index < 0 or index >= self.count:
            return None
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr

    # --- ФУНКЦИЯ 1: Создать/очистить список ---
    def clear_list(self):
        self.head = None
        self.count = 0

    # --- ФУНКЦИЯ 2: Добавить элемент в конец ---
    def add_to_end(self, value):
        self.insert_at(value, self.count)

    # --- ФУНКЦИЯ 3: Получить все элементы (для показа списка) ---
    def get_all_elements(self):
        elements = []
        curr = self.head
        for _ in range(self.count):
            elements.append(curr.data)
            curr = curr.next
        return elements

    # --- ФУНКЦИЯ 4: Вставить элемент на позицию ---
    def insert_at(self, value, position):
        if position < 0 or position > self.count:
            return False
        
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
        elif position == 0:
            last = self._get_node_at(self.count - 1)
            new_node.next = self.head
            last.next = new_node
            self.head = new_node
        else:
            prev = self._get_node_at(position - 1)
            new_node.next = prev.next
            prev.next = new_node
        
        self.count += 1
        return True

    # --- ФУНКЦИЯ 5: Прочитать элемент по позиции ---
    def read_at(self, position):
        node = self._get_node_at(position)
        if node:
            return node.data
        return None

    # --- ФУНКЦИЯ 6: Удалить по позиции ---
    def delete_at(self, position):
        if self.head is None or position < 0 or position >= self.count:
            return False
            
        if position == 0:
            if self.count == 1:
                self.head = None
            else:
                last = self._get_node_at(self.count - 1)
                last.next = self.head.next
                self.head = self.head.next
        else:
            prev = self._get_node_at(position - 1)
            prev.next = prev.next.next
            
        self.count -= 1
        return True

    # --- ФУНКЦИЯ 7: Заполнить случайными элементами ---
    def fill_random(self, amount, min_val, max_val):
        """Добавляет элементы в конец существующего списка"""
        if min_val > max_val:
            return
        for _ in range(amount):
            val = random.randint(min_val, max_val)
            self.add_to_end(val)