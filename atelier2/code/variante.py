# code/variante.py
from classifieur import CONSIGNE_EXEMPLES
from evaluer import evaluer, charger
evaluer("openai/gpt-oss-120b", charger(),
consigne=CONSIGNE_EXEMPLES,
etiquette="gpt-oss-120b + 4 exemples")