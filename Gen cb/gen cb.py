import random
from datetime import datetime, timedelta

def generate_credit_card(card_type):
    """Génère un numéro de carte bancaire, une date d'expiration et un CVV."""
    if card_type == 'visa':
        prefix = '4'
        length = 16
    elif card_type == 'mastercard':
        prefix = '5'
        length = 16
    else:
        raise ValueError("Type de carte non supporté")
    
    card_number = prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - 1)])
    
    # Générer une date d'expiration aléatoire
    today = datetime.today()
    expiration_date = today + timedelta(days=random.randint(30, 365 * 3))  # 1 mois à 3 ans dans le futur
    exp_date = expiration_date.strftime("%m/%y")
    
    # Générer un CVV aléatoire
    cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
    
    return card_number, exp_date, cvv

def is_valid_card_number(card_number):
    """Vérifie si le numéro de carte est valide en utilisant l'algorithme de Luhn."""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    def luhn_algorithm(card_number):
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        
        for d in even_digits:
            doubled = d * 2
            checksum += doubled if doubled < 10 else doubled - 9
        
        return checksum % 10 == 0
    
    return luhn_algorithm(card_number)

def save_valid_cards(cards):
    """Sauvegarde les cartes valides dans le fichier valid.txt, après avoir vidé le fichier précédent."""
    with open("valid.txt", "w") as file:  # Ouvre le fichier en mode écriture pour effacer le contenu existant
        for card in cards:
            file.write(f"Numéro de Carte: {card[0]}\nDate d'Expiration: {card[1]}\nCVV: {card[2]}\n\n")

def homepage():
    """Affiche la page d'accueil et gère l'entrée de l'utilisateur."""
    while True:
        print("\n  ____ _____ _   _    ____ ____    ______   __ ")
        print(" / ___| ____| \\ | |  / ___| __ )  | __ ) \\ / / ")
        print("| |  _|  _| |  \\| | | |   |  _ \\  |  _ \\\\ V /  ")
        print("| |_| | |___| |\\  | | |___| |_) | | |_) || |   ")
        print(" \\____|_____|_| \\_|__\\____|____/__|____/ |_| _ ")
        print("/ ___|| |/ | \\ / /__  / ____| ____| ____| \\ | |")
        print("\\___ \\| ' / \\ V /  / /|  _| |  _| |  _| |  \\| |")
        print(" ___) | . \\  | |  / /_| |___| |___| |___| |\\  |")
        print("|____/|_|\\_\\ |_| /____|_____|_____|_____|_| \\_|")
        print("                                               ")

        print("\nBienvenue dans le Générateur de Cartes Bancaires !")
        print("Veuillez choisir le type de carte :")
        print("1. Visa")
        print("2. Mastercard")
        
        choice = input("Entrez 1 ou 2 : ")
        
        if choice == '1':
            card_type = 'visa'
        elif choice == '2':
            card_type = 'mastercard'
        else:
            print("Choix invalide ! Défault sur Visa.")
            card_type = 'visa'
        
        try:
            num_cards = int(input("Entrez le nombre de cartes à générer : "))
            if num_cards <= 0:
                raise ValueError("Le nombre de cartes doit être un entier positif.")
        except ValueError as e:
            print(f"Entrée invalide : {e}")
            continue
        
        print(f"\nGénération de {num_cards} cartes {card_type.capitalize()} :")
        
        valid_cards = []
        valid_count = 0
        invalid_count = 0
        
        for _ in range(num_cards):
            card_number, exp_date, cvv = generate_credit_card(card_type)
            valid = "Valide" if is_valid_card_number(card_number) else "Invalide"
            if valid == "Valide":
                valid_count += 1
                valid_cards.append((card_number, exp_date, cvv))
            else:
                invalid_count += 1
            
            print(f"\nNuméro de Carte: {card_number} ({valid})")
            print(f"Date d'Expiration: {exp_date}")
            print(f"CVV: {cvv}")
        
        # Sauvegarde les cartes valides dans le fichier
        save_valid_cards(valid_cards)
        
        print("\nRécapitulatif :")
        print(f"Cartes Valides : {valid_count}")
        print(f"Cartes Invalides : {invalid_count}")
        
        # Demander si l'utilisateur souhaite retourner à l'accueil ou quitter
        again = input("\nSouhaitez-vous générer d'autres cartes ? (oui/non) : ").strip().lower()
        if again != 'oui':
            break

    # Message final et attente de l'entrée de l'utilisateur avant de fermer
    print("\nMerci d'avoir utilisé le Générateur de Cartes Bancaires !")
    input("Appuyez sur Entrée pour quitter...")

# Appelle la fonction d'accueil pour commencer
homepage()
