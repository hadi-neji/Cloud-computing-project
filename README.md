# Poké Scraper 🐱‍👤

Un TP pour scraper toutes les images des Pokémons depuis **Bulbapedia** et les stocker automatiquement dans un **bucket AWS S3** via un script Python exécuté sur une instance **EC2**.

---

## 🚀 Objectifs
- Déployer une instance EC2 (Amazon Linux 2).
- Installer Python et les dépendances.
- Exécuter un scraper en Python pour télécharger les images Pokémon.
- Uploader automatiquement les images dans S3 via **boto3**.
- Respecter les bonnes pratiques (sécurité IAM, gestion d’erreurs, délais robots.txt).

---

## 📦 Installation

### 1. Lancer une instance EC2
- Type : `t3.micro` (free tier)
- OS : Amazon Linux 2
- Associer un **Security Group** (SSH, HTTP/HTTPS).
- Télécharger la clé `.pem` pour se connecter.

### 2. Connexion SSH
```bash
ssh -i pokemon-key.pem ec2-user@13.61.105.178
