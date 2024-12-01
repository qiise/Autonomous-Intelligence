# utils/rbac_manager.py
import yaml

class RBACManager:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.rbac_config = yaml.safe_load(file)

    def check_permission(self, role, permission):
        role_config = self.rbac_config.get('roles', {}).get(role, {})
        return permission in role_config.get('permissions', [])

    def is_agent_allowed(self, role, agent_name):
        role_config = self.rbac_config.get('roles', {}).get(role, {})
        restricted_agents = role_config.get('restricted_agents', [])
        return agent_name not in restricted_agents
