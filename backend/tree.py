from synapseclient import Synapse

def build_folder_tree(syn: Synapse, parent_id: str):
    tree = []

    for child in syn.getChildren(parent_id):
        if child["type"] == "org.sagebionetworks.repo.model.Folder":
            tree.append({
                "id": child["id"],
                "name": child["name"],
                "children": build_folder_tree(syn, child["id"]),
            })

    return tree
