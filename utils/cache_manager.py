import json
import os
from datetime import datetime
# Import du logger centralisé
from utils.logger_custom import cyber_log

class CacheManager:
    def __init__(self, cache_path="data/cache.json"):
        self.cache_path = cache_path
        self._ensure_dir()
        self.cache_data = self.load_cache()
        
        if not os.path.exists(self.cache_path):
            self.save_cache()
            cyber_log.info("Système : Fichier cache.json initialisé proprement.")

    def _ensure_dir(self):
        if not os.path.exists(os.path.dirname(self.cache_path)):
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            cyber_log.info("Système : Répertoire /data créé.")

    def load_cache(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "CLUSTERS" not in data:
                        data["CLUSTERS"] = {}
                    return data
            except Exception as e:
                cyber_log.error(f"Cache : Erreur de lecture du fichier JSON : {str(e)}")
        
        return {"LAST_UPDATE": datetime.now().isoformat(), "CLUSTERS": {}}

    def save_cache(self):
        try:
            self.cache_data["LAST_UPDATE"] = datetime.now().isoformat()
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(self.cache_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            cyber_log.error(f"Cache : Échec de la sauvegarde sur disque : {str(e)}")
            return False

    def update_source_data(self, cluster_name, source_name, articles):
        if "CLUSTERS" not in self.cache_data:
            self.cache_data["CLUSTERS"] = {}
        if cluster_name not in self.cache_data["CLUSTERS"]:
            self.cache_data["CLUSTERS"][cluster_name] = {}
            
        count = len(articles)
        self.cache_data["CLUSTERS"][cluster_name][source_name] = articles
        
        if self.save_cache():
            cyber_log.info(f"Cache : {count} articles mis à jour pour [{cluster_name}] -> {source_name}")

    def search_articles(self, query, target_clusters=None):
        results = []
        query = query.lower().strip()
        if not query: return results

        all_clusters = self.cache_data.get("CLUSTERS", {})
        clusters_to_scan = target_clusters if target_clusters else all_clusters.keys()
        
        cyber_log.info(f"OSINT : Recherche de '{query}' dans {list(clusters_to_scan)}")

        for c_name in clusters_to_scan:
            sources = all_clusters.get(c_name, {})
            for s_name, articles in sources.items():
                for art in articles:
                    if query in art.get('title', '').lower() or query in art.get('description', '').lower():
                        art_copy = art.copy()
                        art_copy["_source_origin"] = s_name
                        art_copy["_cluster_origin"] = c_name
                        results.append(art_copy)
        
        cyber_log.info(f"OSINT : {len(results)} résultats trouvés.")
        return results