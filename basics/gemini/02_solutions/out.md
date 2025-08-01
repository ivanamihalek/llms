
        You are an expert at writing clear concise Python code.
        
        Create a doubly linked list.
        
        Insert comments for each line of code
    
        Your solution:
    
```python
class Node:
    """Represents a node in the doubly linked list."""
    def __init__(self, data):
        """Initializes a node with given data."""
        self.data = data  # Store the data in the node
        self.prev = None  # Pointer to the previous node (initially None)
        self.next = None  # Pointer to the next node (initially None)


class DoublyLinkedList:
    """Represents a doubly linked list."""
    def __init__(self):
        """Initializes an empty doubly linked list."""
        self.head = None  # Head of the list (initially None)
        self.tail = None  # Tail of the list (initially None)

    def insert_at_beginning(self, data):
        """Inserts a new node at the beginning of the list."""
        new_node = Node(data)  # Create a new node with the given data
        if self.head is None:  # If the list is empty
            self.head = new_node  # New node becomes both head and tail
            self.tail = new_node
        else:
            new_node.next = self.head  # New node's next points to the current head
            self.head.prev = new_node  # Current head's previous points to the new node
            self.head = new_node  # New node becomes the new head

    def insert_at_end(self, data):
        """Inserts a new node at the end of the list."""
        new_node = Node(data)  # Create a new node with the given data
        if self.tail is None:  # If the list is empty
            self.head = new_node  # New node becomes both head and tail
            self.tail = new_node
        else:
            new_node.prev = self.tail  # New node's previous points to the current tail
            self.tail.next = new_node  # Current tail's next points to the new node
            self.tail = new_node  # New node becomes the new tail

    def delete_node(self, data):
        """Deletes a node with the given data from the list."""
        current = self.head  # Start from the head
        while current:  # Iterate through the list
            if current.data == data:  # If the data is found
                if current.prev is None:  # If it's the head
                    self.head = current.next  # Update head
                    if self.head: #Handle case where only one node existed
                        self.head.prev = None
                elif current.next is None:  # If it's the tail
                    self.tail = current.prev  # Update tail
                    self.tail.next = None
                else:  # If it's in the middle
                    current.prev.next = current.next  # Update pointers
                    current.next.prev = current.prev
                return  # Node deleted, exit
            current = current.next  # Move to the next node
        print(f"Node with data {data} not found.") #Inform user if node not found


    def print_list(self):
        """Prints the data of all nodes in the list."""
        current = self.head  # Start from the head
        while current:  # Iterate through the list
            print(current.data, end=" ")  # Print the data
            current = current.next  # Move to the next node
        print()  # Newline at the end


# Example usage
dll = DoublyLinkedList()
dll.insert_at_end(1)
dll.insert_at_beginning(0)
dll.insert_at_end(2)
dll.insert_at_beginning(-1)
dll.print_list()  # Output: -1 0 1 2 
dll.delete_node(1)
dll.print_list() # Output: -1 0 2
dll.delete_node(5) # Output: Node with data 5 not found.
dll.delete_node(-1)
dll.print_list() # Output: 0 2

```
