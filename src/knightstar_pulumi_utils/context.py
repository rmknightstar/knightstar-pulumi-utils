from dataclasses import dataclass
import pulumi

@dataclass
class KsCtx:
    prefix: str = "ksd"          # KnightStar Digital
    client: str = ""             # e.g., "penobscot"
    system: str | None = None    # e.g., "alfresco"
    base_domain: str | None = None
    env: str = pulumi.get_stack()
    project: str = pulumi.get_project()

    @property
    def namespace(self) -> str:
        return f"{self.prefix}-{self.client}-{self.env}"

    def name(self, base: str) -> str:
        return f"{self.namespace}-{base}"

    def tags(self, extra: dict | None = None) -> dict:
        t = {
            "Company": "KnightStar Digital",
            "Client": self.client,
            "Env": self.env,
            "Project": self.project,
            "Namespace": self.namespace,
        }
        if self.system:
            t["System"] = self.system
        if extra:
            t.update(extra)
        return t

    def private_zone_name(self, private_prefix: str = "int") -> str:
        if not self.base_domain:
            raise ValueError("base_domain is required to compute private zone name")
        return f"{private_prefix}.{self.env}.{self.base_domain}"

def ks_ctx_from_config(ns: str | None = None) -> KsCtx:
    cfg = pulumi.Config(ns) if ns else pulumi.Config()
    client = cfg.require("ks.client")
    base_domain = cfg.get("ks.baseDomain")
    system = cfg.get("ks.system")
    env_override = cfg.get("ks.envOverride")
    prefix = cfg.get("ks.prefix") or "ksd"
    return KsCtx(
        prefix=prefix,
        client=client,
        system=system,
        base_domain=base_domain,
        env=env_override or pulumi.get_stack(),
        project=pulumi.get_project(),
    )
