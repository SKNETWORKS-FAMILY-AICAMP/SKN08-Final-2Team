from abc import ABC, abstractmethod


class GithubActionMonitorRepository(ABC):

    @abstractmethod
    def getGithubActionWorkflow(self, token, repoUrl):
        pass
