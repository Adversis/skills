"""Export policy for synthetic notebooks held in memory."""


def request_export(member_tenant, notebook_tenant, jobs):
    jobs.append((member_tenant, notebook_tenant))
    return True


def render_export(job):
    member_tenant, notebook_tenant = job
    if member_tenant != notebook_tenant:
        return None
    return {"tenant": notebook_tenant}
