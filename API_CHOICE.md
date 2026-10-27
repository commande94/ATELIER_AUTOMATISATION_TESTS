# API Choice

- Étudiant : Joaquim
- API choisie : Cat Facts
- URL base : https://catfact.ninja
- Documentation officielle / README : https://catfact.ninja/
- Auth : None
- Endpoints testés :
- GET /fact (récupère un fait aléatoire sur les chats)
- GET /facts (récupère une liste de faits avec pagination)
- Hypothèses de contrat (champs attendus, types, codes) :
- /fact renvoie un statut 200, Content-Type application/json.
- Champs obligatoires : "fact" (string), "length" (int).
- Limites / rate limiting connu : Pas de limite stricte documentée pour un usage modéré.
- Risques (instabilité, downtime, CORS, etc.) : Très faible risque d'instabilité, service public très stable.
