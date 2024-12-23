from core import Livre, Membre, MembrePremium

def populate_library(biblio):
    books = [
        Livre(1, "Introduction to the Theory of Computation", "Michael Sipser", 1996),
        Livre(2, "Structure and Interpretation of Computer Programs", "Harold Abelson, Gerald Jay Sussman", 1985),
        Livre(3, "Clean Code", "Robert C. Martin", 2008),
        Livre(4, "Design Patterns: Elements of Reusable Object-Oriented Software", "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides", 1994),
        Livre(5, "The Pragmatic Programmer", "Andrew Hunt, David Thomas", 1999),
        Livre(6, "Algorithms", "Robert Sedgewick, Kevin Wayne", 1983),
        Livre(7, "Artificial Intelligence: A Modern Approach", "Stuart Russell, Peter Norvig", 1995),
        Livre(8, "Operating System Concepts", "Abraham Silberschatz, Peter Baer Galvin, Greg Gagne", 1983),
        Livre(9, "Computer Networking: A Top-Down Approach", "James F. Kurose, Keith W. Ross", 2000),
        Livre(10, "The Art of Computer Programming", "Donald E. Knuth", 1968),
        Livre(11, "Code Complete", "Steve McConnell", 1993),
        Livre(12, "Compilers: Principles, Techniques, and Tools", "Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman", 1986),
        Livre(13, "Database System Concepts", "Abraham Silberschatz, Henry F. Korth, S. Sudarshan", 1997),
        Livre(14, "You Don't Know JS", "Kyle Simpson", 2014),
        Livre(15, "Computer Organization and Design", "David A. Patterson, John L. Hennessy", 1994),
        Livre(16, "Introduction to Algorithms", "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein", 1990),
        Livre(17, "Software Engineering", "Ian Sommerville", 1982),
        Livre(18, "Programming Pearls", "Jon Bentley", 1986),
        Livre(19, "Deep Learning", "Ian Goodfellow, Yoshua Bengio, Aaron Courville", 2016),
        Livre(20, "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow", "Aurélien Géron", 2017),
        ]
    for book in books:
        biblio.ajouter_livre(book)

    members = [
        Membre(1, "AGUIR", "MARAM",penalty=1.5),
        Membre(2, "AMMAR", "MOHAMED AMINE"),
        Membre(3, "ASKRI", "MOHAMED DHIA",penalty=2),
        Membre(4, "AYARI", "OMAR"),
        Membre(5, "BAATI", "YOSRI"),
        Membre(6, "BEDOUI", "GHAIETH",penalty=7.2),
        MembrePremium(7, "BEN ABDESSALEM", "LINA"),
        Membre(8, "BEN HAJ SLAMA", "MOHAMED"),
        MembrePremium(9, "BEN LAMINE", "ROUA"),
        Membre(10, "BEN NEHIA", "TAYSSIR"),
        Membre(11, "CHOUAIEB", "RANIM"),
        Membre(12, "DAOUED", "MOHAMED ALI"),
        Membre(13, "EL GARES", "MARIEM"),
        Membre(14, "FRAD", "YOSR"),
        Membre(15, "GALAI ZAR", "ANES",penalty=1.8),
        Membre(16, "GMIZA", "MOHAMED AZIZ"),
        Membre(17, "HAOUAS", "EYA"),
        Membre(18, "HENI", "MOHAMED"),
        Membre(19, "KAROUI", "SLAH EDDINE"),
        Membre(20, "KORBI", "ALAA"),
        Membre(21, "MAKHLOUF", "SARRA"),
        Membre(22, "MSAKNI", "SOULEIMA"),
        Membre(23, "OUESLATI", "BEYREM"),
        Membre(24, "OUIRIEMMI", "MOHAMED YASSINE"),
        Membre(25, "REJEB", "YOUSSEF"),
        Membre(26, "RMADA", "KAMEL"),
        Membre(27, "SOUISSI", "HIBA",penalty=4.2),
        Membre(28, "THABET", "MOHAMED AZIZ"),
        Membre(29, "TRITER", "SYRINE"),
        Membre(30, "ZAGAR", "MARAM"),
        MembrePremium(31, "ZAKHAMA", "YASSER"),
    ]
    for member in members:
        biblio.ajouter_membre(member)

