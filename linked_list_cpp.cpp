#include <iostream>
#include <ctime>
#include <cstdlib>

// Структура узла остается прежней
struct TNode {
    int Data;
    TNode* Next;
};

// Класс, инкапсулирующий логику ОДНОГО циклического списка
class CyclicLinkedList {
public:
    TNode* Head = nullptr;
    int ListCount = 0;

    // Деструктор: автоматически очистит память при удалении объекта
    ~CyclicLinkedList() {
        clear();
    }

    void clear() {
        while (ListCount > 0) {
            if (Head == nullptr) break;
            TNode* temp = Head;
            if (ListCount == 1) {
                Head = nullptr;
            } else {
                TNode* last = getNodeAt(ListCount - 1);
                last->Next = Head->Next;
                Head = Head->Next;
            }
            delete temp;
            ListCount--;
        }
        Head = nullptr;
    }

    TNode* getNodeAt(int index) {
        if (Head == nullptr || index < 0 || index >= ListCount) return nullptr;
        TNode* p = Head;
        for (int i = 0; i < index; i++) p = p->Next;
        return p;
    }

    void add_to_end(int value) {
        TNode* newNode = new TNode;
        newNode->Data = value;
        if (Head == nullptr) {
            Head = newNode;
            newNode->Next = Head;
        } else {
            TNode* last = getNodeAt(ListCount - 1);
            newNode->Next = Head;
            last->Next = newNode;
        }
        ListCount++;
    }
};

// Экспортируемые функции для связи с Python (через ctypes)
extern "C" {

    // ВАЖНО: Создание нового экземпляра структуры
    CyclicLinkedList* create_list() {
        return new CyclicLinkedList();
    }

    // ВАЖНО: Удаление экземпляра структуры из памяти
    void delete_list_obj(CyclicLinkedList* list) {
        delete list;
    }

    void clear_list(CyclicLinkedList* list) {
        if (list) list->clear();
    }

    int get_count(CyclicLinkedList* list) {
        return list ? list->ListCount : 0;
    }

    bool insert_at(CyclicLinkedList* list, int value, int position) {
        if (!list || position < 0 || position > list->ListCount) return false;

        if (position == list->ListCount) {
            list->add_to_end(value);
            return true;
        }

        TNode* newNode = new TNode;
        newNode->Data = value;

        if (position == 0) {
            TNode* last = list->getNodeAt(list->ListCount - 1);
            newNode->Next = list->Head;
            last->Next = newNode;
            list->Head = newNode;
        } else {
            TNode* prev = list->getNodeAt(position - 1);
            newNode->Next = prev->Next;
            prev->Next = newNode;
        }
        list->ListCount++;
        return true;
    }

    int read_at(CyclicLinkedList* list, int position) {
        if (!list) return -1;
        TNode* node = list->getNodeAt(position);
        return node ? node->Data : -1;
    }

    bool delete_at(CyclicLinkedList* list, int position) {
        if (!list || list->Head == nullptr || position < 0 || position >= list->ListCount) return false;

        TNode* toDelete = nullptr;
        if (position == 0) {
            if (list->ListCount == 1) {
                toDelete = list->Head;
                list->Head = nullptr;
            } else {
                TNode* last = list->getNodeAt(list->ListCount - 1);
                toDelete = list->Head;
                last->Next = list->Head->Next;
                list->Head = list->Head->Next;
            }
        } else {
            TNode* prev = list->getNodeAt(position - 1);
            toDelete = prev->Next;
            prev->Next = toDelete->Next;
        }
        delete toDelete;
        list->ListCount--;
        return true;
    }

    void fill_random(CyclicLinkedList* list, int count, int min_val, int max_val) {
        if (!list || min_val > max_val) return;
        for (int i = 0; i < count; i++) {
            int val = rand() % (max_val - min_val + 1) + min_val;
            list->add_to_end(val);
        }
    }
}