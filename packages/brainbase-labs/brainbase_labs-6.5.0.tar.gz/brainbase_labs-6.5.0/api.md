# Workers

Types:

```python
from brainbase_labs.types import Workers, WorkerListResponse
```

Methods:

- <code title="post /api/workers">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">create</a>(\*\*<a href="src/brainbase_labs/types/worker_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/workers.py">Workers</a></code>
- <code title="get /api/workers/{id}">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">retrieve</a>(id) -> <a href="./src/brainbase_labs/types/workers/workers.py">Workers</a></code>
- <code title="patch /api/workers/{id}">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">update</a>(id, \*\*<a href="src/brainbase_labs/types/worker_update_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/workers.py">Workers</a></code>
- <code title="get /api/workers">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">list</a>() -> <a href="./src/brainbase_labs/types/worker_list_response.py">WorkerListResponse</a></code>
- <code title="delete /api/workers/{id}">client.workers.<a href="./src/brainbase_labs/resources/workers/workers.py">delete</a>(id) -> None</code>

## Deployments

Types:

```python
from brainbase_labs.types.workers import VoiceDeployment
```

### Voice

Types:

```python
from brainbase_labs.types.workers.deployments import VoiceListResponse
```

Methods:

- <code title="post /api/workers/{workerId}/deployments/voice">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">create</a>(worker_id, \*\*<a href="src/brainbase_labs/types/workers/deployments/voice_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/voice_deployment.py">VoiceDeployment</a></code>
- <code title="get /api/workers/{workerId}/deployments/voice/{deploymentId}">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">retrieve</a>(deployment_id, \*, worker_id) -> <a href="./src/brainbase_labs/types/workers/voice_deployment.py">VoiceDeployment</a></code>
- <code title="put /api/workers/{workerId}/deployments/voice/{deploymentId}">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">update</a>(deployment_id, \*, worker_id, \*\*<a href="src/brainbase_labs/types/workers/deployments/voice_update_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/voice_deployment.py">VoiceDeployment</a></code>
- <code title="get /api/workers/{workerId}/deployments/voice">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">list</a>(worker_id) -> <a href="./src/brainbase_labs/types/workers/deployments/voice_list_response.py">VoiceListResponse</a></code>
- <code title="delete /api/workers/{workerId}/deployments/voice/{deploymentId}">client.workers.deployments.voice.<a href="./src/brainbase_labs/resources/workers/deployments/voice.py">delete</a>(deployment_id, \*, worker_id) -> None</code>

## Flows

Types:

```python
from brainbase_labs.types.workers import Flows, FlowListResponse
```

Methods:

- <code title="post /api/workers/{workerId}/flows">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">create</a>(worker_id, \*\*<a href="src/brainbase_labs/types/workers/flow_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/flows.py">Flows</a></code>
- <code title="get /api/workers/{workerId}/flows/{flowId}">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">retrieve</a>(flow_id, \*, worker_id) -> <a href="./src/brainbase_labs/types/workers/flows.py">Flows</a></code>
- <code title="put /api/workers/{workerId}/flows/{flowId}">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">update</a>(flow_id, \*, worker_id, \*\*<a href="src/brainbase_labs/types/workers/flow_update_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/flows.py">Flows</a></code>
- <code title="get /api/workers/{workerId}/flows">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">list</a>(worker_id) -> <a href="./src/brainbase_labs/types/workers/flow_list_response.py">FlowListResponse</a></code>
- <code title="delete /api/workers/{workerId}/flows/{flowId}">client.workers.flows.<a href="./src/brainbase_labs/resources/workers/flows.py">delete</a>(flow_id, \*, worker_id) -> None</code>

## Resources

Types:

```python
from brainbase_labs.types.workers import File, Link
```

Methods:

- <code title="get /api/workers/{workerId}/resources/{resourceId}">client.workers.resources.<a href="./src/brainbase_labs/resources/workers/resources/resources.py">retrieve</a>(resource_id, \*, worker_id) -> <a href="./src/brainbase_labs/types/workers/link.py">Link</a></code>
- <code title="delete /api/workers/{workerId}/resources/{resourceId}">client.workers.resources.<a href="./src/brainbase_labs/resources/workers/resources/resources.py">delete</a>(resource_id, \*, worker_id) -> None</code>

### Link

Types:

```python
from brainbase_labs.types.workers.resources import LinkListResponse
```

Methods:

- <code title="post /api/workers/{workerId}/resources/link">client.workers.resources.link.<a href="./src/brainbase_labs/resources/workers/resources/link.py">create</a>(worker_id, \*\*<a href="src/brainbase_labs/types/workers/resources/link_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/link.py">Link</a></code>
- <code title="get /api/workers/{workerId}/resources/link">client.workers.resources.link.<a href="./src/brainbase_labs/resources/workers/resources/link.py">list</a>(worker_id) -> <a href="./src/brainbase_labs/types/workers/resources/link_list_response.py">LinkListResponse</a></code>

### File

Types:

```python
from brainbase_labs.types.workers.resources import FileListResponse
```

Methods:

- <code title="post /api/workers/{workerId}/resources/file">client.workers.resources.file.<a href="./src/brainbase_labs/resources/workers/resources/file.py">create</a>(worker_id, \*\*<a href="src/brainbase_labs/types/workers/resources/file_create_params.py">params</a>) -> <a href="./src/brainbase_labs/types/workers/link.py">Link</a></code>
- <code title="get /api/workers/{workerId}/resources/file">client.workers.resources.file.<a href="./src/brainbase_labs/resources/workers/resources/file.py">list</a>(worker_id) -> <a href="./src/brainbase_labs/types/workers/resources/file_list_response.py">FileListResponse</a></code>

# Team

Types:

```python
from brainbase_labs.types import TeamListResponse
```

Methods:

- <code title="get /api/team">client.team.<a href="./src/brainbase_labs/resources/team.py">list</a>(\*\*<a href="src/brainbase_labs/types/team_list_params.py">params</a>) -> <a href="./src/brainbase_labs/types/team_list_response.py">TeamListResponse</a></code>
