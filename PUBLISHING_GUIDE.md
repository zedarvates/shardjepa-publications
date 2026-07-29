# Guide de publication ShardJEPA

Ce guide distingue quatre opérations différentes : publier un instantané dans
un dépôt GitHub, archiver un artefact sur Zenodo, soumettre un manuscrit sur
arXiv ou HAL, puis rattacher l'identifiant obtenu au profil ORCID.

## 1. Valider l'instantané local

Depuis la racine de ShardJEPA :

```powershell
rtk cargo check --workspace --all-targets
rtk cargo test --workspace --all-targets
rtk python publications/tools/export_metadata.py
rtk python publications/tools/package_release.py --version 2026.07.29
```

Le dernier script crée un ZIP et affiche son SHA-256. Conserver le ZIP et le
hash avec la release.

## 2. Publier la documentation sur GitHub

La release GitHub est le premier niveau de diffusion de ce dossier. Elle rend
les textes citables par URL et version, mais n'attribue pas de DOI et ne
constitue pas une validation par les pairs.

1. Publier le contenu validé de `publications/`.
2. Créer un tag, par exemple `v2026.07.29`.
3. Joindre le ZIP généré et son SHA-256 à la release.
4. Vérifier les URL publiques avant de marquer le registre comme diffusé.

## 3. Archiver sur Zenodo

Zenodo demande un jeton personnel avec les droits d'écriture du dépôt et, pour
une publication définitive, le droit d'action. Ne jamais placer le jeton dans
une URL, un fichier ou un commit.

Prévisualiser sans appel réseau :

```powershell
rtk python publications/tools/publish_zenodo.py `
  publications/dist/shardjepa-publications-2026.07.29.zip `
  --title "ShardJEPA research publications, 2026.07.29"
```

Créer un brouillon Zenodo après avoir défini `ZENODO_API_TOKEN` :

```powershell
rtk python publications/tools/publish_zenodo.py `
  publications/dist/shardjepa-publications-2026.07.29.zip `
  --title "ShardJEPA research publications, 2026.07.29" `
  --execute --yes
```

Ajouter `--publish` uniquement après vérification manuelle des métadonnées et
du fichier : cette action rend le dépôt public et non supprimable via l'API.

## 4. Soumettre sur arXiv ou HAL

Les fichiers Markdown ne sont pas un paquet arXiv prêt à compiler. Chaque
manuscrit doit d'abord disposer d'un `paper.tex`, de sa bibliographie et de ses
figures. Le vérificateur refuse donc les répertoires sans source TeX :

```powershell
rtk python publications/tools/package_arxiv.py 01-shardjepa-runtime --check
```

La soumission arXiv ou HAL reste une action de l'auteur : elle implique choix
de catégorie, licence, déclarations d'auteur, éventuelle approbation et revue
du rendu final. Après acceptation, enregistrer l'identifiant réel dans
`ORCID_INDEX.json` et `citations.bib`.

## 5. Mettre à jour ORCID

Le script `sync_orcid.py` vérifie la cohérence locale mais n'écrit pas dans
ORCID. L'ajout automatisé de travaux exige une intégration Member API et une
permission d'écriture accordée par le titulaire du profil. Sans cette
intégration, importer manuellement `citations.bib` depuis le tableau de bord
ORCID après création d'une URL publique ou d'un DOI.

```powershell
rtk python publications/tools/sync_orcid.py --check
```

