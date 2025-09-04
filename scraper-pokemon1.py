import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import boto3
from botocore.exceptions import ClientError
import time
import logging

# URL cible
URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"

# Configuration S3
BUCKET_NAME = "pokemon-scraper-hadil" 
PREFIX = "images"  # racine dans S3
s3 = boto3.client("s3")

# Logger pour un suivi propre
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def upload_image_to_s3(img_url, filename, category):
    """Télécharge une image depuis le web et l'upload dans S3 si elle n'existe pas déjà"""
    try:
        # Clé S3 (dossier virtuel = prefix/category/filename)
        key = f"{PREFIX}/{category}/{filename}"

        # Vérifier si l'objet existe déjà
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=key)
            logging.info(f"[SKIP] {filename} existe déjà dans S3, pas d'écrasement.")
            return
        except ClientError as e:
            if e.response['Error']['Code'] != "404":
                raise  # autre erreur → la propager

        # Télécharger l’image
        headers = {"User-Agent": "PokemonScraperBot/1.0 (contact: email@example.com)"}
        resp = requests.get(img_url, stream=True, headers=headers, timeout=15)
        resp.raise_for_status()

        # Upload direct vers S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=resp.content,
            ContentType="image/png"
        )

        logging.info(f"[OK] Uploadé sur S3 → s3://{BUCKET_NAME}/{key}")
    except requests.exceptions.RequestException as e:
        logging.error(f"[ERREUR DOWNLOAD] {img_url}: {e}")
    except ClientError as e:
        logging.error(f"[ERREUR S3] {filename}: {e}")
    except Exception as e:
        logging.error(f"[ERREUR INCONNUE] {filename}: {e}")

def scrape_pokemon_images():
    headers = {"User-Agent": "PokemonScraperBot/1.0 (contact: email@example.com)"}
    resp = requests.get(URL, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    generations = soup.find_all("span", {"class": "mw-headline"})

    for gen in generations:
        category = gen.get_text(strip=True).replace(" ", "_")

        # Garder uniquement les sections qui commencent par "Generation"
        if not category.startswith("Generation"):
            continue

        logging.info(f"Scraping {category} ...")

        header_tag = gen.find_parent(["h2", "h3"])
        table = header_tag.find_next("table") if header_tag else None

        if not table:
            logging.warning(f"Pas de tableau trouvé pour {category}")
            continue

        rows = table.find_all("tr")[1:]  # ignorer l'entête
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            dex_num = cols[0].get_text(strip=True).replace("#", "")
            name = cols[2].get_text(strip=True)

            img_tag = cols[1].find("img")
            if not img_tag:
                continue

            src = img_tag.get("src") or img_tag.get("data-src")
            if not src and img_tag.get("srcset"):
                src = img_tag.get("srcset").split(",")[-1].split()[0]
            if not src:
                continue

            img_url = urljoin(URL, src)
            filename = f"{dex_num}_{name}.png"

            upload_image_to_s3(img_url, filename, category)

            # Respect robots.txt → délai entre requêtes
            time.sleep(1)

if __name__ == "__main__":
    scrape_pokemon_images()
