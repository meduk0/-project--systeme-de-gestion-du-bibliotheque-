from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from core import Livre , Membre, MembrePremium, Bibliotheque
from exemple_data import populate_library

class LibraryUI:
    def __init__(self, root):
        self.biblio = Bibliotheque()
        populate_library(self.biblio)
        self.root = root
        self.root.title("Systeme de management du bibliotheque")
        self.root.geometry("1000x700")

        # Styling
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TEntry", padding=5)

        # Frames
        self.frame_books = ttk.LabelFrame(self.root, text="Books")
        self.frame_members = ttk.LabelFrame(self.root, text="Members")
        self.frame_actions = ttk.LabelFrame(self.root, text="Actions")
        self.frame_books.pack(fill="both", expand=True, padx=10, pady=5)
        self.frame_members.pack(fill="both", expand=True, padx=10, pady=5)
        self.frame_actions.pack(fill="both", expand=True, padx=10, pady=5)

        # Search Book Frame
        self.frame_search_books = ttk.Frame(self.frame_books)
        self.frame_search_books.pack(fill="x", padx=10, pady=5)
        self.search_book_label = ttk.Label(self.frame_search_books, text="Search Book:")
        self.search_book_label.pack(side="left", padx=5)
        self.search_book_entry = ttk.Entry(self.frame_search_books, width=20)
        self.search_book_entry.pack(side="left", padx=5)
        self.search_book_button = ttk.Button(self.frame_search_books, text="Search", command=self.search_book)
        self.search_book_button.pack(side="left", padx=5)

        # Book Treeview
        self.tree_books = ttk.Treeview(
        self.frame_books, 
        columns=("ID", "Title", "Author", "Year", "Available", "Reserved By", "Return Date"), 
        show="headings")
        self.tree_books.heading("Reserved By", text="Reserved By")
        self.tree_books.heading("ID", text="ID")
        self.tree_books.heading("Title", text="Title")
        self.tree_books.heading("Author", text="Author")
        self.tree_books.heading("Year", text="Year")
        self.tree_books.heading("Available", text="Available")
        self.tree_books.heading("Return Date", text="Return Date")
        self.tree_books.heading("Reserved By", text="Reserved By")
        self.tree_books.pack(fill="both", expand=True)

        # Search Member Frame
        self.frame_search_members = ttk.Frame(self.frame_members)
        self.frame_search_members.pack(fill="x", padx=10, pady=5)
        self.search_member_label = ttk.Label(self.frame_search_members, text="Search Member:")
        self.search_member_label.pack(side="left", padx=5)
        self.search_member_entry = ttk.Entry(self.frame_search_members, width=20)
        self.search_member_entry.pack(side="left", padx=5)
        self.search_member_button = ttk.Button(self.frame_search_members, text="Search", command=self.search_member)
        self.search_member_button.pack(side="left", padx=5)

        # Member Treeview
        self.tree_members = ttk.Treeview(self.frame_members, columns=("ID", "Name", "Borrowed Books", "Penalties", "Premium"), show="headings")
        self.tree_members.heading("ID", text="ID")
        self.tree_members.heading("Name", text="Name")
        self.tree_members.heading("Borrowed Books", text="Borrowed Books")
        self.tree_members.heading("Penalties", text="Penalties")
        self.tree_members.heading("Premium", text="Premium")
        self.tree_members.pack(fill="both", expand=True)

        # Action Buttons
        ttk.Button(self.frame_actions, text="Add Book", command=self.add_book).pack(side="left", padx=10, pady=5)
        ttk.Button(self.frame_actions, text="Add Member", command=self.add_member).pack(side="left", padx=10, pady=5)
        ttk.Button(self.frame_actions, text="Borrow Book", command=self.borrow_book).pack(side="left", padx=10, pady=5)
        ttk.Button(self.frame_actions, text="Return Book", command=self.return_book).pack(side="left", padx=10, pady=5)
        ttk.Button(self.frame_actions, text="Make Premium", command=self.make_premium).pack(side="left", padx=10, pady=5)
        ttk.Button(self.frame_actions, text="View History", command=self.view_history).pack(side="left", padx=10, pady=5)
        ttk.Button(self.frame_actions, text="Reserve Book", command=self.reserve_book).pack(side="left", padx=10, pady=5)
        ttk.Button(self.frame_actions, text="Refresh", command=self.refresh_data).pack(side="left", padx=10, pady=5)

    def refresh_data(self):
        self.refresh_books()
        self.refresh_members()

    def refresh_books(self, search_query=""):
    
        self.tree_books.delete(*self.tree_books.get_children())  # Clear Treeview
        for book in self.biblio.catalogue_livres:
            if search_query.lower() in book.titre.lower() or search_query.lower() in book.auteur.lower():
                reserved_by = ""
                if book.reserve and book.queue_reservations:
                    reserved_by = self.biblio.trouver_membre(book.queue_reservations[0]).nom +self.biblio.trouver_membre(book.queue_reservations[0]).prenom
                return_date = ""
                for emprunt in self.biblio.historique_emprunts:
                    if emprunt[1].id_livre == book.id_livre and emprunt[3]:
                        return_date = emprunt[3].strftime("%Y-%m-%d")
                        break
                self.tree_books.insert(
                    "", "end", values=(
                        book.id_livre, book.titre, book.auteur, book.annee_publication,
                        book.disponible, reserved_by, return_date
                    )
                )

    def refresh_members(self, search_query=""):
        self.tree_members.delete(*self.tree_members.get_children())  
        for member in self.biblio.membres:
            if (
                search_query.lower() in member.nom.lower() or
                search_query.lower() in member.prenom.lower() or
                search_query in str(member.id_membre)
            ):
                premium_status = "Yes" if isinstance(member, MembrePremium) else "No"
                self.tree_members.insert(
                    "", "end", values=(
                        member.id_membre,
                        f"{member.nom} {member.prenom}",
                        len(member.liste_emprunts),
                        member.penalites,
                        premium_status
                    )
                )

    def search_book(self):
        search_query = self.search_book_entry.get()
        self.refresh_books(search_query)

    def search_member(self):
        search_query = self.search_member_entry.get()
        self.refresh_members(search_query)

    def add_book(self):
        try:
            title = simpledialog.askstring("Add Book", "Enter book title:")
            author = simpledialog.askstring("Add Book", "Enter author name:")
            year = int(simpledialog.askstring("Add Book", "Enter publication year:"))
            
            if any(book.titre.lower() == title.lower() and book.auteur.lower() == author.lower() 
                for book in self.biblio.catalogue_livres):
                messagebox.showwarning("Duplicate Book", "This book already exists in the catalog.")
                return
            
            new_book = Livre(len(self.biblio.catalogue_livres) + 1, title, author, year)
            self.biblio.ajouter_livre(new_book)
            self.refresh_books()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")

    def add_member(self):
        try:
            name = simpledialog.askstring("Add Member", "Enter member name:")
            prenom = simpledialog.askstring("Add Member", "Enter member first name:")

            if any(member.nom.lower() == name.lower() and member.prenom.lower() == prenom.lower() 
                for member in self.biblio.membres):
                messagebox.showwarning("Duplicate Member", "This member already exists.")
                return
            
            new_member = Membre(len(self.biblio.membres) + 1, name, prenom)
            self.biblio.ajouter_membre(new_member)
            self.refresh_members()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add member: {e}")


    def borrow_book(self):
        try:
            id_membre = int(simpledialog.askstring("Borrow Book", "Enter member ID:"))
            id_livre = int(simpledialog.askstring("Borrow Book", "Enter book ID:"))
            return_date = datetime.now() + timedelta(days=14)
            self.biblio.gerer_emprunt(id_membre, id_livre, datetime.now(), return_date)
            messagebox.showinfo("Success", f"Book borrowed successfully! Return date: {return_date.strftime('%Y-%m-%d')}")
            self.refresh_books()
            self.refresh_members()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to borrow book: {e}")

    def return_book(self):
        try:
            id_membre = int(simpledialog.askstring("Return Book", "Enter member ID:"))
            id_livre = int(simpledialog.askstring("Return Book", "Enter book ID:"))
            self.biblio.gerer_retour(id_membre, id_livre, datetime.now())
            messagebox.showinfo("Success", "Book returned successfully!")
            self.refresh_books()
            self.refresh_members()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {e}")
    def gerer_retour(self, id_membre, id_livre, date_retour):
        # Retrieve the book and member objects
        livre = self.trouver_livre(id_livre)
        membre = self.trouver_membre(id_membre)
        
        if not livre or not membre:
            print("Error: Book or member not found.")
            return

        if livre not in membre.liste_emprunts:
            print(f"Error: Member {membre.nom} {membre.prenom} has not borrowed the book '{livre.titre}'.")
            return

        membre.liste_emprunts.remove(livre)


        if livre.queue_reservations:
            # lend the book to the first one in the queue 
            next_member_id = livre.queue_reservations.pop(0)
            next_member = self.trouver_membre(next_member_id)
            if next_member:
                next_member.liste_emprunts.append(livre)  # the next one 
                livre.disponible = False  # rendre le livre indesponible 
                print(f"Book '{livre.titre}' is now reserved and borrowed by {next_member.nom} {next_member.prenom}.")
            else:
                print(f"Warning: Member with ID {next_member_id} not found in the system.")
        else:
            livre.disponible = True

        # Update borrowing history with the return date
        for emprunt in self.historique_emprunts:
            if emprunt[0] == membre and emprunt[1] == livre and emprunt[3] is None:
                emprunt[3] = date_retour  # Record the return date
                break

        print(f"Book '{livre.titre}' returned successfully by {membre.nom} {membre.prenom}.")



    def make_premium(self):
        try:
            id_membre = int(simpledialog.askstring("Make Premium", "Enter member ID:"))
            membre = self.biblio.trouver_membre(id_membre)
            if membre:
                if not isinstance(membre, MembrePremium):
                    self.biblio.promouvoir_membre_premium(id_membre)
                    messagebox.showinfo("Success", 
                        f"Member {membre.nom} {membre.prenom} is now Premium!")
                else:
                    messagebox.showinfo("Info", 
                        f"Member {membre.nom} {membre.prenom} is already Premium.")
                self.refresh_members()
            else:
                messagebox.showwarning("Not Found", "Member not found!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid member ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make member premium: {e}")
    
    def reserve_book(self):
        try:
            id_membre = int(simpledialog.askstring("Reserve Book", "Enter member ID:"))
            id_livre = int(simpledialog.askstring("Reserve Book", "Enter book ID:"))
            livre = self.biblio.trouver_livre(id_livre)
            membre = self.biblio.trouver_membre(id_membre)

            if not livre:
                messagebox.showwarning("Not Found", "Book not found!")
                return
            if not membre:
                messagebox.showwarning("Not Found", "Member not found!")
                return

            if livre.disponible:
                messagebox.showinfo("Available", "The book is currently available. Consider borrowing it instead.")
                return

            if livre.ajouter_reservation(id_membre):
                messagebox.showinfo("Success", f"Book '{livre.titre}' reserved successfully for {membre.nom} {membre.prenom}!")
            else:
                messagebox.showwarning("Already Reserved", "You have already reserved this book.")

            self.refresh_books()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid IDs for both member and book.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reserve book: {e}")
    def ajouter_reservation(self, id_membre):
        if id_membre in self.queue_reservations:
            return False  # Member already reserved
        self.queue_reservations.append(id_membre)
        return True

    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Borrowing History")
        tree_history = ttk.Treeview(history_window, columns=("Member", "Book", "Date", "Return Date"), show="headings")
        tree_history.heading("Member", text="Member")
        tree_history.heading("Book", text="Book")
        tree_history.heading("Date", text="Date")
        tree_history.heading("Return Date", text="Return Date")
        tree_history.pack(fill="both", expand=True)

        for emprunt in self.biblio.historique_emprunts:
            membre, livre, date_emprunt, return_date = emprunt
            tree_history.insert("", "end", values=(
                f"{membre.nom} {membre.prenom}", livre.titre, date_emprunt.strftime("%Y-%m-%d"), return_date.strftime("%Y-%m-%d")
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryUI(root)
    root.mainloop()
