import pymysql
import os

def generer_markdown(conf):
    """
    Génére le contenu Markdown (front matter + contenu)
    pour une conférence issue de la BDD.
    """
    # Construire le front matter
    front_matter = f"""---
layout: conference
title: "{conf['titre']}"
description: "Une conférence sur {conf['theme']}..."
image: "https://votresite.com/images/conf{conf['id']}.jpg"
permalink: /conferences/conf{conf['id']}/
date_conf: "{conf['date_conference']}"
lieu: "{conf['lieu']}"
nb_place: "{conf['nb_place']}"
prix: "{conf['prix']}"
theme: "{conf['theme']}"
status: "{conf['status']}"
---
"""

    # Contenu Markdown additionnel (par ex. programme, etc.)
    content = f"# Contenu de la conférence {conf['titre']}\n\n"
    content += f"Conférence animée par {conf['presentateur']} le {conf['date_conference']} à {conf['lieu']}.\n"
    content += f"Prix : {conf['prix']} | Places : {conf['nb_place']}\n"
    content += f"Ressource : {conf['resource']}\n"
    
    return front_matter + "\n" + content

def main():
    # 1) Se connecter à la BDD
    connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='pi_3a',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

    try:
        with connection.cursor() as cursor:
            # 2) Récupérer toutes les conférences
            sql = "SELECT * FROM conference"
            cursor.execute(sql)
            conferences = cursor.fetchall()

        # 3) Créer le dossier _conferences s'il n'existe pas
        os.makedirs("_conferences", exist_ok=True)

        # 4) Pour chaque conférence, générer un fichier Markdown
        for conf in conferences:
            filename = f"_conferences/conf{conf['id']}.md"
            md_content = generer_markdown(conf)

            with open(filename, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            print(f"Fichier généré : {filename}")

    finally:
        connection.close()

if __name__ == "__main__":
    main()
