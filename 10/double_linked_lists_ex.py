class Node:
    def __init__(self, data, prev=None, forward=None):
        self.data = data
        self.prev = prev
        self.forward = forward


class Double_Linked_List:
    def __init__(self):
        self.head = self.tail = None
        self.length = 0

    def add_to_start(self, given_node):
        """
        :param given_node: A given node to be the head node
        :return: None
        """
        if self.head is None:  # List is empty, front point of view
            self.tail = given_node  # Since no elements, declare node as Tail Node, without Head to the list
        else:
            self.head.prev = given_node  # The node before Head node is the given node
            given_node.forward = self.head  # Node after given node is the original Head node --> append to the start
        self.head = given_node
        # Case 1: Just let node be the Tail node and Head node, since only 1 elements
        # Case 2: The Head node itself -- > The given node, thus being at the start
        self.length += 1

    def add_to_end(self, given_node):
        """
        :param given_node: A given node to be the head node
        :return: None
        """
        if self.tail is None:  # List is empty, back point of view
            self.head = given_node  # Since no elements, declare node as Head Node, without Tail to the list
        else:
            self.tail.forward = given_node  # The node after Tail node is the given node
            given_node.prev = self.tail  # Node before given node is the original Tail node --> append to the end
        self.tail = given_node
        # Case 1: Just let node be the Head node and Tail node, since only 1 elements
        # Case 2: The Tail node itself -- > The given node, thus being at the end
        self.length += 1

    def remove_from_start(self):
        d = self.head.data  # Warning - Assuming the list is not empty
        self.head = self.head.forward  # Todo - changing the Head node to be the next node
        if self.head is None:  # Now the list is empty
            self.tail = None
        else:  # Todo - disconnect old Head note
            self.head.prev.forward = None  # old head node cuts ties
            self.head.prev = None  # new Head node cuts ties
        self.length -= 1
        return d  # Todo - return the value of the removed Head node

    def remove_from_end(self):
        d = self.head.data  # Warning - Assuming the list is not empty
        self.tail = self.tail.prev  # Todo - changing the Tail node to be the previous node
        if self.tail is None:  # Now the list is empty
            self.head = None
        else:  # Todo - disconnect old Tail note
            self.tail.forward.prev = None  # old Tail node cuts ties
            self.tail.forward = None  # new Tail node cuts ties
        self.length -= 1
        return d  # Todo - return the value of the removed Tail node


node1 = Node("A")
node2 = Node("B")
node3 = Node("C")
node4 = Node("Before_A")
linked_list = Double_Linked_List()

linked_list.add_to_start(node1)
# print(linked_list.head.prev)
# print(linked_list.head.forward)

linked_list.add_to_start(node2)
linked_list.add_to_start(node3)
linked_list.add_to_end(node4)


# print(linked_list.head.data)
# print(linked_list.head.forward.data)
# print(linked_list.head.forward.forward.data)
# print(linked_list.head.forward.forward.prev.data)
# print(linked_list.head.forward.prev.data)
# print(linked_list.head.prev)

# print(linked_list.tail.data)
# print(linked_list.tail.prev.data)
linked_list.remove_from_end()
linked_list.remove_from_end()
# print(linked_list.tail.data)


class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


def reverse(head: Node):
    if not head:  # If empty list
        return None
    cur = head
    prev = None
    while True:
        cur2_temporary = cur.next  # To not lose it while reversing
        cur.next = prev  # Reversing

        prev = cur  # Updating for next iteration
        cur = cur2_temporary  # Updating for next iteration

        if cur == head:  # End of cycle
            break
    head.next = prev  # Connecting head and the rest of cyclic list after reverse


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)

# Connect the nodes to form a cyclic list
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node1

# Call the reverse function on the cyclic list
reverse(node1)
print(node1.data)                    # Output: 4
print(node1.next.data)               # Output: 1
print(node1.next.next.data)          # Output: 2
print(node1.next.next.next.data)     # Output: 3
print(node1.next.next.next.next.data)# Output: 4


