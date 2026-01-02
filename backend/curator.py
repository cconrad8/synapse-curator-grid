from synapseclient.models import (
    CurationTask,
    FileBasedMetadataTaskProperties,
)

def list_curation_tasks(syn, project_id: str):
    tasks = []

    for task in CurationTask.list(project_id=project_id, synapse_client=syn):
        tasks.append({
            "taskId": task.task_id,
            "dataType": task.data_type,
            "projectId": task.project_id,
            "instructions": task.instructions,
        })

    return tasks


def create_file_based_task(
    syn,
    *,
    project_id: str,
    folder_id: str,
    datatype: str,
    instructions: str,
):
    task_properties = FileBasedMetadataTaskProperties(
        upload_folder_id=folder_id,
        file_view_id=None,  # created later if needed
    )

    task = CurationTask(
        project_id=project_id,
        data_type=datatype,
        instructions=instructions,
        task_properties=task_properties,
    )

    return task.store(synapse_client=syn)
