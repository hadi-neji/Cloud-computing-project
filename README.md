# Poké Scraper

Un TP pour scraper toutes les images des Pokémons depuis **Bulbapedia** et les stocker automatiquement dans un **bucket AWS S3** via un script Python exécuté sur une instance **EC2**.

---

## Objectifs
- Déployer une instance EC2 (Amazon Linux 2).
- Installer Python et les dépendances.
- Exécuter un scraper en Python pour télécharger les images Pokémon.
- Uploader automatiquement les images dans S3 via **boto3**.
- Respecter les bonnes pratiques (sécurité IAM, gestion d’erreurs, délais robots.txt).

---

## Installation

### 1. Lancer une instance EC2
- Type : `t3.micro` (free tier)
- OS : Amazon Linux 2
- Associer un **Security Group** (SSH, HTTP/HTTPS).
- Télécharger la clé `.pem` pour se connecter.

### 2. Connexion SSH
```bash
ssh -i pokemon-key.pem ec2-user@13.61.105.178

### 3. Installer Python et Git
```bash
sudo yum update -y
sudo yum install -y python3 git
python3 -m pip install --upgrade pip
```

### 4. Cloner le projet et installer les dépendances
```bash
git clone https://github.com/<username>/pokemon-scraper.git
cd pokemon-scraper
pip3 install -r requirements.txt
```

### 5. Configurer AWS CLI
```bash
aws configure
```


### 6. Lancer le script
```bash
python3 scraper.py
```

---

##  Organisation S3
Les images sont envoyées dans le bucket S3 avec la structure suivante :  
```
s3://pokemon-scraper-hadil/images/Generation_I/0001_Bulbasaur.png
s3://pokemon-scraper-hadil/images/Generation_II/0152_Chikorita.png
...
```

---

## Vérification
- Via la **console S3** ou la **CLI** :
```bash
aws s3 ls s3://pokemon-scraper-hadil/images/ --recursive
```
- Exemple d’accès public :  
[https://pokemon-scraper-hadil.s3.eu-north-1.amazonaws.com/images/Generation_II/0152_Chikorita.png](https://pokemon-scraper-hadil.s3.eu-north-1.amazonaws.com/images/Generation_II/0152_Chikorita.png)

---

## 🔐 Sécurité
- Pas de clés AWS en dur dans le code.
- Permissions IAM limitées au bucket concerné.
- Respect robots.txt (1 seconde entre requêtes).

---

## 📊 Architecture
![Architecture](docs/architecture.png)  
*(Instance EC2 → Scraper Python → Upload vers S3 → Accès public via URL S3)*


