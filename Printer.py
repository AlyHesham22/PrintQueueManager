from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, ttk
import time

# Node class represents an individual element in the circular queue
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# CircularQueue class implements a circular queue using linked nodes
class CircularQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.length = 0

    def enqueue(self, element):
        # Add an element to the end of the queue
        new_node = Node(element)
        if self.isEmpty():
            self.front = self.rear = new_node
            self.rear.next = self.front  # Circular link
        else:
            self.rear.next = new_node
            self.rear = new_node
            self.rear.next = self.front  # Maintain circular link
        self.length += 1

    def dequeue(self):
        # Remove and return the front element of the queue
        if self.isEmpty():
            return None
        temp = self.front
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.front = self.front.next
            self.rear.next = self.front
        self.length -= 1
        return temp.data

    def peek(self):
        if self.isEmpty():
            return None
        return self.front.data

    def isEmpty(self):
        return self.length == 0

    def size(self):
        return self.length

    def to_list(self):
        if self.isEmpty():
            return []
        elements = []
        current = self.front
        while True:
            elements.append(current.data)
            current = current.next
            if current == self.front:
                break
        return elements

# PrintJob class represents a print job with relevant attributes
class PrintJob:
    def __init__(self, job_id, name, priority_label="Normal"):
        self.job_id = job_id
        self.name = name
        self.priority_label = priority_label
        self.status = "Queued"

# PrintQueueManagerGUI class manages the GUI for the print queue manager
class PrintQueueManagerGUI:
    def __init__(self, root):
        self.queue = CircularQueue()
        self.job_id_counter = 1
        self.root = root
        self.root.title("Print Queue Manager")
        self.setup_ui()

    def setup_ui(self):
        self.frame = ttk.LabelFrame(self.root, text="Print Queue")
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(self.frame, columns=("Job ID", "Document Name", "Priority Label", "Status"), show="headings")
        self.tree.heading("Job ID", text="Job ID")
        self.tree.heading("Document Name", text="Document Name")
        self.tree.heading("Priority Label", text="Priority Label")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True)

        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        Button(control_frame, text="Add Job", command=self.add_job_window).grid(row=0, column=0, padx=5, pady=5)
        Button(control_frame, text="Process Next Job", command=self.process_first_job).grid(row=0, column=1, padx=5, pady=5)
        Button(control_frame, text="Process Entire Queue", command=self.process_entire_queue).grid(row=0, column=2, padx=5, pady=5)
        Button(control_frame, text="Exit", command=self.root.destroy).grid(row=0, column=3, padx=5, pady=5)

        self.refresh_queue_display()

    def refresh_queue_display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for job in self.queue.to_list():
            self.tree.insert("", "end", values=(job.job_id, job.name, job.priority_label, job.status))

    def add_job_window(self):
        window = Toplevel(self.root)
        window.title("Add New Job")

        Label(window, text="Job Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = Entry(window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(window, text="Priority:").grid(row=1, column=0, padx=5, pady=5)
        priority_combo = ttk.Combobox(window, values=["Normal", "High", "Urgent"])
        priority_combo.set("Normal")
        priority_combo.grid(row=1, column=1, padx=5, pady=5)

        def add_job():
            name = name_entry.get().strip()
            priority = priority_combo.get()

            if not name:
                messagebox.showerror("Error", "Job name cannot be empty.")
                return

            job = PrintJob(self.job_id_counter, name, priority)
            self.job_id_counter += 1

            self.add_job_by_priority(job)
            self.refresh_queue_display()
            window.destroy()

        Button(window, text="Add Job", command=add_job).grid(row=2, column=0, columnspan=2, pady=10)

    def add_job_by_priority(self, job):
        # Enqueue jobs based on priority
        if self.queue.isEmpty():
            self.queue.enqueue(job)
            return

        temp_queue = CircularQueue()
        inserted = False

        while not self.queue.isEmpty():
            current_job = self.queue.dequeue()
            if not inserted and self.compare_priority(job, current_job):
                temp_queue.enqueue(job)
                inserted = True
            temp_queue.enqueue(current_job)

        if not inserted:
            temp_queue.enqueue(job)

        self.queue = temp_queue

    def compare_priority(self, new_job, existing_job):
        # Determine if the new job has higher priority than the existing job
        priority_order = {"Normal": 1, "High": 2, "Urgent": 3}
        return priority_order[new_job.priority_label] > priority_order[existing_job.priority_label]

    def process_first_job(self):
        if self.queue.isEmpty():
            messagebox.showinfo("Info", "The queue is empty. No jobs to process.")
            return

        job = self.queue.peek()
        job.status = "Printing"
        self.refresh_queue_display()

        messagebox.showinfo("Processing", f"Processing Job: {job.name} with Priority: {job.priority_label}")
        time.sleep(2)

        job.status = "Completed"
        self.queue.dequeue()
        self.refresh_queue_display()

    def process_entire_queue(self):
        while not self.queue.isEmpty():
            self.process_first_job()
            continue_processing = messagebox.askyesno("Continue", "Do you want to continue processing jobs?")
            if not continue_processing:
                break

if __name__ == "__main__":
    root = Tk()
    app = PrintQueueManagerGUI(root)
    root.mainloop()
