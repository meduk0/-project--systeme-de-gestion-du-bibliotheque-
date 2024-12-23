from datetime import timedelta

class Livre:
    def __init__(self, id_livre, titre, auteur, annee_publication):
        self.id_livre = id_livre
        self.titre = titre
        self.auteur = auteur
        self.annee_publication = annee_publication
        self.disponible = True
        self.reserve = False
        self.queue_reservations = []  # Liste des ID des membres qui ont réservé

    def afficher_details(self):
        return f"ID: {self.id_livre}, Titre: {self.titre}, Auteur: {self.auteur}, Année: {self.annee_publication}, Disponible: {self.disponible}, Réservé: {self.reserve}"

    def changer_statut(self, disponible):
        self.disponible = disponible

    def ajouter_reservation(self, membre_id):
        if membre_id not in self.queue_reservations:
            self.queue_reservations.append(membre_id)
            self.reserve = True
            return True
        return False

    def get_prochain_reservateur(self):
        if self.queue_reservations:
            return self.queue_reservations[0]
        return None

    def retirer_reservation(self, membre_id):
        if membre_id in self.queue_reservations:
            self.queue_reservations.remove(membre_id)
            if not self.queue_reservations:
                self.reserve = False
            return True
        return False


class Membre:
    def __init__(self, id_membre, nom, prenom, penalty=0):
        self.id_membre = id_membre
        self.nom = nom
        self.prenom = prenom
        self.penalites = penalty 
        self.liste_emprunts = []
        self._premium = False  # par defaut faux 

    @property
    def premium(self):
        return self._premium

    @premium.setter
    def premium(self, value):
        if value and not self._premium:
            self._premium = True
            self.reduction_penalite = 0.5
        elif not value and self._premium:
            self._premium = False
            self.reduction_penalite = None

    def __str__(self):
        return f"{self.nom} {self.prenom} (Premium: {self.premium})"

    def emprunter_livre(self, livre, date_emprunt):
        if livre.disponible:
            livre.changer_statut(False)
            self.liste_emprunts.append((livre, date_emprunt))
        else:
            raise Exception("Le livre n'est pas disponible.")

    def retourner_livre(self, livre, date_retour):
        for emprunt in self.liste_emprunts:
            if emprunt[0] == livre:
                self.liste_emprunts.remove(emprunt)
                livre.changer_statut(True)

                # Calculate penalties for late return
                due_date = emprunt[1] + timedelta(days=14)
                if date_retour > due_date:
                    retard = (date_retour - due_date).days
                    self.penalites += retard
                return
        raise Exception("Ce livre n'a pas été emprunté par ce membre.")

class MembrePremium(Membre):
    def __init__(self, id_membre, nom, prenom, reduction_penalite=0.5, liste_emprunts=None, penalites=0):
        super().__init__(id_membre, nom, prenom)
        self.reduction_penalite = reduction_penalite
        self.liste_emprunts = liste_emprunts if liste_emprunts is not None else []
        self.penalites = penalites

    def retourner_livre(self, livre, date_retour):
        super().retourner_livre(livre, date_retour)
        self.penalites = round(self.penalites * (1 - self.reduction_penalite), 2)

class Bibliotheque:
    def __init__(self):
        self.catalogue_livres = []
        self.membres = []
        self.historique_emprunts = []

    def ajouter_livre(self, livre):
        self.catalogue_livres.append(livre)

    def ajouter_membre(self, membre):
        self.membres.append(membre)

    def trouver_membre(self, id_membre):
        return next((m for m in self.membres if m.id_membre == id_membre), None)

    def trouver_livre(self, id_livre):
        return next((l for l in self.catalogue_livres if l.id_livre == id_livre), None)

    def gerer_emprunt(self, id_membre, id_livre, date_emprunt, date_retour):
        membre = self.trouver_membre(id_membre)
        livre = self.trouver_livre(id_livre)

        if membre and livre:
            membre.emprunter_livre(livre, date_emprunt)
            self.historique_emprunts.append((membre, livre, date_emprunt, date_retour))
        else:
            raise Exception("Membre ou livre introuvable.")

    def gerer_retour(self, id_membre, id_livre, date_retour):
        membre = self.trouver_membre(id_membre)
        livre = self.trouver_livre(id_livre)

        if membre and livre:
            membre.retourner_livre(livre, date_retour)

            # Update the history with the actual return date
            for i, emprunt in enumerate(self.historique_emprunts):
                if emprunt[1] == livre and emprunt[0] == membre:
                    self.historique_emprunts[i] = (emprunt[0], emprunt[1], emprunt[2], date_retour)
                    break
        else:
            raise Exception("Membre ou livre introuvable.")
    def promouvoir_membre_premium(self, id_membre):
        membre = self.trouver_membre(id_membre)
        if not membre:
            raise Exception("Membre introuvable.")

        if isinstance(membre, MembrePremium):
            raise Exception(f"Le membre {membre.nom} {membre.prenom} est déjà Premium.")

        # Replace with MembrePremium instance
        premium_member = MembrePremium(
            id_membre=membre.id_membre,
            nom=membre.nom,
            prenom=membre.prenom,
            penalites=membre.penalites,
            liste_emprunts=membre.liste_emprunts,
        )
        self.membres = [
            premium_member if m.id_membre == id_membre else m
            for m in self.membres
        ]
