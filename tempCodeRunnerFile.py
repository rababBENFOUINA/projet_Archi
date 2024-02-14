                    print(id)
                    utilisateur_id = id  # Remplacez par l'ID de l'utilisateur que vous souhaitez
                    email_destinataire = recuperer_email_par_id(utilisateur_id)

                    personne = db["personne"]
                    utilisateur = personne.find_one({"_id": utilisateur_id})
                    
                    if email_destinataire:
                        sujet_email = "Alerte : Détection d'une personne sans casque de sécurité"
                        corps_email = """
                                    Cher(e) {} {},

                                    Nous avons détecté que vous avez été capturé(e) par notre système de surveillance sans porter de casque de sécurité.

                                    Détails de la détection :
                                    - Identifiant de la personne : [ID de la personne]
                                    - Date et heure de la détection : [Date et heure]
                                    - Emplacement : [Emplacement]

                                    Veuillez prendre les mesures nécessaires pour assurer votre sécurité et vous conformer aux règles de protection en portant un casque approprié dans la zone surveillée.

                                    Cordialement
                                    """.format(utilisateur.get("nom"),utilisateur.get("prenom"))


                        envoyer_email(email_destinataire, sujet_email, corps_email)
                        print(f"L'e-mail a été envoyé à {email_destinataire}")
                    else:
                        print(f"Aucun utilisateur trouvé avec l'ID {utilisateur_id}")
