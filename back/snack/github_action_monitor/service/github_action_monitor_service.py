from abc import ABC, abstractmethod


class GithubActionMonitorService(ABC):

    @abstractmethod
    def requestGithubActionWorkflow(self, token, repoUrl):
        pass
