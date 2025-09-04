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
![Architecture]([docs/architecture.png](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Pokemon%20Scraper%20Architecture%22%20id%3D%22VL7GVqtdrI3ahUQLlkzp%22%3E1Zddb9owFIZ%2FjaXuYlKISQiXgdEPrdWmon3cTSY%2BgFcnpo5TYL9%2Bx4kDhMDabaVbbyL7tY3t9%2FE5NoQO09WFZov5jeIgie%2FxFaHviO%2F3aAe%2FVlhXQhT0KmGmBa%2BkzlYYix%2FgRM%2BpheCQNzoapaQRi6aYqCyDxDQ0prVaNrtNlWzOumAzaAnjhMm2%2BkVwM3e78Htb%2FRLEbF7P3An7VUvK6s5uJ%2FmccbXckeiI0KFWylSldDUEab2rfanGnR9p3SxMQ2aeMsDvFeuunt0%2FqOspDz58L8zn%2FK37lQcmC7dhcu6R%2Fjnpd0jcxZZPRkiRMwOFJn5IfIpg6OAqvnGbMuvaKdzfwhZxVoSDpcFUSDlUUumyA%2BUMommCem60uoOdljCJYDK1I1Rm3BnodOu6m6JeKmgDq6MedDbO4okElYLRa%2BziBtQs1nXV1ZdbtJ3IafNdrIETmTtOs81Pbx3HgjP9NwD4RwH4ZDDAltHQtl9luWFZAli8Flmx2mFxNk4w8gDxeB%2FXZq6yN0fRaIwQls2sPNCqyDjw0tgWqukUwuQgKt7rTzzvBVBRr8lqw2WH1YZfg5V%2FKlb0GKs4JjE2emP7GRTJHZgdQCLFJJHjjBeQgWZGqOzbV7uSY5iStRTIBh0fLOfCwHjBEqsvkTNqc5NKh21SQbyeyMMceQAR7x7iGPkTGoYvwDGIHud4OOb6p%2BLYbTkPGY%2FtZYG1iVTJ3S%2BTVDUaeOvi2LMEZ1CFTuDx9GuYnoF5LEu0LdYg8Tg9NNfx7HYFf2TX5oA9o13%2BE%2B2i%2F9KusJUlhvZtssKwtz7Yz3h82fIUI8w0g5tJMctsOkCfymRg41Dg0yR2DangvMzlh7LENr97Gwh%2Fd3d29i5PP2gFcnggjumpwjhqGV0%2BS7xbJe09SUY%2BiUJ7j%2BIuQacizxEB5mFPilQYMqQk7tu8XKbt10aD7tMIn5hWT4ajXtAOjzOWJIC2T2Tp86KYSHFfQGr3iB0Fsw%2FM2%2Bv2g%2BW%2Ftz%2FoBw37qX%2FA%2FuBF7W8%2F5ePSfdTeg1068e17cgyJts%2BTSnxtvtO9U98%2FYPszJSGsbv%2BclW07%2F3Dp6Cc%3D%3C%2Fdiagram%3E%3Cdiagram%20id%3D%229yp3ivm4WdT2OcnXW7V3%22%20name%3D%22Page-2%22%3E1ZfbcpswEIafRjPpRTuAbAyX2HUObdJ24mnTu45Aa6OJQK4sYrtP3xXgAwE3bpukzQ0jfklI%2Bj%2FtShA6ylZnms3TK8VBEs%2FhK0LfEs8LBz4%2BrbCuBD9wK2GmBa8kZydMxA%2BoRHejFoLDotYqySgljZg3xUTlOSSmoTGt1bLZbKokbwhzNoPGNKwwSZiEVrMbwU1aqYE32OnnIGbpZmTXD6uajG0a1x9epIyr5Z5Ex4SOtFKmKmWrEUjrXdOX0wO124lpyM0xHfrBpw%2BrWRjKgk9voi837sd3%2Bev6K3dMFvWCyalDwlMSuiTqYc1nI6RYMAOFJh6ypAiGDi%2Biq3pRZr1xCtc3t0UcFeFgaTgVUo6UVLpsQDmDYJqgvjBa3cJejZ8EEE9tD5Wbeg%2B4vc17PcRmqqANrA564G6dxR0JKgOj19hk04HSqku9Gwf0Tb8Slju4blATS%2FfB9muR1Rtqtv34znMs1Lb%2FBgLvIAKPDIdYMx7Z%2Bot8YVieABYvRV6s9micTBKMPUBAzqe1SVX%2B6iAcjTHC8pmVh1oVOQdeWtuCNZ2Cn3TC4oMwdpxngNVzm7D6XbA8pwuW91Sw6CFYUUQirHQm9jEsklswe4REhnligSOeQQ6aGaHyb1%2FtTA5xStZSIBy0fLhMhYHJnCVWXyJo1FKTyZpbXFG8jGU3SN6HgPe6QAZeTH3%2FGUD64REgu6MufCqQvZb1kPPIHhj4FkuV3P4yUVW9gW8Oj0Oe4Aiq0Ak8nIIN0zMwD%2BWJtscaJO6nu%2BY8Ht2u%2Fh%2FZtd1hj2iXd6Rd9F%2Fa5bfSxMjeT1YY99YH%2B5hMzlueYoiZZnQzKWa5zQfoU5kNbCAKvJ5EdUUmOC%2BzeVea2GV4ZwvhryKZes1IDoOOSPY7Apk%2BVRwPWk6XdxPnWkl7VJKxRwLfHqW4TNCZWCyQAWZiR4pMGDKiJAptZi4T90vD0buHA683x2bWJwMStICcsCQB9D2WpdHzIpbiewGZXSQ2FMxeM68v25eW%2F97%2FgRM0%2FQ87%2Fe8%2Fp%2F9hy%2F%2BotB%2B192DnTjx7qZxAou0VpRJfmvFu797G9zuNf6RMhK%2B737Sybu9fl45%2FAg%3D%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E#%7B%22pageId%22%3A%22VL7GVqtdrI3ahUQLlkzp%22%7D))  
*(Instance EC2 → Scraper Python → Upload vers S3 → Accès public via URL S3)*


