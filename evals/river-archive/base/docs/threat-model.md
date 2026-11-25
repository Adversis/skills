# River Archive threat model

The Archive team owns the export service. A tenant member can request an export of a notebook in that tenant. The service checks membership before it creates a job. A worker reads the job and produces the export. A denied request must leave the queue empty. SEC-001 covers this boundary.

The Archive team publishes the worker to a named environment. An independent human must approve production releases. The deployment provider stores the reviewer settings outside the repository. SEC-002 covers this boundary.
