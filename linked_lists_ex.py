class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __str__(self):
        return str(self.data)

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next):
        self.next = new_next


class LinkedList:
    ITEM_NOT_FOUND = -1

    def __init__(self, head=None):
        self.head = head
        self.length = 0
        if head is not None:
            self.length += 1

    def get_head(self):  # Todo - Get the head - The 1st element of the linked list
        return self.head

    def is_empty(self):
        return self.head is None

    def add(self, new_head):  # Todo - add to the start
        new_head.set_next(self.head)  # Todo - putting new_head in the front of the linked list
        self.head = new_head  # Todo = declaring the head of the linked list is the new head, thus the 1st element
        self.length += 1

    def __len__(self):
        current = self.head  # Todo - temporary element, moving between throughout the list
        counter = 0
        while current is not None:
            counter += 1
            current = current.get_next()
        return counter

    def reversed_lst(self):
        current = self.head  # Todo - temporary element, moving between throughout the list
        self.head = None  # Todo - cutting the head of the list
        while current:  # Todo - While current is not None, thus the last element of the linked list
            self.add(current)  # Todo - Add to the start
            next_after_current = current.get_next()
            current = next_after_current  # Todo - moving current 1 element forward, thus the head is now the tail

    def r_index(self, item):
        return self.index_helper(self.head, item, 0)

    def index_helper(self, cur, item, index):
        """
        :param cur: current element
        :param item: Given item
        :param index: current index
        :return: Desired index/ None
        """
        if index >= self.length:  # Passed through all the list
            return self.ITEM_NOT_FOUND
        if cur.get_data() == item:  # Found the item
            return index
        return self.index_helper(cur.get_next(), item, index + 1)  # Moving one element forward and one index forward


node4 = Node("Yo")  # Todo = Tail
node3 = Node("Hi", node4)
node2 = Node("Bi", node3)
node1 = Node("Pee", node2)  # # Todo = Head

lnk_lst = LinkedList(node4)
lnk_lst.add(node3)
lnk_lst.add(node2)
lnk_lst.add(node1)
# print(lnk_lst.get_head())
# print(len(lnk_lst))

# print("length = ", len(lnk_lst))
# print(lnk_lst.get_head())
# lnk_lst.reversed_lst()
# print(lnk_lst.get_head())
# print(lnk_lst.r_index("Pee"))


"""Exercise"""


class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class Linked_List2:
    def __init__(self):
        self.__head = None

    def add(self, new_head):
        tmp = self.__head
        self.__head = new_head
        new_head.next = tmp

    def get_head(self):
        return self.__head

    def is_repetative(self, lst):
        d = self.__head
        while d is not None:  # Todo - it only checks once if d is not None, for loop responsible for the rest
            for i in range(len(lst)):
                if not d or d.data != lst[i]:
                    return False
                d = d.next  # But we continue in the while loop for the linked list until linked list's done
        return True


def zipper(head1, head2):
    while head1:
        cur1 = head1.next
        cur2 = head2.next
        head1.next = head2
        head2.next = cur1
        head1 = cur1
        head2 = cur2


# linked_list1 = Node("1", Node("2", Node("3", Node("4"))))
# linked_list2 = Node("A", Node("B", Node("C", Node("D"))))
# my_noes = Node("a", Node("b", Node("a", Node("b", Node("a", Node("b"))))))
linked_list3 = Linked_List2()
linked_list3.add(Node("b"))
linked_list3.add(Node("a"))
linked_list3.add(Node("b"))
linked_list3.add(Node("a"))
linked_list3.add(Node("b"))
# linked_list3.add(Node("a"))

# print(linked_list3.get_head().data)
# print(zipper(linked_list1, linked_list2))
# print(linked_list1.data)
# print(linked_list3.is_repetative(["a", "b"]))
# print(linked_list3.is_repetative(["a", "b", "a"]))
# print(linked_list3.is_repetative(["a", "b", "a", "b"]))



