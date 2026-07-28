# Model path constants used across the app
IFOREST_MODEL_PATHS = "model/iforest__EJERCICIO10_n_components6_fit.pkl"
OCSVM_MODEL_PATH    = "model/ocsvm__EJERCICIO10_n_components6_fit.pkl"
KMEANS_MODEL_PATHS  = "model/kmeans1__EJERCICIO10_n_components6_over.pkl"
AUTOENCODER_MODEL_PATH = "model/autoencoder.pkl"
KMEANS_TXT_PATH     = "model/list_kmeans_over.txt"

# Supervised models (scikit-learn 1.6.1)
DECISION_TREE_MODEL_PATH = "model/Supervisados/dedup_groupip_Decision_tree_fit.pkl"
EXTRA_TREES_MODEL_PATH = "model/Supervisados/dedup_groupip_Extra_trees_fit.pkl"
RANDOM_FOREST_MODEL_PATH = "model/Supervisados/dedup_groupip_Random_forest_fit.pkl"

# Grouped model catalogs for UI and inference flow.
UNSUPERVISED_MODEL_PATHS = {
	"IForest": IFOREST_MODEL_PATHS,
	"OCSVM": OCSVM_MODEL_PATH,
	"KMEANS": KMEANS_MODEL_PATHS,
	"AUTOENCODER": AUTOENCODER_MODEL_PATH,
}

SUPERVISED_MODEL_PATHS = {
	"DecisionTree": DECISION_TREE_MODEL_PATH,
	"ExtraTrees": EXTRA_TREES_MODEL_PATH,
	"RandomForest": RANDOM_FOREST_MODEL_PATH,
}

MODEL_PATHS = {
	**UNSUPERVISED_MODEL_PATHS,
	**SUPERVISED_MODEL_PATHS,
}

MODEL_TYPE_BY_ID = {
	**{k: "No supervisados" for k in UNSUPERVISED_MODEL_PATHS.keys()},
	**{k: "Supervisados" for k in SUPERVISED_MODEL_PATHS.keys()},
}
