"""Export policy for synthetic notebooks held in memory."""


def request_export(member_tenant, notebook_tenant, jobs):
    if member_tenant != notebook_tenant:
        return False
    jobs.append((member_tenant, notebook_tenant))
    return True


def render_export(job):
    return {"tenant": job[1]}
