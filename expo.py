import subprocess
import json 


node_classification_setup = {
    "dataset": ["ACM", "coauthor-cs", "coauthor-phy"],
    "model": ["SGC", "GCN"],
    "node_similarity": ["feature", "structural"],
    "ranking_similarity": ["NDCG", "ERR"]
}

link_prediction_setup = {
    "dataset": ["BlogCatalog", "facebook", "Flickr"],
    "model": ["GCN", "GAE"],
    "node_similarity": ["feature", "structural"],
    "ranking_similarity": ["NDCG", "ERR"]
}

def run_experiment(task, node, ranking, dataset, model):
    print(task, node, ranking, dataset, model)
    if task == "node classification":
        return subprocess.check_output(
            f"cd node\ classification; time python REDRESS_{node}_{ranking}.py --dataset {dataset} --model {model}", 
            shell=True
        ).decode("utf-8")
    else:
        return subprocess.check_output(
            f"cd link\ prediction; time python {model.lower()}_{node}_{ranking}.py --dataset {dataset}",
            shell=True
        ).decode("utf-8")


def run_setup(task, setup):
    results = []
    for ns in setup["node_similarity"]:
        for rs in setup["ranking_similarity"]:
            for d in setup["dataset"]:
                for m in setup["model"]:
                    results.append([task, ns, rs, d, m])
                    try:
                        r = run_experiment(task, ns, rs, d, m)
                    except Exception as e:
                        r = e
                    results[-1].append(str(r))

    with open(f"{task}_results.json", 'w+') as output_file:
        json.dump(results, output_file)

run_setup("node classification", node_classification_setup)
run_setup("link prediction", link_prediction_setup)
