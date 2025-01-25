
        You are a professional Python developer obsessed with code robustness and type safety.
        
        Create a doubly linked list. Prove unit test for each class and function you define, except the main.
        
        Insert comments for each line of code. Make sure your code has a main function
    
        Your solution:
    
```python
import unittest

class Node:
    """
    Represents a node in the doubly linked list.
    """
    def __init__(self, data: int) -> None:  # Type hinting for data
        """Initializes a new node."""
        self.data = data  # Node's data
        self.prev = None  # Pointer to the previous node
        self.next = None  # Pointer to the next node

class DoublyLinkedList:
    """
    Represents a doubly linked list.
    """
    def __init__(self) -> None:
        """Initializes an empty doubly linked list."""
        self.head = None  # Head of the list
        self.tail = None  # Tail of the list

    def append(self, data: int) -> None:
        """Appends a new node with the given data to the end of the list."""
        new_node = Node(data)  # Create a new node
        if not self.head:  # If the list is empty
            self.head = new_node  # Set the new node as the head
            self.tail = new_node  # Set the new node as the tail
        else:
            new_node.prev = self.tail  # Set the previous node of the new node to the current tail
            self.tail.next = new_node  # Set the next node of the current tail to the new node
            self.tail = new_node  # Update the tail to the new node


    def prepend(self, data: int) -> None:
        """Prepends a new node with the given data to the beginning of the list."""
        new_node = Node(data) # Create a new node
        if not self.head: # If the list is empty
            self.head = new_node # Set the new node as the head
            self.tail = new_node # Set the new node as the tail
        else:
            new_node.next = self.head # Set the next node of the new node to the current head
            self.head.prev = new_node # Set the previous node of the current head to the new node
            self.head = new_node # Update the head to the new node

    def delete(self, data: int) -> bool:
        """Deletes the first node with the given data from the list."""
        current = self.head # Start from the head
        while current: # Iterate through the list
            if current.data == data: # If the data is found
                if current == self.head and current == self.tail: # If it's the only node
                    self.head = None # Set head and tail to None
                    self.tail = None
                elif current == self.head: # If it's the head node
                    self.head = current.next # Update the head
                    self.head.prev = None # Set the previous of the new head to None
                elif current == self.tail: # If it's the tail node
                    self.tail = current.prev # Update the tail
                    self.tail.next = None # Set the next of the new tail to None
                else: # If it's a node in the middle
                    current.prev.next = current.next # Update the next pointer of the previous node
                    current.next.prev = current.prev # Update the previous pointer of the next node
                return True # Indicate successful deletion
            current = current.next # Move to the next node
        return False # Indicate that the data was not found


    def __str__(self) -> str:
        """Returns a string representation of the list."""
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes)


class TestNode(unittest.TestCase):
    def test_node_creation(self):
        node = Node(10)
        self.assertEqual(node.data, 10)
        self.assertIsNone(node.prev)
        self.assertIsNone(node.next)

class TestDoublyLinkedList(unittest.TestCase):
    def test_append(self):
        dll = DoublyLinkedList()
        dll.append(1)
        dll.append(2)
        self.assertEqual(str(dll), "1 -> 2")

    def test_prepend(self):
        dll = DoublyLinkedList()
        dll.prepend(1)
        dll.prepend(2)
        self.assertEqual(str(dll), "2 -> 1")

    def test_delete(self):
        dll = DoublyLinkedList()
        dll.append(1)
        dll.append(2)
        dll.append(3)
        dll.delete(2)
        self.assertEqual(str(dll), "1 -> 3")
        dll.delete(1)
        self.assertEqual(str(dll), "3")
        dll.delete(3)
        self.assertEqual(str(dll), "")
        self.assertFalse(dll.delete(4)) #test deleting non-existent element


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False) # Run unit tests
    #Example usage (uncomment to run)
    # dll = DoublyLinkedList()
    # dll.append(1)
    # dll.append(2)
    # dll.prepend(0)
    # print(dll)  # Output: 0 -> 1 -> 2
    # dll.delete(1)
    # print(dll)  # Output: 0 -> 2

```
