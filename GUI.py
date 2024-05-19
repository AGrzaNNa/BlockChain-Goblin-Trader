import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyperclip


class GUI:
    """
    A graphical user interface (GUI) for interacting with the Goblin Trader Coin blockchain.

    Attributes:
        root (tk.Tk): The root window of the GUI.
        label (tk.Label): The main label displaying the app title.
        image (Image): The loaded image object for the logo.
        photo (ImageTk.PhotoImage): The image object formatted for Tkinter.
        image_label (tk.Label): The label widget to display the image.
        button_frame (tk.Frame): The frame containing the action buttons.
        mine_button (tk.Button): Button to mine a new block.
        view_chain_button (tk.Button): Button to view the blockchain.
        new_transaction_button (tk.Button): Button to create a new transaction.
        view_wallet_button (tk.Button): Button to view the wallet balance.
        copy_button (tk.Button): Button to copy the wallet ID to clipboard.
    """

    def __init__(self, root):
        """
        Initializes the GUI with buttons and labels.

        Args:
            root (tk.Tk): The root window of the GUI.
        """
        self.root = root
        self.root.title("Goblin Trader Coin")
        self.root.configure(bg='#006400')

        self.label = tk.Label(root, text="Goblin Trader", font=("Helvetica", 16), fg="gold", bg="#006400")
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        self.image = Image.open("GoblinTrader.png")
        self.image = self.image.resize((250, 250), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(root, image=self.photo, bg="#006400")
        self.image_label.grid(row=1, column=0, pady=10, padx=20)

        self.button_frame = tk.Frame(root, bg="#006400")
        self.button_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.mine_button = tk.Button(self.button_frame, text="Mine block", command=self.mine)
        self.mine_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.view_chain_button = tk.Button(self.button_frame, text="View Chain", command=self.view_chain)
        self.view_chain_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.new_transaction_button = tk.Button(self.button_frame, text="New Transaction", command=self.new_transaction)
        self.new_transaction_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.view_wallet_button = tk.Button(self.button_frame, text="My Wallet", command=self.view_wallet)
        self.view_wallet_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.copy_button = tk.Button(self.button_frame, text="Copy Wallet ID", command=self.copy_to_clipboard)

    def mine(self):
        """
        Handles the mining of a new block.

        Sends a GET request to the server to mine a new block and shows a message box with the result.
        """
        response = requests.get('http://localhost:5000/mine')
        if response.status_code == 200:
            messagebox.showinfo("Success", "New Block Forged")
        else:
            messagebox.showerror("Error", "Failed to mine block")

    def view_chain(self):
        """
        Displays the full blockchain.

        Sends a GET request to the server to retrieve the blockchain and shows a message box with the chain data.
        """
        response = requests.get('http://localhost:5000/chain')
        if response.status_code == 200:
            chain = response.json()['chain']
            length = response.json()['length']
            chain_str = "\n".join([f"Block {block['index']}: {block['transactions']}" for block in chain])
            messagebox.showinfo("Blockchain", f"Chain Length: {length}\n\n{chain_str}")
        else:
            messagebox.showerror("Error", "Failed to retrieve blockchain")

    def new_transaction(self):
        """
        Opens a new window to create a new transaction.

        Collects sender, recipient, and amount information and sends a POST request to create a new transaction.
        """
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("New Transaction")

        sender_label = tk.Label(transaction_window, text="Sender:")
        sender_label.grid(row=0, column=0, padx=10, pady=5)
        sender_entry = tk.Entry(transaction_window)
        sender_entry.grid(row=0, column=1, padx=10, pady=5)

        recipient_label = tk.Label(transaction_window, text="Recipient:")
        recipient_label.grid(row=1, column=0, padx=10, pady=5)
        recipient_entry = tk.Entry(transaction_window)
        recipient_entry.grid(row=1, column=1, padx=10, pady=5)

        amount_label = tk.Label(transaction_window, text="Amount:")
        amount_label.grid(row=2, column=0, padx=10, pady=5)
        amount_entry = tk.Entry(transaction_window)
        amount_entry.grid(row=2, column=1, padx=10, pady=5)

        def submit_transaction():
            """
            Submits the new transaction data to the server.

            Collects input data from entry fields, validates them, and sends a POST request to create the transaction.
            """
            sender = sender_entry.get()
            recipient = recipient_entry.get()
            amount = amount_entry.get()

            if not sender or not recipient or not amount:
                messagebox.showerror("Error", "All fields are required")
                return

            response = requests.post('http://localhost:5000/transactions/new', json={
                'sender': sender,
                'recipient': recipient,
                'amount': amount
            })

            if response.status_code == 201:
                messagebox.showinfo("Success", "Transaction created successfully")
                transaction_window.destroy()
            elif response.status_code == 403:
                messagebox.showerror("Error", "Insufficient balance for transaction")
                transaction_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to create transaction")

        submit_button = tk.Button(transaction_window, text="Submit", command=submit_transaction)
        submit_button.grid(row=3, columnspan=2, padx=10, pady=10)

    def view_wallet(self):
        """
        Displays the wallet balance and node identifier.

        Sends a GET request to the server to retrieve wallet information and shows a message box with the data.
        """
        response = requests.get('http://localhost:5000/wallet')
        if response.status_code == 200:
            node_identifier = response.json()['node_identifier']
            balance = response.json()['balance']

            wallet_info = f"Node Identifier: {node_identifier}\nBalance: {balance}"

            messagebox.showinfo("Wallet", wallet_info)
            self.copy_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        else:
            messagebox.showerror("Error", "Failed to retrieve wallet information")

    def copy_to_clipboard(self):
        """
        Copies the wallet ID to the clipboard.

        Sends a GET request to the server to retrieve the node identifier and copies it to the clipboard.
        """
        response = requests.get('http://localhost:5000/wallet')
        if response.status_code == 200:
            node_identifier = response.json()['node_identifier']
            pyperclip.copy(node_identifier)
            messagebox.showinfo("Wallet", "Node identifier copied to clipboard")
        else:
            messagebox.showerror("Error", "Failed to retrieve wallet information")


if __name__ == "__main__":
    root = tk.Tk()
    blockchain_gui = GUI(root)
    root.mainloop()
