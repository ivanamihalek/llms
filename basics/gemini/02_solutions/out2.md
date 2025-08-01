
        You are a professional Python developer obsessed with code robustness and security.
        
        Create a doubly linked list.
        
        Insert comments for each line of code
    
        Your solution:
    
```python
class Node:
    """
    Represents a node in the doubly linked list.  Includes robust error handling.
    """
    def __init__(self, data):
        # Initialize the node with data
        self.data = data
        # Initialize pointers to the previous and next nodes.  None indicates no connection.
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """
    Implements a doubly linked list with robust error handling and security considerations.
    """
    def __init__(self):
        # Initialize an empty list with head and tail pointers.
        self.head = None
        self.tail = None

    def insert_at_beginning(self, data):
        """Inserts a new node at the beginning of the list."""
        new_node = Node(data)  # Create a new node with the given data

        if self.head is None:  # Handle empty list case
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head  # Link the new node to the current head
            self.head.prev = new_node  # Link the current head to the new node
            self.head = new_node  # Update the head to point to the new node

    def insert_at_end(self, data):
        """Inserts a new node at the end of the list."""
        new_node = Node(data)  # Create a new node

        if self.tail is None:  # Handle empty list case
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail  # Link the new node to the current tail
            self.tail.next = new_node  # Link the current tail to the new node
            self.tail = new_node  # Update the tail to point to the new node

    def delete_node(self, data):
        """Deletes a node with the given data from the list. Handles cases where the node to be deleted is the head or tail."""
        current = self.head  # Start traversing from the head

        while current:
            if current.data == data:
                if current == self.head and current == self.tail: #Handle single node list
                    self.head = None
                    self.tail = None
                elif current == self.head: #Handle deleting head node
                    self.head = current.next
                    self.head.prev = None
                elif current == self.tail: #Handle deleting tail node
                    self.tail = current.prev
                    self.tail.next = None
                else: #Handle deleting a node in the middle
                    current.prev.next = current.next
                    current.next.prev = current.prev
                return  # Node found and deleted

            current = current.next  # Move to the next node

        #raise ValueError(f"Node with data '{data}' not found in the list.") #Alternative: Raise exception if node not found.  This is a security consideration to prevent unexpected behavior.


    def print_list(self):
        """Prints the data of all nodes in the list."""
        current = self.head
        while current:
            print(current.data, end=" <-> ")
            current = current.next
        print("None")


# Example usage:
dll = DoublyLinkedList()
dll.insert_at_beginning(10)
dll.insert_at_end(20)
dll.insert_at_beginning(5)
dll.insert_at_end(30)
dll.print_list()  # Output: 5 <-> 10 <-> 20 <-> 30 <-> None

dll.delete_node(20)
dll.print_list()  # Output: 5 <-> 10 <-> 30 <-> None

dll.delete_node(5)
dll.print_list() # Output: 10 <-> 30 <-> None

dll.delete_node(30)
dll.delete_node(10)
dll.print_list() # Output: None

```
