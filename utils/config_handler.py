import json
import os

class ConfigHandler:
    def __init__(self, config_path="data/config.json"):
        self.config_path = config_path
        self.ensure_data_dir()
        self.config = self.load_initial_config()

    def ensure_data_dir(self):
        """Crée le dossier data s'il n'existe pas."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

    def load_initial_config(self):
        """Charge le JSON ou crée une config par défaut."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "settings": {
                "timeout": 5, 
                "retention": 30, 
                "critical": "exploit 1, zero-day 3, execution 2", 
                "spam": "promo", 
                "notify": True
            },
            "clusters": {
                "DEFAULT": {"sources": {}}
            }
        }

    def save(self):
        """Sauvegarde l'état actuel dans le fichier JSON."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    # --- GESTION DES CLUSTERS ---
    
    def add_cluster(self, cluster_name):
        cluster_name = cluster_name.strip().upper()
        if cluster_name and cluster_name not in self.config["clusters"]:
            self.config["clusters"][cluster_name] = {"sources": {}}
            self.save()
            return True, f"Cluster {cluster_name} créé."
        return False, "Nom invalide ou déjà existant."

    def remove_cluster(self, cluster_name):
        """Supprime seulement si le cluster est vide."""
        if cluster_name not in self.config["clusters"]:
            return False, "Cluster inexistant."
        
        if self.config["clusters"][cluster_name]["sources"]:
            return False, "Le cluster n'est pas vide (contient des sources)."
        
        del self.config["clusters"][cluster_name]
        self.save()
        return True, f"Cluster {cluster_name} supprimé."

    def get_clusters_list(self):
        return list(self.config["clusters"].keys())

    # --- GESTION DES SOURCES ---

    def add_source(self, cluster_name, source_name, url):
        if cluster_name not in self.config["clusters"]:
            return False, f"Le cluster {cluster_name} n'existe pas."
        
        self.config["clusters"][cluster_name]["sources"][source_name] = url
        self.save()
        return True, f"Source {source_name} ajoutée à {cluster_name}."

    def remove_source(self, cluster_name, source_name):
        if cluster_name in self.config["clusters"]:
            if source_name in self.config["clusters"][cluster_name]["sources"]:
                del self.config["clusters"][cluster_name]["sources"][source_name]
                self.save()
                return True, "Source supprimée."
        return False, "Source introuvable."

    def get_all_sources_flat(self):
        """Retourne un dictionnaire plat {nom: (url, cluster)} pour le scan."""
        flat = {}
        for c_name, c_data in self.config["clusters"].items():
            for s_name, s_url in c_data["sources"].items():
                flat[s_name] = (s_url, c_name)
        return flat